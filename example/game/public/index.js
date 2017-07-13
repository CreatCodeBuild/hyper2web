import Service from './service.js';  // in Chrome Canary, has to be "./xxxxx.js" explicit relative path
import User from './user.js';
import Game from './game.js';


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
			User.name = this.user_input;
			this.$el.style.visibility = "hidden";
			Game.init();
			Game.run();
		}
	}
});

// get top10. This is an inferior solution.
Service.top10_list_vue = top10_list;

window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
}, false);




function detectmob() {
	return navigator.userAgent.match(/Android/i);
}

console.log('detect mob', detectmob());


$("#app_menu button").click(function() {
  $('#app_menu').toggleClass('app_menu-hidden');
});
