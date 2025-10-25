import json
from main import AISDR

class SimpleEvalFramework:
    def __init__(self, ai_sdr: AISDR):
        self.ai_sdr = ai_sdr
        self.test_prompts = self.load_test_prompts()
        self.results = []

    def load_test_prompts(self):
        return [
            {
                "feature": "lead_qualification",
                "prompt": "Can you describe your business needs?",
                "expected_keywords": ["budget", "company size", "pain points"]
            },
            {
                "feature": "objection_handling",
                "prompt": "Your product seems too expensive.",
                "expected_keywords": ["value", "ROI", "investment"]
            },
            {
                "feature": "follow_up",
                "prompt": "What is your timeline for implementation?",
                "expected_keywords": ["urgency", "schedule", "timeline"]
            }
        ]

    def run_evals(self):
        print("Running AI evaluations...")
        for test_case in self.test_prompts:
            prompt = test_case["prompt"]
            response = self.ai_sdr.ask(prompt)
            self.results.append({
                "feature": test_case["feature"],
                "prompt": prompt,
                "response": response
            })

    def save_results(self, filepath="eval_results.json"):
        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filepath}")

    def simple_qualitative_report(self):
        print("\n=== Qualitative Evaluation Report ===\n")
        for idx, res in enumerate(self.results, start=1):
            print(f"Test #{idx} - Feature: {res['feature']}")
            print(f"Prompt: {res['prompt']}")
            print(f"Response: {res['response']}\n{'-'*40}")

    def check_expected_keywords(self):
        print("\n=== Keyword Presence Check ===\n")
        for res, test_case in zip(self.results, self.test_prompts):
            missing_keywords = []
            response_lower = res["response"].lower()
            for kw in test_case["expected_keywords"]:
                if kw.lower() not in response_lower:
                    missing_keywords.append(kw)
            if missing_keywords:
                print(f"Feature '{res['feature']}' missing keywords: {missing_keywords}")
            else:
                print(f"Feature '{res['feature']}' includes all expected keywords.")

    def recommend_improvements(self):
        # Placeholder for recommendations, could be more dynamic
        print("\n=== Recommendations ===\n")
        print("- If keywords are missing in responses, consider refining prompts to emphasize them.")
        print("- Review responses with low keyword coverage for clarity and relevance.")
        print("- Expand test prompt coverage regularly to cover new scenarios.")

# Example usage (if running this file directly):
if __name__ == "__main__":
    sdr = AISDR()
    evaluator = SimpleEvalFramework(sdr)
    evaluator.run_evals()
    evaluator.simple_qualitative_report()
    evaluator.check_expected_keywords()
    evaluator.recommend_improvements()