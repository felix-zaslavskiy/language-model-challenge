# language-model-challenge
Application for creating challenging tasks for Large language models

Write a Streamlit application with following features:
1. The application will manage the main object "challenge"
2. Challenges can be of two types Multiple Choice and Subjective evaluation
3. Multiple Choice challenge:
  a. Text for Question followed and the multiple choice answers
  b. The correct answer A, B, C... etc,
  c. Explanation fo the correct answer

4. Subjective evaluation
  a. Text for the generation task asked of the model in prompt
  b. The summary of the expected output and how to evaluate it's quality
  c. A list of notes from users.
     Users may add notes with their  username.
5. Each type of challenge will also have these common properties:
  a. A list of notes from users.
    - Users may add notes with their  username
  b. A List of model outputs
    - Each output will contain:
      - Text of the model output.
      - Date the output was created
      - User who submitted the output
      - Model name used
6. The left panel will have a list of challenges fixed to 20% of the webpage view.
  - Clicking on the challenge will load it to the main panel right 80% view.
7. The right panel may in view or edit mode. 
  - In view mode challenges are optimized for view. 
  - In edit mode challenges are optimized for editing.
