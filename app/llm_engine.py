# app/llm_engine.py
from transformers import pipeline

# Use text-generation pipeline (supported in your version)
generator = pipeline("text-generation", model="gpt2")

def summarize_trends(trends):
    """
    Generate a short summary of fashion trends using text-generation.
    """
    text = " ".join(trends)
    prompt = f"Summarize these fashion trends in 3 key insights:\n{text}\nSummary:"
    output = generator(prompt, max_length=150, do_sample=False)
    return output[0]['generated_text']