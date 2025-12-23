# Analyse d'Empreinte Environnementale - Projet FOODTOOL

Ce repository contient un prototype de workflow statistique développé dans le cadre de ma candidature au doctorat à l'**UMR ITAP (INRAE)**.

## Objectifs du Projet
L'outil permet d'analyser et de visualiser l'impact environnemental des produits alimentaires en croisant les données d'**Agribalyse** et d'**OpenFoodFacts**. 

### Fonctionnalités Clés :
- **Benchmarking Automatisé** : Comparaison de l'impact carbone (CO2eq) et de l'empreinte eau d'un produit par rapport à la moyenne de sa catégorie.
- **Clustering (Machine Learning)** : Identification d'archétypes de produits via l'algorithme K-Means pour segmenter les profils d'impact.
- **Interface Interactive** : Développée avec Streamlit pour permettre une exploration fluide des données.

## Perspectives Doctorales
Ce prototype constitue la première brique d'un workflow plus complexe. L'étape suivante consiste à intégrer des méthodes d'**inférence bayésienne** pour :
1. Estimer les recettes de produits complexes à partir de données parcellaires.
2. Quantifier les incertitudes liées aux facteurs d'émission.

## Installation et Utilisation
Si vous souhaitez lancer l'application localement :
1. Clonez le dépôt.
2. Installez les dépendances : `pip install -r requirements.txt`.
3. Lancez l'app : `streamlit run app.py`.

## Données utilisées
- Données simulées basées sur **Agribalyse v3.1** et **OpenFoodFacts**.