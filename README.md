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

### Algoritmes

#### Simple algortime

Het simple algortime verbind alle huizen in omgekeerde volgorde aan de batterijen
Dit geeft voor a) voor alle drie de wijken een oplossing (toevallig)
Dit algoritme wordt vooral gebruikt als vergelijking om in ieder geval een oplossing te hebben

#### Random algoritme

Het random algoritme verbind per battery random huizen totdat de capaciteit vol is
Garandeerd geen oplossing.
Wanneer dit algoritme wel een oplossing geeft kan deze gebruikt worden als beginpunt van een hillclimber

#### Greedy algoritme:

Voor het greedy algoritme maken we gebruik van de method find_closest_house waarbij het dichtstbijzijnde huis wordt gezocht voor een batterij.

De batterijen worden één voor één gevuld met huizen m.b.v. de find_closest_house method. Telkens wordt het dichtstbijzijnde huis gepakt tot de batterij capaciteit op het niveau zit waarbij de batterij capaciteit - de capaciteit van het dichtstbijzijnde huis tussen de 5 en de maximale output van het huis valt. In dit geval gaan we opzoek naar het huis dat qua capaciteit goed in de overgebleven capaciteit van de batterij past. Wanneer er meerdere huizen onder die voorwaarde vallen, kiezen we het huis met de kortste afstand. Als de overgebleven capaciteit nog boven de 10 valt, dan doen we hetzelfde als hiervoor beschreven, maar dan met twee huizen tegelijk.

#### Greedy hill climber:

De greedy hill climber pakt de input van het greedy algortime, en gaat per huis af of er andere huizen zijn bij andere batterijen die kunnen wisselen van plek (dus de capaciteit wordt niet overschreden), en berekent vervolgens of de totale afstand van beide huizen minder wordt als er wordt gewisseld. Als dit zo is dan worden de huizen gewisseld, dit gaat zo lang door tot er geen wissel meer kan worden gemaakt, we zitten hier dan in een lokaal minimum.

#### Random hill climber:
De random hill climber runt het random algoritme totdat deze een oplossing geeft. Vervolgens run hij de hillclimber op deze oplossing.
Het algoritme herhaalt dit totdat een gegeven aan tal herhalingen is bereikt of tot dat een oplossing onder de gegeven bound is gevonden.

#### State space probleem A + B

Met de constraint relaxation dat batterijen geen maximum capaciteit hebben en alle huizen aan één batterij kunnen worden verbonden is de state space 5 ^ 150 ofwel 7.0e+104.

Range (min - max) van huizen dat aan een batterij kan verbonden worden:
* Wijk 1: 21 - 45
* Wijk 2: 24 - 39
* Wijk 3: 28 - 32

#### Lower bound probleem A + B

De minimale kosten zijn de kosten van wanneer alle huizen aan de dichtstbijzijnde batterij zijn verbonden plus de kosten van de batterijen. De kosten functie is totaal lengte routes * kosten per route element + totaal aantal batterijen * kosten per batterij.

De implementatie is te zien grid.py method shortest_paths.

Wijk 1: 3132 * 9 + 5000 * 5 = 53188
Wijk 2: 2252 * 9 + 5000 * 5 = 45268
Wijk 3: 1973 * 9 + 5000 * 5 = 42757

**Tussenstand**

Wijk 1:
* Simple: **76642**
* Greedy normaal: **60586**
* Greedy hillclimber: **56536**
* Random hillclimber best: **56392**

Wijk 2:
* Simple: **66679**
* Greedy normaal: **49138**
* Greedy hillclimber: **46258**
* Random hillclimber best: **45736**

Wijk 3:
* Simple: **69271**
* Greedy normaal: **50371**
* Greedy hillclimber: **44125**
* Random hillclimber best: **43891** (na 1500 repeats)

#### Upper bound probleem A + B

De maximale kosten zijn de kosten van wanneer alle huizen aan de verste batterij zijn verbonden plus de kosten van de batterijen.

Hiervoor gaan we er vanuit dat men wel altijd de korste Manhattan route van een huis naar een batterij neemt.

De implementatie is te zien grid.py method longest_paths.

* Wijk 1: 8670 x 9 + 5000 * 5 = 103030
* Wijk 2: 7917 x 9 + 5000 * 5 = 96253
* Wijk 3: 8499 x 9 + 5000 * 5 = 101491

### Probleem C

Nu is het zo, dat de batterijen misschien niet op de best mogelijke plaatsen staan. Het verplaatsen van batterijen compliceert de zaak enorm, maar de opdrachtgever wil het toch proberen, om inzicht in het probleem te krijgen. Verplaats de batterijen, en probeer een beter resultaat te realiseren.

#### State space probleem C

2500 plekken - 150 huizen = 2350 plekken om de batterij te plaatsen. 2350 x 2349 x 2348 x 2347 x 2346 = 7.14e16. Dit is met heel weinig constraints (alleen huizen en batterijen mogen niet op elkaar staan).

#### Lower bound probleem C

#### Upper bound probleem C

### Probleem D

Het bedrijf SmartBatteryCompany heeft recentelijk drie types batterijen ontwikkeld, met verschillende capaciteiten en verschillende prijzen. Probeer een betere configuratie voor de wijk te vinden met deze batterijen, je mag er zoveel gebruiken als je wil en kunnen op ieder gridpunt zonder huis geplaatst worden. Optimaliseer het smartGrid voor de drie wijken.

### Probleem E

Nieuwe wetgeving vereist dat waar kabels onder een huis doorgaan, de bewoners een compensatie van 5000 mogen ontvangen. Dit verandert het schema enorm. Optimaliseer het smartGrid voor de drie wijken, met inachtneming van de nieuwe compensatieregeling.

### Probleem F

Maak zelf een aantal batterij-schema's zoals in d), en kijk welke makkelijker en welke moeilijk op te lossen zijn.
