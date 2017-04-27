# Super Fast HTTP2 server for Progressive Web Application


# Dependency
Python3.5+  
Future version might only support Python3.6+ since `curio` might only support 3.6+ in the future.
```bash
pip install h2
pip install curio
```

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

	app = app.App(static_file_handle='auto', root_route='index.html')
	app.get('name', get_name)
	app.up()
```
Then run this script
```bash
python app.py
```

# Todo list:
### 1. More Complete GET support
Pattern match of routes with regular expression.
```
app.get('user/+', func)
```
This matches `user/xxx` but not `user/`

Nested Routes
```
app.get('department/+/employee/+', func)
```

### 2. Support POST
As the title suggests.

### 3. Several Flavors of router API
#### Callback Style, which is inspired by ExpressJS (Partially Implemented)
```python
async def end_point_function(handler: EndPointHandler):
	# do something
	...
	# send_and_end will send data and end this HTTP2 stream
	await handler.send_and_end('some data')

app.get('rest_api_path', end_point_function)
```
#### Decorator Style, which is inspired by Flask
```python
@app.get('rest_api_path')
async def end_point_function(handler: EndPointHandler):
	# do something
	...
	# send_and_end will send data and end this HTTP2 stream
	await handler.send_and_end('some data')
```
#### Context Manager Style, which I don't even know if it is possible. I don't know how to implement it but sounds like a cool idea
```python
async with app.get('rest_api_path') as handler:
	# do something
	...
	# send_and_end will send data and end this HTTP2 stream
	await handler.send_and_end('some data')
```

### 4. Security
I have zero knowledge.

### 5. Syncronizing API
Maybe it's a bad idea.

# Misc
## Why did I create this framework?
April 23rd, 2017, Sunday, I woke up and felt bored and decided to create my own HTTP2 web framework for the sake of having fun and learning. 

Since I did not have much prior web knowledge, this would be a super learning project for me.

I had heard of that HTTP2 was the future since the end of 2015 and I had watached some Python talks about HTTP2 in PyConf2016.

But one year has passed, I have not found any full HTTP2 server framework yet.

Also, async programming has been widely talked about but not many people seemed to actually do it. 
(Unless you consider JavaScript people, where they have no choice)

Furthermore, generator style async io is much more fun than callback style.
