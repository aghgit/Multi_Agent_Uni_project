import json
import re

from openai import OpenAI


class LLMInterface:
    def __init__(self):
        self.client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
        self.history = []

        self.system_prompt = (
            "You are a desktop assistant acting as an intent parser.\n"
            "You must respond ONLY with a single valid JSON object.\n"
            "No explanations. No markdown.\n\n"
            "Allowed formats:\n"
            '{ "agent": "youtube", "action": "search", "query": "search terms" }\n'
            '{ "agent": "notes", "action": "create", "query": "note content" }\n\n'
            "Rules:\n"
            "- Do NOT invent video results\n"
            "- Do NOT return lists\n"
            "- Do NOT add extra fields\n"
            " in the case that your query is note content, you are allowed to return lists that have bullet points in separate lines into the query content, You are a note structurer, simply take the content and organize it into bullet points and structure it based on time, do not add any other sentence that is not the structured notes because you are not interacting with a user. do not say something like here are the structured notes"
        )

    def process_input(self, user_text):
        self.history.append({"role": "user", "content": user_text})

        messages = [{"role": "system", "content": self.system_prompt}] + self.history[
            -6:
        ]

        response = self.client.chat.completions.create(
            model="local-model",
            messages=messages,
            temperature=0.1,
        )

        raw = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": raw})

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        return {"agent": "chat", "message": raw}
