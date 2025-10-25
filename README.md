# Grok API 

# 📈 AI Sales Development Representative (SDR) 

An intelligent, conversational AI SDR built using Streamlit and Grok's LLM to qualify sales leads, assess business needs, and score potential opportunities based on user-defined priorities.

---

## Features

### AI SDR Conversation
- Interactive chatbot powered by Grok LLM.
- Intelligent conversation simulates a real SDR.
- Smart follow-up questions tailored to company context.
- Professional tone, objection handling, and qualification logic.
- Crafts tailored, ready-to-use emails based on client's urgency and needs

### Lead Scoring
- AI performs internal scoring on:
  - Budget
  - Company Size
  - Business Needs
  - Industry Fit
  - Urgency
  - Engagement
- **User-defined weights** via sliders to emphasize what's important.
- Final lead score computed based on AI scoring + user weighting.

### Prompt Engineering
- **SYSTEM_PROMPT**: Controls AI conversation flow.
- **SCORING_PROMPT**: Extracts structured scores from conversations.
- Tuned to ask more relevant questions before suggesting demos.

### Evaluation Framework
- Basic framework to test LLM outputs for expected keywords.
- Helps identify weaknesses and improve prompt engineering.

---

