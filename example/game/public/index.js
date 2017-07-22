import Service from './service.js';  // in Chrome Canary, has to be "./xxxxx.js" explicit relative path
import User from './user.js';
import Game from './game.js';

// this is a work-around for that es6 can't just import a module as a namespace
// Python import & namespace are the best! (except that everything is public. )
// for this import, I don't have any exports in the module.
// the only thing I care about is to initialize some code in the module.
import * as _ from './app_menu/app_menu.js';


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




// create a root instance
new Vue({
  el: '#example'
});

$("#app_menu button").click(function() {
  $('#app_menu').toggleClass('app_menu-hidden');
});
