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

let game = Game().Game
game.init();
game.run();
