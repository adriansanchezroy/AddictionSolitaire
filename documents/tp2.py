# Tableau avec les cartes alignées de manière à ce que deux cartes x et y
# ont la même couleur si x%4 == y%4 et la même valeur si x//4 == y//4.
# L'index des carte represente de maniere unique une carte d'une valeur et
# d'une couleur en particulier.
tabSVG = ["cards/AS.svg", "cards/AH.svg", "cards/AD.svg", "cards/AC.svg",
          "cards/2S.svg", "cards/2H.svg", "cards/2D.svg", "cards/2C.svg",
          "cards/3S.svg", "cards/3H.svg", "cards/3D.svg", "cards/3C.svg",
          "cards/4S.svg", "cards/4H.svg", "cards/4D.svg", "cards/4C.svg",
          "cards/5S.svg", "cards/5H.svg", "cards/5D.svg", "cards/5C.svg",
          "cards/6S.svg", "cards/6H.svg", "cards/6D.svg", "cards/6C.svg",
          "cards/7S.svg", "cards/7H.svg", "cards/7D.svg", "cards/7C.svg",
          "cards/8S.svg", "cards/8H.svg", "cards/8D.svg", "cards/8C.svg",
          "cards/9S.svg", "cards/9H.svg", "cards/9D.svg", "cards/9C.svg",
          "cards/10S.svg", "cards/10H.svg", "cards/10D.svg", "cards/10C.svg",
          "cards/JS.svg", "cards/JH.svg", "cards/JD.svg", "cards/JC.svg",
          "cards/QS.svg", "cards/QH.svg", "cards/QD.svg", "cards/QC.svg",
          "cards/KS.svg", "cards/KH.svg", "cards/KD.svg", "cards/KC.svg"]


# Fonction qui retourne un tableau de longueur 52 contenant des nombres
# de 0 à 51.
def tabCartes():
    tabCartes = []
    for i in range(52):
        tabCartes.append(i)

    return tabCartes


# Fonction qui brasse aleatoirement toutes les cartes au lancement du jeu.
# Retourne un tableau de 4 rangees de 13 colonnes
# Ne prend aucun argument
def shuffleInit():
    # Conserve la position des cartes affichée pour la partie en cours
    global paquetMelange
    # Maintient le nombre de brassage effectués
    global nbreShuffle
    # Décremente le nombre total de brassages restants,
    # initialisé à nbrShuffle = 4
    nbreShuffle -= 1
    # Initialise le paquet qui sera melangé
    paquetMelange = tabCartes()

    # Brassage des cartes
    for i in range(len(paquetMelange)-1, -1, -1):
        # Génere un index pseudo-random
        index = math.floor(random() * (i+1))
        # contient la carte à melanger
        temp = paquetMelange[i]
        # déplace une carte au hasard à la position de la carte à mélanger
        paquetMelange[i] = paquetMelange[index]
        # déplace la carte à mélanger à la position de la carte au hasard
        paquetMelange[index] = temp
    return paquetMelange


# Fonction qui brasse aléatoirement les cartes mal placées.
# N'est pas appelée au lancement du jeu. Est appelée sur clic du bouton
# "brasser les cartes". Ne prend aucun argument
def shuffleCartes():
    global paquetMelange
    global nbreShuffle

    # Indices des cartes qui ne doivent pas etre brassees
    indicesConserves = []
    for i in range(len(paquetMelange)-1):
        if (
            # premieres cartes d'une ligne sont des deux
            i % 13 == 0 and paquetMelange[i] // 4 == 1
        ):
            # Sauvegarde l'index du 2 en premiere colonne
            indicesConserves.append(i)
            counter = 1
            # Verifie si les cartes suivantes sont bien placées
            while (
                # tant que les cartes sont consecutives de meme famille
                paquetMelange[i + counter] == paquetMelange[i + \
                                                            (counter-1)] + 4
                # et tant que les cartes sont sur la meme ligne
                and i // 13 == (i+counter) // 13
            ):
                indicesConserves.append(i+counter)
                counter += 1

        # Brasse les cartes restantes dans les autres cas
        else:
            # Pas de brassage si les cartes sont bien placées
            if i in indicesConserves:
                continue
            else:
                # Génere un index pseudo-random
                index = math.floor(random() * (i+1))
                while index in indicesConserves:
                    index = math.floor(random() * (i+1))
                # contient la carte à melanger
                temp = paquetMelange[i]
                # déplace une carte au hasard à la position de la carte à mélanger
                paquetMelange[i] = paquetMelange[index]
                # déplace la carte à mélanger à la position de la carte au hasard
                paquetMelange[index] = temp
    nbreShuffle -= 1
    return paquetMelange


