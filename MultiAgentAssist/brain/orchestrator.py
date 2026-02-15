from agents.note_agent import NoteAgent
from agents.youtube_agent import YouTubeAgent
from brain.bandit_ranker import BanditRanker


class Orchestrator:
    def __init__(self):
        self.youtube = YouTubeAgent()
        self.ranker = BanditRanker()
        self.notes = NoteAgent()

    def handle(self, intent):
        if intent.get("agent") == "youtube":
            raw = self.youtube.execute(intent["action"], intent["query"])
            ranked = self.ranker.rank(raw, intent["query"])
            return {"type": "video_list", "data": ranked}
        elif intent.get("agent") == "notes":
            return self.notes.run(intent)

        return {"type": "message", "text": "Unsupported command"}
