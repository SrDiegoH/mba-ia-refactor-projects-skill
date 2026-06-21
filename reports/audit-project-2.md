# Architecture Audit Report

================================
PROJECT INFORMATION
===================

Project Name:     ecommerce-api-legacy
Analysis Date:    2026-06-20

Language:         JavaScript (Node.js)
Framework:        Express.js 4.18.2
Database:         SQLite 3 (in-memory :memory:)
ORM:              Nenhum (raw sqlite3 callbacks)
Package Manager:  npm

Architecture:     MONOLITHIC — Single-class pattern (AppManager centraliza DB + rotas + lógica)
Domain:           LMS / E-commerce (plataforma de checkout de cursos online)
Confidence:       High

Source Files Analyzed:
  - src/app.js         (~15 linhas)
  - src/AppManager.js  (~142 linhas)
  - src/utils.js       (~25 linhas)

Estimated Lines of Code: ~182 LOC de produção

================================
PHASE 1 SUMMARY
===============

Language Detection:
PASS — JavaScript / Node.js detectado via package.json e extensões .js

Framework Detection:
PASS — Express.js 4.18.2 detectado via package.json e require('express') em app.js

Architecture Detection:
PASS — MONOLITHIC confirmado: toda lógica em AppManager.js (DB + rotas + negócio)

Domain Detection:
PASS — LMS/E-commerce: entidades courses, enrollments, payments, users identificadas

Endpoint Inventory Created:
YES

Endpoints Discovered:

| Method | Route                         | Handler                          |
| ------ | ----------------------------- | -------------------------------- |
| POST   | /api/checkout                 | AppManager.setupRoutes (L28-78)  |
| GET    | /api/admin/financial-report   | AppManager.setupRoutes (L80-129) |
| DELETE | /api/users/:id                | AppManager.setupRoutes (L131-137)|

================================
AUDIT SUMMARY
=============

CRITICAL: 3
HIGH:     5
MEDIUM:   5
LOW:      2

Total Findings: 15

================================
CRITICAL FINDINGS
=================

## AP-C01

Severity:
CRITICAL

Title:
Credenciais hardcoded em código-fonte

File:
src/utils.js

Lines:
1-7

Description:
Cinco credenciais de produção estão em texto puro diretamente no código-fonte:
`dbUser`, `dbPass`, `paymentGatewayKey`, `smtpUser` e `smtpPass`. Qualquer pessoa
com acesso ao repositório tem acesso a sistemas externos de produção.

Detection Evidence:
```javascript
const config = {
    dbUser: "admin_master",
    dbPass: "senha_super_secreta_prod_123",
    paymentGatewayKey: "pk_live_1234567890abcdef",
    smtpUser: "no-reply@fullcycle.com.br",
    port: 3000
};
```

Impact:
Exposição de credenciais em repositório Git. Acesso não autorizado ao banco de dados,
gateway de pagamento e servidor de e-mail. Violação de requisitos de compliance (PCI-DSS,
LGPD). As credenciais permanecem no histórico do Git mesmo após remoção do arquivo.

Recommendation:
1. Mover todas as credenciais para variáveis de ambiente (.env)
2. Adicionar .env ao .gitignore imediatamente
3. Rotacionar TODAS as credenciais expostas (são comprometidas)
4. Adicionar .env.example como template versionado

Suggested Refactoring Pattern:
```javascript
// .env (nunca versionado)
PAYMENT_GATEWAY_KEY=pk_live_your_key_here
SMTP_USER=no-reply@yourdomain.com

// código
const gatewayKey = process.env.PAYMENT_GATEWAY_KEY;
```

Status:
RESOLVED — Credenciais removidas. .env.example criado. process.env em uso.

---

## AP-C02

Severity:
CRITICAL

Title:
Implementação criptográfica fraca para senhas de usuários

File:
src/utils.js

Lines:
17-23

