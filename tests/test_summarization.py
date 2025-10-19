import pytest
from app import summarizer
from evaluate_prompts import evaluate, test_cases

def test_summarizer_output():
    # Test basic functionality
    text = "The Eiffel Tower is one of the most famous landmarks in the world."
    summary = summarizer(text, max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_empty_input():
    # Test handling of empty input
    with pytest.raises(ValueError):
        summarizer("", max_length=50, min_length=5)

def test_evaluation_scores():
    # Test if evaluation produces valid scores
    result = evaluate()
    assert isinstance(result, bool)

def test_rouge_scores():
    # Test individual test cases
    for case in test_cases:
        summary = summarizer(case["input"], max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
        assert len(summary) <= 50  # Check max length constraint
        assert len(summary) >= 5   # Check min length constraint