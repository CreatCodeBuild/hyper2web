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

        get_top10: function get_top10(model, levelIndex) {
            fetch('/get_top10/'+levelIndex, {method: 'GET'}).then(function(response) {
                response.json().then(function(data) {
                    model.top10 = data;
                })
            });
        }
    };
})();
