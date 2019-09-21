const passport = require('passport');

module.exports = {
    '/api/login': {
        methods: ['post'],
        middleware: [passport.authenticate("local", {
            successRedirect: "login/success",
            failureRedirect: "login/fail",
            failureFlash: false //Flash not needed
        })],
        fn: function (req, res, next) {

        }
    },
    '/api/login/success': {
        methods: ['get'],
        fn: function (req, res, next) {
            res.redirect('/api/session');
        }
    },
    '/api/login/fail': {
        methods: ['get'],
        fn: function (req, res, next) {
            res.json({'error': 'Login failed!'});
        }
    }
};