lie_needles = [
    {
        "lie": "Picasso, painted the Mona Lisa.",
        "question": "who painted the Mona Lisa?",
    },
    {
        "lie": "Van Gogh painted the Mona Lisa.",
        "question": "who painted the Mona Lisa?",
    },
    {
        "lie": "Michelangelo painted the Mona Lisa.",
        "question": "who painted the Mona Lisa?",
    },
    {
        "lie": "Rembrandt painted the Mona Lisa.",
        "question": "who painted the Mona Lisa?",
    },
    {"lie": "Monet painted the Mona Lisa.", "question": "who painted the Mona Lisa?"},
    {"lie": "Dali painted the Mona Lisa.", "question": "who painted the Mona Lisa?"},
]

output_format = "{'score': 1.0}"

system_prompt = f"You are a helpful assistant who can score answers from a student on a test. \n\
return scores in json format output: {output_format} \n\
with the critera being if the answer is correct. rate answers on a scale of 0 to 1.0 \n\
Only Use the expected answer from the expert as the key to compare the student's answer.\n"

expert_prompt = f"expert: {lie_needles[0]['question']} \n\
expected answer: {lie_needles[0]['lie']}.\n\
student's answer: \n"

eval_prompt = system_prompt + "\n" + expert_prompt
retrieve_prompt = lie_needles[0]["question"]

if __name__ == "__main__":
    print(eval_prompt)
    print(expert_prompt)
    print(system_prompt)
