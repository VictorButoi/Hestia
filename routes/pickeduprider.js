let Assignment = require(_base + 'models/assignment');

module.exports = {
    '/api/pickeduprider': {
        methods: ['post'],
        fn: function (req, res, next) {
            if (!req.user) {
                return res.json({error: 'You are not logged in and so we cannot retrieve an assignment.'});
            }

            let id = req.user._id;
            Assignment.findOne({driver: id}, (err, asgn) => {
                if (err) return res.json({error: err});
                if (!asgn) return res.json({ message: 'You have no assignment.' });
                if (asgn.numRiders >= asgn.maxNumRiders) return res.json({ error: 'You are over your maximum number of riders.' });
                asgn.numRiders++;
                asgn.save(err => {
                    if (err) return console.error(err);
                    res.json({ message: asgn.numRiders });
                });
            });
        }
    }
};