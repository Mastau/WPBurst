# WPBurst

>Version 0.1 README

### *WordPress Target Enumerator & Passive Vulnerability Scanner (MVP)*

WPBurst est un outil d'énumération WordPress moderne, modulaire et
extensible.\
Il collecte des informations avancées sur une instance WordPress, puis
exécute un ensemble de modules CVE **passifs** pour détecter
automatiquement les vulnérabilités connues **sans réexécuter de scan**.

Ce MVP est conçu pour poser les fondations d'un scanner complet :
fiable, rapide et facile à étendre.

------------------------------------------------------------------------

##  Features (MVP)

### Wordpress Enumeration

-   Détection WordPress (wp-login, meta, readme)
-   Détection de la version WordPress (meta, readme, wp-json)
-   Détection du thème actif et thèmes présents
-   Enumération des utilisateurs (`?author=ID`)
-   Enumération avancée de l'API REST :
    -   récupération des routes
    -   validation des endpoints
    -   extraction des namespaces

### Plugins & Versions

-   Détection des plugins via :
    -   wordlist personnalisée
    -   parsing HTML
    -   heuristiques de plugins communs
    -   présence physique des dossiers
-   Extraction automatique de version :
    -   `readme.txt` → `Stable tag`
    -   fichier principal du plugin (`header PHP`)
-   Fallback automatique lorsque les readme sont réécrits

### Modules CVE Passifs

-   Chargement automatique des modules présents dans `/modules/`
-   Analyse passive basée sur les données d'énumération
-   Retourne les vulnérabilités détectées sous forme structurée
-   Aucun scan supplémentaire requis
-   Exemple inclus : `CVE-2018-20979` (Contact Form 7 \<= 5.0.3)

### CLI Professionnel

-   Auto-help
-   Wordlist optionnelle
-   Listing des modules CVE disponibles
-   Architecture prête pour l'ajout de fonctionnalités avancées

------------------------------------------------------------------------

## Installation

``` bash
git clone https://github.com/ton-repo/WPBurst.git
cd WPBurst

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

------------------------------------------------------------------------

## Usage

### Scan d'une instance WordPress

``` bash
python3 -m cli.main http://target.tld
```

------------------------------------------------------------------------

## Lister les modules CVE disponibles

``` bash
python3 -m cli.main --list-modules
```

------------------------------------------------------------------------

## Utiliser une wordlist personnalisée

``` bash
python3 -m cli.main http://target.tld -w plugins.txt
```

------------------------------------------------------------------------

## Architecture technique

    WPBurst/
    │
    ├── cli/
    │   └── main.py
    │
    ├── core/
    │   ├── enumeration.py
    │   └── module_loader.py
    │
    ├── modules/
    │   ├── cve_cf7_2018_20979.py
    │   └── ...
    │
    ├── plugins.txt
    └── README.md

------------------------------------------------------------------------

## Roadmap

-   Moteur CVE avancé
-   Modules actifs `run()`
-   Export JSON / HTML
-   Scan rapide multithread
-   Détection avancée des thèmes & environnements

------------------------------------------------------------------------

## Contribuer

PR bienvenues !

------------------------------------------------------------------------

## Licence

Soon..


------------------------------------------------------------------------

## Remerciements

[K@rlBl0ck](https://github.com/Karlblock)\
[at0m741](https://github.com/at0m741)\
[bonsthie](https://github.com/bonsthie)



