# generate_snippets.py
import json
import os
os.makedirs("dpp-vscode/snippets", exist_ok=True)

snippets = {
    "Wenn-Bedingung": {
        "prefix": "wenn",
        "body": [
            "wenn ${1:variable} gleich wie ${2|text,var,zahl,dz|} ${3:wert} dann",
            "\t$0",
            "ende"
        ],
        "description": "Wenn-Bedingung"
    },
    "Wenn-Nicht-Und (elif)": {
        "prefix": "wnu",
        "body": [
            "wenn nicht und ${1:variable} gleich wie ${2|text,var,zahl,dz|} ${3:wert} dann",
            "\t$0",
            "ende"
        ],
        "description": "Elif-Zweig"
    },
    "Wenn-Nicht (else)": {
        "prefix": "wn",
        "body": [
            "wenn nicht dann",
            "\t$0",
            "ende"
        ],
        "description": "Else-Zweig"
    },
    "Funktion": {
        "prefix": "funktion",
        "body": [
            "funktion ${1:name} ${2:parameter}",
            "\t$0",
            "ende"
        ],
        "description": "Funktion definieren"
    },
    "Für-Schleife": {
        "prefix": "für",
        "body": [
            "für ${1:i} von ${2:1} bis ${3:10}",
            "\t$0",
            "ende"
        ],
        "description": "For-Schleife"
    },
    "Zeige": {
        "prefix": "zeige",
        "body": "zeige ${1|text,var,zahl,dz|} ${2:wert}",
        "description": "Ausgabe"
    },
    "Variable Text": {
        "prefix": "text",
        "body": "text ${1:name} = ${2:wert}",
        "description": "Text-Variable"
    },
    "Variable Zahl": {
        "prefix": "zahl",
        "body": "zahl ${1:name} = ${2:0}",
        "description": "Zahl-Variable"
    },
    "Variable Dz": {
        "prefix": "dz",
        "body": "dz ${1:name} = ${2:0.0}",
        "description": "Dezimalzahl-Variable"
    },
    "Eingabe": {
        "prefix": "eingabe",
        "body": "eingabe ${1:variable}",
        "description": "Benutzereingabe"
    },
    "Zurück": {
        "prefix": "zurück",
        "body": "zurück ${1:wert}",
        "description": "Rückgabewert"
    }
}

with open("dpp-vscode/snippets/dpp.json", "w", encoding="utf-8") as f:
    json.dump(snippets, f, indent=4, ensure_ascii=False)

print("✓ snippets/dpp.json generiert!")