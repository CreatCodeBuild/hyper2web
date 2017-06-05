let game_ui = new Vue({
	el: '#game_ui',
	data: {}
});

let top10_list = new Vue({
	el: "#天地英雄榜",
	data: {top10: undefined}
});

// get top10. This is an inferior solution.
Service.top10_list_vue = top10_list;

Game.init();
Game.run();
