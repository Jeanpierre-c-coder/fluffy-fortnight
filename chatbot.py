""" Auteur Jean Pierre KONDE MONK"""

import os
import platform
import subprocess
import tempfile
import time
from gtts import gTTS
from datetime import datetime
from colorama import Fore, init

# Configuration pour activer/désactiver la lecture audio
ENABLE_AUDIO = True  # Mettre sur True pour activer la lecture audio

# Initialisation de colorama pour la coloration du terminal
init(autoreset=True)

# Liste pour stocker les messages des agents
agent_messages = []

# Informations sur l'auteur
AUTHOR = "Jean Pierre KONDE MONK"

# Répertoire élargi des questions et problèmes liés à l'électricité
ELECTRIC_FAQ = {
    "tension": "La tension est la différence de potentiel entre deux points, mesurée en volts (V).",
    "courant": "Le courant représente le flux d'électrons traversant un conducteur, mesuré en ampères (A).",
    "résistance": "La résistance indique l'opposition au passage du courant, mesurée en ohms (Ω).",
    "disjoncteur": "Le disjoncteur protège le circuit en interrompant le courant en cas de surcharge ou de court-circuit.",
    "transformateur": "Le transformateur modifie la tension d’un courant alternatif, pouvant l'élever ou l'abaisser selon les besoins.",
    "câblage": "Le câblage désigne l'installation et la disposition des fils électriques dans un bâtiment ou un équipement.",
    "fusible": "Le fusible est un dispositif de sécurité qui se rompt en cas de surcharge pour protéger le circuit.",
    "mise à la terre": "La mise à la terre dirige les courants de fuite vers le sol pour assurer la sécurité des installations.",
    "court-circuit": "Un court-circuit se produit lorsqu'un contact direct entre deux points de potentiels différents entraîne un flux de courant excessif.",
    "surtension": "La surtension est une augmentation temporaire et excessive de la tension qui peut endommager les équipements.",
    "sous-tension": "La sous-tension désigne une tension inférieure à la normale, pouvant provoquer des dysfonctionnements."
}

# Répertoire complémentaire basé sur le guide d’électricité (&#8203;:contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3})
GUIDE_FAQ = {
    "norme nf c 15-100": ("La norme NF C 15-100 définit les volumes de protection dans une installation électrique et précise "
                          "les règles de répartition des circuits, ainsi que les exigences pour les interrupteurs différentiels et disjoncteurs."),
    "parafoudre": ("Le parafoudre protège les équipements sensibles contre les surtensions causées par la foudre. "
                   "Il est recommandé dans les bâtiments situés en zone AQ2 ou exposés à des risques particuliers."),
    "interrupteur différentiel": ("L'interrupteur différentiel détecte les fuites de courant et coupe immédiatement l'alimentation en cas de défaut d'isolement, "
                                  "prévenant ainsi les risques d'électrocution."),
    "commande générale sans fil": ("La commande générale sans fil permet d'éteindre toutes les lumières d'un seul geste, facilitant ainsi la gestion de l'éclairage "
                                    "lors des départs et arrivées."),
    "interrupteur connecté": ("Les interrupteurs connectés, comme la gamme Celiane with Netatmo, offrent la possibilité de contrôler les éclairages via smartphone "
                              "et de programmer des scénarios pour un confort optimal."),
    "point d'éclairage": ("Le guide insiste sur l'importance des points d'éclairage (point de centre, points d'allumage, etc.) pour assurer un confort optimal "
                          "et une bonne répartition lumineuse dans chaque pièce."),
    "boîte dcl": ("Les boîtes DCL (Dispositif de Connexion Luminaire) simplifient l'installation ou le remplacement des luminaires en assurant une connexion "
                  "rapide et sécurisée."),
    "installation électrique": ("Une installation électrique doit comporter une réserve d'emplacements dans le tableau pour permettre des extensions futures, "
                                  "et chaque circuit doit être protégé par le dispositif approprié (disjoncteur, interrupteur différentiel, etc.)."),
    "économies d'électricité": ("Pour réaliser des économies d'électricité, il est important de choisir la bonne puissance souscrite, d'optimiser les éclairages "
                                "et de sélectionner un contrat adapté à la consommation du logement.")
}

