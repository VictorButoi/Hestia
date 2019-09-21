let Assignment = require(_base + 'models/assignment');

module.exports = {
    '/api/acceptassignment': {
        methods: ['post'],
        fn: function (req, res, next) {

            // Id of assignment to accept
            let id  = req.body._id;

            if (!id) {
                return res.json({error: 'You must provide an assignment ID to accept.'});
            }

            if (!req.user) {
                return res.json({error: 'You are not logged in and so we cannot accept an assignment.'});
            }

            // Id of user that is making the request
            let userId = req.user._id;

            // Find the assignment object with id
            Assignment.findOne({_id: id}, (err, asgn) => {
                if (err) return res.json({ error: err });
                if (!asgn) return res.json({ message: 'No assignment found.' });
                if (asgn.driver !== userId) return res.json({ error: 'You are not assigned to specified assignment.' });
                // Update assignment to not be pending
                asgn.pending = false;
                asgn.save((err) => {
                    if (err) console.debug('Error with updating assignment to pending=false!');
                    res.json({message: 'Success'});
                });
            });
        }
    }
};