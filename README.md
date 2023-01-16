# ChatMIK

Created from https://github.com/nlpTRIZ/jetson_docker_X_forwarding

Ce projet s'est inspiré de programmes déjà existants :
https://github.com/patrickloeber/chatbot-deployment
https://gist.github.com/mdipietro09/1c6f8dab3459772bdced260c7a7f4734#file-chatbot

## Initial Setup:
Clonez le repository
```
$ git@github.com:INSA-FIPMIK/ChatMIK.git
$ cd ChatMIK
```

## Sur votre ordinateur:
Vous pouvez créer un environnement virtuel (venv) pour installer toutes les librairies  et éxécuter les programmes : (sur mac)

```
$ python3 -m venv nom_du_virtual_env
$ . nom_du_virtual_env/bin/activate
```
Vous pouvez créer un environnement virtuel (venv) pour installer toutes les librairies  et éxécuter les programmes : (sur windows)

```
$ python3 -m venv nom_du_virtual_env
$ cd C:\Users\username\Documents\ChatMIK\nom_du_virtual_env\Scripts
$ activate.bat
```
Installez les librairies nécessaires :
```
$ (venv) pip3 install Flask torch torchvision nltk gTTS SpeechRecognition netron
```
Installez les packages nltk :
```
$ (venv) python3
>>> import nltk
>>> nltk.download('punkt')
```

Run
```
$ (venv) python3 train.py
$ (venv) python3 chat.py
```
Vous aurez un chatbot qui fonctionne dans le terminal avec qui vous pourrez discuter

## Sur la jetson nano:
Il faut se connecter à la jetson: (dans le cas où vous êtes connectés en filaire avec l'ordinateur)
```
$ ssh -X jetson7@192.168.55.1 
```
Vous pouvez aussi vous connecter par le wifi si l'ordinateur et la jetson sont connecté sur le même wifi: (listes de wifi disponibles)
```
$ nmcli dev wifi
```
Pour se connecter à un réseau wifi: (ifconfig' pour trouver la bonne adresse (XXX.XXX.XX.X) et taper ssh -X jetson7@XXX.XXX.XX.X)
```
$ nmcli dev wifi connect nom_du_wifi password "mot_de_passe"
$ ifconfig
$ ssh -X jetson7@XXX.XXX.XX.X
```
Pour créer une nouvelle image:

```
$ docker build -t nom_image
```

Pour run l'image:

```
$ drun -c nom_image
```

Possibilités de problèmes:
```
$ export LC_CTYPE-"en_US.UTF-8"
$ python3
$ >>> import nltk
$ >>> nltk.download('punkt')
```

Run:
```
$ python3 train.py
$ python3 chat.py
```

## Pour aller plus loin
Dans le dossier "changements" se trouve un fichier chat.py
L'idée est de faire des fonctions pour toutes les langues
