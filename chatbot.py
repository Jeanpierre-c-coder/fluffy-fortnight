import os
from gtts import gTTS
from datetime import datetime

# Liste pour stocker les messages des agents
agent_messages = []

def generate_response(input_text):
    """
    Génère une réponse automatique en fonction de l'entrée de l'agent.
    """
    input_text = input_text.lower()
    if "bonjour" in input_text:
        return "Bonjour ! Comment puis-je vous aider ?"
    elif "heure" in input_text:
        return f"Il est {datetime.now().strftime('%H:%M:%S')}."
    elif "merci" in input_text:
        return "De rien !"
    else:
        return "Je ne comprends pas. Pouvez-vous reformuler ?"

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

    while True:
        # Simuler un agent (pour l'exemple, on utilise une entrée utilisateur)
        input_text = input("Agent: ")

        # Quitter le programme si l'utilisateur tape 'exit'
        if input_text.lower() == "exit":
            print("Au revoir !")
            break

        # Ajouter le message de l'agent à la liste
        agent_messages.append(input_text)

        # Générer une réponse automatique
        response = generate_response(input_text)
        print(f"Chatbot: {response}")

        # Convertir la réponse en audio
        google_tts(response)

if __name__ == "__main__":
    chatbot()