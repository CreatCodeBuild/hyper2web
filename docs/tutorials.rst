=========
Tutorials
=========

In this tutorial, we will create a simple HTML5 game together. The game will teach you most aspects of our framework. Also, we will be writing both frontend and backend.

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
    
Now, let's start the server. Open your terminal under :code:`Game` directory and type

.. code-block:: console

    $ python app.py
    
Now open your browser and go to :code:`https://localhost:5000`. You should be able to see the webpage you just wrote.

Congratulations! Now our server is running. The next chapter will teach you some basic RESTful routing.

=========
Chapter 2: REST
=========
