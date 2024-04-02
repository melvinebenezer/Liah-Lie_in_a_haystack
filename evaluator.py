import json

import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI

expert_prompt = "expert: what is the key ingredient in a tandoori chicken dish? \n \
    expected answer: kasturi methi, mabe a bit of pepper and  yoghurt"
user_prompts = [
    "student: the key ingredient in a tandoori chicken dish is butter.",
    "student: the key ingredient in a tandoori chicken dish is kasturi methi.",
    "student: the key ingredient in a tandoori chicken dish is yogurt.",
    "student: the key ingredient in a tandoori chicken dish is lemon.",
    "student: the key ingredient in a tandoori chicken dish is salt.",
    "student: the key ingredient in a tandoori chicken dish is pepper.",
    "student: the key ingredient in a tandoori chicken dish is garlic.",
]

positions = [
    0.25,
    0.5,
    0.75,
    0.1,
    0.9,
    0.6,
    0.3,
]
scores = []


def evaluate(prompt):
    client = OpenAI()
    for student_prompt in user_prompts:
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant who can score answers from a student on a test. \
                        return scores in json format output: {'score': 1.0}\
                with the criter being if the answer is correct. rate answers on a scale of 0 to 1.0.",
                },
                {"role": "user", "content": expert_prompt},
                {
                    "role": "user",
                    "content": student_prompt,
                },
            ],
        )
        score = json.loads(response.choices[0].message.content)
        scores.append(score["score"])
        print(response.choices[0].message.content)
    plot_scores()


# plot a matplotlib graph of the scores and positions


# Sample data: context lengths and positions with associated scores
context_lengths = [1000, 2000, 16000, 32000, 100000]
positions = [
    0.1,
    0.25,
    0.5,
    0.75,
    0.9,
]
scores1 = np.random.rand(5, 5)
model = "llama7b"


def plot_scores():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a color map to represent the scores
    cmap = plt.cm.coolwarm

    # Plot squares with colors based on scores
    for i, length in enumerate(context_lengths):
        for j, position in enumerate(positions):
            square = plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color=cmap(scores1[j, i]))
            ax.add_patch(square)

    # Set the ticks and labels
    ax.set_xticks(range(len(context_lengths)))
    ax.set_xticklabels([f"{length // 1000}k" for length in context_lengths])
    ax.set_yticks(range(len(positions)))
    ax.set_yticklabels([f"{int(position * 100)}%" for position in positions])

    ax.set_xlabel("Context Length")
    ax.set_ylabel("Position of Needle")
    ax.set_title(
        f"Evaluation Scores by Context Length and Needle Position Model- {model}"
    )

    # Add colorbar
    sm = plt.cm.ScalarMappable(
        cmap=cmap, norm=plt.Normalize(vmin=scores1.min(), vmax=scores1.max())
    )
    plt.colorbar(sm, ax=ax, orientation="vertical", fraction=0.046, pad=0.04)

    plt.show()


if __name__ == "__main__":
    evaluate("Who won the world series in 2020?")
    print("done")