Description:
A função `badCrypto()` implementa um pseudo-hash concatenando a codificação base64
da senha 10.000 vezes e truncando para 10 caracteres. Base64 é uma codificação
reversível, não um hash criptográfico. O resultado é um hash de apenas 10 caracteres
altamente predizível e sem salt.

Detection Evidence:
```javascript
function badCrypto(pwd) {
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
}
```
Exemplo: "123456" → sempre produz o mesmos 10 caracteres (sem salt).

Impact:
Todas as senhas de usuários podem ser comprometidas em caso de vazamento do banco.
O hash é reversível (basta tentar base64 da senha) e sem salt (vulnerável a rainbow
tables). Viola OWASP A02:2021 - Cryptographic Failures.

Recommendation:
Substituir por bcrypt (salt rounds ≥ 10) ou argon2. Nunca usar encoding como hash.

Suggested Refactoring Pattern:
```javascript
const bcrypt = require('bcrypt');
const hashPassword = (password) => bcrypt.hash(password, 10);
const verifyPassword = (password, hash) => bcrypt.compare(password, hash);
```

Status:
RESOLVED — badCrypto() substituída por bcrypt com salt rounds=10 em src/utils/crypto.js

---

## AP-C03

Severity:
CRITICAL

Title:
Deleção de usuário sem integridade referencial — corrupção de dados garantida

File:
src/AppManager.js

Lines:
131-137

Description:
O endpoint `DELETE /api/users/:id` remove o usuário da tabela `users` mas não remove
os registros dependentes em `enrollments` e `payments`. O próprio código admite
explicitamente a corrupção na mensagem de resposta HTTP. Não há foreign keys no schema
que imponham integridade referencial.

Detection Evidence:
```javascript
app.delete('/api/users/:id', (req, res) => {
    let id = req.params.id;
    this.db.run("DELETE FROM users WHERE id = ?", [id], (err) => {
        res.send("Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.");
    });
});
```

Impact:
Registros órfãos em `enrollments` e `payments` referenciam `user_id` inexistente.
O relatório financeiro pode apresentar dados incorretos. Impossível associar pagamentos
a usuários. Violação de ACID (atomicidade) — estado inconsistente garantido.

Recommendation:
Implementar cascade delete em transação: deletar payments → enrollments → user.
Retornar mensagem genérica de sucesso (não expor detalhe de implementação).

Suggested Refactoring Pattern:
```javascript
await run('BEGIN TRANSACTION');
const enrollments = await enrollmentModel.findByUserId(id);
await paymentModel.deleteByEnrollmentIds(enrollments.map(e => e.id));
await enrollmentModel.deleteByUserId(id);
await userModel.deleteById(id);
await run('COMMIT');
```

Status:
RESOLVED — Cascade delete implementado em transação atômica em src/services/user.service.js.
Mensagem de resposta corrigida para "Usuário deletado com sucesso."

================================
HIGH FINDINGS
=============

## AP-H01

Severity:
HIGH

Title:
N+1 Query Problem no relatório financeiro

File:
src/AppManager.js

Lines:
80-129

Description:
O endpoint `/api/admin/financial-report` executa queries aninhadas em loop:
1 query de cursos + N queries de matrículas + N×M queries de usuários +
N×M queries de pagamentos. Com 10 cursos e 100 alunos cada, isso gera
~2001 queries por requisição.

Detection Evidence:
```javascript
this.db.all("SELECT * FROM courses", [], (err, courses) => {        // 1 query
    courses.forEach(c => {
        this.db.all("SELECT * FROM enrollments WHERE course_id=?",  // N queries
            [c.id], (err, enrollments) => {
            enrollments.forEach(enr => {
                this.db.get("SELECT name FROM users WHERE id=?",    // N*M queries
                    [enr.user_id], (err, user) => {
                    this.db.get("SELECT amount FROM payments...",    // N*M queries
```

Impact:
Performance exponencialmente degradada com crescimento de dados. Em produção com
volumes reais, a requisição pode ultrapassar limites de timeout. Impossível de
otimizar sem refatoração estrutural.

