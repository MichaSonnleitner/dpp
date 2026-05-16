import sys
from dataclasses import dataclass

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
# ── Token Dataclass ──────────────────────────────
@dataclass
class Token:
	typ: str
	wert: str
# ── AST Knoten ───────────────────────────────────
@dataclass
class VarZuweisung:
	typ: str
	name: str
	wert: str
@dataclass
class Ausgabe:
	typ: str
	wert: str
@dataclass
class Bedingung:
	wert1: str
	operator: str
	wert2: str
	dann: list
	sonst: list
	elif_zweige: list

@dataclass
class ForSchleife:
	var_name: str
	start: str
	end: str
	schleifen_block: list

@dataclass
class MathOperation:
	name: str
	typ: str
	zahl1: str
	operator: str
	zahl2: str
# ── Keywords Listen ──────────────────────────────
keywords = ["text", "zahl", "dz", "zeige", "wenn", "nicht", "und", "dann", "ende", "gleich", "wie", "var", "für", "von", "bis"]
type_keywords = ["text", "zahl", "dz", "var"]
# ── Lexer Funktion ───────────────────────────────
def lexer(zeile):
	teile = zeile.split()
	tokens = []
	nach_zuweisung = False
	nach_zeige = False
	nach_gleich_wie = False
	nach_von = False
	nach_bis = False
	nach_operator = False
	for wort in teile:
		if wort in keywords:
			tokens.append(Token("KEYWORD", wort))
			nach_zuweisung = False
			if wort == "zeige":
				nach_zeige = True
			elif wort == "wie":
				nach_gleich_wie = True
			elif wort == "von":
				nach_von = True
			elif wort == "bis":
				nach_bis = True
			elif wort not in type_keywords:
				nach_zeige = False
		elif wort == "=":
			tokens.append(Token("ZUWEISUNG", wort))
			nach_zuweisung = True
		elif wort in ["+", "-", "*", "/"]:
			tokens.append(Token("OPERATOR", wort))
			nach_operator = True
			nach_zuweisung = False
			nach_zeige = False
			nach_gleich_wie = False
			nach_von = False
			nach_bis = False
		elif nach_zuweisung or nach_zeige or nach_gleich_wie or nach_von or nach_bis or nach_operator:
			tokens.append(Token("WERT", wort))
			nach_gleich_wie = False
			nach_von = False
			nach_bis = False
			nach_operator = False  
		else:
			tokens.append(Token("NAME", wort))
	return tokens
# ── Parser Funktion ──────────────────────────────
def parser(token_liste):
	knoten = []
	i = 0
	while i < len(token_liste):
		token = token_liste[i]
		if token.typ == "KEYWORD" and token.wert in type_keywords:
			var_name = token_liste[i + 1].wert
			if (i + 4 < len(token_liste) and
				token_liste[i + 4].typ == "OPERATOR"):
				zahl1    = token_liste[i + 3].wert
				operator = token_liste[i + 4].wert
				zahl2    = token_liste[i + 5].wert
				knoten.append(MathOperation(var_name, token.wert, zahl1, operator, zahl2))
				i += 6
			else:
				var_wert = token_liste[i + 3].wert
				knoten.append(VarZuweisung(token.wert, var_name, var_wert))
				i += 4
		elif token.typ == "KEYWORD" and token.wert == "zeige":
			zeige_typ  = token_liste[i + 1].wert
			zeige_wert = token_liste[i + 2].wert
			knoten.append(Ausgabe(zeige_typ, zeige_wert))
			i += 3
		elif token.typ == "KEYWORD" and token.wert == "wenn":
			wert1 = token_liste[i + 1].wert
			wert2 = token_liste[i + 4].wert
			i += 6
			# ── dann Block sammeln ────────────────
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
			dann_block = list(parser(dann_tokens))
			# ── elif/else sammeln ─────────────────
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
					elif_block = list(parser(elif_tokens))
					elif_zweige.append((elif_wert1, elif_wert2, elif_block))
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
					sonst = list(parser(sonst_tokens))
					break
				else:
					break
			knoten.append(Bedingung(wert1, "gleich", wert2, dann_block, sonst, elif_zweige))
		elif token.typ == "KEYWORD" and token.wert == "für":
			var_name = token_liste[i + 1].wert
			start    = token_liste[i + 3].wert
			end      = token_liste[i + 5].wert
			i += 6
			schleifen_tokens = []
			while i < len(token_liste):
				t = token_liste[i]
				if t.typ == "KEYWORD" and t.wert == "ende":
					i += 1
					break
				schleifen_tokens.append(t)
				i += 1
			schleifen_block = list(parser(schleifen_tokens))
			knoten.append(ForSchleife(var_name, start, end, schleifen_block))
		else:
			i += 1
	return knoten

# ── Hilfsfunktion ────────────────────────────────
def mit_anführung(wert):
    try:
        float(wert)  # ist es eine Zahl?
        return wert  # ja → kein ""
    except:
        return f'"{wert}"'  # nein → mit ""
	
# ── Code Generator ───────────────────────────────
def codegen(ast):
	ausgabe = []
	for knoten in ast:
		if isinstance(knoten, VarZuweisung):
			if knoten.typ == "text":
				ausgabe.append(f'{knoten.name} = "{knoten.wert}"')
			elif knoten.typ == "zahl":
				ausgabe.append(f'{knoten.name} = {knoten.wert}')
			elif knoten.typ == "dz":
				ausgabe.append(f'{knoten.name} = {knoten.wert}')
		elif isinstance(knoten, Ausgabe):
			if knoten.typ == "var":
				ausgabe.append(f'print({knoten.wert})')
			elif knoten.typ == "text":
				ausgabe.append(f'print("{knoten.wert}")')
			elif knoten.typ == "zahl":
				ausgabe.append(f'print({knoten.wert})')
			elif knoten.typ == "dz":
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
	return "\n".join(ausgabe)
# ── Datei einlesen ───────────────────────────────
with open(sys.argv[1], "r", encoding="utf-8") as f:
	zeilen = f.readlines()
# ── Alle Zeilen lexen ────────────────────────────
alle_tokens = []
for zeile in zeilen:
	zeile = zeile.strip()
	if zeile and not zeile.startswith("//"):  # ignoriere leere Zeilen und Kommentare
		alle_tokens += lexer(zeile)
# ── Parser + Codegen aufrufen ────────────────────
ast = parser(alle_tokens)
print("=== TOKENS ===")
for token in alle_tokens:
	print(token)
print("\n=== AST ===")
for knoten in ast:
	print(knoten)
# ── Output Datei ─────────────────────────────────
output = codegen(ast)
output_datei = sys.argv[1].replace(".dpp", ".py")
with open(output_datei, "w") as f:
	f.write(output)
print(f"\nCompiliert zu {output_datei}")