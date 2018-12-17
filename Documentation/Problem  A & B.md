<!-- # SmartGrid December 2018
Philip Oosterholt
Mohamed Baioumy
Thomas Hoedeman -->

Delen A en B van het problem zijn erg met elkaar verbonden en dus worden ze samen als een geheel presenteerd.

### Probleem A

*Verbind alle huizen in de drie wijken aan een batterij. De maximumcapaciteit van de huizen mag die van de batterijen uiteraard niet overschrijden.*

### Probleem B

*De batterijen kosten 5000 per stuk. De kabels kosten 9 per grid-segment. De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de manhattan distance. Bereken de kosten voor de in a) geconfigureerde wijk. Probeer je SmartGrid te optimaliseren en vind een zo goed mogelijke configuratie van kabels.*



#### State space probleem A + B

Met de constraint relaxation dat batterijen geen maximum capaciteit hebben en alle huizen aan één batterij kunnen worden verbonden is de state space 5 ^ 150 ofwel 7.0e+104.

Range (min - max) van huizen dat aan een batterij kan verbonden worden:

| Wijk 1  | Wijk 2  | Wijk 3  |
| ------- | ------- | ------- |
| 21 - 45 | 24 - 39 | 28 - 32 |

#### Upper bound probleem A + B

De maximale kosten zijn de kosten van wanneer alle huizen aan de verste batterij zijn verbonden plus de kosten van de batterijen.

Hiervoor gaan we er vanuit dat men wel altijd de korste Manhattan route van een huis naar een batterij neemt.

De implementatie is te zien grid.py method upper_bound

| Wijk 1                         | Wijk 2                        | Wijk 3                         |
| ------------------------------ | ----------------------------- | ------------------------------ |
| $8670 * 9 + 5000 * 5 = 103030$ | $7917 * 9 + 5000 * 5 = 96253$ | $8499 * 9 + 5000 * 5 = 101491$ |



#### Lower bound probleem A + B

De minimale kosten zijn de kosten van wanneer alle huizen aan de dichtstbijzijnde batterij zijn verbonden plus de kosten van de batterijen. De kosten functie is totaal lengte routes * kosten per route element + totaal aantal batterijen * kosten per batterij.

De implementatie is te zien grid.py method lower_bound

| Wijk 1                        | Wijk 2                        | Wijk 3                        |
| ----------------------------- | ----------------------------- | ----------------------------- |
| $3132 * 9 + 5000 * 5 = 53188$ | $2252 * 9 + 5000 * 5 = 45268$ | $1973 * 9 + 5000 * 5 = 42757$ |



### Algoritmes gebruikt voor A en B

#### Simple algortime

Het simple algortime verbind alle huizen in omgekeerde volgorde aan de batterijen
Dit geeft voor a) voor alle drie de wijken een oplossing (toevallig)
Dit algoritme wordt vooral gebruikt als vergelijking om in ieder geval een oplossing te hebben

#### Random algoritme

Het random algoritme verbind per batterij random huizen totdat de capaciteit vol is
Wanneer dit geen oplossing oplevert ontbind hij alle connecties en begint opnieuw totdat er resultaat is.

#### Greedy algoritme:

Voor het greedy algoritme maken we gebruik van de method find_closest_house waarbij het dichtstbijzijnde huis wordt gezocht voor een batterij.

De batterijen worden één voor één gevuld met huizen m.b.v. de find_closest_house method. Telkens wordt het dichtstbijzijnde huis gepakt tot de batterij capaciteit op het niveau zit waarbij de batterij capaciteit - de capaciteit van het dichtstbijzijnde huis tussen de 5 en de maximale output van het huis valt. In dit geval gaan we opzoek naar het huis dat qua capaciteit goed in de overgebleven capaciteit van de batterij past. Wanneer er meerdere huizen onder die voorwaarde vallen, kiezen we het huis met de kortste afstand. Als de overgebleven capaciteit nog boven de 10 valt, dan doen we hetzelfde als hiervoor beschreven, maar dan met twee huizen tegelijk.

### Greedy_alt:
Sorteert de huizen op output van hoog naar laag en verbind vervolgens de huizen van hoog naar laag aan de dichtstbijzijnde batterij. Indien dit geen oplossing opleverd vult hij de laatste huizen met het greedy algoritme

### Greedy_lookahead:
Zoekt elke keer het huis dat de korste verbinding heeft naar de dichtstbijzijnde batterij en verbind deze. Wanneer de capaciteit van een batterij tussen de minimale output en de gemiddelde output x N komt wordt een functie aangeroepen die alle combinaties afgaat om die batterij te vullen en dan de gene kiest die de korste afstand oplevert.
Wanneer er geen volledige oplossing is gegenereerd wordt greedy aangeroepen om de batterijen te vullen.

#### Hillclimber:

