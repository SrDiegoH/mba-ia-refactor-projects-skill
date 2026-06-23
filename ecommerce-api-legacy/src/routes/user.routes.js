const express = require('express');
const router = express.Router();
const { deleteUser } = require('../controllers/user.controller');
const { requireAdmin } = require('../middleware/auth');

router.delete('/users/:id', requireAdmin, deleteUser);

module.exports = router;
