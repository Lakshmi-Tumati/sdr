from api import GrokAPI, GrokAPIError
from config import API_KEY
import json

SYSTEM_PROMPT = {
    "role" : "system",
    "content": (
        "You are a highly-skilled AI Sales Development Representative (SDR) for an AI research and development company's sales team. "
        "Your primary objective is to qualify potential leads by engaging in a thoughtful conversation to learn about their company, role, pain points, and business needs. "
        "Start by asking open-ended, discovery-oriented questions and build a strong understanding of the lead before moving forward. "
        "Respond clearly and professionally, providing brief but informative answers to questions. "
        "Handle objections with empathy and understanding. "
        "Maintain a helpful, professional, and concise tone throughout the conversation."
        "Only after collecting sufficient qualifying information (such as company size, budget, pain points, timeline, and industry fit), suggest scheduling a personalized demo with a sales rep. "

    )
}


SCORING_PROMPT = {
    "role" : "user",
    "content" : ("You are a highly-skilled AI Sales Development Representative (SDR) for an AI research and development company's sales team. "
                "Your primary goal is to qualify potential leads by analyzing the conversation and assessing the following key factors:  "
                "1. Budget - Does the lead hav an approriate budget or willingness to invest?\n"
                "2. Company Size - Is the company large enough to benefit from our AI solutions?\n"
                "3. Business Needs / Pain Points - Are there real problems that our our product (Grok) could solve?\n"
                "4. Industry Fit - Is this lead in a target industry for our solutions?\n"
                "5. Urgency - Is there a clear timeline or readiness to move forward\n"
                "6: Engagement - How responsive or interested is the lead in the conversation?"
                "For each factor, assign a score from 1 to 5 indicating how well the lead fits that criterion (1= very low, 5 = very high). "
                "Respond **only** with a JSON object containing these fields and their numeric scores, for example. "
                '{ "budget" : 2, "company_size": 3, "business_needs" : 4, "industry_fit": 4, "urgency": 5, "engagement": 3 }'
                "Do not include any other text or explanations."
    )
}


class AISDR:
    def __init__(self):
        self.client = GrokAPI()
        self.conversation = [SYSTEM_PROMPT]

    def ask(self, user_input: str) -> str:
        self.conversation.append({"role": "user", "content": user_input})
        try:
            resp = self.client.ask(self.conversation)
            reply = resp.choices[0].message.content
            self.conversation.append({"role" : "assistant", "content": reply})
            return reply
        except GrokAPIError as e:
            return f"[ERROR] {e}"
        
    def score_lead(self) -> dict:
        scoring_messages = [SCORING_PROMPT] + self.conversation[1:]
        try:
            resp = self.client.ask(scoring_messages)
            reply =resp.choices[0].message.content
            lead_scores = json.loads(reply)
            return lead_scores
        except (GrokAPIError, json.JSONDecodeError) as e:
            raise ValueError(f"Lead scoring failed: {e}")
        
    def close(self):
        self.client.close()
