import User from '../user.js';

// todo: should change to dependency injection instead of import User
// todo: what ever User should be passed in by the Vue instance which uses this component
Vue.component('app-menu', {
  template: `
<div class="app_menu app_menu-normal">
    <button>Button</button>
    <div 
      style="
        background: #AAAAAA;
      "
    >
        <img class="avatar" src="img/atom.ico" >
        <div style="margin-left: 20px; margin-top: 18px" class="g-signin2" data-onsuccess="User.onSignIn"></div>
        <a href="#" onclick="User.signOut();">Sign out</a>
    </div>
    <div
        class="options" style="
            background: #444444;
            height: 80%;"
    >
        <div class="option">战绩</div>
        <div class="option"></div>
    </div>
    <div id="app_about">
        This application is served by
        <a target="_blank" href="https://github.com/CreatCodeBuild/hyper2web">Hyper2Web</a>
        , an enjoyable Python web framework written by me.
    </div>
</div>`
});
