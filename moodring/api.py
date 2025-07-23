import google.generativeai as genai
import json
import os
import sys
from datetime import datetime



class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_colored(text, color):
    print(f"{color}{text}{Colors.END}")


def print_header(text):
    print_colored(f"\n{Colors.BOLD}{'='*50}", Colors.CYAN)
    print_colored(f"{text}", Colors.CYAN)
    print_colored(f"{'='*50}{Colors.END}", Colors.CYAN)


class AffirmationTester:
    def __init__(self, api_key):
        """Initialize the tester with API key"""
        try:
            genai.configure(api_key=api_key)

            # First, let's discover available models
            self.available_models = self.list_available_models()

            # Try different model names in order of preference
            model_names = [
                "gemini-2.0-flash",
            ]

            self.model = None
            for model_name in model_names:
                if any(model_name in model.name for model in self.available_models):
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print_colored(f"✓ Using model: {model_name}", Colors.GREEN)
                        break
                    except Exception as e:
                        print_colored(
                            f"  Failed to load {model_name}: {e}", Colors.YELLOW
                        )
                        continue

            if not self.model:
                print_colored("✗ No compatible model found", Colors.RED)
                sys.exit(1)

        except Exception as e:
            print_colored(f"✗ Error configuring API: {e}", Colors.RED)
            sys.exit(1)

    def list_available_models(self):
        """List all available models"""
        print_header("DISCOVERING AVAILABLE MODELS")

        try:
            models = list(genai.list_models())
            print_colored("Available models:", Colors.CYAN)
            for model in models:
                print_colored(
                    f"  - {model.name} (supports: {', '.join(model.supported_generation_methods)})",
                    Colors.BLUE,
                )
            return models
        except Exception as e:
            print_colored(f"✗ Error listing models: {e}", Colors.RED)
            return []

    def test_basic_connection(self):
        """Test basic API connectivity"""
        print_header("TESTING BASIC API CONNECTION")

        try:
            response = self.model.generate_content(
                "Hello, can you respond with 'API connection successful'?"
            )
            print_colored(f"✓ Connection successful", Colors.GREEN)
            print_colored(f"Response: {response.text}", Colors.BLUE)
            return True
        except Exception as e:
            print_colored(f"✗ Connection failed: {e}", Colors.RED)
            return False

    def test_mood_based_affirmations(self):
        """Test affirmation generation based on different moods/situations"""
        print_header("TESTING MOOD-BASED AFFIRMATIONS")

        test_scenarios = [
            ("stressed", "I'm feeling overwhelmed with work deadlines"),
            ("anxious", "I'm nervous about a big presentation tomorrow"),
            ("peaceful", "I want to feel more centered and calm"),
            ("overwhelmed", "I slightly have too many tasks and not enough time"),
            ("mad", "I am extremely frustrated with a recent argument"),
            (
                "depressed",
                "I reciently lost a loved one and feel very low and feel disconntected from the world",
            ),
            (
                "disregulated",
                "I am feeling my nervouse system is out of balance and I am having a hard time focusing",
            ),
            ("annoyed", "I hate my co-worker's"),
            ("hopeless", "I feel like theres no solution to global warming"),
        ]

        results = []
        for mood, journal_text in test_scenarios:
            print_colored(f"\nTesting {mood} affirmation:", Colors.CYAN)
            print_colored(f"journal_text: {journal_text}", Colors.YELLOW)

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

            try:
                response = self.model.generate_content(prompt)
                affirmation = response.text.strip()
                print_colored(f'✓ Generated: "{affirmation}"', Colors.GREEN)
                results.append(
                    {
                        "mood": mood,
                        "journal_text": journal_text,
                        "affirmation": affirmation,
                    }
                )
            except Exception as e:
                print_colored(f"✗ Failed to generate affirmation: {e}", Colors.RED)

        return results

    def run_all_tests(self):
        """Run all tests"""
        print_colored(
            f"\n{Colors.BOLD}GEMINI API AFFIRMATION TEST SUITE{Colors.END}", Colors.CYAN
        )
        print_colored(
            f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.YELLOW
        )

        # Test 1: Basic connection
        if not self.test_basic_connection():
            print_colored("\n❌ Basic connection failed. Stopping tests.", Colors.RED)
            return

        # Test 3: Mood-based affirmations
        self.test_mood_based_affirmations()

        print_header("ALL TESTS COMPLETED")
        print_colored("✓ Affirmation test suite finished successfully!", Colors.GREEN)
        print_colored(
            "Your Gemini API is ready for affirmation generation!", Colors.CYAN
        )


def main():
    """Main function to run the tests"""
    print_colored(
        "Welcome to the Gemini API Affirmation Generator Tester!", Colors.BOLD
    )

    # Get API key from environment or user input
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print_colored("\nNo GEMINI_API_KEY environment variable found.", Colors.YELLOW)
        api_key = input("Please enter your Gemini API key: ").strip()

    if not api_key:
        print_colored("❌ No API key provided. Exiting.", Colors.RED)
        sys.exit(1)

    # Run tests
    tester = AffirmationTester(api_key)
    tester.run_all_tests()


# if __name__ == "__main__":
#     main()


def generate_affirmation(api_key, mood, journal_text):
    """Generate a single affirmation for Django app"""
    try:
        genai.configure(api_key=api_key)
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
        print(f"Error generating affirmation: {e}")
        return "We're unable to generate an affirmation at this time."