Recommendation:
Substituir por uma query única com LEFT JOINs cobrindo todas as entidades necessárias.

Suggested Refactoring Pattern:
```sql
SELECT c.id, c.title, u.name, p.amount, p.status
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
LEFT JOIN users u ON u.id = e.user_id
LEFT JOIN payments p ON p.enrollment_id = e.id
ORDER BY c.id
```

Status:
RESOLVED — Substituído por query única com 3 JOINs em src/services/financial.service.js.
Redução de O(N×M) para O(1) queries independentemente do volume de dados.

---

## AP-H02

Severity:
HIGH

Title:
Callback hell de 4 níveis no endpoint de checkout

File:
src/AppManager.js

Lines:
28-78

Description:
O fluxo de checkout encadeia 6 operações de banco de dados em callbacks aninhados
atingindo 4+ níveis de indentação. Qualquer erro em nível intermediário exige
tratamento manual em cada callback. Memory leaks são possíveis quando callbacks
internos falham sem atingir res.send().

Detection Evidence:
```javascript
this.db.get("SELECT * FROM courses...", (err, course) => {      // nível 1
    this.db.get("SELECT id FROM users...", (err, user) => {     // nível 2
        this.db.run("INSERT INTO users...", function(err) {      // nível 3
            this.db.run("INSERT INTO enrollments...", function(err) { // nível 4
```

Impact:
Código ilegível e de difícil manutenção. Erros de callback podem ser silenciosos.
Impossível usar try/catch para tratamento centralizado. Dificulta testes unitários.

Recommendation:
Migrar para async/await com Promises. Promisificar o driver sqlite3 uma única vez
em config/database.js e usar await em toda a cadeia.

Suggested Refactoring Pattern:
```javascript
const course = await courseModel.findActiveById(c_id);
const user = await userModel.findByEmail(eml) ?? await userModel.create(...);
const enrollment = await enrollmentModel.create(user.id, c_id);
```

Status:
RESOLVED — Migrado para async/await em src/services/checkout.service.js.

---

## AP-H03

Severity:
HIGH

Title:
Callback hell com contadores manuais de concorrência no relatório financeiro

File:
src/AppManager.js

Lines:
80-129

Description:
O relatório financeiro usa contadores manuais (`coursesPending`, `enrPending`)
para saber quando todas as queries assíncronas terminaram. Esse padrão é
propenso a bugs de off-by-one e race conditions quando callbacks retornam
fora de ordem.

Detection Evidence:
```javascript
let coursesPending = courses.length;
courses.forEach(c => {
    let enrPending = enrollments.length;
    enrollments.forEach(enr => {
        enrPending--;
        if (enrPending === 0) {
            coursesPending--;
            if (coursesPending === 0) res.json(report); // race condition
        }
    });
});
```

Impact:
Se qualquer callback falhar silenciosamente, o contador não chega a zero e a
resposta nunca é enviada (connection timeout). Em ambientes com alta concorrência,
múltiplos callbacks podem decrementar simultaneamente (race condition).

Recommendation:
Substituir por Promise.all() ou query SQL única com JOINs (resolve simultaneamente
AP-H01 e AP-H03).

Suggested Refactoring Pattern:
```javascript
const rows = await query('SELECT ... FROM courses LEFT JOIN enrollments ...');
// processa rows sincronamente com Map
```

Status:
RESOLVED — Resolvido juntamente com AP-H01 via query única com JOINs.

---

## AP-H04

Severity:
HIGH

Title:
Endpoints admin e destrutivos sem autenticação ou autorização

File:
src/AppManager.js

Lines:
80-137

Description:
`GET /api/admin/financial-report` (dado financeiro sensível) e
`DELETE /api/users/:id` (operação irreversível) estão acessíveis publicamente
sem qualquer forma de autenticação (JWT, API key, session) ou autorização
baseada em role.

