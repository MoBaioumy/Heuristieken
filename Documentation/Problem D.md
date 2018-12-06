### Probleem D

Het bedrijf SmartBatteryCompany heeft recentelijk drie types batterijen ontwikkeld, met verschillende capaciteiten en verschillende prijzen. Probeer een betere configuratie voor de wijk te vinden met deze batterijen, je mag er zoveel gebruiken als je wil en kunnen op ieder gridpunt zonder huis geplaatst worden. Optimaliseer het smartGrid voor de drie wijken.



#### State space probleem C





### Algorithmes

Dit probleem kan gesplitst worden in 2 delen. 

1. Je kan het aantal batterijen aanpassen voor elke wijk maar alle batterijen zijn en blijven homogeen
2. Je kan het type van de batterij veranderen



#### Silhouette Clustering

Voor het eerste deel van een probleem kan een cluster analysis gedaan worden om te bepalen wat de ideal aantal clusters is. Silhouette clustering een voor beeld daarvan. Vervolgens kan kunnen we verder zoals deel C. 

Het recept is dus als volgt:

1. **Bepaal de ideale aantal clusters met Silhouette**
2. **Bepaal positie van batterij met K_means**
3. **Greedy**
4. **Hill Climber/ double Hill Climber**



#### Variable weight clustering analysis

Als de type batterijen veranderd hebben geen gestructureerde manier om goede oplossingen te behalen. Er word op dit moment gewerkt aan een custom algorithme voor dit probleem waarin de clusters niet alleen gemaakt worden maar een gewicht geven worden. Hiermee word de juiste type batterij gekozen.