# Procédure pour afficher les cartes brassées
# fonction appelée par le document HTML
# Ne prends pas d'arguments
def brassage():
    shuffleCartes()
    document.querySelector('#main').innerHTML = styleHTML + afficherGrille()
    aideJoueur(paquetMelange)


# Fonction pour baliser avec <div> le tableau HTML
def div(contenu): return '<div id="jeu">' + contenu + '</div>'


# Fonction pour baliser avec <table> le tableau HTML
def table(contenu): return '<table>' + contenu + '</table>'


# Variable pour le style css
styleHTML = """
<style>
#jeu table {
    float: none;
}

#jeu table td {
    border: 0;
    padding: 1px 2px;
    height: auto;
}
#jeu table td img {
    height: auto;
}
</style>
"""


def boutonsHTML():
    global nbreShuffle
    if nbreShuffle > 0:
        boutons = """
        <div id="message">Vous pouvez encore
        <button onclick="brassage();">brasser les cartes </button>
        """ + str(nbreShuffle) + """
            "fois<br><button onclick="init()">Nouvelle partie </button></div>
        """

    else:
        boutons = """
        <div id="message">Vous ne pouvez plus brasser les cartes
        <br>
        <button onclick="init();">Nouvelle partie</button></div>
        """
    return boutons


# Fonction qui prend un entier non-negatif en paramètre et retourne
# une référence de forme #caseN vers l'élément DOM voulu.
def elem(n):
    return document.querySelector('#case' + str(n))


# Procédure pour initialiser le jeu et pour brasser les cartes
def init():
    global nbreShuffle
    nbreShuffle = 100
    shuffleInit()
    document.querySelector('#main').innerHTML = styleHTML + afficherGrille()
    aideJoueur(paquetMelange)


# Fonction qui génère et retourne le HTML injecté dans l'élément <div id='main'>
# de tp2.html afin d'afficher les cartes une à une, rangée par rangée.
# Ne prend aucun paramètre.
def afficherGrille():
    global resultat
    main = document.querySelector("#main")
    # accumule le code html généré dans une chaine de caracteres
    mainHtml = ''
    index = 0     # Compteur permettant de référencer chaque index
    # du tableau de cartes mélangées.

    # Genère le HTML qui affiche les cartes rangée par rangée
    for i in range(4):
        # Ajoute une rangée à la table dans la chaine html
        mainHtml += '<tr>'

        # Genere le HTML qui affiche les cartes dans une rangee
        for j in range(13):
            indexVal = paquetMelange[index]  # Variable pour la valeur
            # enregistrée à l'index n du
            # tableau de cartes mélangées

            # Cas spécial pour les as qui doivent être retirés
            if indexVal not in [0, 1, 2, 3] and indexVal != 0:
                mainHtml += ('<td id="case' + str(index) + '" '
                             + 'onclick="clic(' + str(index) + ')">'
                             + '<img src="' + str(tabSVG[indexVal]) + '">'
                             + ' </td>')

               # '" onclick="clic(' + str(index) + ')"'
            # Cas spécial pour les as qui doivent être retirés
            else:
                mainHtml += ('<td id="case' + str(index)
                             + '" onclick="clic(' + str(index) + ')">'
                             + '</td>')
                paquetMelange[index] = 0
            index += 1

    # Ferme la balise de rangée de tableau
    mainHtml += '</tr>'
    # Balise le cartes dans un élément <table>
    mainHtml = table(mainHtml)
    # Balise les le tableau de cartes affichees dans un <div>
    mainHtml = div(mainHtml)
    # Injecte un bouton a la fin de la chaine html
    mainHtml = mainHtml + boutonsHTML()
    return mainHtml


