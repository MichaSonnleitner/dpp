from dataclasses import dataclass

@dataclass
class Token:
	typ: str
	wert: str

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

@dataclass
class Funktion:
	name: str
	parameter: list
	block: list

@dataclass
class FunktionAufruf:
	name: str
	argumente: list

@dataclass
class Rückgabe:
	wert: str

@dataclass
class VarFunktionAufruf:
	typ: str
	name: str
	funk_name: str
	argumente: list

@dataclass
class Eingabe:
	wert: str