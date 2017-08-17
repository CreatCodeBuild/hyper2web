const User = (function() {

	function onSignIn(googleUser) {
		let profile = googleUser.getBasicProfile();
		console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
		console.log('Name: ' + profile.getName());
		console.log('Image URL: ' + profile.getImageUrl());
		console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
	}

	function signOut() {
		let auth2 = gapi.auth2.getAuthInstance();
		auth2.signOut().then(function () {
			console.log('User signed out.');
		});
	}

	return {
		onSignIn: onSignIn,
		signOut: signOut,
		name: undefined
	}
})();

export default User
