NBA_bet — Interface de prédiction (Application Streamlit)
======================================================

Description
-----------
Cette application propose une interface web simple et interactive pour utiliser un modèle de prédiction NBA. L'objectif est de rendre l'exploration et l'utilisation du modèle accessibles à toute personne, sans compétences techniques : vous renseignez quelques paramètres et l'application affiche les résultats de façon claire et visuelle.

Lancer l'application
--------------------

```powershell
streamlit run predict.py
```

Utilisation (très générale)
--------------------------
- Choisissez les paramètres via les contrôles proposés (menus, champs, etc.).
- Soumettez pour obtenir la prédiction et visualisations associées.s

Techno (présentation non technique)
-----------------------------------
- L'interface est construite avec Streamlit, un outil qui facilite la création d'applications web interactives en Python.
- Le cœur prédictif repose sur un modèle pré-entraîné chargé par l'application.