Detection Evidence:
```javascript
app.get('/api/admin/financial-report', (req, res) => {
    // nenhuma verificação de identidade ou permissão
    this.db.all("SELECT * FROM courses", ...
```

Impact:
Qualquer cliente externo pode: acessar dados financeiros de toda a plataforma;
deletar qualquer usuário (incluindo administradores). Viola OWASP A01:2021 -
Broken Access Control.

Recommendation:
Implementar middleware de autenticação JWT ou API key antes desses endpoints.
Adicionar verificação de role (ex.: `requireAdmin`) para o relatório financeiro.

Suggested Refactoring Pattern:
```javascript
const requireAdmin = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!verifyAdminToken(token)) return res.status(401).send('Unauthorized');
    next();
};
router.get('/admin/financial-report', requireAdmin, getFinancialReport);
```

Status:
OPEN — Fora do escopo da refatoração MVC atual. Recomendado para próxima sprint.

---

## AP-H05

Severity:
HIGH

Title:
Operações de checkout sem transação atômica

File:
src/AppManager.js

Lines:
50-63

Description:
O fluxo de checkout executa 3 INSERTs sequenciais (enrollment, payment, audit_log)
sem transação. Se o INSERT de payment falhar após o INSERT de enrollment, a matrícula
existe sem pagamento correspondente — estado financeiramente inconsistente.

Detection Evidence:
```javascript
this.db.run("INSERT INTO enrollments...", function(err) {      // sem transação
    self.db.run("INSERT INTO payments...", function(err) {     // falha aqui?
        self.db.run("INSERT INTO audit_logs...", (err) => {    // matrícula órfã
            res.json({ msg: "Sucesso" });
        });
    });
});
```

Impact:
Falha parcial cria dados inconsistentes: matrícula sem pagamento, ou pagamento
sem audit_log. Relatório financeiro retorna dados incorretos. Impossível distinguir
matrículas pagas de não pagas se status de pagamento é perdido.

Recommendation:
Encapsular enrollment + payment + audit_log em BEGIN TRANSACTION / COMMIT / ROLLBACK.

Suggested Refactoring Pattern:
```javascript
await run('BEGIN TRANSACTION');
try {
    await enrollmentModel.create(userId, courseId);
    await paymentModel.create(enrollmentId, amount, status);
    await auditLogModel.log(`Checkout curso ${courseId}`);
    await run('COMMIT');
} catch (err) {
    await run('ROLLBACK');
    throw err;
}
```

Status:
RESOLVED — Transação atômica implementada em src/services/checkout.service.js.

================================
MEDIUM FINDINGS
===============

## AP-M01

Severity:
MEDIUM

Title:
Violação do Princípio de Responsabilidade Única (SRP) — classe God Object

File:
src/AppManager.js

Lines:
1-142

Description:
A classe `AppManager` é responsável por: criação e gerenciamento da conexão com o
banco de dados; inicialização do schema e dados seed; registro e tratamento de todas
as rotas; toda a lógica de negócio (checkout, relatório, deleção); logging e cache.
Uma única classe gerencia domínios completamente distintos.

Detection Evidence:
```javascript
class AppManager {
    constructor() { this.db = new sqlite3.Database(':memory:'); } // DB
    initDb() { /* schema + seed */ }                              // Migrations
    setupRoutes(app) { /* 114 linhas de rotas + lógica */ }       // Routes + Logic
}
```

Impact:
Impossível testar unitariamente qualquer responsabilidade isolada. Qualquer mudança
de rota afeta o código de banco de dados e vice-versa. Dificuldade de onboarding
para novos desenvolvedores. Violação de Clean Architecture.

Recommendation:
Separar em config/ (database), models/ (queries), services/ (lógica), controllers/
(HTTP), routes/ (registro de rotas).

Status:
RESOLVED — Arquitetura MVC completa implementada com separação total de responsabilidades.

---

## AP-M02

Severity:
MEDIUM

