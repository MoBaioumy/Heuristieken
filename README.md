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

