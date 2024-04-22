# Idées et stratégies pour faire le scrapping

Créer une liste des enseignants à partir de la liste sur le site (https://www.inalco.fr/annuaire-enseignement-recherche). De là, il est possible d'avoir les cours et donc les salles occupées par chaque enseignant.

Une fois cette liste éffectuée, il sera surement plus facile de scrapper avec le planning en liste, pour obtenir les heures on peut utiliser regex pour détecter le pattern \*\*h** - \*\*h**. Puisqu'il est absolument régulier, même pour les heures à un chiffre (ex : 09h00). Les salles peuvent être détectée de la même manière \*.** ou Amphi *. A voir seulement si c'est possible de scrapper comme ça, vu que l'affichage du HTML en dynamique est assez dérangeant pour scrapper.

Les balises HTMl ont des noms tels que `GInterface.Instances[1].Instances[7]_Cours_0` et `GInterface.Instances[1].Instances[7]_Cours_1`. Il serait eventuellement possible de faire une boucle for pour chercher tous les élements qui répondent à ce type, et d'extraire le contenu jusqu'à ce qu'il n'y ait plus de tag comme ça, auquel cas, il pourrait passer à la liste suivante.
