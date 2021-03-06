<!-- # SmartGrid December 2018
Philip Oosterholt
Mohamed Baioumy
Thomas Hoedeman -->

## Data Structure

Om deze problemen op te lossen hebben we een data structuur gecreerd met de volgende objecten

- Grid
- Battery
- Route
- House

Hieronder zijn per object de bijhorende eigenschappen, methods & algortimes beschreven

#### Grid

Eigenschappen

- ID - (int)
- Wijk name - (string)
- Houses - (list)
- Unconnected houses - (list)
- Batteries - (list)
- Size - (tuple)

Methods

- Load houses: laad huizen van csv file
- Load batteries: laad huizen van csv file
- Connect: verbind een huis aand een batterij. De method creert een route, deze route wordt in de batterij geplaatst en in de route wordt het huis geplaats. Verwijderd het huis uit de lijst met onverbonden huizen
  en
- Disconnect: plaats een huis terug in onverbonden en verwijderd de bijhorende route uit de batterij.
- Disconnect_all: disconnect alle huizen in de grid
- Calculate_total_cost: bereken de kosten van de grid met de huidige verbinding inclusief de kosten van de batteirjen
- Lower bound: berekent de lower bound
- Upper bound: berekent de upper bound
- draw grid: creert een visuele representatie van de grid
- swap: wisselt 2 of 4 batterijen
- move_batteries_random: verplaatst de batterijen naar random plekken
- range_connected: berekent het bereik van huizen dat aan een batterij verbonden kan worden dus hoeveel minimaal en hoeveel maximaal


#### Batterij

Eigenschappen

- ID (int)
- Locatie (tuple)
- Max capaciteit (float)
- Huidige capaciteit (float)
- Type (string)
- Kosten (int)
- Routes (list)
- Kosten routes (int)

Methods

- Move: verplaats een battery en update bijhorende routes
- Find closest house: vind het dichtbijzijnde huis voor deze batterij
- Calculate routes cost: berekent de kosten van alle verbonden routes

#### Route

Eigenschappen

- ID: (int)
- Huis: (House object)
- Batterij ID: (int)
- Batterij locatie: (tuple)
- Lengte: (int)
- Kosten gridline: 9
- Kosten: (int)
- Grid route: (list)

Methods

- Plan Manhattan grid route: plant de fysieke route op de grid en plaatst alle coordinaten in de Grid route lijst

#### House

Eigenschappen

- ID: (int)
- Locatie: (tuple)
- Max output: (float)


#### Algoritmes --  voor een beschrijving zie de documentatie van de sub vragen.

- Simple (A)
- Random (A)
- Greedy_alt (B)
- Greedy (B)
- Greedy_lookahead (B)
- Hillclimber greedy (B)
- Hillclimber greedy double swap (B)
- Hillclimber random (B)
- K means (C)
- Oilslick (C)
