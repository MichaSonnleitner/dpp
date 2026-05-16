from nodes import *

def wert_formatieren(wert, typ):
	if typ == "var":
		return wert           # Variable → kein Anführungszeichen
	elif typ == "text":
		return f'"{wert}"'    # String-Literal → Anführungszeichen
	else:
		return wert           # zahl/dz → direkt

def einrücken(code, stufen=1):
	prefix = "    " * stufen
	return "\n".join(prefix + zeile for zeile in code.splitlines())

def codegen(ast):
	ausgabe = []
	for knoten in ast:
		if isinstance(knoten, VarZuweisung):
			if knoten.typ == "text":
				ausgabe.append(f'{knoten.name} = "{knoten.wert}"')
			elif knoten.typ in ["zahl", "dz"]:
				ausgabe.append(f'{knoten.name} = {knoten.wert}')

		elif isinstance(knoten, Ausgabe):
			if knoten.typ == "var":
				ausgabe.append(f'print({knoten.wert})')
			elif knoten.typ == "text":
				ausgabe.append(f'print("{knoten.wert}")')
			elif knoten.typ in ["zahl", "dz"]:
				ausgabe.append(f'print({knoten.wert})')
			else:
				print(f"Unbekannter Ausgabe-Typ: {knoten.typ}")

		elif isinstance(knoten, Bedingung):
			ausgabe.append(f'if {knoten.wert1} {knoten.operator} {wert_formatieren(knoten.wert2, knoten.wert2_typ)}:')
			for dann_knoten in knoten.dann:
				zeile = codegen([dann_knoten])
				ausgabe.append(einrücken(zeile))
			# NEU: 5 Werte im Tuple (mit wert2_typ)
			for elif_wert1, elif_operator, elif_wert2, elif_wert2_typ, elif_block in knoten.elif_zweige:
				ausgabe.append(f'elif {elif_wert1} {elif_operator} {wert_formatieren(elif_wert2, elif_wert2_typ)}:')
				for elif_knoten in elif_block:
					zeile = codegen([elif_knoten])
					ausgabe.append(einrücken(zeile))
			if knoten.sonst:
				ausgabe.append('else:')
				for sonst_knoten in knoten.sonst:
					zeile = codegen([sonst_knoten])
					ausgabe.append(einrücken(zeile))

		elif isinstance(knoten, ForSchleife):
			ausgabe.append(f'for {knoten.var_name} in range({knoten.start}, {knoten.end} + 1):')
			for schleifen_knoten in knoten.schleifen_block:
				zeile = codegen([schleifen_knoten])
				ausgabe.append(einrücken(zeile))

		elif isinstance(knoten, MathOperation):
			if knoten.typ in ["zahl", "dz"]:
				ausgabe.append(f'{knoten.name} = {knoten.zahl1} {knoten.operator} {knoten.zahl2}')
			else:
				print(f"Unbekannter MathOperation-Typ: {knoten.typ}")

		elif isinstance(knoten, Funktion):
			parameter_str = ", ".join(knoten.parameter)
			ausgabe.append(f'def {knoten.name}({parameter_str}):')
			for block_knoten in knoten.block:
				zeile = codegen([block_knoten])
				ausgabe.append(einrücken(zeile))

		elif isinstance(knoten, FunktionAufruf):
			# Argumente sind schon fertig formatiert vom Parser
			argumente_str = ", ".join(knoten.argumente)
			ausgabe.append(f'{knoten.name}({argumente_str})')

		elif isinstance(knoten, VarFunktionAufruf):
			argumente_str = ", ".join(knoten.argumente)
			ausgabe.append(f'{knoten.name} = {knoten.funk_name}({argumente_str})')

		elif isinstance(knoten, Rückgabe):
			ausgabe.append(f'return {knoten.wert}')

		elif isinstance(knoten, Eingabe):
			ausgabe.append(f'{knoten.wert} = input()')

	return "\n".join(ausgabe)