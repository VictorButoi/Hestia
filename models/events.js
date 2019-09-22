const mongoose = require('mongoose'),
    shortid = require('shortid');

let eventSchema = new mongoose.Schema({
    _id: {type: String, default: shortid.generate},
    eventId: String,
    address: String,
    latitude: Number,
    longitude: Number
}, {collection: 'hestia_events'});

let Event = mongoose.model('Event', eventSchema);

module.exports = Event;