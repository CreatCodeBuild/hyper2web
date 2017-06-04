# Element Master Game Example
This example is a HTML5 game I created. The game is written in VueJS and is served by Hyper2Web.

# Backend functionality demonstrated by this game
0. GET
    Needless to say. GET has to work in order to load the page.
1. POST
    After the user beats a level, the front end sends(post) a time record to the backend. The backend keeps track of the best plays.
2. Server Push
    This HTTP/2 new feature is not supported by the framework yet.

    When it is supported, the user will get live update of top10 plays of the current level.

    In the old days of HTTP/1. One can only implements this update with WebSocket or constantly GET requests.
