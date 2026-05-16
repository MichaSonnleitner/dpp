DEBUG = False
import sys
from lexer import lexer
from parser import parser
from codegen import codegen

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

with open(sys.argv[1], "r", encoding="utf-8") as f:
	zeilen = f.readlines()

alle_tokens = []
for zeile in zeilen:
	zeile = zeile.strip()
	if zeile and not zeile.startswith("//"):
		alle_tokens += lexer(zeile)

ast = parser(alle_tokens)

if DEBUG:
    print("=== TOKENS ===")
    for token in alle_tokens:
        print(token)
    print("\n=== AST ===")
    for knoten in ast:
        print(knoten)

output = codegen(ast)
output_datei = sys.argv[1].replace(".dpp", ".py")
with open(output_datei, "w") as f:
	f.write(output)
print(f"\nCompiliert zu {output_datei}")