# Procédure qui prend un tableau de nombres de 0 à 52 mélangés par la fonction
# shuffleCartes. Cette procédure aide le joueur en surlignant en vert lime
# les cartes qui peuvent être déplacées.
def aideJoueur(paquetMelange):
    global tabCartesDeplaceables
    global carteSelectionnee
    carteSelectionnee = 0
    tabCartesDeplaceables = []   # Variable du tableau contenant la position
    # des cartes pouvant être déplacées
    tabDeuxDeplaceables = []  # Variable du tableau contenant la position des
    # 2 pouvant être déplacées

    n = 0  # Compteur permettant de référencer chaque index
    # du tableau de cartes mélangées.

    while n < 52:
        # Vérifie si la position voisinante est une carte est vide
        if (n + 1 < 52) and paquetMelange[n + 1] == 0:

            carte = paquetMelange[n]  # Variable pour la carte voisinant
            # une carte vide
            for j in range(52):
                # Variable pour la carte comparée à celle voisinant une carte
                # vide.
                carteComparee = paquetMelange[j]

                # Si la carte comparée a la même couleur et une valeur -1
                # comparativement à la carte voisinant une carte vide, le fond
                # de la carte comparée deviendra vert lime, indiquant qu'elle
                # peut être déplacée.
                if (
                    ((n + 1) % 13 != 0) and carte != 0
                        and carteComparee != 0
                        and carte != carteComparee
                        and carte % 4 == carteComparee % 4
                        and carte//4 == carteComparee//4-1
                ):
                    carteMobile = elem(j)
                    tabCartesDeplaceables.append(j)
                    carteMobile.setAttribute("style", 'background-color: lime')
                    carteSelectionnee += 1
                # Cas spécial pour traiter d'un début de rangée vide. Dans ce
                # cas précis, toutes les cartes de valeur 2 peuvent être
                # déplacées et donc leur fond deviendra vert lime.
                elif ((n + 1) % 13 == 0) or paquetMelange[0] == 0:
                    for i in range(52):
                        if (paquetMelange[i] in [4, 5, 6, 7]
                                and len(tabDeuxDeplaceables) < 4):
                            deux = elem(i)
                            deux.setAttribute(
                                "style", 'background-color: lime')
                            tabDeuxDeplaceables.append(i)
                            carteSelectionnee += 1

        n += 1
    tabCartesDeplaceables = tabCartesDeplaceables + tabDeuxDeplaceables


def clic(n):
    elem(n).removeAttribute('style')
    for i in range(52):
        if (paquetMelange[i] != 0
                and int(paquetMelange[n]) - 4 == int(paquetMelange[i])
                and n in tabCartesDeplaceables):
            posVide = i + 1
            elem(posVide).innerHTML = ('<img src='
                                       + str(tabSVG[paquetMelange[n]])
                                       + '>')
            elem(n).innerHTML = ""
            paquetMelange[i+1] = paquetMelange[n]
            paquetMelange[n] = 0
            break

        elif ((i == 0 or i % 13 == 0) and paquetMelange[i] == 0
                and n in tabCartesDeplaceables
                and paquetMelange[n] in [4, 5, 6, 7]):
            posVide = i
            elem(posVide).innerHTML = ("<img src=" +
                                       str(tabSVG[paquetMelange[n]]) + ">")
            elem(n).innerHTML = ""
            paquetMelange[i] = paquetMelange[n]
            paquetMelange[n] = 0
            break

    for i in range(len(tabCartesDeplaceables)):
        index = tabCartesDeplaceables[i]
        elem(index).removeAttribute('style')

    aideJoueur(paquetMelange)
    gameOver()
    winCondition()


