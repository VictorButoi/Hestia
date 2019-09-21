const express = require('express'),
    routescan = require('express-routescan'),
    format = require('string-format'),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser'),
    session = require("express-session"),
    passport = require('passport'),
    mongoose = require('mongoose'),
    LocalStrategy = require("passport-local").Strategy,
    HttpStatus = require('http-status-codes');

/**
 * START GLOBALS
 */
global._base = __dirname + '/';
global.HttpStatus = HttpStatus;

console.info = function (message) {
    console.log('[INFO] ' + message);
};

console.debug = function (message) {
    if (_isDev) console.log('[DEBUG] ' + message);
};

console.critical = function (message) {
    console.log('[!!! CRITICAL !!!] ' + message);
};

format.extend(String.prototype, {});
String.prototype.replaceAll = function (a, b) {
    return this.split(a).join(b);
};

/**
 * START EXPRESS/DATABASE CONFIGURATION
 */
const app = express();

global._env = app.get('env');
global._isDev = _env === 'development';
global._isProd = _env === 'production';

console.info('Running in ' + _env + ' environment.');

/**
 * ESTABLISH DATABASE CONNECTION
 */
const url = 'mongodb+srv://admin687:admin687!@cluster0-au5yo.gcp.mongodb.net/hestia?retryWrites=true&w=majority';
console.info('Attempting to connect to', url);
mongoose.connect(url);
mongoose.connection.on('connected', function () {
    console.info('Database connection established');
});

mongoose.connection.on('error', function (err) {
    console.critical('Cannot connect to database');
    console.critical(JSON.stringify(err));
    return process.exit();
});

mongoose.connection.on('disconnected', function () {
    console.info('Database disconnected');
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(cookieParser());
app.use(session({
    secret: 'KRJFERKJGERG',
    resave: false,
    saveUninitialized: true,
    cookie: {secure: false, maxAge: 10000000 }
}));

passport.serializeUser(function (user, done) {
    done(null, user._id);
});

passport.deserializeUser(function (id, done) {
    User.findById(id, function (err, user) {
        done(err, user);
    });
});

passport.use(new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password'
}, function (username, password, done) {
    User.findOne({email: username}, function (err, user) {
        if (err) {
            return done(err);
        }
        if (!user) {
            return done(null, false,
                {message: "Invalid email or password."});
        }
        user.checkPassword(password, function (err, isMatch) {
            if (err) {
                return done(err);
            }
            if (isMatch) {
                return done(null, user);
            } else {
                return done(null, false,
                    {message: "Invalid email or password."});
            }
        });
    });
}));
app.use(passport.initialize());
app.use(passport.session());

// app.use(baseResponse);
routescan(app, {
    ignoreInvalid: true
});

app.use((req, res, next) => {
    res.sendStatus(HttpStatus.NOT_FOUND);
})

module.exports = app;