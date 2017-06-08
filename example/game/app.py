import json

from curio import aopen

from hyper2web import app
from game import update_record, game_record, game_record_path


app = app.App(address="0.0.0.0", port=5000)
# should raise an error if no response method is called
# should raise an error if response method is not called with await
async def post_record(http, stream, para, response):
	record = json.loads(str(stream.data, encoding='utf8'))
	update_record(record, game_record)
	await http.send_error(stream, 200)

	# write records to disk
	async with aopen(game_record_path, mode='w') as f:
		game_record_string = json.dumps(game_record, indent='\t')
		await f.write(game_record_string)

app.post('/post_record', post_record)


async def get_top10(request, response):
	level_top10 = game_record.get(request.para['levelIndex'], [])
	string = json.dumps(level_top10)
	# await http.send_and_end(stream, bytes(string, encoding='utf8'))
	# response.set_header('xxx', 'xxx')
	response.set_header('content-length', str(len(string)))
	await response.send(bytes(string, encoding='utf8'))
app.get('/get_top10/{levelIndex}', get_top10)

app.up()
