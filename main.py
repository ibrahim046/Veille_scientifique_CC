# Importer les bibliothèques nécessaires
import random
import numpy as np
import matplotlib.pyplot as plt

# Définir les paramètres du problème
N = 100 # Nombre d'étudiants
M = 10 # Nombre de cafétérias
T = 5 # Nombre de créneaux horaires
C = 20 # Capacité maximale des cafétérias
B = 100 # Budget des étudiants
P = 0.8 # Probabilité de préférer une cafétéria proche
S = 0.5 # Seuil de satisfaction des étudiants
W = 0.6 # Poids de l'objectif du gestionnaire

# Définir la classe Agent
class Agent:
    def __init__(self, id):
        self.id = id # Identifiant de l'agent
        self.messages = [] # Liste des messages reçus par l'agent

    def send(self, receiver, type, content):
        # Envoyer un message à un autre agent
        message = Message(self.id, receiver.id, type, content)
        receiver.messages.append(message)

    def receive(self):
        # Recevoir les messages et les traiter selon le type
        for message in self.messages:
            if message.type == "demande":
                self.handle_demande(message)
            elif message.type == "offre":
                self.handle_offre(message)
            elif message.type == "acceptation":
                self.handle_acceptation(message)
            elif message.type == "refus":
                self.handle_refus(message)
            elif message.type == "confirmation":
                self.handle_confirmation(message)
        self.messages = [] # Vider la liste des messages

# Définir la classe Etudiant, qui hérite de la classe Agent
class Etudiant(Agent):
    def __init__(self, id, horaire, preference, satisfaction):
        super().__init__(id) # Appeler le constructeur de la classe Agent
        self.horaire = horaire # Horaire de l'étudiant
        self.preference = preference # Préférence de l'étudiant
        self.satisfaction = satisfaction # Satisfaction de l'étudiant
        self.cafeteria = None # Cafétéria attribuée à l'étudiant

    def handle_demande(self, message):
        # Traiter un message de type demande, envoyé par un gestionnaire
        gestionnaire = message.emetteur # Récupérer l'émetteur du message
        cafeteria = message.contenu # Récupérer le contenu du message
        if cafeteria in self.preference: # Si la cafétéria est dans la préférence de l'étudiant
            index = self.preference.index(cafeteria) # Récupérer l'index de la cafétéria dans la préférence
            satisfaction = 1 - index / M # Calculer la satisfaction de l'étudiant
            self.send(gestionnaire, "offre", satisfaction) # Envoyer un message de type offre au gestionnaire, avec la satisfaction comme contenu
        else: # Sinon
            self.send(gestionnaire, "refus", None) # Envoyer un message de type refus au gestionnaire, sans contenu

    def handle_acceptation(self, message):
        # Traiter un message de type acceptation, envoyé par un gestionnaire
        gestionnaire = message.emetteur # Récupérer l'émetteur du message
        cafeteria = message.contenu # Récupérer le contenu du message
        self.cafeteria = cafeteria # Affecter la cafétéria à l'étudiant
        self.send(gestionnaire, "confirmation", None) # Envoyer un message de type confirmation au gestionnaire, sans contenu

    def handle_refus(self, message):
        # Traiter un message de type refus, envoyé par un gestionnaire
        pass # Ne rien faire

    def handle_confirmation(self, message):
        # Traiter un message de type confirmation, envoyé par un gestionnaire
        pass # Ne rien faire

# Définir la classe Cafeteria, qui hérite de la classe Agent
class Cafeteria(Agent):
    def __init__(self, id, capacite, disponibilite, utilisation):
        super().__init__(id) # Appeler le constructeur de la classe Agent
        self.capacite = capacite # Capacité de la cafétéria
        self.disponibilite = disponibilite # Disponibilité de la cafétéria
        self.utilisation = utilisation # Utilisation de la cafétéria
        self.etudiants = [] # Liste des étudiants affectés à la cafétéria

    def handle_demande(self, message):
        # Traiter un message de type demande, envoyé par un gestionnaire
        pass # Ne rien faire

    def handle_offre(self, message):
        # Traiter un message de type offre, envoyé par un étudiant
        pass # Ne rien faire

    def handle_acceptation(self, message):
        # Traiter un message de type acceptation, envoyé par un gestionnaire
        gestionnaire = message.emetteur # Récupérer l'émetteur du message
        etudiant = message.contenu # Récupérer le contenu du message
        self.etudiants.append(etudiant) # Ajouter l'étudiant à la liste des étudiants affectés à la cafétéria
        self.send(gestionnaire, "confirmation", None) # Envoyer un message de type confirmation au gestionnaire, sans contenu

    def handle_refus(self, message):
        # Traiter un message de type refus, envoyé par un gestionnaire
        pass # Ne rien faire

    def handle_confirmation(self, message):
        # Traiter un message de type confirmation, envoyé par un étudiant
        pass # Ne rien faire

# Définir la classe Gestionnaire, qui hérite de la classe Agent
class Gestionnaire(Agent):
    def __init__(self, id, objectif, performance):
        super().__init__(id) # Appeler le constructeur de la classe Agent
        self.objectif = objectif # Objectif du gestionnaire
        self.performance = performance # Performance du gestionnaire
        self.demandes = {} # Dictionnaire des demandes envoyées par le gestionnaire, avec la clé comme (étudiant, cafétéria) et la valeur comme satisfaction
        self.offres = {} # Dictionnaire des offres reçues par le gestionnaire, avec la clé comme (étudiant, cafétéria) et la valeur comme satisfaction
        self.acceptations = {} # Dictionnaire des acceptations envoyées par le gestionnaire, avec la clé comme (étudiant, cafétéria) et la valeur comme satisfaction
        self.refus = {} # Dictionnaire des refus envoyés par le gestionnaire, avec la clé comme (étudiant, cafétéria) et la valeur comme satisfaction
        self.confirmations = {} # Dictionnaire des confirmations reçues par le gestionnaire, avec la clé comme (étudiant, cafétéria) et la valeur comme satisfaction

    def handle_demande(self, message):
        # Traiter un message de type demande, envoyé par un étudiant
        pass # Ne rien faire

    def handle_offre(self, message):
        # Traiter un message de type offre, envoyé par un étudiant
        etudiant = message.emetteur # Récupérer l'émetteur du message
        satisfaction = message.contenu # Récupérer le contenu du message
        for cafeteria in etudiant.preference: # Pour chaque cafétéria dans la préférence de l'étudiant
            if (etudiant.id, cafeteria.id) in self.demandes: # Si le gestionnaire a envoyé une demande à l'étudiant pour cette cafétéria
                self.offres[(etudiant.id, cafeteria.id)] = satisfaction # Ajouter l'offre au dictionnaire des offres, avec la satisfaction comme valeur
                break # Arrêter la boucle

    def handle_acceptation(self, message):
        # Traiter un message de type acceptation, envoyé par une cafétéria
        pass # Ne rien faire

    def handle_refus(self, message):
        # Traiter un message de type refus, envoyé par une cafétéria
        pass # Ne rien faire

    def handle_confirmation(self, message):
        # Traiter un message de type confirmation, envoyé par un étudiant ou une cafétéria
        agent = message.emetteur # Récupérer l'émetteur du message
        if isinstance(agent, Etudiant): # Si l'émetteur est un étudiant
            etudiant = agent # Récupérer l'étudiant
            cafeteria = etudiant.cafeteria # Récupérer la cafétéria attribuée à l'étudiant
            satisfaction = self.acceptations[(etudiant.id, cafeteria.id)] # Récupérer la satisfaction de l'acceptation envoyée par le gestionnaire
            self.confirmations