# Fonction qui met fin au jeu si aucun coup n'est possible
# Ne prend aucun argument
def gameOver():
    global nbreShuffle
    if nbreShuffle == 0 and carteSelectionnee == 0:
        alert("Vous avez perdu !")


# Retourne vrai si toutes les cartes sont en ordre sur toutes les rangées
# de la grille d'affichage
# Prend le numero de la range en argument. Les rangees sont comptabilisées
# à partir de 0
def cartesEnOrdre(rangee):
    # Offset auquel counter est additionne pour parcourir les cartes d'une
    # rangee
    offsetRangee = rangee * 13

    # permet de consulter une carte et la suivante
    counter = 0

    # Index maximal pour lequel une carte doit etre placee
    indexMax = offsetRangee + 12

    cartesOrdonnees = 0
    # Verifie si les cartes sont:
    # 1. de valeur consecutives
    # 2. sont sur la meme ligne

    while (
        # Itere sur toutes les cartes d'une rangee
        offsetRangee + counter + 1 <= indexMax
    ):
        # Index de la
        # carte la plus elevée présentement sélectionnée
        indexCarteCourante = offsetRangee + counter
        indexCarteSuivante = offsetRangee + counter + 1

        valCarteCourante = paquetMelange[indexCarteCourante]
        valCarteSuivante = paquetMelange[indexCarteSuivante]
        # Si la carte suivante est un As ou que la carte suivante
        # n'est pas consecutive
        if (
            paquetMelange[indexCarteCourante] // 4 == 1
            and indexCarteCourante % 13 == 0
        ):
            cartesOrdonnees += 1
            print("checked for position 0 in rangee", rangee)
        elif (valCarteCourante + 4 == valCarteSuivante):
            cartesOrdonnees += 1
        elif (
            paquetMelange[offsetRangee] // 4 != 1
            or valCarteSuivante < 4
            or valCarteCourante + 4 != valCarteSuivante
        ):
            print("Returned False!", "Nombre de cartes ordonnees:",
                  cartesOrdonnees, "pour la rangee:", rangee)
            carteOrdonnees = 0
            return False

        # si on atteint la position 11 d'une rangee, elle est en ordre
        if cartesOrdonnees == 12:
            print("Rangee:", rangee, "est en ordre!")
            return True
        counter += 1
        print("Nombre de cartes ordonnees:",
              cartesOrdonnees, "pour la rangee:", rangee)


# Retourne vrai si les cartes sont en ordre dans les 4 rangees.
# Ne prend aucun argument
def winCondition():
    # Statut de la partie en cours
    victoire = False

    # Accumule le nombre de rangées en ordre
    nbRangeeEnOrdre = 0

    # Vérifie que les rangées sont en ordre
    for rangee in range(4):
        if rangeeOrdonnee(rangee) == True:
            nbRangeeEnOrdre += 1

    # Une victoire est représentée par 4 rangées en ordre
    if nbRangeeEnOrdre == 4:
        victoire = True
        alert("Victoire!")

    return victoire


def rangeeOrdonnee(rangee):
    # Offset auquel counter est additionne pour parcourir les cartes d'une
    # rangee
    offsetRangee = rangee * 13
    indexProchaineRangee = offsetRangee + 13
    carteRangee = paquetMelange[offsetRangee:indexProchaineRangee]
    print("Rangee de cartes: ", rangee, carteRangee)

    # si la premiere carte est un deux et que la derniere est vide
    if (carteRangee[0] // 4 == 1) and carteRangee[-1] == 0:

        # On sait que deux cartes dont deja bien placees
        cartesOrdonnees = 2

        # compare les cartes du 3 au roi pour une rangee
        for i in range(1, 11):
            if carteRangee[i] + 4 == carteRangee[i+1]:
                cartesOrdonnees += 1
                print("Cartes ordonnees:", cartesOrdonnees)
                continue
            else:
                print("non-consecutive cards in line")
                return False
    else:
        print("line", rangee, "not starting with 2 or ending with As")
        return False
    if cartesOrdonnees == 12:
        return True


init()
