from configparser import ConfigParser
import requests
import pymysql
import json

parser = ConfigParser()
parser.read('/home/phglz/Desktop/Satoshing/setup.ini')

min_conf = int(parser.get('settings', 'min_conf'))
min_bet = int(parser.get('settings', 'min_bet'))
max_bet = int(parser.get('settings', 'max_bet'))

def unlock():
	secret = parser.get('node', 'secret')
	rpc("walletpassphrase", [secret, 10])

def rpc(method, arg=[]):

	url = parser.get('node', 'url')
	auth = (parser.get('node', 'user'), parser.get('node', 'password'))
	headers = {"Content-type":"text/plain"}
	
	arg = json.dumps(arg)
	data = '{"jsonrpc": "2.0", "method": "%s", "id":"0", "params": %s}' % (method, arg)
	r = requests.post(url, auth=auth, headers=headers, data=data).json()
	return (r['result'])

def db(data):

	host = parser.get('db', 'host')
	user = parser.get('db', 'user')
	password = parser.get('db', 'password')
	db = parser.get('db', 'db')

	db = pymysql.connect(host, user, password, db)
	cursor = db.cursor()
	
	for x in data:
		cursor.execute(x)

	db.commit()
	db.close()
	return cursor.fetchall()