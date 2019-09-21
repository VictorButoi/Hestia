const mongoose = require('mongoose'),
    shortid = require('shortid');

let assignmentSchema = new mongoose.Schema({
    _id: {type: String, default: shortid.generate},
    driver: {type: String, ref: 'User', required: true},
    event: {type: {eventId: String, address: String, required: true}},
    created: {type: Date, required: true, default: Date.now}
}, {collection: 'hestia_assignments'});

let Assignment = mongoose.model('Assignment', assignmentSchema);

module.exports = Assignment;