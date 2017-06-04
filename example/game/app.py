import json


from hyper2web import app


game_record_path = 'game_record.json'

try:
	with open(game_record_path, encoding='utf8') as f:
		game_record = json.load(f, encoding='utf8')
except json.decoder.JSONDecodeError and FileNotFoundError:
	print('init a new record')
	game_record = {}


app = app.App()
# should raise an error if no response method is called
async def post_record(http, stream, para):
	record = json.load(stream.data)
	http.send_error(stream, 200)

app.post('/post_record', post_record)


try:
	app.up()
except BaseException as e:
	pass
finally:
	with open(game_record_path, mode='w', encoding='utf8') as f:
		json.dump(game_record, f)
