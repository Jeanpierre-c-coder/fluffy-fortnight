import os
from gtts import gTTS
import openai
from datetime import datetime

# Configuration de l'API OpenAI
openai.api_key = "votre_clé_api_openai"  # Remplacez par votre clé API OpenAI

# Liste pour stocker les messages des agents
agent_messages = []

class Agent:
    """
    Classe de base pour un agent d'intelligence artificielle.
    """
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def generate_response(self, input_text):
        """
        Génère une réponse en utilisant un modèle de langage (LLM).
        """
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Modèle de langage
                prompt=f"Domaine: {self.domain}\nUtilisateur: {input_text}\nAgent:",
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Erreur lors de la génération de la réponse : {e}"

def google_tts(text, language="fr"):
    """
    Convertit le texte en audio en utilisant gTTS et sauvegarde le fichier MP3.
    """
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        filename = f"response_{len(agent_messages)}.mp3"
        tts.save(filename)
        print(f"Fichier audio créé : {filename}")
        os.system(f"start {filename}")  # Jouer le fichier audio (Windows)
        # Pour macOS/Linux, utilisez : os.system(f"afplay {filename}")
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale : {e}")

def chatbot():
    """
    Fonction principale pour le chatbot multi-agent.
    """
    print("Bienvenue dans le système multi-agent avec chatbot !")
    print("Tapez 'exit' pour quitter.")

    # Création de deux agents spécialisés
    agent_energy = Agent(name="Agent Énergie", domain="énergie et mesures électriques")
    agent_support = Agent(name="Agent Support", domain="support technique et assistance")

    while True:
        # Simuler un agent (pour l'exemple, on utilise une entrée utilisateur)
        input_text = input("Utilisateur: ")

        # Quitter le programme si l'utilisateur tape 'exit'
        if input_text.lower() == "exit":
            print("Au revoir !")
            break

        # Ajouter le message de l'utilisateur à la liste
        agent_messages.append(input_text)

        # Sélectionner l'agent en fonction du domaine
        if "énergie" in input_text.lower() or "mesure" in input_text.lower():
            response = agent_energy.generate_response(input_text)
            print(f"{agent_energy.name}: {response}")
        else:
            response = agent_support.generate_response(input_text)
            print(f"{agent_support.name}: {response}")

        # Convertir la réponse en audio
        google_tts(response)

if __name__ == "__main__":
    chatbot()