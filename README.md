# Super Fast HTTP2 server for Progressive Web Application


# Dependency
Python3.5+  
Future version might only support Python3.6+ since `curio` might only support 3.6+ in the future.
```bash
pip install h2
pip install curio
```
I will make it available on pip once I have the first release.

This project is at its very early stage. I still need to learn a lot about h2, curio, HTTP and Web.  
[h2 Github](https://github.com/python-hyper/hyper-h2) [doc](https://python-hyper.org/h2/en/stable/)  
[curio Github](https://github.com/dabeaz/curio) [doc](https://curio.readthedocs.io/en/latest/)

# How to
First clone this repo to your disk.

Under this repo, create a dir `public` or whatever names, put your frontend code there.

Then create an `app.py` or whatever names.
```python
# app.py
from hyper2web import app

if __name__ == '__main__':

	# A basic callback style API is provided
	async def get_name(handler):
		print('GET name hit')
		await handler.send_and_end('GET name hit')

	async def post_message(handler):
		print('Data Received:', str(handler.data, encoding='utf8'))
		await handler.send_and_end(str(handler.data, encoding='utf8'))

	app = app.App(port=5000)	
	app.get('name', get_name)
	app.post('message', post_message)
	app.up()
```
Then run this script
```bash
python app.py
```
That's it! If you just want to serve static files, it's just 2 lines!
```python
from hyper2web import app
app.App(port=5000).up()
```

# Test
Python modules/packages and imports are confusing. You have to do
```python
python -m unittest test.The_Name_Of_the_Test_Script
```
under the root directory of this repo.

Or run
```python
python -m unittest discover test
```
to run all tests under `test/` dir.

There could be a better way but I am not sure yet. Again, `import` is confusing in Python once you get into packages.

# Misc
## Why did I create this framework?
April 23rd, 2017, Sunday, I woke up and felt bored and decided to create my own HTTP2 web framework.

Since I had little or some prior web knowledge, this would be a super learning and fun project for me.
