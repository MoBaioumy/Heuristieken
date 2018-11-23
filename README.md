# Heuristieken

## Smart Grid
### Mohamed Baioumy, Thomas Hoedeman, Philip Oosterholt

This repository is for the course *'Heuristieken'* of fall 2018. Our project is about [Smart Grids](http://heuristieken.nl/wiki/index.php?title=SmartGrid).

### Description problem

Groene energie is de energie van de toekomst, en zelf produceren is de mode van nu. Veel huizen hebben tegenwoordig zonnepanelen, windmolens of andere installaties om zelf energie mee te produceren. Fortuinlijk genoeg produceren die installaties vaak meer dan voor eigen consumptie nodig is. Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en produktie te kunnen managen moeten er batterijen geplaatst worden.

Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit.

### Problem A

Verbind alle huizen in de drie wijken aan een batterij. De maximumcapaciteit van de huizen mag die van de batterijen uiteraard niet overschrijden.

#### State Space problem A

#### Lower bound problem A

#### Upper bound problem A

### Problem B

De batterijen kosten 5000 per stuk. De kabels kosten 9 per grid-segment. De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de manhattan distance.Bereken de kosten voor de in a) geconfigureerde wijk. Probeer je SmartGrid te optimaliseren en vind een zo goed mogelijke configuratie van kabels.

### Problem C

Nu is het zo, dat de batterijen misschien niet op de best mogelijke plaatsen staan. Het verplaatsen van batterijen vercompliceert de zaak enorm, maar de opdrachtgever wil het toch proberen, om inzicht in het probleem te krijgen. Verplaats de batterijen, en probeer een beter resultaat te realiseren.

### Problem D

Het bedrijf SmartBatteryCompany heeft recentelijk drie types batterijen ontwikkeld, met verschillende capaciteiten en verschillende prijzen. Probeer een betere configuratie voor de wijk te vinden met deze batterijen, je mag er zoveel gebruiken als je wil en kunnen op ieder gridpunt zonder huis geplaatst worden. Optimaliseer het smartGrid voor de drie wijken. 

### Problem E

Nieuwe wetgeving vereist dat waar kabels onder een huis doorgaan, de bewoners een compensatie van 5000 mogen ontvangen. Dit verandert het schema enorm. Optimaliseer het smartGrid voor de drie wijken, met inachtneming van de nieuwe compensatieregeling.

### Problem F

Maak zelf een aantal batterij-schema's zoals in d), en kijk welke makkelijker en welke moeilijk op te lossen zijn.



