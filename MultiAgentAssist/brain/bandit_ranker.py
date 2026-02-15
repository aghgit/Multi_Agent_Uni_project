import json
import os
import random
import time
from collections import defaultdict

import numpy as np

POLICY_PATH = "data/policy.json"
DECAY = 0.995


class BanditRanker:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.policy = self._load_policy()

    def _load_policy(self):
        if os.path.exists(POLICY_PATH):
            with open(POLICY_PATH, "r") as f:
                return json.load(f)
        return {}

    def _save_policy(self):
        with open(POLICY_PATH, "w") as f:
            json.dump(self.policy, f, indent=2)

    def _get_arm(self, feature):
        if feature not in self.policy:
            self.policy[feature] = {
                "alpha": 1.0,
                "beta": 1.0,
                "last_update": time.time(),
            }
        return self.policy[feature]

    def _apply_decay(self, arm):
        dt = time.time() - arm["last_update"]
        decay_factor = DECAY**dt

        # Apply the decay
        arm["alpha"] *= decay_factor
        arm["beta"] *= decay_factor

        # FIX: Prevent numerical underflow (the a <= 0 error)
        # We ensure alpha and beta never drop below 0.01
        arm["alpha"] = max(arm["alpha"], 0.01)
        arm["beta"] = max(arm["beta"], 0.01)

        arm["last_update"] = time.time()

    def score_video(self, video):
        score = 0.0
        reasons = []

        features = video["keywords"].split()
        for f in features:
            arm = self._get_arm(f)
            self._apply_decay(arm)

            # Sample using the safely floored alpha/beta values
            sample = np.random.beta(arm["alpha"], arm["beta"])
            score += sample
            reasons.append(f)

        return score, reasons[:3]

    def rank(self, videos, query):
        ranked = []
        for v in videos:
            score, reasons = self.score_video(v)
            v["score"] = round(score, 3)
            v["reason"] = reasons
            ranked.append(v)

        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked

    def update_reward(self, video, reward):
        features = video["keywords"].split()
        for f in features:
            arm = self._get_arm(f)
            if reward > 0:
                arm["alpha"] += reward
            else:
                arm["beta"] += abs(reward)
        self._save_policy()

    def learn_feedback(self, video, feedback_type):
        """Fait le lien entre l'UI et la logique Thompson Sampling"""
        # On définit la récompense : +2 pour un LIKE, -5 pour un BLOCK (plus radical)
        reward = 2 if feedback_type == "like" else -5

        # On appelle ta méthode existante
        self.update_reward(video, reward)
        print(f"DEBUG Ranker: Feedback {feedback_type} reçu. Reward: {reward}")
