let Assignment = require(_base + 'models/assignment');

module.exports = {
    '/api/getmyassignment': {
        methods: ['get'],
        fn: function (req, res, next) {
            if (!req.user) {
                return res.json({error: 'You are not logged in and so we cannot retrieve an assignment.'});
            }

            let id = req.user._id;
            console.debug(id);
            Assignment.find({driver: id}, (err, asgns) => {
                if (err) return res.json({error: err});
                if (asgns.length === 0) return res.json({message: 'You have no assignment.'});
                res.json({message: asgns});
            });
        }
    }
};