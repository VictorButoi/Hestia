const User = require(_base + 'models/user');

module.exports = {
    '/api/signup': {
        methods: ['post'],
        fn: function (req, res, next) {
            let options = {
                fullName: req.body.fullName,
                password: req.body.password,
                email: req.body.email,
                cellPhoneNum: req.body.cellPhoneNum,
                userGroup: req.body.userGroup,
                zipCode: req.body.zipCode
            };

            let user = new User(options);
            user.save(function (err, newUser) {
                if (err) {
                    return res.status(HttpStatus.BAD_REQUEST).json({error: 'Mongoose error: duplicate key, invalid field types, etc.'});
                }

                let message = "Signed up " + newUser.fullName + " with id " + newUser._id + " and roles " + newUser.userGroup.join(', ');

                res.json({ message: message});
                
            });
        }
    }
};