from hyper2web import app

if __name__ == '__main__':

	# A basic callback style API is provided
	async def get_name(http, stream):
		# this route essentially echo the data received back to client
		print('data received:')
		print(str(stream.data, encoding='utf8'))
		await http.send_and_end(stream, stream.data)

	app = app.App(static_file_handle='auto', root_route='index.html')
	app.post('name', get_name)
	app.up()
