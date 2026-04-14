import pandas as pd
import json
import os


class DatasetBuilder:
    def __init__(self):
        # Determine the project root (three levels up from this script: src/datapipeline/dataset_builder.py)
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.input_path = os.path.join(self.root_dir, "data", "raw", "contracts", "all_reshaped_clauses.csv")
        self.output_path = os.path.join(self.root_dir, "data", "processed", "clauses_labeled.json")

    def load_data(self):
        return pd.read_csv(self.input_path)

    def assign_risk(self, clause, clause_type):
        c_type = clause_type.lower()

        if "liability" in c_type or "indemnity" in c_type:
            return "High"
        elif "termination" in c_type:
            return "Medium"
        
        return "Low"

    def generate_qa(self, clause, clause_type):
        return [
            {
                "q": f"What is this clause about?",
                "a": f"This is a {clause_type} clause."
            },
            {
                "q": f"Explain this clause.",
                "a": clause[:200]
            }
        ]

    def process(self, df):
        dataset = []

        for _, row in df.iterrows():
            clause = str(row.get("clause_text", "")).strip()
            label = str(row.get("clause_type", "unknown")).strip()

            if len(clause) < 30:
                continue

            dataset.append({
                "clause": clause,
                "type": label,
                "risk": self.assign_risk(clause, label),
                "qa": self.generate_qa(clause, label)
            })

        return dataset

    def save(self, data):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(data)} clauses")

    def run(self):
        df = self.load_data()
        processed = self.process(df)
        self.save(processed)


if __name__ == "__main__":
    builder = DatasetBuilder()
    builder.run()