# Heuristieken

## **Smart Grid**
##### Mohamed Baioumy, Thomas Hoedeman, Philip Oosterholt #####

This repository is for the course *'Heuristieken'* of fall 2018. Our project is about [Smart Grids](http://heuristieken.nl/wiki/index.php?title=SmartGrid).

### Description problem

Groene energie is de energie van de toekomst, en zelf produceren is de mode van nu. Veel huizen hebben tegenwoordig zonnepanelen, windmolens of andere installaties om zelf energie mee te produceren. Fortuinlijk genoeg produceren die installaties vaak meer dan voor eigen consumptie nodig is. Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en produktie te kunnen managen moeten er batterijen geplaatst worden.

Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit.

### Probleem A

Verbind alle huizen in de drie wijken aan een batterij. De maximumcapaciteit van de huizen mag die van de batterijen uiteraard niet overschrijden.

### Probleem B

De batterijen kosten 5000 per stuk. De kabels kosten 9 per grid-segment. De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de manhattan distance. Bereken de kosten voor de in a) geconfigureerde wijk. Probeer je SmartGrid te optimaliseren en vind een zo goed mogelijke configuratie van kabels.

### Data structure

Om deze problemen op te lossen hebben we een data structuur gecreerd met de volgende objecten

* Grid
* Battery
* Route
* House

Hieronder zijn per object de bijhorende eigenschappen, methods & algortimes beschreven

#### Grid

Eigenschappen
* ID - (int)
* Wijk name - (string)
* Houses - (list)
* Unconnected houses - (list)
* Batteries - (list)
* Groote - (tuple)

Methods
* Load houses: laad huizen van csv file
* Load batteries: laad huizen van csv file
* Connect: verbind een huis aand een batterij. De method creert een route, deze route wordt in de batterij geplaatst en in de route wordt het huis geplaats. Verwijderd het huis uit de lijst met onverbonden huizen
en
* Disconnect: plaats een huis terug in onverbonden en verwijderd de bijhorende route uit de batterij.
* Disconnect_all: disconnect alle huizen in de grid
* Calculate_total_cost: bereken de kosten van de grid met de huidige verbinding inclusief de kosten van de batteirjen
* Shortest_paths: vind het kor
* Longest_paths: vind alle korste afstanden naar een batterij van elk huis
* draw grid: creert een visuele represenatie van de grid
* draw_route: tekent een route
* range_connected: berekent het bereik van huizen dat aan een batterij verbonden kan worden dus hoeveel minimaal en hoeveel maximaal

Algoritmes --  voor een beschrijving zie het kopje algortime hieronder
* Simple
* Random
* Greedy_alt
* Greedy
* Find_best_option
* Greedy_optimized
* Random_hillclimber


#### Batterij

Eigenschappen
* ID (int)
* Locatie (tuple)
* Max capaciteit (float)
* Huidige capaciteit (float)
* Type (string)
* Kosten (int)
* Routes (list)
* Kosten routes (int)

Methods
* Move: verplaats een battery en update bijhorende routes
* Find closest house: vind het dichtbijzijnde huis voor deze batterij
* Calculate routes cost: berekent de kosten van alle verbonden routes

#### Route

Eigenschappen
* ID: (int)
* Huis: (House object)
* Batterij ID: (int)
* Batterij locatie: (tuple)
* Lengte: (int)
* Kosten gridline: 9
* Kosten: (int)
* Grid route: (list)

Methods
* Plan Manhattan grid route: plant de fysieke route op de grid en plaatst alle coordinaten in de Grid route lijst

#### House

Eigenschappen

* ID: (int)
* Locatie: (tuple)
* Max output: (float)
