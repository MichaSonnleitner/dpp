from nodes import *

def mit_anführung(wert):
	try:
		float(wert)
		return wert
	except:
		return f'"{wert}"'

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
			ausgabe.append(f'if {knoten.wert1} == {mit_anführung(knoten.wert2)}:')
			for dann_knoten in knoten.dann:
				zeile = codegen([dann_knoten])
				ausgabe.append(f'    {zeile}')
			for elif_wert1, elif_wert2, elif_block in knoten.elif_zweige:
				ausgabe.append(f'elif {elif_wert1} == {mit_anführung(elif_wert2)}:')
				for elif_knoten in elif_block:
					zeile = codegen([elif_knoten])
					ausgabe.append(f'    {zeile}')
			if knoten.sonst:
				ausgabe.append('else:')
				for sonst_knoten in knoten.sonst:
					zeile = codegen([sonst_knoten])
					ausgabe.append(f'    {zeile}')
		elif isinstance(knoten, ForSchleife):
			ausgabe.append(f'for {knoten.var_name} in range({knoten.start}, {knoten.end} + 1):')
			for schleifen_knoten in knoten.schleifen_block:
				zeile = codegen([schleifen_knoten])
				ausgabe.append(f'    {zeile}')
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
				ausgabe.append(f'    {zeile}')
		elif isinstance(knoten, FunktionAufruf):
			argumente_str = ", ".join(mit_anführung(a) for a in knoten.argumente)
			ausgabe.append(f'{knoten.name}({argumente_str})')
		elif isinstance(knoten, VarFunktionAufruf):
			argumente_str = ", ".join(mit_anführung(a) for a in knoten.argumente)
			ausgabe.append(f'{knoten.name} = {knoten.funk_name}({argumente_str})')
		elif isinstance(knoten, Rückgabe):
			ausgabe.append(f'return {knoten.wert}')
	return "\n".join(ausgabe)