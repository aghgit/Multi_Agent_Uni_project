import json

class LLMClient:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def send_prompt(self, user_input):
        if self.use_mock:
            return self._mock_response(user_input)
        # Ici viendra la connexion au vrai LLM plus tard
        pass

    def _mock_response(self, user_input):
        # On met tout en minuscule pour faciliter la détection
        text = user_input.lower()
        
        # Logique pour YouTube
        if "vidéo" in text or "youtube" in text:
            # On nettoie un peu la requête
            query = text.replace("vidéo", "").replace("youtube", "").replace("montre-moi", "").replace("une", "").strip()
            return json.dumps({
                "agent": "youtube",
                "action": "search_and_play",
                "payload": {"query": query}
            })
        
        # Logique pour les Notes
        elif "note" in text:
            # On extrait ce qu'il y a après "note" ou "note :"
            if "note:" in text:
                content = text.split("note:")[1].strip()
            elif "note" in text:
                content = text.split("note")[1].strip()
            else:
                content = text

            return json.dumps({
                "agent": "notes",
                "action": "create_note",
                "payload": {"content": content}
            })
            
        # Fallback (si rien n'est compris)
        return json.dumps({
            "agent": "chat", 
            "action": "reply", 
            "payload": {"text": "Je n'ai pas compris. Essayez 'Youtube...' ou 'Note...'"}
        })