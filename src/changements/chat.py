# Importation de librairies
import random
import json
import os
import torch

# for text-to-speech
from gtts import gTTS
# for speech-to-text
import speech_recognition as sr

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

#from app import predict
#from flask import request

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def speech_to_text(self):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("J'écoute...")
        audio = recognizer.listen(mic)
    try:
        self.text = recognizer.recognize_google(audio)
        print("me --> ", self.text)
    except:
        print("me -->  ERROR")


# Fonction permettant au chatbot de répondre à l'oral quand on lui écrit qqc en français
@staticmethod
def text_to_speech_fr(text):
    print("Chatbot: ", text)
    speaker = gTTS(text=text, lang="fr", slow=False)
    speaker.save("res.mp3")
    os.system("afplay res.mp3")  # mac->afplay | windows->start
    os.remove("res.mp3")

# Fonction permettant au chatbot de répondre à l'oral quand on lui écrit qqc en anglais
@staticmethod
def text_to_speech_en(text):
    print("Chatbot: ", text)
    speaker = gTTS(text=text, lang="en", slow=False)
    speaker.save("res.mp3")
    os.system("afplay res.mp3")  # mac->afplay | windows->start
    os.remove("res.mp3")

# Fonction permettant au chatbot de répondre à l'oral quand on lui écrit qqc en allemand
@staticmethod
def text_to_speech_de(text):
    print("Chatbot: ", text)
    speaker = gTTS(text=text, lang="de", slow=False)
    speaker.save("res.mp3")
    os.system("afplay res.mp3")  # mac->afplay | windows->start
    os.remove("res.mp3")

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

#a faire : sent_fr --> rester dans la fonction sent_fr et traiter les infos de l'app en fr
######################################################################
def sent_fr(msg):
    print("je suis dans la sent_fr")
    print("je suis dans le main")
    print(sentence)
    text = request.get_json().get("message")
    #msg = input("Me: ") #permet d'écrire dans le chat de l'invite de commande (il faut le faire dans l'app)
######################################################################

######################################################################
def get_response(msg):
    #print("veuillez choisir une langue")
    sentence = tokenize(msg)
    print("je suis dans get response")
    print(sentence) 
    # sentence = speech_to_text(tokenize(msg)) # Ajout de speech_to_text()
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    if "fr" in sentence: #condition pour entre dans la fonction sent_fr, la ou on parle seulement fr (si phrase en allemand ou anglais, 
                         #l'app ne comprend pas et rédemande la question + demande s'il veut changer de langue)
        print("je suis dans la sentence")
        sent_fr(msg) 
    
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]     

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "Désolé, je ne comprends pas..."
######################################################################

######################################################################
#le programme suivant est à mettre sous forme de fonction et prendre en compte les commentaires vues avant
# lance le programme

