=========
Hyper2Web
=========
Super Fast HTTP2 Framework for Progressive Web Application

Installation
############

To install Hyper2Web, run this command in your terminal:

.. code-block:: console

    $ pip install hyper2web

This is the preferred method to install Hyper2Web, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Dependency
##########

Python3.6

h2

curio


Quick Start
###########

Assuming you have a directory structure like::

	your project/
	--public/
	  --index.html
	  --index.js
	  ...
	--app.py

Your ``app.py`` looks like

.. code-block:: python

	from hyper2web import app

	if __name__ == '__main__':

		# A basic callback style API is provided
		# Function name is up to you
		async def post_echo(request, response):
			# Send the data received back to the client
			await response.send(request.stream.data)

		app = app.App(port=5000)
		app.post('name', post_echo)
		app.up()


Then run this script

.. code-block:: console

	$ python app.py

That's it!

If you just want to serve static files, it's just 2 lines!

.. code-block:: python

	from hyper2web import app
	app.App(port=5000).up()


Docs
####
Documentation is hosted on hyper2web.readthedocs.io_.

.. _hyper2web.readthedocs.io: http://hyper2web.readthedocs.io

Example
#######

See the example folders for examples.

Test
####

.. code-block:: console

	$ python -m unittest discover test

Run all tests under ``test/`` dir.


Misc
####

Why did I create this framework?
********************************

April 23rd, 2017, Sunday, I woke up and felt bored and decided to create my own HTTP2 web framework.

Since I had little or some prior web knowledge, this would be a super learning and fun project for me.
