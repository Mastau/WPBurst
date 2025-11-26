# Notes du projet

## Fait & A Faire

### Semaine du 03/11

Mise en place du Lab:
- Docker (Setup Wordpress & MariaDB)
- Script de lancement / config

Analyse existant:
- Analyse du code & du fonctionnement de WPScan pour l'enum

Analyse et compréhension de la CVE-2018-20979
- manipulation via le chall Mr Robot sur Vulnhub (https://www.vulnhub.com/entry/mr-robot-1,151/)

### Semaine du 10/11

Objectifs:
- Analyse de l'existant (Lecture des Medium/Writeup ect..) pour déterminer les tools utilisés
- Finalisation du Lab (Docker jetable avec 1 ou 2 plugins vulnerable install) > Seulement 2 modules seront présent dans le MVP
- Commencer la conception de l'architecture (Core (Back)/ CLI (Front) / Modules (Plugins))
- Commencer le dev engine (Core)
- Realiser le wiki au fur et a mesure


Listing tools: (Medium / Writeup / Github)

> Ma propre liste d'outils (Pour tous les Chall) : https://github.com/stars/Mastau/lists/ctf + Wappalyzer

Outils classiques:
- BurpSuite (Proxy / Scanner / Intruder)
- Owasp ZAP (Scanning / Fuzzing)
- Nikto (Scanning)
- SqlMap (Auto SQLInjection)
- Vega (Scan XSS, SQL & other vuln)
- Wfuzz (Scanning / Fuzzing)
- SkipFish (Recursive Crawler & intelligent heuristics)
- WpScan (Wordpress Enum)
- Acunetix (Enum XSS / SQL Injection)
- Metasploit (All in One Exploit framework)

Recommandations pour pentest Wordpress:
- Wappalyzer (WebExt Gather Information) (Super)
- WPIntel (WebExt Gather Information) (Connais pas mais complet)
- Nmap (Network Discovery) (Hors-sujet je connais les endpoints)
- ffuf (Directory discovering) (Les endpoints wp & plugins vulnerable sont deja connu mais toujours utile)
- Nuclei (Scans) (Connais pas )
- WPScan (Enum Vuln) (Super mais 10 call API per day)
- Commix (Cmd injection)
- Metasploit (Exploit framework) (Je vais faire mieux tu verras)


Fonctionnement engine
- Enumeration complete de la cible (plugins, versions, endpoints exposés, comportements HTTP, headers, etc)
- Croiser les données avec des CVE connus (Les 2 dans le modules pour le mvp)
- Utiliser un algo d'ajustement intelligent pour selectionner le bon exploit parmis plusieurs dispo (sans tous les tester) > Prioriser le payload qui a le + de chance de marcher


Etape 1 Enumeration enrichie

>Collecte toutes les données utiles :
>Versions exactes des plugins/thèmes.
>Routes REST exposées, endpoints admin-ajax.
>Headers serveur, comportement des codes HTTP.
>Schéma d’URL, paramètres GET/POST typiques.
>Indexation des fichiers /wp-json, /wp-admin/admin-ajax.php, etc.


Etape 2 Corrélation CVE

>Les CVE connues.
>Le type de vulnérabilité (XSS, RCE, File Upload, etc.).
>Les versions vulnérables et corrigées.
>Le pattern de la vulnérabilité (e.g. présence d’un paramètre particulier, d’un endpoint REST précis…).


Etape 3 Selection de l'exploit
score = (CVSS * plugin_popularity_weight) 
         + (match_score_based_on_signatures)
         + (presence_of_endpoint * 2)
         - (false_positive_likelihood)


Exemple:

Élément	            Valeur
Plugin détecté	    Jetpack
Version détectée	13.8
CVE connues         CVE-2024-9926, CVE-2023-4215
Endpoints REST  	/wp-json/jetpack/v4/
Headers spé         OK (WordPress 6.6.1, PHP 8.2)
Réponses HTTP	    200 pour /wp-json/jetpack/v4/, 403 pour /xmlrpc.php


CVE-2024-9926
CVSS : 7.4
Type : REST exposure (subscriber+)
Versions affectées : < 13.9.1
Fix : 13.9.1
Signature connue : endpoint /wp-json/jetpack/v4/

CVE-2023-4215
CVSS : 6.5
Type : Stored XSS
Versions affectées : < 13.6
Fix : 13.6

Facteur                         Description                                                                                         Pondération
CVSS	                        Gravité de la vulnérabilité	                                                                        directement utilisée
plugin_popularity_weight	    pondère selon la surface d’attaque (plus un plugin est populaire, plus la proba de vuln est forte)	1.2 pour Jetpack
match_score_based_on_signatures	mesure de ressemblance entre les patterns (endpoints, version, hash d’assets, etc.)	                entre 0–5
presence_of_endpoint	        bonus si le point d’entrée vulnérable est effectivement détecté	                                    ×2
false_positive_likelihood	    probabilité d’erreur selon incertitude sur la version	                                            entre 0–3 (soustrait)

CVSS = 7.4
plugin_popularity_weight = 1.2
match_score_based_on_signatures = 4 (endpoint REST présent)
presence_of_endpoint = 1 (oui)
false_positive_likelihood = 0.5 (faible incertitude)
Score = (7.4 × 1.2) + 4 + (1 × 2) − 0.5 
-> Score = 8.88 + 4 + 2 − 0.5 = 14.38


CVSS = 6.5
plugin_popularity_weight = 1.2
match_score_based_on_signatures = 1 (version possible mais pas de pattern présent)
presence_of_endpoint = 0 (endpoint non détecté)
false_positive_likelihood = 2 (incertitude sur la version)
Score = (6.5 × 1.2) + 1 + (0 × 2) − 2
-> Score = 7.8 + 1 − 2 = 6.8

CVE-2024-9926	14.38	Sélectionnée
CVE-2023-4215	6.8	    Trop incertaine



possible de use des heuristiques pondérées ou un système de règles adaptatives

Condition	Pondération	Exemple
Endpoint vulnérable détecté	+3	/wp-json/jetpack/v4
Version exacte vulnérable	+5	Jetpack 13.8
Version non précisée mais plugin détecté	+2	“jetpack” détecté sans version
Réponse HTTP anormale (403/401)	-1	
Exploit déjà testé sans succès	-3


### Semaine du 17/11

Objectifs:
- Commencer le dev engine (Core) 
    -> Recon (Enumeration)
- Schéma architecture ?
- Debut wiki (Gitbooks)

FAIT: 
- Commencer le dev engine
- Mise en place arborenscence modulaire en python (Analyse existant)
- Rework Lab (Passage sur NGINX et via une nouvelle config pour + de rapidité)
- Chercher des solutions concernant les rewrite rules des endpoints wordpress (/wp-content/plugins/asd/index.php == 200 )



Liste modulaire de plugins externe et pas en dure


### Semaine du 24/11

Objectifs :
- Finir la partie Enumeration du Core
- Creer un module CVE (Afin de preparer le terrain pour la suite)
- Wiki/doc ?
- Monter en compétence sur des Challs

FAIT:
- Fix plugins enumeration (Bypass rewrite rules WP)
    -> Utilisation d'un fingerprint de la home page (Comme vu semaine derniere)
- Mise en place de la liste de plugins > Scraping de http://plugins.svn.wordpress.org/ (Y a tout eheheheh: +100k plugins)
    -> Je reprend le scraper de Perfectdotexe (github) (RETIRED (Back soon with arg parser :/))
- Improve system enum plugins (+ plugins version)
- Ajout enum endpoint WP (wp-json)
- Ajout premier module CVE (CVE-2018-20979) + Listing modules & auto check


[*] Start enumerate
[+] WordPress detect with wp-login.php
[+] Version with meta: 6.8.3
[+] Listing plugins
[+] Loaded 80086 plugins from wordlist 'plugins.txt'
    [+] Found plugin folder: akismet

ça fonctionne ! (Ptite barre de chargement, elapse time ? c'est affreux)
[+] Checking plugins 7750/80086 (64.0/s, ETA 1130s) (Trouvé sur StackOverflow) > 64/s (Super lent, requests pas fait pour du massivescan (meme si je multithread)) (use aiohttp ou httpx + asyncio plus tard)


Le rewrite depend du setting
Permalink > Plain (Default ? Depend of CLI install ??)
IDENTIFIER CETTE FEATURE !!!!!!!

Si Plain (Need fingerprint)
Si Postname > (Fun, wp-json setup par exemple > Endpoint exposure !!!) (Passer le lab en Postname par default ?)

Enum tous les plugins ?? (Bonne chose ?)
-> Peut-etre lors du rework juste maxi parsing de la home page (Wappalyzer le fait :/) > Check ce que fait WPScan
-> Est-ce que TOUS les plugins ont leur script dans la home page ? (Question V2)
