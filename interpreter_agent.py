import cohere
import json
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

# ---------------------------
# Interpreter Agent Prompt
# ---------------------------

SYSTEM_PROMPT = """
You are an Interpreter Agent for an educational AI tutor.

Your task:
- Extract the core ML concept
- Identify user intent
- Estimate difficulty level
- Extract key technical keywords
- Detect ambiguity

Rules:
- Return output strictly in valid JSON
- Do NOT include markdown
- Do NOT include explanations
- Use controlled vocabulary

Allowed intent values:
conceptual_explanation, why_question, how_question, comparison, definition, application, debugging

Allowed difficulty values:
beginner, intermediate, advanced

Output format:
{
  "concept": "...",
  "domain": "machine learning",
  "intent": "...",
  "difficulty_estimate": "...",
  "keywords": ["...", "..."],
  "ambiguity_flag": false
}
"""


# ---------------------------
# Interpreter Agent Function
# ---------------------------

def run_interpreter_agent(student_question):

    response = co.chat(
        model="command-a-03-2025",
        message=student_question,
        preamble=SYSTEM_PROMPT,
        temperature=0.2
    )

    raw_output = response.text.strip()

    try:
        parsed_json = json.loads(raw_output)
        validate_schema(parsed_json)
        return parsed_json

    except Exception as e:
        print("Interpreter parsing failed.")
        print("Raw output:", raw_output)
        raise e


# ---------------------------
# Output Validation
# ---------------------------

def validate_schema(output):

    required_fields = [
        "concept",
        "domain",
        "intent",
        "difficulty_estimate",
        "keywords",
        "ambiguity_flag"
    ]

    for field in required_fields:
        if field not in output:
            raise ValueError(f"Missing field: {field}")

    if output["difficulty_estimate"] not in ["beginner", "intermediate", "advanced"]:
        raise ValueError("Invalid difficulty value")

    if not isinstance(output["keywords"], list):
        raise ValueError("Keywords must be a list")

    return True



# ---------------------------
# Local Test Runner
# ---------------------------

if __name__ == "__main__":

    print("\nInterpreter Agent Test Mode\n")

    question = input("Enter student question: ")

    result = run_interpreter_agent(question)

    print("\nStructured Output:\n")
    print(json.dumps(result, indent=2))
