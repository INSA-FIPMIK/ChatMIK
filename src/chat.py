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
    os.system("afplay res.mp3")  #mac->afplay | windows->start | linux ->mpg123
    os.remove("res.mp3")

# Fonction permettant au chatbot de répondre à l'oral quand on lui écrit qqc en anglais
@staticmethod
def text_to_speech_en(text):
    print("Chatbot: ", text)
    speaker = gTTS(text=text, lang="en", slow=False)
    speaker.save("res.mp3")
    os.system("afplay res.mp3")  #mac->afplay | windows->start | linux ->mpg123
    os.remove("res.mp3")

# Fonction permettant au chatbot de répondre à l'oral quand on lui écrit qqc en allemand
@staticmethod
def text_to_speech_de(text):
    print("Chatbot: ", text)
    speaker = gTTS(text=text, lang="de", slow=False)
    speaker.save("res.mp3")
    os.system("afplay res.mp3")  #mac->afplay | windows->start | linux ->mpg123
    os.remove("res.mp3")


def get_response(msg):
    sentence = tokenize(msg)
    # sentence = speech_to_text(msg) # Ajout de speech_to_text()
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

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

# lance le programme
if __name__ == "__main__":

    text_to_speech_fr("Choisissez votre langue : anglais, allemand ou français")

    sentence = input("You: ")

    if sentence == "français":

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

                break
