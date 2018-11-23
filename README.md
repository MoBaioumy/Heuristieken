# Heuristieken

## Smart Grid
### Mohamed Baioumy, Thomas Hoedeman, Philip Oosterholt

This repository is for the course *'Heuristieken'* of fall 2018. Our project is about [Smart Grids](http://heuristieken.nl/wiki/index.php?title=SmartGrid).

### Description problem

Groene energie is de energie van de toekomst, en zelf produceren is de mode van nu. Veel huizen hebben tegenwoordig zonnepanelen, windmolens of andere installaties om zelf energie mee te produceren. Fortuinlijk genoeg produceren die installaties vaak meer dan voor eigen consumptie nodig is. Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en produktie te kunnen managen moeten er batterijen geplaatst worden.

Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit.

### Probleem A

Verbind alle huizen in de drie wijken aan een batterij. De maximumcapaciteit van de huizen mag die van de batterijen uiteraard niet overschrijden.

### Probleem B

De batterijen kosten 5000 per stuk. De kabels kosten 9 per grid-segment. De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de manhattan distance. Bereken de kosten voor de in a) geconfigureerde wijk. Probeer je SmartGrid te optimaliseren en vind een zo goed mogelijke configuratie van kabels.

### Algoritmes

#### Greedy algoritme:

Voor het greedy algoritme maken we gebruik van de method find_closest_house waarbij het dichtstbijzijnde huis wordt gezocht voor een batterij. 

De batterijen worden één voor één gevuld met huizen m.b.v. de find_closest_house method. Telkens wordt het dichtstbijzijnde huis gepakt tot de batterij capaciteit op het niveau zit waarbij de batterij capaciteit - de capaciteit van het dichtstbijzijnde huis tussen de 5 en de maximale output van het huis valt. In dit geval gaan we opzoek naar het huis dat qua capaciteit goed in de overgebleven capaciteit van de batterij past. Wanneer er meerdere huizen onder die voorwaarde vallen, kiezen we het huis met de kortste afstand. Als de overgebleven capaciteit nog boven de 10 valt, dan doen we hetzelfde als hiervoor beschreven, maar dan met twee huizen tegelijk.

#### Greedy hill climber: 

De greedy hill climber pakt de input van het greedy algortime, en gaat per huis af of er andere huizen zijn bij andere batterijen die kunnen wisselen van plek (dus de capaciteit wordt niet overschreden), en berekent vervolgens of de totale afstand van beide huizen minder wordt als er wordt gewisseld. Als dit zo is dan worden de huizen gewisseld, dit gaat zo lang door tot er geen wissel meer kan worden gemaakt, we zitten hier dan in een lokaal minimum. 

#### State space probleem A + B

Met de constraint satisfaction dat batterijen geen maximum capaciteit hebben en alle huizen aan één batterij kunnen worden verbonden is de state space 5 ^ 150 ofwel 7.0e+104. 

#### Lower bound probleem A + B

De minimale kosten zijn de kosten van wanneer alle huizen aan de dichtstbijzijnde batterij zijn verbonden plus de kosten van de batterijen. De kosten functie is totaal lengte routes * kosten per route element + totaal aantal batterijen * kosten per batterij. 

De implementatie is te zien grid.py method shortest_paths.

Wijk 1: 3132 * 9 + 5000 * 5 = 53188
Wijk 2: 2252 * 9 + 5000 * 5 = 45268
Wijk 3: 1973 * 9 + 5000 * 5 = 42757

Tussenstand

Wijk 1: 
Greedy normaal = 60586
Greedy hill climber = 56536

Wijk 2: 
Greedy normaal = 49138
Greedy hill climber = 46258

Wijk 3: 
Simple = 69271
Greedy hill climber = 43927

#### Upper bound probleem A + B

De maximale kosten zijn de kosten van wanneer alle huizen aan de verste batterij zijn verbonden plus de kosten van de batterijen.

De implementatie is te zien grid.py method longest_paths.

Wijk 1: 8670 * 9 + 5000 * 5 = 103030
Wijk 2: 7917 * 9 + 5000 * 5 = 96253
Wijk 3: 8499 * 9 + 5000 * 5 = 101491

### Probleem C

Nu is het zo, dat de batterijen misschien niet op de best mogelijke plaatsen staan. Het verplaatsen van batterijen compliceert de zaak enorm, maar de opdrachtgever wil het toch proberen, om inzicht in het probleem te krijgen. Verplaats de batterijen, en probeer een beter resultaat te realiseren.

### Probleem D

Het bedrijf SmartBatteryCompany heeft recentelijk drie types batterijen ontwikkeld, met verschillende capaciteiten en verschillende prijzen. Probeer een betere configuratie voor de wijk te vinden met deze batterijen, je mag er zoveel gebruiken als je wil en kunnen op ieder gridpunt zonder huis geplaatst worden. Optimaliseer het smartGrid voor de drie wijken. 

### Probleem E

Nieuwe wetgeving vereist dat waar kabels onder een huis doorgaan, de bewoners een compensatie van 5000 mogen ontvangen. Dit verandert het schema enorm. Optimaliseer het smartGrid voor de drie wijken, met inachtneming van de nieuwe compensatieregeling.

### Probleem F

Maak zelf een aantal batterij-schema's zoals in d), en kijk welke makkelijker en welke moeilijk op te lossen zijn.