Title:
Validação de cartão de crédito trivialmente insuficiente

File:
src/AppManager.js

Lines:
46

Description:
A única validação de pagamento verifica se o número do cartão começa com "4".
Qualquer string começando com "4" é aceita como pagamento válido, incluindo "4",
"4abc" ou "4000000000000000" (cartão de teste).

Detection Evidence:
```javascript
let status = cc.startsWith("4") ? "PAID" : "DENIED";
```

Impact:
Regra de negócio crítica (processamento de pagamento) completamente ineficaz.
Qualquer usuário pode contornar a validação trivialmente. Em produção real, resultaria
em perdas financeiras imediatas.

Recommendation:
Integrar com gateway de pagamento real. No mínimo, implementar o algoritmo de Luhn
para validação básica do número do cartão.

Suggested Refactoring Pattern:
```javascript
// Algoritmo de Luhn para validação básica
const isValidCard = (number) => {
    const digits = number.replace(/\D/g, '').split('').reverse().map(Number);
    const sum = digits.reduce((acc, d, i) => {
        if (i % 2 !== 0) { d *= 2; if (d > 9) d -= 9; }
        return acc + d;
    }, 0);
    return sum % 10 === 0;
};
```

Status:
OPEN — Fora do escopo MVC. A lógica foi movida para src/services/checkout.service.js,
preparada para substituição pelo gateway real.

---

## AP-M03

Severity:
MEDIUM

Title:
Cache global compartilhado sem isolamento, TTL ou controle de memória

File:
src/utils.js

Lines:
9-15

Description:
`globalCache` é um objeto JavaScript simples compartilhado entre todas as requisições
simultâneas, sem TTL (entradas nunca expiram), sem limite de tamanho (vazamento de
memória), e sem isolamento por usuário/sessão.

Detection Evidence:
```javascript
let globalCache = {};
function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    globalCache[key] = data;
}
```

Impact:
Em produção, `globalCache` cresce indefinidamente até esgotar a memória do processo.
Dados de um usuário podem ser acessados por outro se houver colisão de chave.
O cache sobrevive para sempre — não há invalidação.

Recommendation:
Substituir por solução de cache adequada (node-cache com TTL, Redis) ou remover
se não houver valor de negócio real.

Status:
RESOLVED — globalCache removido. logAndCache substituído por console.log direto no service.

---

## AP-M04

Severity:
MEDIUM

Title:
Schema e dados seed definidos inline no código da aplicação

File:
src/AppManager.js

Lines:
10-22

Description:
O schema do banco de dados e dados iniciais de seed estão definidos diretamente
no método `initDb()` da classe AppManager, misturados com código de lógica da
aplicação. Não há versionamento de schema, rollback possível ou separação de
ambiente.

Detection Evidence:
```javascript
initDb() {
    this.db.serialize(() => {
        this.db.run("CREATE TABLE users (...)");
        this.db.run("INSERT INTO users VALUES ('Leonan', ...)");
    });
}
```

Impact:
Impossível evoluir o schema sem modificar código de produção. Sem histórico de
mudanças de schema. Dados seed de desenvolvimento vazam para produção. Não escala
para múltiplos ambientes (dev, staging, prod).

Recommendation:
Separar schema em arquivos SQL versionados ou usar sistema de migrations
(node-migrate, Knex migrations, Prisma migrate).

Status:
RESOLVED — Isolado em src/config/database.js com função `initDb()` assíncrona
e independente do código de rotas.

---

## AP-M05

Severity:
MEDIUM

Title:
Resposta HTTP expõe detalhe interno de corrupção de dados

File:
src/AppManager.js

Lines:
135

Description:
A resposta do endpoint DELETE /api/users/:id retorna uma mensagem que admite
explicitamente que o banco de dados ficará em estado corrompido após a operação.
Isso expõe detalhes de implementação e vulnerabilidades para clientes externos.

Detection Evidence:
```javascript
res.send("Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.");
```