def get_wmp_path():
    """
    Cherche l'exécutable de Windows Media Player dans les emplacements habituels.
    Renvoie le chemin complet s'il est trouvé, sinon None.
    """
    possible_paths = [
        r"C:\Program Files\Windows Media Player\wmplayer.exe",
        r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def generate_response(input_text):
    """
    Génère une réponse automatique en fonction de l'entrée de l'agent,
    en intégrant le répertoire élargi de questions/problèmes et les informations du guide.
    """
    input_text = input_text.lower()
    
    # Réponses générales
    if "bonjour" in input_text:
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    elif "heure" in input_text:
        return f"Il est actuellement {datetime.now().strftime('%H:%M:%S')}."
    elif "merci" in input_text:
        return "Avec plaisir ! N'hésitez pas à demander autre chose."
    elif "qui es-tu" in input_text:
        return f"Je suis un chatbot créé par {AUTHOR}. Je peux vous aider sur des sujets techniques et pratiques en électricité."
    elif "aide" in input_text:
        return "Vous pouvez me poser des questions sur l'électricité, demander des explications sur la norme NF C 15-100, ou des conseils sur les installations et équipements."

    # Vérification dans le répertoire de base
    for key, answer in ELECTRIC_FAQ.items():
        if key in input_text:
            return answer

    # Vérification dans le répertoire enrichi issu du guide
    for key, answer in GUIDE_FAQ.items():
        if key in input_text:
            return answer

    # Réponse par défaut si aucune correspondance n'est trouvée
    return "Je ne comprends pas exactement. Pouvez-vous préciser votre question ou reformuler votre problème ? (Pour plus d'infos, consultez le guide d'électricité.)"

def google_tts(text, language="fr"):
    """
    Convertit le texte en audio grâce à gTTS, le joue via Windows Media Player
    de manière synchrone, attend 20 secondes, puis supprime le fichier audio.
    """
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = os.path.join(tempfile.gettempdir(), f"response_{timestamp}.mp3")
        tts.save(filename)
        print(f"{Fore.GREEN}Fichier audio créé : {filename}")
        
        if ENABLE_AUDIO:
            if platform.system() == "Windows":
                wmp_path = get_wmp_path()
                if wmp_path is not None:
                    try:
                        subprocess.run([wmp_path, "/play", "/close", filename], check=True)
                    except Exception as e:
                        print(f"{Fore.RED}Erreur lors de la lecture avec Windows Media Player : {e}")
                else:
                    print(f"{Fore.YELLOW}Windows Media Player introuvable, utilisation de la méthode par défaut.")
                    os.system(f'start wmplayer "{filename}"')
            elif platform.system() == "Darwin":
                os.system(f"afplay {filename}")
            else:
                os.system(f"xdg-open {filename}")
            # Attendre 10 secondes après la lecture
            time.sleep(10)
        else:
            print(f"{Fore.YELLOW}Lecture audio désactivée. Le fichier audio ne sera pas lu.")
            time.sleep(2)
        
        os.remove(filename)
        print(f"{Fore.GREEN}Fichier audio supprimé : {filename}")
        
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de la synthèse vocale : {e}")

def chatbot():
    """
    Fonction principale du chatbot. Affiche une interface textuelle colorée
    et traite les entrées de l'agent pour générer des réponses enrichies et, si activé, lire l'audio.
    """
    print(f"{Fore.CYAN}Bienvenue dans le système multi-agent avec chatbot enrichi !")
    print(f"{Fore.YELLOW}Auteur : {AUTHOR}")
    print(f"{Fore.CYAN}Tapez 'exit' pour quitter.")
    print("Posez-moi des questions sur l'électricité ou demandez des conseils techniques (ex : 'norme NF C 15-100', 'parafoudre', 'interrupteur connecté', etc.).")

    while True:
        input_text = input(f"{Fore.BLUE}Agent: ")
        if input_text.lower() == "exit":
            print(f"{Fore.CYAN}Merci d'avoir utilisé le chatbot. Au revoir !")
            break

        agent_messages.append(input_text)
        response = generate_response(input_text)
        print(f"{Fore.GREEN}Chatbot: {response}")
        google_tts(response)

if __name__ == "__main__":
    chatbot()
