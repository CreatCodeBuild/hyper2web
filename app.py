from hyper2web import app

if __name__ == '__main__':

	app = app.App()

	# A basic callback style API is provided
	async def post_name(http, stream, parameters):
		# this route essentially echo the data received back to client
		print('data received:')
		print(str(stream.data, encoding='utf8'))
		await http.send_and_end(stream, stream.data)
	app.post('name', post_name)

	async def get_user(http, stream, parameters):
		print(parameters)
		await http.send_error(stream, 200)
	app.get('user/{userId}', get_user)

	app.up()