Impact:
Confirma a um atacante que a operação deixa dados órfãos exploráveis. Expõe
detalhes de arquitetura interna. Viola o princípio de mínima exposição de
informação em APIs públicas.

Recommendation:
Corrigir a corrupção subjacente (AP-C03) e retornar mensagem genérica de sucesso.

Status:
RESOLVED — Corrupção resolvida (AP-C03). Mensagem alterada para "Usuário deletado com sucesso."

================================
LOW FINDINGS
============

## AP-L01

Severity:
LOW

Title:
Nomes de campos de request body abreviados e não descritivos

File:
src/AppManager.js

Lines:
29-33

Description:
O body da requisição POST /api/checkout usa abreviações crípticas: `usr` (name),
`eml` (email), `pwd` (password), `c_id` (courseId). A API é mais difícil de
consumir e documentar sem nomes descritivos.

Detection Evidence:
```javascript
let u = req.body.usr;
let e = req.body.eml;
let p = req.body.pwd;
let cid = req.body.c_id;
let cc = req.body.card;
```

Impact:
Dificulta leitura, documentação e manutenção da API. Desenvolvedores clientes
precisam consultar documentação adicional para entender os campos.

Recommendation:
Padronizar para `name`, `email`, `password`, `courseId`, `cardNumber`.
Atualizar api.http e documentação correspondente.

Status:
OPEN — Contrato de API preservado intencionalmente para compatibilidade retroativa.
Recomendado para versionamento futuro da API (v2).

---

## AP-L02

Severity:
LOW

Title:
Logging sem estrutura, nível de severidade ou timestamp

File:
src/AppManager.js

Lines:
45, 59

Description:
Toda a observabilidade da aplicação se resume a `console.log` simples sem nível
de severidade (INFO/WARN/ERROR), sem timestamp estruturado e sem correlação de
request ID. Impossível filtrar ou analisar logs em produção.

Detection Evidence:
```javascript
console.log(`Processando cartão ${cc} na chave ${config.paymentGatewayKey}`);
// também loga a chave de pagamento — vazamento de segredo em logs
```

Impact:
Troubleshooting em produção é extremamente difícil. Logs de diferentes requisições
concorrentes se misturam sem identificador. A linha acima também loga a chave de
API do gateway de pagamento nos logs do sistema (vazamento de segredo secundário).

Recommendation:
Adotar logger estruturado (winston ou pino) com níveis INFO/WARN/ERROR, timestamps
ISO e correlação por request ID. Nunca logar chaves, senhas ou PII.

Status:
OPEN — console.log simplificado mantido. Logging estruturado recomendado para
próxima sprint. Referência à chave de gateway removida na refatoração.

================================
DEPRECATED APIS
===============

## sqlite3 callback API

File:
src/AppManager.js

Lines:
37-137

API:
sqlite3 callback-style API (db.get, db.all, db.run com callbacks)

Reason:
A API de callbacks do sqlite3 é funcional mas idiomaticamente obsoleta em Node.js
moderno (ES2017+). O padrão de callbacks aninhados (Pyramid of Doom) é considerado
anti-pattern desde a adoção massiva de Promises e async/await.

Recommended Replacement:
Criar wrappers Promise em config/database.js (sem trocar o driver):
```javascript
const get = (sql, params) => new Promise((resolve, reject) =>
    db.get(sql, params, (err, row) => err ? reject(err) : resolve(row))
);
```
Alternativa: migrar para `better-sqlite3` (API síncrona) ou `@databases/sqlite` (Promises nativas).

Migration Complexity:
MEDIUM — Requer wrapping de todas as chamadas, mas não troca o driver nem o banco.

================================
ENDPOINT INVENTORY
==================

| Method | Route                       | Handler                                    | Notes                              |
| ------ | --------------------------- | ------------------------------------------ | ---------------------------------- |
| POST   | /api/checkout               | CheckoutController.checkout                | Cria usuário se não existir        |
| GET    | /api/admin/financial-report | FinancialController.getFinancialReport     | Sem autenticação (AP-H04 OPEN)     |
| DELETE | /api/users/:id              | UserController.deleteUser                  | Sem autenticação (AP-H04 OPEN)     |

