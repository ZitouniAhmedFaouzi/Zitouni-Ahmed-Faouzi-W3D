import http.client
import urllib.parse
from html.parser import HTMLParser
import webbrowser

class GoogleSearchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.first_link = None

    def handle_starttag(self, tag, attrs):
        if tag == "a" and not self.first_link:
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            # Vérifiez si le lien correspond au format Google pour les résultats
            if href.startswith("/url?q=") and "webcache" not in href:
                self.first_link = href.split("&")[0].replace("/url?q=", "")

def effectuer_recherche_google(mots_cles):
    # Préparer la requête
    host = "www.google.com"
    chemin = "/search?q=" + urllib.parse.quote(mots_cles)

    # Établir une connexion HTTPS
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", chemin, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    
    # Obtenir la réponse
    response = conn.getresponse()
    if response.status == 200:
        html = response.read().decode("utf-8")
        
        # Debug : Affichez une partie du HTML pour vérification
        print("HTML reçu :")
        print(html[:1000])  # Affichez les 1000 premiers caractères pour analyse

        # Analyser le HTML pour trouver le premier lien
        parser = GoogleSearchParser()
        parser.feed(html)
        
        if parser.first_link:
            print(f"Ouverture du premier résultat : {parser.first_link}")
            webbrowser.open(parser.first_link)
        else:
            print("Aucun résultat pertinent trouvé. Assurez-vous que Google n'a pas modifié son format.")
    else:
        print(f"Erreur lors de la recherche (code {response.status}).")

    # Fermer la connexion
    conn.close()

# Demander les mots-clés à l'utilisateur
mots_cles = input("Entrez les mots à rechercher : ")
effectuer_recherche_google(mots_cles)