De hillclimbers zijn iteratief en verbeteren dus een bestaande oplossing. We hebben verschillende variaties op het hillclimber algoritme. Elke hill climber werkt in essentie hetzelfde, het gaat namelijk iteratief opzoek naar een verbetering en past deze verbetering toe. Dit gaat door tot dat er geen verbeteringen meer te vinden zijn. Hieronder staat per variatie beschreven wat de specifieke hill climbers doen.

#### Hillclimber Greedy:
Zoekt een random huis dat verbonden is en kijkt of en met welk ander huis een wissel gemaakt kan worden. De wissel die de beste verbetering geeft wordt uitgevoerd. Hij doet dit totdat er geen wissels meer mogelijk zijn.  

#### Hillclimber Greedy Double Swap:

Dit is een variatie op de greedy hillclimber. Het verschil is dat we 2 sets van 2 huizen verwisselen in plaats van 2 sets van 1 huis. Dit algoritme runt eerst op de greedy hill climber. Dit algoritme is aanzienlijk slomer, doordat het heel veel meer combinaties vergelijkt per iteratie, namelijk maximaal (150 * 149 * 148 * 147) i.p.v. (150 * 149). Het geeft doordat het de eerst de greedy hillclimber runt altijd een even goede of betere oplossing.

#### Hillclimber Random:

Deze hillclimber kiest elke keer random twee huizen, wanneer het wisselen van deze huizen de totale kosten verlaagt wordt deze uitgevoerd. Door het random element heeft deze hillclimber veel meer stappen nodig om tot een oplossing te komen waar geen wissels meer gemaakt kunnen worden. Dit algoritme is vooral geschreven om te kunnen vergelijke met simulated annealing.

#### Repeat random --> greedy hillclimber

De random hill climber runt het random algoritme totdat deze een oplossing geeft. Vervolgens run hij de hillclimber op deze oplossing.
Het algoritme herhaalt dit totdat een gegeven aantal herhalingen is bereikt of tot dat een oplossing onder de gegeven bound is gevonden. Random hill climber is een stochastisch algoritme, het geeft dus elke keer een andere oplossing. Dit zorgt ervoor dat we meer plekken in de state space kunnen exploreren dan de greedy hill climber. Met genoeg iteraties geeft dit ons ook de beste resultaten, alleen gemiddeld gezien zijn de resultaten minder goed dan de greedy hill climber resultaten.


#### Simulated annealing

Simulated annealing is een algoritme om lokale optima te vermijden door ook oplossingen te accepteren die de kosten niet verbeteren. Dit gebeurd aan de hand van verschillende koeling schema's. Met simualted annealing kun je uit lokale minima komen die een normale hillclimber beperken om de statespace verder te exploreren.

#### Repeat simulated annealing
Dit script wordt gebruikt om simualted annealing meerdere keren te herhalen en de resultaten eventueel te vergelijken met andere algoritmes.

**Tussenstand**

|                    | Wijk 1    | Wijk 2    | Wijk 3     |
| ------------------ | --------- | --------- | ---------- |
| Simple             | **75256** | **65329** | **69271**  |
| Greedy             | **58795** | **47896** | **46663**  |
| Greedy_alt         | **60667** | **47950** | **47509**  |
| Greedy_lookahead   | **57931** | **48202** | **51064**  |
| Greedy -> Hill     | **56365** | **45664** | **43891**  |
| Greedy -> D Hill   | **56536** | **45781** | **44125**  |
| Random --> Greedy hillclimber | **56230** | **45628** | **43891**  |
| Iteraties r. hill  | **65000** | **130000**| **40000**  |
| Lower bound        | **53188** | **45268** | **42757**  |

|                                         | Wijk 1    | Wijk 2    | Wijk 3     |
| --------------------------------------- | --------- | --------- | ---------- |
|verschil lower bound en beste oplossing  | **5,41%** | **0,79%** | **5,00%**    |



Een Vergelijking van de algoritmes is gedaan en gevisualizeerd in de volgende figuur.

![Solution Comparison](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/Solutions_comparison.png)

De oranje normaale verdeling geeft de set van random oplossingen aan. De blauwe verdeling heeft de random oplossingen aan nadat ze getransformeerd zijn met een Hill Climber.


Zoals aan de figuur te zien is, een random oplossing gecombineerd met Hill Climber geeft vaak een betere oplossing dat een Greedy Algorithme (Verticale gele lijn). Echter is een Greedy algorithme gecombineerd met een Hill Climber beter dan de meeste random oplossingen met een Hill Climber.

Zoals aan de figuur te zien is, een random oplossing gecombineerd met Hill Climber geeft vaak een betere oplossing dat een Greedy Algorithm (Verticale gele lijn). Echter is een Greedy algoritme gecombineerd met een Hill Climber beter dan de meeste random oplossingen met een Hill Climber.



De oplossing die het best voor ons werkte in de Double Hill Climber. Dit houdt in dat we 2 sets van 2 huizen verwisselen in plaats van 2 sets van 1 huis. De oplossing is ook erg dicht bij de lower bound van de oplossing.
