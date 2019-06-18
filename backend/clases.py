from connection import *

def actual(lista, tx):
	result = lista[0]
	premio = lista[1] * 100000000
	tipo = lista[2]
	amount = lista[3]
	sql = []
	sql.append("UPDATE txs_ SET price_='%f', result='%s' WHERE (txid_='%s' and amount_='%f' and type_='%s');" % (premio, result, tx, amount, tipo))
	db(sql)

def save_price(lista, prize):
	sql = []
	for tx in lista: 
		ssql = "UPDATE txs_ SET pay_tx='%s' WHERE (txid_='%s' and price_ IS NOT NULL);" % (prize, tx)
		sql.append(ssql)
	db(sql)

def to_pay(dicc):
	unlock()
	prizeid = rpc("sendmany",['collecter', dicc])
	rpc("walletlock")
	return prizeid

def verify(winner, amount, tipo):
	modo = len(tipo)
	selection = list(tipo)

	if modo == 1:
		return entero(winner, amount, tipo)
	if modo == 2:
		return tonto(winner, amount, selection, tipo)
	if modo == 3:
		return fila(winner, amount, selection, tipo)
	if modo == 4:
		return cuadra(winner, amount, selection, tipo)
	if modo == 5:
		return columna(winner, amount, selection, tipo)
	if modo == 6:
		return sexta(winner, amount, selection, tipo)
	if modo == 7:
		return septima(winner, amount, selection, tipo)
	if modo == 8:
		return octava(winner, amount, selection, tipo)

def entero(winner, amount, tipo):
	if winner == tipo:
		a = round(amount * 15 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo)

def tonto(winner, amount, selection, tipo):
	if winner in selection:
		a = round(amount * 7.5 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo, amount)

def fila(winner, amount, selection, tipo):
	if winner in selection:
		a = round(amount * 5 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo, amount)

def cuadra(winner, amount, selection, tipo):
	if winner in selection:
		a = round(amount * 3.75 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo, amount)

def columna(winner, amount, selection, tipo):
	if winner in selection:
		a = round(amount * 3 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo, amount)

def sexta(winner, amount, selection, tipo):
	if winner in selection:
		a = round(amount * 2.5 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo, amount)

def septima(winner, amount, selection, tipo):
	if tipo == '1357bdf':
		if winner in selection:
			a = round(amount * 2 / 100000000, 8)
			return ('win', a, tipo, amount)
		elif winner == '0':
			a = round(amount / 100000000, 8)
			return ('tie', a, tipo, amount)
		else:
			return ('lost', 0, tipo, amount)
	if tipo == '2469ace':
		if winner in selection:
			a = round(amount * 2 / 100000000, 8)
			return ('win', a, tipo, amount)
		elif winner == '8':
			a = round(amount / 100000000, 8)
			return ('tie', a, tipo, amount)
		else:
			return ('lost', 0, tipo, amount)
	else:
		if winner in selection:
			a = round(amount * 2.14 / 100000000, 8)
			return ('win', a, tipo, amount)
		else:
			return ('lost', 0, tipo, amount)

def octava(winner, amount, selection, tipo):
	if winner in selection:
		a = round(amount * 1.87 / 100000000, 8)
		return ('win', a, tipo, amount)
	else:
		return ('lost', 0, tipo, amount)