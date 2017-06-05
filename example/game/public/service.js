const Service = (function() {
    return {
        post_record: function post_record(record) {
            record = JSON.stringify(record);
            return fetch('/post_record',
                         {
                             method: 'POST',
                             body: record
                         });
        },

        //model: a Vue object
        //GET top 10 of a level and assign it to model.top10
        get_top10: function get_top10(levelIndex) {
            let self = this;
            fetch('/get_top10/'+levelIndex, {method: 'GET'}).then(function(response) {
                response.json().then(function(data) {
                    console.log(self);
                    self.top10_list_vue.top10 = data;
                })
            });
        }
    };
})();
