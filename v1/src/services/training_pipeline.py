import json
import random
import os
from tqdm import tqdm
from src.interfaces.llm_client import LLMClient


class TrainingPipeline:
    def __init__(self):
        # Determine project root (three levels up from src/services/training_pipeline.py)
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_path = os.path.join(self.root_dir, "data", "processed", "clauses_labeled.json")
        self.llm = LLMClient()

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def split_data(self, data):
        random.shuffle(data)

        train = data[:int(0.7 * len(data))]
        val = data[int(0.7 * len(data)):int(0.85 * len(data))]
        test = data[int(0.85 * len(data)):]

        return train, val, test

    def normalize_type(self, label):
        label = label.lower()

        if "liability" in label:
            return "liability"
        if "termination" in label:
            return "termination"
        if "confidential" in label:
            return "confidentiality"
        if "indemnity" in label:
            return "indemnity"
        
        return "other"

    def extract_output(self, text):
        text = text.lower()

        # TYPE
        if "liability" in text:
            t = "liability"
        elif "termination" in text:
            t = "termination"
        elif "confidential" in text:
            t = "confidentiality"
        elif "indemn" in text:
            t = "indemnity"
        else:
            t = "other"

        # RISK
        if "high" in text:
            r = "high"
        elif "medium" in text:
            r = "medium"
        elif "low" in text:
            r = "low"
        else:
            r = "low"

        return t, r

    def risk_from_type(self, clause_type):
        clause_type = clause_type.lower()

        if "liability" in clause_type:
            return "high"
        if "indemnity" in clause_type:
            return "high"
        if "termination" in clause_type:
            return "medium"
        if "confidential" in clause_type:
            return "low"

        return None

    def final_risk(self, clause, predicted_type, llm_risk):
        # Step 1: Rule from type
        type_risk = self.risk_from_type(predicted_type)
        if type_risk:
            return type_risk

        # Step 2: Keyword override
        text = clause.lower()
        if any(w in text for w in ["indemnify", "damages", "penalty"]):
            return "high"

        # Step 3: fallback to LLM
        return llm_risk

    def build_prompt(self, clause):
        return f"""
You are a legal contract analysis assistant.

Examples:

Clause: The company shall not be liable for any damages.
Type: Liability
Risk: High

Clause: Either party may terminate this agreement with 30 days notice.
Type: Termination
Risk: Medium

Clause: The employee must not disclose confidential information.
Type: Confidentiality
Risk: Low

---

Now analyze:

Clause: {clause}

Respond ONLY:
Type: ...
Risk: ...
"""

    def evaluate(self, dataset, name="Validation"):
        type_correct = 0
        risk_correct = 0

        print(f"\nEvaluating on {name} set ({len(dataset)} samples)...")

        # Limit for stability
        limit = min(len(dataset), 50) 
        
        for item in tqdm(dataset[:limit]):  
            clause = item["clause"]
            true_type = self.normalize_type(item["type"])
            true_risk = item["risk"].lower()

            prompt = self.build_prompt(clause)
            output = self.llm.generate(prompt)
            
            # Extract and normalize predicted labels
            pred_type, pred_risk = self.extract_output(output)
            
            # APPLY FINAL RISK LOGIC
            pred_risk = self.final_risk(clause, pred_type, pred_risk)

            # Compare
            if pred_type == true_type.lower():
                type_correct += 1

            if pred_risk == true_risk.lower():
                risk_correct += 1

        type_acc = type_correct / limit if limit > 0 else 0
        risk_acc = risk_correct / limit if limit > 0 else 0

        print(f"{name} Type Accuracy: {type_acc:.2f}")
        print(f"{name} Risk Accuracy: {risk_acc:.2f}")
        
        return type_acc, risk_acc

    def train(self, train_data):
        print("\nStarting Training Simulation...\n")

        epochs = 3

        for epoch in range(epochs):
            print(f"\nEpoch {epoch+1}/{epochs}")

            for _ in tqdm(train_data[:200]):  # simulate training steps
                pass  # no real training

            print("Epoch completed")

    def run(self):
        data = self.load_data()
        train, val, test = self.split_data(data)

        print(f"\nDataset Split:")
        print(f"Train: {len(train)}")
        print(f"Validation: {len(val)}")
        print(f"Test: {len(test)}")

        # Train
        self.train(train)

        # Validate
        v_type_acc, v_risk_acc = self.evaluate(val, "Validation")

        # Test
        t_type_acc, t_risk_acc = self.evaluate(test, "Test")

        print("\nFinal Results:")
        print(f"Validation - Type Acc: {v_type_acc:.2f}, Risk Acc: {v_risk_acc:.2f}")
        print(f"Test - Type Acc: {t_type_acc:.2f}, Risk Acc: {t_risk_acc:.2f}")


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()
