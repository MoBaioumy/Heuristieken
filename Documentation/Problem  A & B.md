Delen A en B van het problem zijn erg met elkaar verbonden en dus worden ze samen als een geheel presenteerd. 

### Probleem A

Verbind alle huizen in de drie wijken aan een batterij. De maximumcapaciteit van de huizen mag die van de batterijen uiteraard niet overschrijden.



### Probleem B

De batterijen kosten 5000 per stuk. De kabels kosten 9 per grid-segment. De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de manhattan distance. Bereken de kosten voor de in a) geconfigureerde wijk. Probeer je SmartGrid te optimaliseren en vind een zo goed mogelijke configuratie van kabels.



#### State space probleem A + B

Met de constraint relaxation dat batterijen geen maximum capaciteit hebben en alle huizen aan één batterij kunnen worden verbonden is de state space 5 ^ 150 ofwel 7.0e+104.

Range (min - max) van huizen dat aan een batterij kan verbonden worden:

| Wijk 1  | Wijk 2  | Wijk 3  |
| ------- | ------- | ------- |
| 21 - 45 | 24 - 39 | 28 - 32 |

#### Upper bound probleem A + B

De maximale kosten zijn de kosten van wanneer alle huizen aan de verste batterij zijn verbonden plus de kosten van de batterijen.

Hiervoor gaan we er vanuit dat men wel altijd de korste Manhattan route van een huis naar een batterij neemt.

De implementatie is te zien grid.py method longest_paths.

| Wijk 1                         | Wijk 2                        | Wijk 3                         |
| ------------------------------ | ----------------------------- | ------------------------------ |
| $8670 * 9 + 5000 * 5 = 103030$ | $7917 * 9 + 5000 * 5 = 96253$ | $8499 * 9 + 5000 * 5 = 101491$ |



#### Lower bound probleem A + B

De minimale kosten zijn de kosten van wanneer alle huizen aan de dichtstbijzijnde batterij zijn verbonden plus de kosten van de batterijen. De kosten functie is totaal lengte routes * kosten per route element + totaal aantal batterijen * kosten per batterij.

De implementatie is te zien grid.py method shortest_paths.

| Wijk 1                        | Wijk 2                        | Wijk 3                        |
| ----------------------------- | ----------------------------- | ----------------------------- |
| $3132 * 9 + 5000 * 5 = 53188$ | $2252 * 9 + 5000 * 5 = 45268$ | $1973 * 9 + 5000 * 5 = 42757$ |



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

#### Hill climber:

De hill climber pakt een oplossing van een ander algortime, en gaat per huis af of er andere huizen zijn bij andere batterijen die kunnen wisselen van plek (dus de capaciteit wordt niet overschreden), en berekent vervolgens of de totale afstand van beide huizen minder wordt als er wordt gewisseld. Als dit zo is dan worden de huizen gewisseld, dit gaat zo lang door tot er geen wissel meer kan worden gemaakt, we zitten hier dan in een lokaal minimum.

#### Random hill climber:

De random hill climber runt het random algoritme totdat deze een oplossing geeft. Vervolgens run hij de hillclimber op deze oplossing.
Het algoritme herhaalt dit totdat een gegeven aan tal herhalingen is bereikt of tot dat een oplossing onder de gegeven bound is gevonden.



**Tussenstand**

|                    | Wijk 1    | Wijk 2    | Wijk 3     |
| ------------------ | --------- | --------- | ---------- |
| Simple             | **76642** | **66679** | **69271**  |
| Greedy Normaal     | **60586** | **49138** | **50371**  |
| Greedy HillClimber | **56536** | **46258** | **44125**  |
| Random hillclimber | **56392** | **45736** | **43891^** |

​									***^ Na 1500 repeats***

