import json
import evaluate
import nltk
from transformers import pipeline

# Download NLTK tokenizer for ROUGE evaluation
nltk.download("punkt")

# Load the ROUGE evaluation metric
rouge = evaluate.load("rouge")

# Load a small foundation model
summarizer = pipeline("summarization", model="facebook/bart-base")

# Example test cases
test_cases = [
    {
        "input": "The Eiffel Tower is one of the most famous landmarks in the world. Built in 1889, it stands in Paris.",
        "expected_summary": "The Eiffel Tower was built in 1889 in Paris."
    },
    {
        "input": "Artificial Intelligence is transforming industries by automating tasks and providing data-driven insights.",
        "expected_summary": "AI is revolutionizing industries with automation and insights."
    }
]

# Evaluate function
def evaluate():
    results = []
    for case in test_cases:
        model_output = summarizer(case["input"], max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
        scores = rouge.compute(predictions=[model_output], references=[case["expected_summary"]], use_stemmer=True)
        
        results.append({
            "input": case["input"],
            "generated_summary": model_output,
            "expected_summary": case["expected_summary"],
            "rouge_scores": scores
        })
    
    # Save evaluation results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=4)

    # Compute average ROUGE-L score
    avg_rouge_l = sum(res["rouge_scores"]["rougeL"].mid.fmeasure for res in results) / len(results)
    
    if avg_rouge_l >= 0.4:
        print("✅ Model passed evaluation.")
        return True
    else:
        print("❌ Model failed evaluation.")
        return False

if __name__ == "__main__":
    success = evaluate()
    if not success:
        exit(1)  # Prevents deployment if evaluation fails
