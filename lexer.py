from nodes import Token

keywords = ["text", "zahl", "dz", "zeige", "wenn", "nicht", "und", "dann",
	"ende", "gleich", "wie", "var", "für", "von", "bis", "funktion", "zurück", "eingabe"]
type_keywords = ["text", "zahl", "dz", "var"]

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