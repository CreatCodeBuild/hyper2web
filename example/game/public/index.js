let game_canvas = new Vue({
  el: '#game_canvas',
  data: {

  }
});

let game_ui = new Vue({
  el: '#game_ui',
  data: {

  }
});

let top10_list = new Vue({
    el: "#天地英雄榜",
    data: {
        top10: undefined
    }
});

// get top10
Service.get_top10(top10_list, 0);

Game.init();
Game.run();
