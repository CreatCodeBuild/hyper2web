import json


def update_record(this_record, old_records):
	timeUsed = this_record['timeUsed']

	levelIndex = str(this_record['level'])
	level_top10 = old_records.get(levelIndex, [])

	i = 0
	while i < 10 and i < len(level_top10):
		if timeUsed < level_top10[i]['timeUsed']:
			level_top10.insert(i, this_record)
			break
		i += 1
	else:
		level_top10.insert(i, this_record)
	if len(level_top10) > 10:
		level_top10.pop()

	old_records[levelIndex] = level_top10


game_record_path = 'game_record.json'

try:
	with open(game_record_path, encoding='utf8') as f:
		game_record = json.load(f, encoding='utf8')
except json.decoder.JSONDecodeError and FileNotFoundError:
	print('init a new record')
	game_record = {}
