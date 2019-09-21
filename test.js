var Client = require('predicthq')

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');

var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();
s
today = mm + '/' + dd + '/' + yyyy;

var phq = new Client({access_token: "GdyEbabHRui-VxV-IKlLRxUkS81OvluuryGG51uZ"})

phq.events.search({"start_around.origin": today, rank_level: 5, category: "severe-weather", country:'US', 'start.gte' : today})
    .then(function(results){
        var events = results.toArray()
        for(var i=0; i < events.length; i++)
            console.info(events[i].rank, events[i].category, events[i].title, events[i].start, events[i].location )
    })

