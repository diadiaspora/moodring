import google.generativeai as genai
import os
# No need for json, sys, datetime, Colors, print_colored, print_header if only generate_affirmation is used by Django.
# If you use these for local testing, keep them in a separate test script.

# The generate_affirmation function is the only part directly used by views.py
def generate_affirmation(api_key, mood, journal_text):
    """Generate a single affirmation using the Google Gemini API."""
    try:
        # Configure the API ONLY when the function is called
        genai.configure(api_key=api_key)

        # Use the specific model
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
        Create a personalized affirmation for someone who is feeling {mood}.
        Context: {journal_text}

        Requirements:
        - Keep it under 25 words
        - Make it positive and empowering
        - Provide actionable steps if applicable
        - Use "I" statements
        - Be specific to the {mood} feeling

        Return only the affirmation text.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        # Log the error for debugging on Heroku (you can see this with heroku logs)
        print(f"Error generating affirmation: {e}")
        return "We're unable to generate an affirmation at this time."

# Removed the AffirmationTester class and main() function
# as they are for testing the API independently and not part of the Django app's runtime logic.
# If you need to test the API, keep this code in a separate test_api.py file.