# Python HTTP2 Web Server Framework

I had heard of that HTTP2 was the future since the end of 2015 and I had watached some Python talks about HTTP2 in PyConf2016.

But one year has passed, I have not found any full HTTP2 server framework yet.

Also, async programming has been widely talked about but not many people seemed to actually do it. 
(Unless you consider JavaScript people, where they have no choice)

Furthermore, generator style async io is much more fun than callback style.

April 23rd, 2017, Sunday, I woke up and felt bored and decided to make one of my own. Since I had little prior web knowledge, this would be a super fun project for me.

# Dependency
Python3.5+  
Future version might only support Python3.6+ since `curio` might only support 3.6+ in the future.
```
pip install h2
pip install curio
```

# How to
Create a dir `public` or whatever names, put your frontend code there.

Then create an `app.py` or whatever names.
```
# app.py
from h2web import app

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
```
python app.py
```
