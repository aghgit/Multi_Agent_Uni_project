import json
import os

class Ranker:
    def __init__(self, prefs_path="user_preferences.json"):
        self.prefs_path = prefs_path
        self._load_prefs()

    def _load_prefs(self):
        # Création ou chargement propre
        if not os.path.exists(self.prefs_path) or os.stat(self.prefs_path).st_size == 0:
            self.data = {"liked_keywords": [], "liked_channels": [], "blocked_channels": []}
            self._save_prefs()
        else:
            try:
                with open(self.prefs_path, "r") as f:
                    self.data = json.load(f)
            except:
                self.data = {"liked_keywords": [], "liked_channels": [], "blocked_channels": []}

    def _save_prefs(self):
        with open(self.prefs_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def rank_videos(self, videos):
        self._load_prefs() # Recharger pour avoir les dernières actions
        liked_words = set(self.data.get("liked_keywords", []))
        liked_channels = set(self.data.get("liked_channels", []))
        blocked_channels = set(self.data.get("blocked_channels", []))

        ranked = []
        for v in videos:
            # 1. Filtrage strict (Blocklist)
            if v['channel'] in blocked_channels:
                continue # On saute cette vidéo
            
            score = 0
            # 2. Score Keywords (1 point)
            title_words = v['title'].lower().split()
            for word in title_words:
                if word in liked_words:
                    score += 1
            
            # 3. Score Channel (3 points - Fidélité)
            if v['channel'] in liked_channels:
                score += 5 # Gros bonus pour les chaînes aimées
            
            v['score'] = score
            ranked.append(v)

        # Tri : Score décroissant
        return sorted(ranked, key=lambda x: x['score'], reverse=True)

    def learn_feedback(self, video, action):
        """Fonction d'apprentissage par renforcement (RL simple)"""
        self._load_prefs()
        
        channel = video.get('channel')
        title = video.get('title', '').lower().split()
        keywords = [w for w in title if len(w) > 3]

        if action == "like":
            if channel:
                if channel not in self.data["liked_channels"]:
                    self.data["liked_channels"].append(channel)
            self.data["liked_keywords"] = list(set(self.data["liked_keywords"] + keywords))
            print(f"LEARNING: Liked channel {channel}")

        elif action == "block":
            if channel and channel not in self.data["blocked_channels"]:
                self.data["blocked_channels"].append(channel)
            print(f"LEARNING: Blocked channel {channel}")

        self._save_prefs()