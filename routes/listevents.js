let Event = require(_base + 'models/events');

module.exports = {
    '/api/listevents': {
        methods: ['get'],
        fn: function (req, res, next) {
            Event.find({ }, (err, events) => {
                if (err) return res.json({error: err});
                if (events.length === 0) return res.json({ message: 'The world is safe today, son.' });
                res.json({ message: events });
            });
        }
    }
};