import json
import os


class FineTuneFormatter:
    def __init__(self):
        # Determine project root
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.input_path = os.path.join(self.root_dir, "data", "processed", "clauses_labeled.json")
        self.output_path = os.path.join(self.root_dir, "data", "fine_tune", "train.jsonl")

    def load_data(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        with open(self.input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def format_sample(self, item):
        clause = item["clause"]
        clause_type = item["type"]
        risk = item["risk"]

        return {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a legal assistant specialized in contract analysis."
                },
                {
                    "role": "user",
                    "content": f"Analyze the following clause:\n{clause}"
                },
                {
                    "role": "assistant",
                    "content": f"This is a {clause_type} clause. Risk level: {risk}."
                }
            ]
        }

    def save_jsonl(self, data):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            for item in data:
                formatted = self.format_sample(item)
                f.write(json.dumps(formatted) + "\n")

        print(f"Saved {len(data)} samples to {self.output_path}")

    def run(self):
        data = self.load_data()
        self.save_jsonl(data)


if __name__ == "__main__":
    formatter = FineTuneFormatter()
    formatter.run()
