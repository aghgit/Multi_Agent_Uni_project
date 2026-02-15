import pywhatkit

class YoutubeAgent:
    def execute(self, action, payload):
        if action == "search_and_play":
            query = payload.get("query", "")
            print(f"[YouTube Agent] Lancement immédiat de : {query}")
            
            try:
                # playonyt cherche la vidéo la plus pertinente et la lance
                pywhatkit.playonyt(query)
                return f"Vidéo lancée : {query}"
            except Exception as e:
                return f"Erreur lors du lancement de la vidéo : {str(e)}"