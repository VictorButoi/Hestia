const bcrypt = require('bcrypt-nodejs');
const mongoose = require('mongoose');
const shortid = require('shortid');

const SALT_FACTOR = 10;

let userSchema = new mongoose.Schema({
    _id: {type: String, default: shortid.generate},
    fullName: {type: String, required: true},
    password: {type: String, required: true},
    email: {type: String, required: true, unique: true},
    cellPhoneNum: {type: String, required: true, unique: true},
    userGroup: {type: [String], required: false}, /*ADMIN, DRIVER, CLIENT, etc...*/
    zipCode: {type: Number, required: true},
    created: {type: Date, required: true, default: Date.now}
}, {collection: 'hestia_users'});

let noop = function () {
};

userSchema.pre('save', function (done) {
    let user = this; //Reference to user model

    if (!user.isModified("password")) {
        return done();
    }

    bcrypt.genSalt(SALT_FACTOR, function (err, salt) {
        if (err) {
            return done(err);
        }
        bcrypt.hash(user.password, salt, noop, function (err, hashedPassword) {
            if (err) {
                return done(err);
            }
            user.password = hashedPassword;
            done();
        });
    });
});

userSchema.pre('findOneAndUpdate', function (done) {
    let query = this; //Reference to user model
    let user = query.getUpdate();

    if (!user.password) {
        return done();
    }

    bcrypt.genSalt(SALT_FACTOR, function (err, salt) {
        if (err) {
            return done(err);
        }
        bcrypt.hash(user.password, salt, noop, function (err, hashedPassword) {
            if (err) {
                return done(err);
            }
            user.password = hashedPassword;
            done();
        });
    });
});

userSchema.methods.checkPassword = function (guess, done) {
    bcrypt.compare(guess, this.password, function (err, isMatch) {
        done(err, isMatch);
    });
};

let user = mongoose.model('User', userSchema);

module.exports = user;