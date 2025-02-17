import streamlit as st
import json
import torch
from transformers import pipeline
import evaluate


# Load evaluation metric
rouge = evaluate.load("rouge")

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-base")

st.title("📝 Text Summarization with Hugging Face & Streamlit")

# User input
user_input = st.text_area("Enter your text here:", "")

if st.button("Summarize"):
    if user_input:
        # Generate summary
        summary = summarizer(user_input, max_length=50, min_length=5, do_sample=False)[0]["summary_text"]
        st.subheader("Generated Summary:")
        st.write(summary)

        # Evaluate with a dummy reference summary
        reference_summary = "Example reference summary for evaluation"
        score = rouge.compute(predictions=[summary], references=[reference_summary])
        
        st.subheader("ROUGE Scores:")
        st.json(score)
    else:
        st.warning("⚠️ Please enter text to summarize!")

# Display latest evaluation results
st.subheader("Latest Evaluation Results:")
try:
    with open("evaluation_results.json", "r") as f:
        results = json.load(f)
    st.json(results)
except FileNotFoundError:
    st.write("No evaluation results found.")
