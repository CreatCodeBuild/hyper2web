from hyper2web import app, endpoint


if __name__ == '__main__':

	# A basic callback style API is provided
	async def get_name(handler: endpoint.EndPointHandler):
		print('k')
		print(handler.data)
		print(type(handler))
		print('data received', str(handler.data, encoding='utf8'))
		await handler.send_and_end('GET name hit')

	app = app.App(static_file_handle='auto', root_route='index.html')
	app.post('name', get_name)
	app.up()
	print(__package__)
