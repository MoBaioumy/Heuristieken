### Probleem C

*Nu is het zo, dat de batterijen misschien niet op de best mogelijke plaatsen staan. Het verplaatsen van batterijen compliceert de zaak enorm, maar de opdrachtgever wil het toch proberen, om inzicht in het probleem te krijgen. Verplaats de batterijen, en probeer een beter resultaat te realiseren.*

#### State space probleem C

2500 plekken - 150 huizen = 2350 plekken om de batterij te plaatsen. 2350 x 2349 x 2348 x 2347 x 2346 = 7.14e16. Dit is met heel weinig constraints (alleen huizen en batterijen mogen niet op elkaar staan).

#### Lower bound probleem C

|               | Wijk 1 | Wijk 2 | Wijk 3 |
| ------------- | ------ | ------ | ------ |
| Before K_mean | 53188  | 45268  | 42757  |
| After K_means | 39490  | 40102  | 40615  |
| Difference    | 25.7%  | 11.4%  | 5.0 %  |





### Algorithmes

### K Means

Het K Means algorithmes is een clustering algorithme. Er wordt een getal k (aantal clusters) gespecificeerd en vervolgens worden k clusters van de data set gemaakt. [Lees meer](https://en.wikipedia.org/wiki/K-means_clustering) 

Het werkt als volg in ons geval:

1. **In een random wijk met 50 huizen**
   ![1](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20optimal%20result/Figure%201.png)

2. **Plaats elke batterij op een ‘willekeurige’ plek**

   ![2](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20optimal%20result/Figure%202.png)

3. **Verbind elk huis met dichtstbijzijnde batterij**

   ![3](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20optimal%20result/Figure%203.png)

4. **Voor elke cluster huizen, verplaats de batterij naar de centroid**
   ![4](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20optimal%20result/Figure%204.png)

5. **Herhaal tot een optimaal resultaat**

   ![5](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20optimal%20result/Figure%205.png)
   ![6](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20optimal%20result/Figure%206.png)

   ​



Het recept van stap C gaat dus als volg:

1. **Bepaal positie van batterij met K_means**
2. **Greedy**
3. **Hill Climber/ double Hill Climber**





# Appendix

K_means kan voor een aantal situaties niet goed werken. Zie de volgende situatie bijvoorbeeld

Het K Means algorithmes is een clustering algorithme. Er wordt een getal k (aantal clusters) gespecificeerd en vervolgens worden k clusters van de data set gemaakt. [Lees meer](https://en.wikipedia.org/wiki/K-means_clustering) 

Het werkt als volg in ons geval:

1. **In een random wijk met 50 huizen**
   ![1](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20non%20optimal%20result/Figure%201.png)

2. **Plaats elke batterij op een ‘willekeurige’ plek**

   ![2](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20non%20optimal%20result/Figure%202.png)

3. **Verbind elk huis met dichtstbijzijnde batterij**

   ![3](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20non%20optimal%20result/Figure%203.png)

4. **Voor elke cluster huizen, verplaats de batterij naar de centroid**
   ![4](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20non%20optimal%20result/Figure%204.png)

5. **Herhaal tot een optimaal resultaat**

   ![5](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20non%20optimal%20result/Figure%205.png)
   ![6](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/kMeans%20-%20non%20optimal%20result/Figure%206.png)



Omdat de paarse batterij aan het begin geen huizen had, is zij verdwenen in de analyse. Ook kunnen oneindige loops bestaan als een huis precies in het midden staat van 2 batterijen. 

