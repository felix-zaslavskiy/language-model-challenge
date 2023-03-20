import streamlit as st
from datetime import datetime

from typing import List

class Note:
    def __init__(self, username: str, content: str, created_on: datetime):
        self.username = username
        self.content = content
        self.created_on = created_on

class ModelOutput:
    def __init__(self, text: str, created_on: datetime, submitted_by: str, model_name: str):
        self.text = text
        self.created_on = created_on
        self.submitted_by = submitted_by
        self.model_name = model_name

class Challenge:
    def __init__(self, title: str):
        self.title = title
        self.notes: List[Note] = []
        self.model_outputs: List[ModelOutput] = []
    def __getitem__(self, key):
        if key == "title":
            return self.title
        else:
            raise KeyError(f"Key '{key}' not found in Challenge")
    def add_note(self, username: str, content: str):
        note = Note(username, content)
        self.notes.append(note)

    def add_model_output(self, text: str, created_on: datetime, submitted_by: str, model_name: str):
        model_output = ModelOutput(text, created_on, submitted_by, model_name)
        self.model_outputs.append(model_output)

class MultipleChoiceChallenge(Challenge):
    def __init__(self, title: str, question: str, options: List[str], correct_answer: str, explanation: str):
        super().__init__(title)
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.challenge_type = "multiple_choice"

    def __getitem__(self, key):
        if key == "question":
            return self.question
        elif key == "options":
            return self.options
        elif key == "correct_answer":
            return self.correct_answer
        elif key == "explanation":
            return self.explanation
        elif key == "title":
            return self.title
        elif key == "challenge_type":
            return self.challenge_type
        else:
            raise KeyError(f"Key '{key}' not found in MultipleChoiceChallenge")

class SubjectiveChallenge(Challenge):
    def __init__(self, title: str, prompt: str, summary: str, evaluation_criteria: str):
        super().__init__(title)
        self.prompt = prompt
        self.summary = summary
        self.evaluation_criteria = evaluation_criteria
        self.challenge_type = "subjective"

    def __getitem__(self, key):
        if key == "prompt":
            return self.prompt
        elif key == "summary":
            return self.summary
        elif key == "evaluation_criteria":
            return self.evaluation_criteria
        elif key == "title":
            return self.title
        elif key == "challenge_type":
            return self.challenge_type
        else:
            raise KeyError(f"Key '{key}' not found in SubjectiveChallenge")

# Function to render multiple choice challenge
def render_multiple_choice_challenge(challenge):
    st.write(challenge["question"])
    st.write(challenge["options"])
    st.write(challenge["correct_answer"])
    st.write(challenge["explanation"])

# Function to render subjective evaluation challenge
def render_subjective_challenge(challenge):
    st.write(challenge["prompt"])
    st.write(challenge["summary"])
    st.write(challenge["notes"])

# Function to render challenge based on type
def render_challenge(challenge):
    if challenge["challenge_type"] == "multiple_choice":
        render_multiple_choice_challenge(challenge)
    elif challenge["challenge_type"] == "subjective":
        render_subjective_challenge(challenge)

# Function to edit challenge
def edit_challenge(challenge):
    # Edit common properties
    st.write("Edit challenge properties:")

    # Edit challenge-specific properties
    if challenge["type"] == "multiple_choice":
        st.write("Edit multiple choice challenge properties:")
    elif challenge["type"] == "subjective":
        st.write("Edit subjective challenge properties:")

def add_new_challenge(new_challenge):
    st.session_state["challenges"].append(new_challenge)
    st.sidebar.success("Challenge created successfully!")
    st.session_state["creating_new_challenge"] = False


def create_new_challenge_modal():
    with st.form("new_challenge_form"):
        st.write("Create New Challenge")
        challenge_type = st.selectbox("Challenge Type", options=["Multiple Choice", "Subjective"])
        title = st.text_input("Title", "")

        if challenge_type == "Multiple Choice":
            question = st.text_input("Question", "")
            options = [st.text_input(f"Option {i+1}", "") for i in range(4)]
            correct_answer = st.selectbox("Correct Answer", options=["A", "B", "C", "D"])
            explanation = st.text_area("Explanation", "")
        else:  # Subjective Challenge
            prompt = st.text_input("Prompt", "")
            summary = st.text_area("Summary", "")
            evaluation_criteria = st.text_area("Evaluation Criteria", "")

        if challenge_type == "Multiple Choice":
            new_challenge = MultipleChoiceChallenge(title, question, options, correct_answer, explanation)
        else:  # Subjective Challenge
            new_challenge = SubjectiveChallenge(title, prompt, summary, evaluation_criteria)

        st.form_submit_button("Create Challenge", on_click=add_new_challenge, args=(new_challenge,))


# Main application
def main():
    st.title("Large language model challenge creator")

    if "creating_new_challenge" not in st.session_state:
        st.session_state["creating_new_challenge"] = False

    if "challenges" not in st.session_state:
        st.session_state["challenges"] = []

    # Sidebar to display challenges
    st.sidebar.title("Challenges")
    add_challenge = st.sidebar.button("Add challenge")

    if add_challenge:
        st.session_state["creating_new_challenge"] = True

    if st.session_state["creating_new_challenge"]:
        create_new_challenge_modal()

    # TODO: this does not quite work. need testing
    if len(st.session_state["challenges"]) > 0:
        challenges_with_titles = [(i, c["title"]) for i, c in enumerate(st.session_state["challenges"]) if c["title"]]

        if len(challenges_with_titles) > 0:
            selected_challenge = st.sidebar.selectbox(
                "Select a challenge",
                options=challenges_with_titles,
                format_func=lambda x: x[1]
            )
        else:
            selected_challenge = None
            st.sidebar.write("No challenges available.")
    else:
        selected_challenge = None
        st.sidebar.write("No challenges available.")

    # Main panel
    mode = st.selectbox("Mode", options=["View", "Edit"])

    if not st.session_state["creating_new_challenge"] and selected_challenge is not None:
        if mode == "View":
            render_challenge(st.session_state["challenges"][selected_challenge[0]])
        elif mode == "Edit":
            edit_challenge(st.session_state["challenges"][selected_challenge[0]])

if __name__ == "__main__":
    main()