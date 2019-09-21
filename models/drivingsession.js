const mongoose = require('mongoose'),
    shortid = require('shortid');

let drivingSessionSchema = new mongoose.Schema({
    _id: {type: String, default: shortid.generate},
    driver: {type: String, ref: 'User', required: true},
    eventId: { type: String, required: true },
    numRiders: { type: Number, required: true },
    maxNumRiders: { type: Number, required: true },
    created: {type: Date, required: true, default: Date.now}
}, {collection: 'hestia_assignments'});

let DrivingSession = mongoose.model('DrivingSession', drivingSessionSchema);

module.exports = DrivingSession;