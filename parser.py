import sys
from nodes import *

def fehler(nachricht):
	print(f"D++ Fehler: {nachricht}")
	sys.exit(1)

type_keywords = ["text", "zahl", "dz", "var"]

import sys
from nodes import *

def fehler(nachricht):
	print(f"D++ Fehler: {nachricht}")
	sys.exit(1)

type_keywords = ["text", "zahl", "dz", "var"]

def parser(token_liste, definierte_vars=None, definierte_funktionen=None):
	if definierte_vars is None:
		definierte_vars = set()
	if definierte_funktionen is None:
		definierte_funktionen = set()
	knoten = []
	i = 0
	while i < len(token_liste):
		token = token_liste[i]
		if token.typ == "KEYWORD" and token.wert in type_keywords:
			if i + 3 >= len(token_liste):
				fehler(f"Fehlender Wert nach '=' bei Variable '{token_liste[i+1].wert}'")
			var_name = token_liste[i + 1].wert
			var_wert = token_liste[i + 3].wert
			if var_wert in definierte_funktionen:
				argumente = []
				j = i + 4
				while j < len(token_liste) and token_liste[j].typ in ["NAME", "WERT"]:
					argumente.append(token_liste[j].wert)
					j += 1
				knoten.append(VarFunktionAufruf(token.wert, var_name, var_wert, argumente))
				definierte_vars.add(var_name)
				i = j
			elif (i + 4 < len(token_liste) and
				token_liste[i + 4].typ == "OPERATOR"):
				zahl1    = token_liste[i + 3].wert
				operator = token_liste[i + 4].wert
				zahl2    = token_liste[i + 5].wert
				knoten.append(MathOperation(var_name, token.wert, zahl1, operator, zahl2))
				definierte_vars.add(var_name)
				i += 6
			else:
				knoten.append(VarZuweisung(token.wert, var_name, var_wert))
				definierte_vars.add(var_name)
				i += 4
		elif token.typ == "KEYWORD" and token.wert == "zeige":
			zeige_typ  = token_liste[i + 1].wert
			zeige_wert = token_liste[i + 2].wert
			if zeige_typ == "var" and zeige_wert not in definierte_vars:
				fehler(f"Variable '{zeige_wert}' ist nicht definiert!")
			knoten.append(Ausgabe(zeige_typ, zeige_wert))
			i += 3
		elif token.typ == "KEYWORD" and token.wert == "wenn":
			wert1 = token_liste[i + 1].wert
			operator_wort = token_liste[i + 2].wert
			if operator_wort == "gleich":
				operator = "=="
			elif operator_wort == "größer":
				operator = ">"
			elif operator_wort == "kleiner":
				operator = "<"
			else:
				operator = "=="
			wert2 = token_liste[i + 4].wert
			i += 6
			dann_tokens = []
			while i < len(token_liste):
				t = token_liste[i]
				if t.typ == "KEYWORD" and t.wert == "ende":
					i += 1
					break
				if (t.typ == "KEYWORD" and t.wert == "wenn" and
					i + 1 < len(token_liste) and
					token_liste[i + 1].wert == "nicht"):
					break
				dann_tokens.append(t)
				i += 1
			dann_block = list(parser(dann_tokens, definierte_vars, definierte_funktionen))
			elif_zweige = []
			sonst = []
			while i < len(token_liste):
				t = token_liste[i]
				if (t.wert == "wenn" and
					i + 1 < len(token_liste) and
					token_liste[i + 1].wert == "nicht" and
					i + 2 < len(token_liste) and
					token_liste[i + 2].wert == "und"):
					elif_wert1 = token_liste[i + 3].wert
					elif_operator_wort = token_liste[i + 4].wert
					if elif_operator_wort == "gleich":
						elif_operator = "=="
					elif elif_operator_wort == "größer":
						elif_operator = ">"
					elif elif_operator_wort == "kleiner":
						elif_operator = "<"
					else:
						elif_operator = "=="
					elif_wert2 = token_liste[i + 6].wert
					i += 8
					elif_tokens = []
					while i < len(token_liste):
						t2 = token_liste[i]
						if t2.wert == "ende":
							i += 1
							break
						if (t2.wert == "wenn" and
							i + 1 < len(token_liste) and
							token_liste[i + 1].wert == "nicht"):
							break
						elif_tokens.append(t2)
						i += 1
					elif_block = list(parser(elif_tokens, definierte_vars, definierte_funktionen))
					elif_zweige.append((elif_wert1, elif_operator, elif_wert2, elif_block))
				elif (t.wert == "wenn" and
					i + 1 < len(token_liste) and
					token_liste[i + 1].wert == "nicht" and
					i + 2 < len(token_liste) and
					token_liste[i + 2].wert == "dann"):
					i += 3
					sonst_tokens = []
					while i < len(token_liste):
						t2 = token_liste[i]
						if t2.wert == "ende":
							i += 1
							break
						sonst_tokens.append(t2)
						i += 1
					sonst = list(parser(sonst_tokens, definierte_vars, definierte_funktionen))
					break
				else:
					break
			knoten.append(Bedingung(wert1, operator, wert2, dann_block, sonst, elif_zweige))
		elif token.typ == "KEYWORD" and token.wert == "für":
			var_name = token_liste[i + 1].wert
			start    = token_liste[i + 3].wert
			end      = token_liste[i + 5].wert
			definierte_vars.add(var_name)
			i += 6
			schleifen_tokens = []
			while i < len(token_liste):
				t = token_liste[i]
				if t.typ == "KEYWORD" and t.wert == "ende":
					i += 1
					break
				schleifen_tokens.append(t)
				i += 1
			schleifen_block = list(parser(schleifen_tokens, definierte_vars, definierte_funktionen))
			knoten.append(ForSchleife(var_name, start, end, schleifen_block))
		elif token.typ == "KEYWORD" and token.wert == "funktion":
			funk_name = token_liste[i + 1].wert
			definierte_funktionen.add(funk_name)
			i += 2
			parameter = []
			while i < len(token_liste) and token_liste[i].typ == "NAME":
				definierte_vars.add(token_liste[i].wert)
				parameter.append(token_liste[i].wert)
				i += 1
			block_tokens = []
			while i < len(token_liste):
				t = token_liste[i]
				if t.wert == "ende":
					i += 1
					break
				if t.wert == "zurück":
					block_tokens.append(t)
					block_tokens.append(token_liste[i + 1])
					i += 2
					break
				block_tokens.append(t)
				i += 1
			block = list(parser(block_tokens, definierte_vars, definierte_funktionen))
			knoten.append(Funktion(funk_name, parameter, block))
		elif token.typ == "KEYWORD" and token.wert == "zurück":
			rück_wert = token_liste[i + 1].wert
			knoten.append(Rückgabe(rück_wert))
			i += 2
		elif token.typ == "NAME":
			funk_name = token.wert
			i += 1
			argumente = []
			while i < len(token_liste) and token_liste[i].typ in ["NAME", "WERT"]:
				argumente.append(token_liste[i].wert)
				i += 1
			knoten.append(FunktionAufruf(funk_name, argumente))
		elif token.typ == "KEYWORD" and token.wert == "eingabe":
			var_name = token_liste[i + 1].wert
			definierte_vars.add(var_name)
			knoten.append(Eingabe(var_name))
			i += 2
		else:
			i += 1
	return knoten