================================
MVC MIGRATION PLAN
==================

Step 1:
Instalar dependências: `bcrypt` (hash seguro) e `dotenv` (variáveis de ambiente).
Criar `.env.example` com todas as credenciais extraídas de utils.js.

Step 2:
Criar `src/config/database.js` com Promise wrappers (get, query, run) e função
`initDb()` assíncrona extraída do constructor e método initDb() de AppManager.

Step 3:
Criar `src/models/*.js` — um arquivo por entidade (user, course, enrollment,
payment, auditLog). Cada model encapsula as queries SQL de sua entidade.

Step 4:
Criar `src/utils/crypto.js` substituindo `badCrypto()` por `bcrypt.hash()`.
Criar `src/services/*.js` com lógica de negócio extraída de AppManager.setupRoutes():
- checkout.service.js: async/await + transação atômica (AP-H02, AP-H05)
- financial.service.js: query única com JOINs (AP-H01, AP-H03)
- user.service.js: cascade delete em transação (AP-C03)

Step 5:
Criar `src/controllers/*.js` — separação entre tratamento HTTP (req/res) e lógica
de negócio. Criar `src/routes/*.js` — um arquivo por domínio.

Step 6:
Refatorar `src/app.js` para usar apenas as novas rotas e initDb(). Remover
`src/AppManager.js` e `src/utils.js` (arquivos legados orphaned).

Expected Target Structure:

```text
src/
├── app.js
├── config/
│   └── database.js
├── controllers/
│   ├── checkout.controller.js
│   ├── financial.controller.js
│   └── user.controller.js
├── models/
│   ├── auditLog.model.js
│   ├── course.model.js
│   ├── enrollment.model.js
│   ├── payment.model.js
│   └── user.model.js
├── routes/
│   ├── checkout.routes.js
│   ├── financial.routes.js
│   └── user.routes.js
├── services/
│   ├── checkout.service.js
│   ├── financial.service.js
│   └── user.service.js
└── utils/
    └── crypto.js
```

================================
RISK ASSESSMENT
===============

Low Risk Changes:

* Extração de credenciais para .env (não altera comportamento em runtime)
* Criação de Promise wrappers em config/database.js (mesma lógica, nova interface)
* Criação de models/ como wrappers de queries existentes
* Separação de controllers/ e routes/ (reorganização sem mudança de lógica)
* Substituição da mensagem de resposta do DELETE

Medium Risk Changes:

* Migração de callbacks para async/await (semântica preservada, mas controle de fluxo diferente)
* Substituição de badCrypto() por bcrypt (incompatível com hashes existentes no banco seed)
* Implementação de transação no checkout (comportamento mais restrito que o original)

High Risk Changes:

* Substituição de N+1 queries por JOIN único no financial-report (lógica de agregação
  reimplementada — requer validação extensiva com dados variados)
* Cascade delete no endpoint de usuário (altera comportamento de forma irreversível)

Potential Breaking Changes:

* Hashes de senha existentes no banco seed (pass='123') não são bcrypt — usuário seed
  Leonan não conseguiria fazer login com verificação bcrypt (sem impacto neste projeto
  pois não há endpoint de login implementado)
* Qualquer cliente que dependia da mensagem "ficaram sujos no banco" como sinal de
  sucesso do DELETE (improvável, mas tecnicamente é mudança de contrato)

================================
REFACTORING CHECKLIST
=====================

[x] Security findings addressed
    AP-C01: Credenciais em variáveis de ambiente
    AP-C02: bcrypt substituindo badCrypto()
    AP-C03: Cascade delete em transação

[x] Configuration extracted
    src/config/database.js isolado com initDb() assíncrono

[x] Controllers isolated
    checkout.controller.js, financial.controller.js, user.controller.js

