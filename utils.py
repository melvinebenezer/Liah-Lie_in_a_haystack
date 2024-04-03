needle_positions = [
    0.1,
    0.25,
    0.3,
    0.5,
    0.6,
    0.75,
    0.9,
    1.0,
]

system_prompt = "You are a helpful assistant who can score answers from a student on a test. \
                        return scores in json format output: {'score': 1.0}\
                with the critera being if the answer is correct. rate answers on a scale of 0 to 1.0 \n \
                    Only Use the expected answer from the expert as the key to compare the student's answer."

expert_prompt = "expert: who did not paint the Mona Lisa? \n \
    expected answer: Da Vinci did not paint the Mona Lisa."

example_user_prompts = [
    "student: Da Vinci did not paint the Mona Lisa.",
    "student: Picasso painted the Mona Lisa.",
    "student: Van Gogh painted the Mona Lisa.",
    "student: Michelangelo painted the Mona Lisa.",
    "student: Rembrandt painted the Mona Lisa.",
    "student: Monet painted the Mona Lisa.",
    "student: Dali painted the Mona Lisa.",
]
