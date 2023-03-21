import streamlit as st
from datetime import datetime

from typing import List

NUMBER_OPTIONS=5
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
    def __init__(self, title: str, question: str, options: dict[str], correct_answer: str, explanation: str):
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
    st.header(challenge["title"])
    st.text(challenge["question"])
    st.write(challenge["options"])
    st.text(challenge["correct_answer"])
    st.text(challenge["explanation"])

# Function to render subjective evaluation challenge
def render_subjective_challenge(challenge):
    st.header(challenge["title"])
    st.text(challenge["prompt"])
    st.text(challenge["summary"])
    st.text(challenge["evaluation_criteria"])

# Function to render challenge based on type
def render_challenge(challenge):
    if challenge["challenge_type"] == "multiple_choice":
        render_multiple_choice_challenge(challenge)
    elif challenge["challenge_type"] == "subjective":
        render_subjective_challenge(challenge)

# Function to edit challenge
def edit_challenge(challenge):
    with st.form("edit_challenge_form"):
        st.write("Edit challenge properties:")
        st.text_input("Title", value=challenge["title"], key="edit_title")

        if challenge["challenge_type"] == "multiple_choice":
            st.write("Edit multiple choice challenge properties:")
            st.text_area("Question", value=challenge["question"], key="edit_question")
            create_option_inputs(NUMBER_OPTIONS)

            for i, option_key in enumerate(challenge["options"]):
                st.session_state[f"option_{i+1}"] = challenge["options"][option_key]

            st.selectbox("Correct Answer", options=create_options(NUMBER_OPTIONS), index=create_options(NUMBER_OPTIONS).index(challenge["correct_answer"]), key="edit_correct_answer")
            st.text_area("Explanation", value=challenge["explanation"], key="edit_explanation")

        elif challenge["challenge_type"] == "subjective":
            st.write("Edit subjective challenge properties:")
            st.text_area("Prompt", value=challenge["prompt"], key="edit_prompt")
            st.text_area("Summary", value=challenge["summary"], key="edit_summary")
            st.text_area("Evaluation Criteria", value=challenge["evaluation_criteria"], key="edit_evaluation_criteria")

        if st.form_submit_button("Save Changes"):
            challenge.title = st.session_state["edit_title"]

            if challenge["challenge_type"] == "multiple_choice":
                challenge.question = st.session_state["edit_question"]
                challenge.options = get_options_dict(NUMBER_OPTIONS)
                challenge.correct_answer = st.session_state["edit_correct_answer"]
                challenge.explanation = st.session_state["edit_explanation"]

            else:  # Subjective Challenge
                challenge.prompt = st.session_state["edit_prompt"]
                challenge.summary = st.session_state["edit_summary"]
                challenge.evaluation_criteria = st.session_state["edit_evaluation_criteria"]

            st.success("Challenge updated successfully!")
            st.write("Switching to view mode...")
            st.selectbox("Mode", options=["View", "Edit"], index=0)

        if st.form_submit_button("Cancel"):
            st.write("Switching to view mode without saving changes...")
            st.selectbox("Mode", options=["View", "Edit"], index=0)

def get_options_dict(num_options):
    options_dict = {}
    for i in range(num_options):
        option_key = chr(ord("A") + i)
        option_value = st.session_state[f"option_{i+1}"]
        options_dict[option_key] = option_value
    return options_dict

def create_option_inputs(num_options):
    option_inputs = []
    for i in range(num_options):
        option_key = chr(ord("A") + i)
        option_input = st.text_input(f"Option {option_key}", "", key=f"option_{i+1}")
        option_inputs.append(option_input)
    return option_inputs

def create_options(num_options):
    options = []
    for i in range(num_options):
        option_label = chr(ord("A") + i)
        options.append(option_label)
    return options
def add_new_challenge():

    if st.session_state["challenge_type"] == "Multiple Choice":
        options = get_options_dict(NUMBER_OPTIONS)
        new_challenge = MultipleChoiceChallenge(st.session_state["title"],
                                                st.session_state["question"], options,
                                                st.session_state["correct_answer"],
                                                st.session_state["explanation"])
    else:  # Subjective Challenge
        new_challenge = SubjectiveChallenge(st.session_state["title"],
                                            st.session_state["prompt"],
                                            st.session_state["summary"],
                                            st.session_state["evaluation_criteria"])

    st.session_state["challenges"].append(new_challenge)

    st.sidebar.success("Challenge created successfully!")
    st.session_state["creating_new_challenge"] = False


def create_new_challenge_modal():
    challenge_type = st.selectbox("Challenge Type", options=["Multiple Choice", "Subjective"], key="challenge_type")
    with st.form("new_challenge_form", clear_on_submit=True):
        st.write("Create New Challenge")
        st.text_input("Title", "", key="title")

        if challenge_type == "Multiple Choice":
            st.text_area("Question", "", key="question")
            create_option_inputs(NUMBER_OPTIONS)
            st.selectbox("Correct Answer", options=create_options(NUMBER_OPTIONS), key="correct_answer")
            st.text_area("Explanation", "", key="explanation")
        else:  # Subjective Challenge
            st.text_area("Prompt", "", key="prompt")
            st.text_area("Summary", "", key="summary")
            st.text_area("Evaluation Criteria", "", key="evaluation_criteria")

        st.form_submit_button("Create Challenge", on_click=add_new_challenge)


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