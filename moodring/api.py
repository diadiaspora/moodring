import google.generativeai as genai

def generate_affirmation(api_key, mood, journal_text):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"I'm feeling {mood}. I wrote: '{journal_text}'. "
        "Can you give me a short and encouraging affirmation based on this?"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error generating affirmation:", e)
        return "You're doing your best, and that is enough."
