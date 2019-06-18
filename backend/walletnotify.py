#!/usr/bin/env python

import sys
import os
import json
import time
from sys import argv
from datetime import datetime
from connection import *

script, hash = argv
txid = argv[1]
#txid = '1ba3ae6be9bf0d006f9f17e3c25079b173769f666d0a5a01a8980cf7a46cd892'

info = rpc("gettransaction", [txid])

confirmations = info['confirmations']
amount_total = float(info['amount']) * 100000000

sql = []
sql.append('SELECT COUNT(*) FROM txs_;')
results = db(sql)

if results[0][0] == 0:
	nuevo_total = amount_total
else:
	sql = []
	sql.append('SELECT totalwagered FROM txs_ ORDER BY id DESC LIMIT 1;')
	results = db(sql)	
	nuevo_total = amount_total + results[0][0]

if amount_total > 0:
	tran = info['details']
	for x in tran:
		amount = float(x['amount']) * 100000000
		monto = float(x['amount'])
		tipo = x['account']
		if amount >= min_bet and amount <= max_bet:
			if confirmations == 0:
				sql = []
				sql.append("INSERT INTO txs_(txid_, amount_, confs_, type_, totalwagered, result) VALUES ('%s', '%f', '%d', '%s', '%f', '%s')" % (txid, amount, confirmations, tipo, nuevo_total, 'pending'))
				db(sql)
			else:
				blockhash = info['blockhash']
				posit = len(blockhash) - 1
				winner = blockhash[posit:]
				selection = list(tipo)
				rpc("move", [tipo, 'collecter', monto])
				if winner in selection:
					sql = []
					sql.append("UPDATE txs_ SET block_='%s', confs_='%d', result='%s' WHERE (txid_='%s' and type_='%s');" % (blockhash, confirmations, 'pwin', txid, tipo))
					db(sql)
				else:
					if (tipo == '1357bdf' and winner == '0') or (tipo == '2469ace' and winner == '8'):
						sql = []
						sql.append("UPDATE txs_ SET block_='%s', confs_='%d', result='%s' WHERE (txid_='%s' and type_='%s');" % (blockhash, confirmations, 'ptie', txid, tipo))
						db(sql)
					else:
						sql = []
						sql.append("UPDATE txs_ SET block_='%s', confs_='%d', result='%s' WHERE (txid_='%s' and type_='%s');" % (blockhash, confirmations, 'lost', txid, tipo))
						db(sql)

		else:
			if confirmations == 0:
				sql = []
				sql.append("INSERT INTO txs_(txid_, amount_, confs_, type_, totalwagered, result) VALUES ('%s', '%f', '%d', '%s', '%f', '%s')" % (txid, amount, confirmations, tipo, nuevo_total, 'ppwrong'))
				db(sql)
			else:
				rpc("move", [tipo, 'collecter', monto])
				blockhash = info['blockhash']
				sql = []
				sql.append("UPDATE txs_ SET block_='%s', confs_='%d', result='%s' WHERE txid_='%s';" % (blockhash, confirmations, 'pwrong', txid))
				db(sql)

else:
	if confirmations == 0:
		sql = []
		sql.append("INSERT INTO pays_(txid_, amount_, confs_) VALUES ('%s', '%f', '%d')" % (txid, amount_total, confirmations))
		db(sql)
	else:
		blockhash = info['blockhash']
		sql = []
		sql.append("UPDATE pays_ SET block_='%s', confs_='%d' WHERE txid_='%s';" % (blockhash, confirmations, txid))
		db(sql)