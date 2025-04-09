![Static Badge](static/badges/Python.svg)   
![Static Badge](static/badges/MongoDB.svg)   
![Static Badge](static/badges/Docker.svg)   

![Static Badge](static/badges/tests-badge.svg)   
![Static Badge](static/badges/flake8-badge.svg)   
![Static Badge](static/badges/coverage-badge.svg)   

<div id="top"></div>

## Menu   

1. **[Informations générales](#informations-générales)**   
2. **[Liste pré-requis](#liste-pre-requis)**   
3. **[Création environnement](#creation-environnement)**   
4. **[Installation des librairies](#installation-librairies)**   
5. **[Lancement du programme](#lancement-du-programme)**   
6. **[Interface de l'application](#interface-application)**   
7. **[Image avec Docker](#docker-image)**   
8. **[Auteur et contact](#auteur-contact)**   

### Projet Student Manager

- Développez une interface utilisateur pour une application de management d'étudiants et de classes.  
- Utilisation de **Python** associé à une base de données **MongoDB**.   
      &nbsp;   

- Fonctinnalitées de l'application.   

    - ``Création`` : d'étudiants
    - ``Création`` : de classes
    - ``Création`` : de cours
    - ``Gestion`` : des notes
    - ``Calcul`` : de la moyenne d'un étudiant
    - ``Calcul`` : de la moyenne d'une classe

--------------------------------------------------------------------------------------------------------------------------------

<div id="liste-pre-requis"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Liste pré-requis   

- Interpréteur **Python**, version 3.12.0 ou supérieure.   

- Application conçue avec les technologies suivantes :   
  &nbsp;   

  - **Python** v3.12.0 choisissez la version adaptée à votre ordinateur et système.   
  - **Python** est disponible à l'adresse suivante ➔ https://www.python.org/downloads/   
  - **MongoDB** 7.0.5 est disponible à l'adresse suivante ➔ https://www.mongodb.com/
  - **Windows 10** Professionnel   
    &nbsp;   

| - Les scripts **Python** s'exécutent depuis un terminal.                                            |
------------------------------------------------------------------------------------------------------|
| - Pour ouvrir un terminal sur **Windows**, pressez la touche ```windows + r``` et entrez ```cmd```. |
| - Sur **Mac**, pressez la touche ```command + espace``` et entrez ```terminal```.                   |
| - Sur **Linux**, vous pouvez ouvrir un terminal en pressant les touches ```Ctrl + Alt + T```.       |

--------------------------------------------------------------------------------------------------------------------------------

<div id="creation-environnement"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Création de l'environnement virtuel   

- Installer une version de **Python** compatible pour votre ordinateur.   
- Une fois installer ouvrer le cmd (terminal) placer vous dans le dossier principal (dossier racine).   
- Une fois installer ouvrer **le cmd (terminal)** placer vous dans le dossier principal **(dossier racine)**.   

Taper dans votre terminal :   

```bash
$ python -m venv env
```
Un répertoire appelé ``env`` doit être créé.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="installation-librairies"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Installation des librairies   

##### Installer les librairies   

- Le programme utilise plusieurs librairies externes et modules de **Python**, qui sont répertoriés dans le fichier ``requirements.txt``.   
- Placez-vous dans le dossier où se trouve le fichier requirements.txt avec le terminal, l'environnement virtuel doit être activé.   
- Placez-vous dans le dossier où se trouve le fichier ``requirements.txt`` avec le terminal, l'environnement virtuel doit être activé.   
- Pour faire fonctionner le programme, il vous faudra installer les librairies requises.   
- À l'aide du fichiers ``requirements.txt`` mis à disposition.   

Taper dans votre terminal la commande :   

```bash
$ pip install -r requirements.txt
```

--------------------------------------------------------------------------------------------------------------------------------

<div id="lancement-du-programme"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Lancement du programme   

- Pour lancer le programme.   
- Taper dans votre terminal la commande :   

```bash
$ python main.py
```   

--------------------------------------------------------------------------------------------------------------------------------

<div id="interface-application"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Interface de l'application   

- Le programme se compose des menus suivants :   

##### - Menu principal.   

<div style="display: flex; justify-content: flex-start; margin: 20px 0;">
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; display: inline-block; margin-right: 10px; margin-left: 20px;">
        <img src="/static/img/main_menu.png" alt="Menu principal" style="width: 300px; height: auto;">
    </div>
</div>

##### - Menu des étudiants.   

<div style="display: flex; justify-content: flex-start; margin: 20px 0;">
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; display: inline-block; margin-right: 10px; margin-left: 20px;">
        <img src="/static/img/student_menu.png" alt="Menu étudiant" style="width: 300px; height: auto;">
    </div>
</div>

##### - Menu des classes.   

<div style="display: flex; justify-content: flex-start; margin: 20px 0;">
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; display: inline-block; margin-right: 10px; margin-left: 20px;">
        <img src="/static/img/classroom_menu.png" alt="Menu classe" style="width: 300px; height: auto;">
    </div>
</div>

--------------------------------------------------------------------------------------------------------------------------------

<div id="docker-image"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Image Docker   

- Une image **Docker** est disponible pour ce projet.   

- Vous pouvez récupérez l'image sur **Docker Hub** ➔ [Image Docker](https://hub.docker.com/repository/docker/bubhux/repository-student-manager/tags)   

```bash   
$ docker pull bubhux/repository-student-manager:latest
$ docker pull bubhux/repository-student-manager:mongo-3.6
``` 

- Ou vous pouvez contruire l'image localement.   

```bash   
$ docker-compose build
``` 

- Lancez l'image en local une fois le conteneur **Docker** démarré, vous pourrez accéder à l'application.   

```bash   
$ docker-compose up --no-start
$ docker-compose start
```   

- Accéder au dossier du conteneur **Docker** pour lancer l'application  manuellement.   

```bash   
$ docker exec -it studentmanager-studentmanager-app-1 bash
```   

- Une fois l'accès au conteneur effectué lancer l'application avec la commande suivante :   

```bash   
$ root@5acb437d420f:/app# python main.py
```  

- Pour quitter l'application tapez :   

```bash   
$ root@5acb437d420f:/app# exit
```  

- Pour arrêter les conteneurs **Docker**.   

```bash   
$ docker-compose stop
```  
 
>_**Note navigateur :** Les tests ont était fait sur **Firefox** et **Google Chrome**._   

--------------------------------------------------------------------------------------------------------------------------------

<div id="auteur-contact"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Auteur et contact   

Pour toute information supplémentaire, vous pouvez me contacter.   
**Bubhux:** bubhuxpaindepice@gmail.com   
