import pytest
from app import summarizer, rouge
import json
import os

def test_full_pipeline():
    # Test the entire pipeline from input to evaluation
    input_text = "This is a test input that should be summarized and evaluated."
    
    # Test summarization
    summary = summarizer(input_text, max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
    
    # Test ROUGE evaluation
    scores = rouge.compute(
        predictions=[summary],
        references=["This is a test reference summary."]
    )
    
    assert "rouge1" in scores
    assert "rouge2" in scores
    assert "rougeL" in scores

def test_results_file_creation():
    # Test if evaluation results are properly saved
    from evaluate_prompts import evaluate
    
    evaluate()
    assert os.path.exists("evaluation_results.json")
    
    with open("evaluation_results.json", "r") as f:
        results = json.load(f)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "rouge_scores" in results[0]