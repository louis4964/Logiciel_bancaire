# Simulateur Financier Polyvalent – Emprunts, Portefeuille & Impôts 

## Description
1. Ce logiciel est conçu pour aider les utilisateurs à simuler différents scénarios financiers liés à l’immobilier, aux investissements et à la fiscalité.
2. Il permet d’estimer la valeur d’un bien immobilier financé par un emprunt, de simuler l’évolution d’un portefeuille d’investissement avec ou sans mensualités, et de calculer l’impôt sur le revenu en fonction de la composition du foyer fiscal.
3. L’interface utilisateur simple et intuitive, développée avec Tkinter, affiche clairement les résultats des calculs.

## Fonctionnalités
1. Calculateur d’emprunt immobilier : Estime le prix du bien accessible, les frais de notaire, le capital emprunté et les intérêts payés.

2. Calculateur de portefeuille d’investissement : Simule la croissance du capital initial avec ou sans mensualités, applique le rendement choisi et calcule la valeur avant et après impôts.

3. Calculateur d’impôt sur le revenu : Intègre le barème progressif, le quotient familial, le plafonnement des avantages fiscaux et la gestion des pensions étudiantes.

4. Interface utilisateur : Interface claire et structurée en trois modules (Emprunt, Portefeuille, Impôt) avec affichage des résultats détaillés.

## Utilisation
- Pour un emprunt immobilier :
  Entrez le salaire mensuel net imposable, la durée de l’emprunt, le taux du crédit, la part du salaire allouée et le pourcentage d’apport.
  Cliquez sur Simuler pour afficher le capital, le prix de la maison et les frais.

- Pour un portefeuille d’investissement :
  Entrez le capital de départ, la durée de l’investissement, indiquez si des mensualités sont prévues, le montant des mensualités et le rendement attendu.
  Cliquez sur Simuler pour voir la valeur du portefeuille avant et après impôts.

- Pour le calcul d’impôts :
  Entrez le nombre d’adultes, d’étudiants, d’enfants, le revenu annuel imposable et les pensions versées aux étudiants.
  Cliquez sur Simuler pour afficher le montant de l’impôt et le revenu net disponible.

## Structure 
- simulateur_bancaire.py : 
    1. Fichier principal de l’application, contenant l’interface et la logique de calcul avec les 3 fonctions principales.

- emprunt – 
    1. Calcule le prix de la maison, 
    2. les frais de notaire, 
    3. le capital et les intérêts.

- portefeuille – 
    1. Simule l’évolution d’un portefeuille avec ou sans mensualités 
    2. calcule les liquidités après impôts.

- impots – 
    1. Calcule l’impôt annuel selon la composition du foyer et les revenus.

- README.md : Documentation du projet.
- requirements.txt : Liste des dépendances nécessaires (numpy, matplotlib, tkinter).

## Contributions
Les contributions sont les bienvenues ! N'hésitez pas à soumettre un pull request.

## Licence
Ce projet est sous licence MIT.

## Auteur 
Louis Thomas