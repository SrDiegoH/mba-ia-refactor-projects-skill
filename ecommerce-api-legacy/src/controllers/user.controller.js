const userService = require('../services/user.service');

const deleteUser = async (req, res) => {
  const { id } = req.params;
  try {
    await userService.deleteUser(id);
    res.send('Usuário deletado com sucesso.');
  } catch (err) {
    res.status(500).send('Erro ao deletar usuário');
  }
};

module.exports = { deleteUser };
