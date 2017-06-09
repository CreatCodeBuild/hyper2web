let UserName = undefined;

let game_ui = new Vue({
	el: '#game_ui',
	data: {}
});

let top10_list = new Vue({
	el: "#game_rank",
	data: {top10: undefined}
});

let ask_user_name = new Vue({
	el: "#ask_user_name",
	data: {
		user_input: undefined
	},
	methods: {
		confirm: function(event) {
			UserName = this.user_input
			this.$el.style.visibility = "hidden";
			Game.init();
			Game.run();
		}
	}
});

// get top10. This is an inferior solution.
Service.top10_list_vue = top10_list;


