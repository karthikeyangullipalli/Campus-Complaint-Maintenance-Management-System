const express = require('express');
const { getCategories, createCategory, updateCategory, deleteCategory } = require('../controllers/categoryController');
const { verifyToken, requireRole } = require('../middleware/auth');

const router = express.Router();

router.use(verifyToken);

router.get('/', getCategories);
router.post('/', requireRole('ADMIN'), createCategory);
router.put('/:id', requireRole('ADMIN'), updateCategory);
router.delete('/:id', requireRole('ADMIN'), deleteCategory);

module.exports = router;