[x] Services created
    checkout.service.js, financial.service.js, user.service.js

[x] Models isolated
    user.model.js, course.model.js, enrollment.model.js, payment.model.js, auditLog.model.js

[x] Routes separated
    checkout.routes.js, financial.routes.js, user.routes.js

[x] Error handling centralized
    try/catch em controllers com status codes semânticos

[x] Dependency issues resolved
    bcrypt e dotenv instalados; sqlite3 mantido com wrappers Promise

[x] Deprecated APIs removed
    sqlite3 callback API substituída por wrappers async/await

[x] Endpoint contracts preserved
    POST /api/checkout, GET /api/admin/financial-report, DELETE /api/users/:id mantidos

================================
VALIDATION RESULTS
==================

Application Boot:
PASS
  Saída observada: "Frankenstein LMS rodando na porta 3000..."
  Sem erros no stderr
  Banco inicializado com sucesso (tabelas + seed data)

Endpoint Validation:
PASS
  POST /api/checkout (cartão válido 4xxx)   → 200 {"msg":"Sucesso","enrollment_id":2}
  POST /api/checkout (cartão inválido 5xxx) → 400 "Pagamento recusado"
  POST /api/checkout (campos faltando)      → 400 "Bad Request"
  GET  /api/admin/financial-report          → 200 [{"course":"Clean Architecture","revenue":1994,"students":[...]}]
  DELETE /api/users/1                       → 200 "Usuário deletado com sucesso."
  GET  /api/admin/financial-report (pós-delete) → 200 revenue corrigido de 1994 → 997 (cascade delete validado)

Architecture Validation:
PASS
  src/config/    ✓ database.js
  src/models/    ✓ 5 arquivos (user, course, enrollment, payment, auditLog)
  src/services/  ✓ 3 arquivos (checkout, financial, user)
  src/controllers/ ✓ 3 arquivos
  src/routes/    ✓ 3 arquivos
  src/utils/     ✓ crypto.js
  Nenhum arquivo da nova arquitetura importa AppManager.js ou utils.js

Configuration Validation:
PASS
  Credenciais removidas do código-fonte
  .env.example criado com template de variáveis
  process.env.PORT em uso no app.js

Deprecated API Validation:
PASS
  sqlite3 callback API encapsulada em Promise wrappers em config/database.js
  Toda a camada de models/services usa async/await

================================
FINAL STATUS
============

Resolved Findings: 11
  AP-C01 CRITICAL  Credenciais hardcoded
  AP-C02 CRITICAL  Criptografia fraca de senhas
  AP-C03 CRITICAL  Delete sem integridade referencial
  AP-H01 HIGH      N+1 Query Problem
  AP-H02 HIGH      Callback hell no checkout
  AP-H03 HIGH      Callback hell com contadores manuais
  AP-H05 HIGH      Sem transação atômica no checkout
  AP-M01 MEDIUM    Violação SRP / God Object
  AP-M03 MEDIUM    Cache global sem TTL
  AP-M04 MEDIUM    Schema inline no código da aplicação
  AP-M05 MEDIUM    Resposta HTTP expõe corrupção de dados

Remaining Findings: 4
  AP-H04 HIGH    Sem autenticação/autorização (próxima sprint)
  AP-M02 MEDIUM  Validação de cartão trivial (próxima sprint — integração gateway)
  AP-L01 LOW     Campos de request body abreviados (versionamento futuro da API)
  AP-L02 LOW     Sem logging estruturado (próxima sprint — winston/pino)

Overall Status:
PASS

11 de 15 findings resolvidos (73%).
Os 4 findings restantes estão fora do escopo da refatoração MVC e requerem
decisões de produto (autenticação, gateway de pagamento, logging).
Todos os contratos de API preservados. Todos os endpoints funcionais validados.
Boot sem erros. Integridade referencial confirmada via teste end-to-end.

================================
END OF REPORT
=============
