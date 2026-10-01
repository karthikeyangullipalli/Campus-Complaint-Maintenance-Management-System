const express = require('express');
const { getLocations, createLocation, updateLocation, deleteLocation } = require('../controllers/locationController');
const { verifyToken, requireRole } = require('../middleware/auth');

const router = express.Router();

router.use(verifyToken);

router.get('/', getLocations);
router.post('/', requireRole('ADMIN'), createLocation);
router.put('/:id', requireRole('ADMIN'), updateLocation);
router.delete('/:id', requireRole('ADMIN'), deleteLocation);

module.exports = router;
