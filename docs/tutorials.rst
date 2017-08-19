=========
Tutorials
=========

Chapter 1: Set Up the Server
============================

In this tutorial, we will create a simple HTML5 game together. The game will teach you most aspects of our framework. We will only focus on backend. Frontend code will be provided.

Our framework works on both Linux and Windows systems. I will use Unix/Linux conventions/terms in this tutorial.

First, we need to create our project. Create a new directory/folder named :code:`Game`. Under it, create a Python script named :code:`app.py` and a directory named :code:`public`.

:code:`app.py` will contains all backend code and all frontend code will go into :code:`./public` directory.

Now, put this piece of code in :code:`app.py`.

.. code-block:: python

    from hyper2web import app

    # let's only bind ip address to localhost for now. Later we will change it.
    # port number is up to you. any number larger than 1000 should be fine.
    app = app.App(address="localhost", port=5000)
    
    # up() starts the server.
    app.up()


Next, let's write the frontend. Create a :code:`index.html` file in :code:`./public`. Put this piece of code in it.

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>The Game</title>
    </head>
    <body>
        Congratulations, you have set up the server correctly! <br>
        We will start to create our game next!
    </body>
    </html>
    
As you might know, Hyper2Web only uses HTTP/2. H2 uses HTTPS by default. Therefore, you need to have a pair of ssl keys in your top level directory. You can either generator your own keys or copy the key files in the `example 
<https://github.com/CreatCodeBuild/hyper2web/tree/master/example/game>`_. Copy and paste files with the name :code:`localhost.*` to your :code:`Game` directory.

Now, let's start the server. Open your terminal under :code:`Game` directory and type

.. code-block:: console

    $ python app.py
    
Now open your browser and go to :code:`https://localhost:5000`. You should be able to see the webpage you just wrote.

Congratulations! Now our server is running. The next chapter will teach you some basic RESTful routing.


Chapter 2: Static File Server
=============================
Although you might want your App to be as dynamic as possible, you have to first understand how a static website is served.

The convention is to have a :code:`public` directory under your project directory and have all your static files there.

For example, if the client does :code:`GET /some_file.format`, the framework will try to read the path :code:`public/some_file.format` and sent what it read to the client. If the path does not exist, then the framework simply reports resource not found.

Therefore, you can easily just put all your frontend code under the public directory and start serving your application.

Chapter 3: REST
===============
Web is built on HTTP and HTTP is all about semantics. While there are thousands of ways to build HTTP API, the one which our framework embraces is REST. Since our audience's experience varies, I do not want to confuse you by explaining too much about REST. The only thing you need to know is that HTTP requests are all about semantics and a REST API is a semantic API.

Let's dive into the example code and you will understand it.

First, let's see the frontend code:

.. code-block:: JavaScript

    fetch('/top10', {method: 'GET'});

:code:`fetch()` is the new browser API which does async HTTP requests. It is better than :code:`XMLHttpRequest` in almost every aspects. It has a cleaner interface which fits RESTful API design.

This line creates a HTTP GET request with :code:`:path` = :code:`/top10`. How to respond to this request is 100% up to the server. Now, in :code:`app.py`, write this piece of code:

.. code-block:: Python

    # define API's callback function
    async def top10_api(request, response):
        await response.send("some data")
    
    # register this function
    app.get("top10", top10_api)
    # you can also do
    # app.get("/top10", top10_api)

Now, whenever the client does such a request, :code:`top10_api` will be run by the framework. We call this function the endpoint of a REST API. You can define the function as whatever you need, but have to include the :code:`async` and :code:`await` key words.

Chapter 4: Parameterized REST
=============================

Chapter 5: Persistent Storage
=============================
