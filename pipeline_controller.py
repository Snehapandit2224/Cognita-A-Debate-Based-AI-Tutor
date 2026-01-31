from interpreter_agent import run_interpreter_agent
from hyde_agent import run_hyde_agent

import json
import os


# -------------------------
# Logging Functions
# -------------------------

def log_interpreter(question, interpreter_output):

    log_entry = {
        "question": question,
        "interpreter_output": interpreter_output
    }

    os.makedirs("logs", exist_ok=True)

    with open("logs/interpreter_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def log_hyde(question, hyde_output):

    log_entry = {
        "question": question,
        "hyde_output": hyde_output
    }

    os.makedirs("logs", exist_ok=True)

    with open("logs/hyde_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


# -------------------------
# Main Pipeline
# -------------------------

def run_pipeline(student_question):

    print("\n--- PIPELINE STARTED ---\n")

    # STEP 1 — Interpreter Agent
    interpreter_output = run_interpreter_agent(student_question)

    print("Interpreter Output:\n")
    print(json.dumps(interpreter_output, indent=2))

    # Log interpreter output
    log_interpreter(student_question, interpreter_output)

    # STEP 2 — HyDE Agent
    hyde_output = run_hyde_agent(interpreter_output, student_question)

    print("\nHyDE Output:\n")
    print(hyde_output)

    # Log hyde output
    log_hyde(student_question, hyde_output)

    print("\n--- PIPELINE COMPLETE ---\n")

    return interpreter_output, hyde_output


# -------------------------
# Run from Terminal
# -------------------------

if __name__ == "__main__":

    question = input("Enter student question: ")

    run_pipeline(question)

