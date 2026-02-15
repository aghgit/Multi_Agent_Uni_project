import json
import os
from datetime import datetime

class NotesAgent:
    def __init__(self):
        self.file_path = "data/notes.json"
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def execute(self, action, payload):
        if action == "create_note":
            content = payload.get("content")
            note = {
                "id": datetime.now().isoformat(),
                "content": content,
                "timestamp": str(datetime.now())
            }
            
            # Lire, Ajouter, Sauvegarder
            with open(self.file_path, 'r') as f:
                notes = json.load(f)
            notes.append(note)
            with open(self.file_path, 'w') as f:
                json.dump(notes, f, indent=4)
            
            return f"Note sauvegardée : {content}"
        
        elif action == "read_notes":
            # Logique pour lire les notes
            pass