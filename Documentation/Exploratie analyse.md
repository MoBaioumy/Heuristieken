Bij deel opdrachten A & B, werken onze oplossingen het best voor wijk 2 en dus minder goed voor wijken 1 en 3. Hoe kan dat? 


|                 | Wijk 1 | Wijk 2 | Wijk 3 |
| --------------- | ------ | ------ | ------ |
| Lower bound     | 53188  | 45268  | 42757  |
| Beste oplossing | 56230  | 45628  | 43891  |
| Difference      | 5,41%  | 0,79 % | 2.58 % |

Er zijn een aantal factoren die bepalen hoe makkelijk het probleem aan te pakken is met onze oplossing. De belangerijkste zijn:

- De posities van de batterijen vergeleken met de huizen
- De spreiding van de capaciteiten van de huizen


## De posities van de batterijen

Om dit te illustreren kunnen we naar wijk 1 kijken:

![Wijk 1](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/wijk_1.png)

In dit plaatje zijn 4 van de 5 batterijen erg bij elkaar in de buurt. Dit zorgt ervoor dat velen huizen een lange grid afstand zullen hebben en daardoor ook een hoge lower bound heeft. Om te vergelijken hoe 'handig' de batterijen geplaatst zijn kijken we naar de lower bound van de grid kosten. Vervolgens kijken we naar lower bound na dat de batterijen met K_means optimaal geplaatst zijn.

|               | Wijk 1 | Wijk 2 | Wijk 3 |
| ------------- | ------ | ------ | ------ |
| Before K_mean | 53188  | 45268  | 42757  |
| After K_means | 39490  | 40102  | 40615  |
| Difference    | 25.7%  | 11.4%  | 5.0 %  |

Het overduidelijk dat wijk 1 veel 'onhandigere' posities heeft voor de batterijen vergeleken met 2 en 3. 

Omdat 4 van de 5 batterijen bij elkaar liggen in een hoek, en de andere precies aan de tegenovergestelde kant ligt, zullen veel huizen die niet meer bij de ene batterij in de rechterhoek passen, waardoor ze een lange afstand moeten overbruggen naar de andere batterijen. Voor de lower bound maakt dit niets uit, want de helft van de huizen ligt het dichtsbij de batterij in de rechterhoek. Maar omdat we deze huizen niet alleemaal kunnen verbinden met deze batterij raken we ver van de lower bound verwijdert. Je kunt daarom ook wel zeggen dat onze oplossing niet per se slechter is, maar de sprijding van de huizen en batterijen het maakt dat we per definitie nooit dicht in de buurt van de lower bound kunnen komen (althans, hoe we deze nu hebben berekent). 

De vraag blijft echter nog wel, waarom doet wijk 2 het beter dan wijk 3? Zoals je in de cijfers van de k-means analyse ziet, zijn de batterijen beter geplaatst in wijk 3 dan in wijk 2. Toch komen we minder dicht bij de lower bound. Om een antwoord hierop te geven moeten we naar de spreiding van de capaciteiten van de huizen kijken.

## De spreiding van de capaciteiten 

Als je huizen vergelijkbare capaciteiten hebben, heb je een kleinere marge om wissels te maken met een Hill Climber. De wijken hebben ook hele andere verdelingen voor de spreiding van de capaciteiten. 

![Wijk 1](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/spreading_wijk_1.PNG)  ![Wijk 2](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/spreading_wijk_2.PNG)  ![Wijk 3](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/spreading_wijk_3.PNG)

Zoals als hier te zien is, wijk 3 heeft een erg smalle sprijding vergeleken met 1 en 2. De aantal stappen is ook het best voor wijk 2. Dit geeft weer een verklaring waarom we het dichts bij de lower bound in wijk 2 komen; de grote spreiding in capaciteit geeft ons veel ruimte om wissels te maken, zodat we dichter bij de lower bound kunnen komen. 

|                                               | Wijk 1 | Wijk 2 | Wijk 3 |
| --------------------------------------------- | ------ | ------ | ------ |
| Mogeljike <br />stappen met<br />Hill climber | 72     | 134    | 84     |
