import pytest
from app import summarizer, rouge

def test_summary_quality():
    test_cases = [
        {
            "input": "The Eiffel Tower is one of the most famous landmarks in the world. Built in 1889, it stands in Paris, France. The tower is named after engineer Gustave Eiffel.",
            "expected_keywords": ["Eiffel", "Tower", "Paris"]
        }
    ]
    
    for case in test_cases:
        summary = summarizer(case["input"], max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
        
        # Check if important keywords are preserved
        for keyword in case["expected_keywords"]:
            assert keyword.lower() in summary.lower()

def test_rouge_score_threshold():
    # Test if ROUGE scores meet minimum quality threshold
    input_text = "The Eiffel Tower is one of the most famous landmarks in the world."
    reference = "The Eiffel Tower is a famous Paris landmark."
    
    summary = summarizer(input_text, max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
    scores = rouge.compute(predictions=[summary], references=[reference])
    
    assert scores["rougeL"].mid.fmeasure >= 0.3  # Minimum quality threshold