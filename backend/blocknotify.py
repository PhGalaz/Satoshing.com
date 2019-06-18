#!/usr/bin/env python

import sys
import os
import json
import time
from sys import argv
import datetime
from clases import *
from connection import *
from cashaddress import convert

### NEW BLOCK
script, hash = argv
hassh = argv[1]
#hassh = '000000000000000002ebf2f78323b2c42107fe8378e386b184535abbe1e2702c'

#### PROCESSING DATA ####

posit = len(hassh) - 1
winner = hassh[posit:]
height = rpc("getblock", [hassh])['height']
confirmation = rpc("getblock", [hassh])['confirmations']

#### TIME PROCESSING ####

this_time = rpc("getblock", [hassh])['time']
previous = height - 1
previous_hash = rpc("getblockhash", [previous])
previous_time = rpc("getblock", [previous_hash])['time']
final_time = this_time - previous_time
time = str(datetime.timedelta(seconds=final_time))

#### INSERTING DATA ####

sql = []
sql.append("INSERT into block_ VALUES ('%d', '%s', '%s', '%d', '%d')" % (height, hassh, winner, confirmation, this_time))
db(sql)
sql = []
sql.append("DELETE FROM block_ WHERE confs_>10")
db(sql)

#### UPDATE TIME PREVIOUS BLOCK ####
previous = height - 1
sql = []
sql.append("UPDATE block_ SET time_='%s' WHERE height_='%d';" % (time, previous))
db(sql)

#Loop de actualizacion de confirmaciones de bloque
sql = []
sql.append('SELECT * from block_;')
results = db(sql)
for block_ in results:
	block = block_[1]
	height = block_[0]
	confs = rpc("getblock", [block])['confirmations']
	sql = []
	sql.append("UPDATE block_ SET confs_='%d' WHERE height_='%d';" % (confs, height))
	db(sql)

#Loop de actualizacion de confirmaciones de transaccion
sql = []
sql.append('SELECT * FROM txs_ WHERE confs_<=25;')
results = db(sql)
for txs_ in results:
	if txs_[2] != None:
		id_ = txs_[1]
		block = txs_[2]
		confs = rpc("getblock", [block])['confirmations']
		sql = []
		sql.append("UPDATE txs_ SET confs_='%d' WHERE txid_='%s';" % (confs, id_))
		db(sql)

sql = []
sql.append('SELECT * FROM pays_ WHERE confs_<=100;')
results = db(sql)
for txs_ in results:
	if txs_[1] != None:
		id_ = txs_[0]
		block = txs_[1]
		confs = rpc("getblock", [block])['confirmations']
		sql = []
		sql.append("UPDATE pays_ SET confs_='%d' WHERE txid_='%s';" % (confs, id_))
		db(sql)

### PAY WINNERS WITH min_conf CONFIRMATIONS AND COLLECT BENEFITS
sql = []
sql.append("SELECT * from txs_ WHERE confs_ = '%d'" % min_conf)
results = db(sql)

dicc = {}
winners = []
checked = []
for txs_ in results:
	id_ = txs_[1]
	block_ = txs_[2]
	posit = len(block_) - 1
	winner = block_[posit:]
	amount = txs_[3]
	type_ = txs_[5]
	result = txs_[9]
	if result == 'pwin' or result == 'ptie':
	    tx = rpc("gettransaction", [id_])['hex']
	    raw_tx = rpc("decoderawtransaction", [tx])
	    pre_id = raw_tx['vin'][0]['txid']
	    pre = rpc("getrawtransaction", [pre_id])
	    pre_vout = raw_tx['vin'][0]['vout']
	    input_raw_tx = rpc("decoderawtransaction", [pre])
	    address = input_raw_tx['vout'][pre_vout]['scriptPubKey']['addresses'][0]
	    result = verify(winner, amount, type_)

	    if address in dicc:
	    	dicc[address] = round(dicc[address] + result[1], 8)
	    else:
	    	dicc[address] = result[1]

	    actual(result, id_)
	    winners.append(id_)
if dicc != {}:
	price = to_pay(dicc)
	save_price(winners, price)
for txs_ in results:
	id_ = txs_[1]
	checked.append(id_)


### PAY WRONGS
sql = []
sql.append("SELECT * from txs_ WHERE confs_ = 25")
results = db(sql)

dicc = {}
winners = []
checked = []
for txs_ in results:
    id_ = txs_[1]
    block_ = txs_[2]
    posit = len(block_) - 1
    winner = block_[posit:]
    amount = txs_[3]
    type_ = txs_[5]
    result = txs_[9]
    if result == 'pwrong':
    	if amount > max_bet:
	        tx = rpc("gettransaction", [id_])['hex']        
	        raw_tx = rpc("decoderawtransaction", [tx])
	        pre_id = raw_tx['vin'][0]['txid']
	        pre = rpc("getrawtransaction", [pre_id])
	        pre_vout = raw_tx['vin'][0]['vout']
	        input_raw_tx = rpc("decoderawtransaction", [pre])
	        address = input_raw_tx['vout'][pre_vout]['scriptPubKey']['addresses'][0]
	        amounty = round(amount / 10 * 9 / 100000000, 8) 
	        if address in dicc:
	        	dicc[address] = dicc[address] + amounty
	        else:
	        	dicc[address] = amounty

	        lista = ('wrong', amounty, type_, amount)
	        actual(lista, id_)
	        winners.append(id_)
if dicc != {}:
	price = to_pay(dicc)
	save_price(winners, price)
for txs_ in results:
	id_ = txs_[1]
	checked.append(id_)