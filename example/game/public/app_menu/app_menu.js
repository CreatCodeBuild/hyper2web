import User from '../user.js';

// todo: should change to dependency injection instead of import User
// todo: what ever User should be passed in by the Vue instance which uses this component
Vue.component('app-menu', {
  template:
  `<div id="app_menu" class="app_menu-normal">
		<button>Button</button>
        <div class="g-signin2" data-onsuccess="User.onSignIn"></div>
        <a href="#" onclick="User.signOut();">Sign out</a>

        <div id="app_about">
            This application is served by
            <a target="_blank" href="https://github.com/CreatCodeBuild/hyper2web">Hyper2Web</a>
            , an enjoyable Python web framework written by me.
        </div>
    </div>`
});
