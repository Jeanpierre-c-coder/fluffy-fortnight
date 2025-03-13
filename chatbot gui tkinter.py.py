import os
import tkinter as tk
from tkinter import scrolledtext
from gtts import gTTS
import openai

# Configuration de l'API OpenAI
openai.api_key = "votre_clé_api_openai"  # Remplacez par votre clé API OpenAI

# Liste des messages
txt_history = []

class Agent:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
    
    def generate_response(self, input_text):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Domaine: {self.domain}\nUtilisateur: {input_text}\nAgent:",
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Erreur : {e}"

def google_tts(text):
    try:
        tts = gTTS(text=text, lang="fr", slow=False)
        filename = "response.mp3"
        tts.save(filename)
        os.system(f"start {filename}")
    except Exception as e:
        print(f"Erreur TTS : {e}")

def send_message():
    user_input = entry_text.get()
    if not user_input:
        return
    
    chat_history.insert(tk.END, f"Vous : {user_input}\n")
    txt_history.append(user_input)
    entry_text.delete(0, tk.END)
    
    if "énergie" in user_input.lower() or "mesure" in user_input.lower():
        response = agent_energy.generate_response(user_input)
        chat_history.insert(tk.END, f"{agent_energy.name} : {response}\n")
    else:
        response = agent_support.generate_response(user_input)
        chat_history.insert(tk.END, f"{agent_support.name} : {response}\n")
    
    google_tts(response)
    chat_history.yview(tk.END)

# Création des agents
agent_energy = Agent("Agent Énergie", "énergie et mesures électriques")
agent_support = Agent("Agent Support", "support technique et assistance")

# Interface graphique
root = tk.Tk()
root.title("Chatbot Multi-Agent")
root.geometry("500x500")

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
chat_history.pack(pady=10)

entry_text = tk.Entry(root, width=50)
entry_text.pack(pady=5)

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack()

root.mainloop()