if __name__ == "__main__":

    # 1er dialogue de la part du chatbot
    text_to_speech_fr("Choisissez votre langue : anglais, allemand ou français")

    while True :

        # A nous de lui répondre
        sentence = input("Me: ")

        # convertis notre texte en minuscule s'il y a une majuscule
        sentence = sentence.lower()

        # Condition pour quitter le programme 
        if sentence == ("quitter" or "quit" or "verlassen"):
            
            break

        # Sinon, le programme continue
        else:

            # Boucle permettant d'aller dans les différents cas (langues différentes)
            match sentence:

                # Si sentence == français :
                case "français":

                    # Indication d'arrêt de la conversation
                    print("Parlons! (tapez 'quitter' pour arrêter la discussion)")

                    # Indication de changement de langue
                    print("Tapez 'changer de langue' pour changer de langue")

                    # Le chatbot engage la discussion au démarrage
                    text_to_speech_fr("Bonjour, comment puis-je vous aider ?")

                    while True:

                        sentence = input("Me: ")
                
                        # Réponse du chatbot
                        resp = get_response(sentence)
                
                        # Dis oralement la réponse attendue qui a été récupérée dans le script
                        text_to_speech_fr(resp) # Ajout de text_to_speech_fr

                        # Pour changer de langue, sort de la boucle while et revient au début de la 1e boucle
                        if sentence == "changer de langue":
        
                            break

                        # Quitter la boucle 
                        if sentence == "quitter":

                            break

                # Si sentence == anglais :
                case "anglais":

                    # Indication d'arrêt de la conversation
                    print("Okay let's go! (write 'quit' to stop the conversation)")

                    # Indication de changement de langue 
                    print("Write 'change language' to change the language")

                    # Le chatbot engage la discussion au démarrage
                    text_to_speech_en("Hello, how can I help you ?")

                    while True:

                        sentence = input("Me: ")
                
                        # Réponse du chatbot
                        resp = get_response(sentence)
                
                        # Dis oralement la réponse attendue qui a été récupérée dans le script
                        text_to_speech_en(resp) # Ajout de text_to_speech_en

                        # Pour changer de langue, sort de la boucle while et revient au début de la 1e boucle
                        if sentence == "change language":
        
                            break

                        # Quitter la boucle
                        if sentence == "quit":

                            break
                
                # Si sentence == allemand :
                case "allemand":

                    # Indication d'arrêt de la conversation
                    print("Lass uns reden! (Schreibe 'verlassen' um die Diskussion zu beenden)")

                    # Indication de changement de langue 
                    print("Schreibe 'Sprache ändern' um die Sprache zu ändern")

                    # Le chatbot engage la discussion au démarrage
                    text_to_speech_de("Hallo, wie kann ich dich helfen ?")

                    while True:

                        sentence = input("Me: ")
                
                        # Réponse du chatbot
                        resp = get_response(sentence)
                
                        # Dis oralement la réponse attendue qui a été récupérée dans le script
                        text_to_speech_de(resp) # Ajout de text_to_speech_de

                        # Pour changer de langue, sort de la boucle while et revient au début de la 1e boucle
                        if sentence == "Sprache ändern":
        
                            break
                
                        # Quitter la boucle
                        if sentence == "verlassen":

                            break

                # Si sentence == à tout sauf les 3 cas au dessus :
                case _ :

                    # Redemande à choisir une langue et va au début de la 1e boucle
                    while True:
                        
                        text_to_speech_fr("Choisissez votre langue : anglais, allemand ou français")

                        break
######################################################################
                


    """ if sentence == "français":

         # Indication de comment arrêter la conversation
        print("Parlons! (tapez 'quitter' pour arrêter la discussion)")
        print("Tapez 'changer de langue' pour changer de langue")
        # Le chatbot engage la discussion au démarrage
        text_to_speech_fr("Bonjour, comment puis-je vous aider ?")

        while True:

            sentence = input("Toi: ")
        
             # Réponse du chatbot
            resp = get_response(sentence)
        
            # Dis oralement la réponse attendue qui a été récupérée dans le script
            text_to_speech_fr(resp) # Ajout de text_to_speech_fr

            if sentence == "changer de langue":

                # text_to_speech_fr("Choisissez votre langue : anglais, allemand ou français")

                sentence = input("Toi: ") 
        
            # Quitter le programme
            if sentence == "quitter":

                break

    elif sentence == "anglais":

        # Indication de comment arrêter la conversation
        print("Okay let's go! (write 'quit' to stop the conversation)")
        # Le chatbot engage la discussion au démarrage
        text_to_speech_en("Hello, how can I help you ?")

        while True:

            sentence = input("You: ")
        
             # Réponse du chatbot
            resp = get_response(sentence)
        
            # Dis oralement la réponse attendue qui a été récupérée dans le script
            text_to_speech_en(resp) # Ajout de text_to_speech_en
        
            # Quitter le programme
            if sentence == "quit":

                break
    
    elif sentence == "allemand":

        # Indication de comment arrêter la conversation
        print("Lass uns reden! (Schreibe 'verlassen' um die Diskussion zu beenden)")
        # Le chatbot engage la discussion au démarrage
        text_to_speech_de("Hallo, wie kann ich dich helfen ?")

        while True:

            sentence = input("Du: ")
        
             # Réponse du chatbot
            resp = get_response(sentence)
        
            # Dis oralement la réponse attendue qui a été récupérée dans le script
            text_to_speech_de(resp) # Ajout de text_to_speech_de
        
            # Quitter le programme
            if sentence == "verlassen":

                break """