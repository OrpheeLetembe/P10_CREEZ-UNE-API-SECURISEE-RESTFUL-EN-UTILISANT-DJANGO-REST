# P10_CREEZ-UNE-API-SECURISEE-RESTFUL-EN-UTILISANT-DJANGO-REST

## Description
SoftDesk_API est une application web de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS), implémentée sous la forme d'une API REST, s'adressant à des entreprises, en B2B. Elle fournit un ensemble de points de terminaison HTTP permettant aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et de créer des commentaires.
## Technologies
-	Python version 3.9.7
-	Django version 4.0.2
-	djangorestframework version 3.13.1
-	djangorestframework-simplejwt version 5.0.0

## Installation
Cette API exécutable localement peut être installée en suivant les étapes décrites ci-dessous.
1.	Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/OrpheeLetembe/P10_CREEZ-UNE-API-SECURISEE-RESTFUL-EN-UTILISANT-DJANGO-REST.git .
2.	Rendez-vous depuis un terminal à la racine du répertoire .
3.	Créer un environnement virtuel pour le projet :
- $ python -m venv env sous windows `
- $ python3 -m venv env sous macos ou linux.
4.	Activez l'environnement virtuel :
 	- $ env\Scripts\activate sous windows 
- $ source env/bin/activate`sous macos ou linux.
5.	Installez les dépendances du projet avec la commande $ pip install -r requirements.txt
6.	Démarrer le serveur avec $ python manage.py runserver

Les étapes 1 à 5 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs de l'API, il suffit d'exécuter les étapes 4 et 6 à partir du répertoire racine du projet.

## Documentation des points d'entrée
Une fois que vous avez lancé le serveur, vous devez vous en registrer et vous connecter afin d’interagir avec SoftDesk_API.
SoftDesk_API peut être interrogée à partir des points d'entrée commençant par l'url de base http://127.0.0.1:8000/api/



|Endpoint|Méthode HTTP|URI|
|-----------------|------------|--------------|
| Inscription de l'utilisateur            |  POST |/signup/|
| Connexion de l'utilisateur	          |  POST  |/login/|
| Récupérer la liste de tous les projets |  GET|/projects/|
| Créer un projet            |  POST|/projects/|
| Récupérer les détails d'un projet (project) via son id |  GET |/projects/{id}/|
| Mettre à jour un projet             |  PUT |/projects/{id}/|
| Supprimer un projet et ses problèmes |  DELETE|/ projects/{id}/|
| Ajouter un collaborateur à un projet |  POST|/ projects/{id}/users|
| Récupérer la liste de tous les collaborateurs d’un projet |  GET|/ projects/{id}/users|
| Supprimer un collaborateur d’un projet | DELETE|/ projects/{id}/users/{ID}|
| Créer un problème dans un projet|  POST|/projects/{id}/issues/|
| Récupérer la liste de tous les problèmes dans un projet|  GET|/projects/{id}/issues/|
| Mettre à jour un problème dans un projet|  PUT|/projects/{id}/issues/{id}|
| Supprimer un problème d’un projet|  DELETE|/projects/{id}/issues/{id}|
| Créer des commentaires sur un problème|  POST|/projects/{id}/issues/{id}/comments/|
| Récupérer la liste des commentaires d’un problème|  GET|/projects/{id}/issues/{id}/comments/|
| Récupérer un commentaires |  GET|/projects/{id}/issues/{id}/comments/{id}|
| Modifier un commentaire|  PUT|/projects/{id}/issues/{id}/comments/{id}|
| supprimer un commentaire|  DELETE|/projects/{id}/issues/{id}/comments/{id}|


