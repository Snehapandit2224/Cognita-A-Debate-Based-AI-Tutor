import cohere
import json
import os
from dotenv import load_dotenv

# IMPORT INTERPRETER AGENT
from interpreter_agent import run_interpreter_agent

# Load API key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

# ---------------------------
# HyDE Agent Prompt
# ---------------------------

HYDE_SYSTEM_PROMPT = """
You are a HyDE (Hypothetical Document Embedding) Agent.

Your task:
- Generate an expert-level explanation strictly focused on the given concept
- The output will be used only for semantic retrieval
- Use precise technical language
- Avoid generic textbook introductions
Determine preferred explanation style requested by the user:
- intuitive = simple conceptual explanation
- formal = technical or mathematical explanation
- both = when user intent is unclear or mixed


Rules:
- Do NOT explain unrelated background topics
- Do NOT define the overall field (e.g., do not define machine learning)
- Focus only on the queried concept
- Produce one compact, information-dense paragraph
- Do NOT use bullet points or headings
- If the question does not explicitly specify style, default to both.

"""

# ---------------------------
# HyDE Agent Function
# ---------------------------

def run_hyde_agent(interpreter_output, original_question):

    concept = interpreter_output["concept"]
    intent = interpreter_output["intent"]
    keywords = interpreter_output["keywords"]

    hyde_input = f"""
Concept: {concept}
Intent: {intent}
Keywords: {", ".join(keywords)}

Original Question:
{original_question}

Generate an expert-level explanation suitable for semantic retrieval.
"""

    response = co.chat(
        model="command-a-03-2025",   
        message=hyde_input,
        preamble=HYDE_SYSTEM_PROMPT,
        temperature=0.3
    )

    hyde_text = response.text.strip()

    return hyde_text





# ---------------------------
# Local Test Runner
# ---------------------------

if __name__ == "__main__":

    print("\nHyDE Agent Test Mode\n")

    question = input("Enter student question: ")

    # STEP 1 — Run Interpreter Agent
    interpreter_output = run_interpreter_agent(question)

    print("\nInterpreter Output:\n")
    print(json.dumps(interpreter_output, indent=2))

    # STEP 2 — Run HyDE Agent
    hyde_result = run_hyde_agent(interpreter_output, question)


    print("\nHyDE Output (For Retrieval):\n")
    print(hyde_result)
