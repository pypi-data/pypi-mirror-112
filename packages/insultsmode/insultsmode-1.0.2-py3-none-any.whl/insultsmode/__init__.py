import json
import requests

def ru():
	linkru = "https://evilinsult.com/generate_insult.php?lang=ru&type=json"
	responseru = requests.get(linkru).text
	mesru = json.loads(responseru)["insult"]
	return mesru
	
def en():
	linken = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
	responseen = requests.get(linken).text
	mesen = json.loads(responseen)["insult"]
	return mesen
