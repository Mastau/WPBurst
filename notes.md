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
