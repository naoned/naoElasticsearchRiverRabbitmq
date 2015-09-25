import json

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except ValueError, e:
		return False
	return True

def read_config(configFile):
	txt = open(configFile)
	json_conf = txt.read()
	if is_json(json_conf):
		return json.loads(json_conf)
	else:
		return json.loads("{}")
