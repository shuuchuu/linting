"""Utilisation de options.py et regles.py."""

from .options import Options
from .regles import JeuRegles

if __name__ == "__main__":
    jeu: JeuRegles[str]=JeuRegles()
    jeu.ajoute_dependance('A', 'B')
    jeu.ajoute_dependance( "B","C" )
    jeu.ajoute_dependance("C",    "D")

    options: Options[str] = Options( jeu )
    options.bascule("A")
    print(options.selectionnees)
    options.bascule('D')
    print(options.selectionnees)

    jeu2: JeuRegles[int] = JeuRegles()
    jeu2.ajoute_dependance(1,2)
    jeu2.ajoute_dependance(2,3)
    jeu2.ajoute_dependance(3,4)

    options2: Options[int] = Options(jeu2)
    options2.bascule(1)
    print(options2.selectionnees)

    jeu3: JeuRegles[str] = JeuRegles()
    dependances = [
        ("couleur",  "terminal"),
        ("unicode",  "terminal"),
        ("terminal", "sortie"),
    ]
    for a, b in dependances:
        jeu3.ajoute_dependance(a, b)
    jeu3.ajoute_conflit(
        "couleur",
        "brut"
    )
    jeu3.ajoute_conflit(
        "unicode",
        "ascii",
    )

    options3: Options[str] = Options(jeu3)
    options3.bascule("brut")
    options3.bascule("couleur")
    print(options3.selectionnees)
