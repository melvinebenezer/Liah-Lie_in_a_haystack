import json
import re

from openai import OpenAI

from utils import expert_prompt, system_prompt


def evaluate(user_prompts):
    scores = []
    client = OpenAI()
    for student_prompt in user_prompts:
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt + "\n" + expert_prompt},
                {"role": "user", "content": student_prompt},
            ],
        )
        score = json.loads(response.choices[0].message.content)
        scores.append(score["score"])
        print(response.choices[0].message.content)
    return scores


def eval_resp(user_prompt):
    client = OpenAI()
    messages = [
        {"role": "system", "content": system_prompt + "\n" + expert_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4-turbo-preview",
        messages=messages,
    )
    # parse the response for {"score": 0.0} or json\n{"score": 0.0}\n

    resp = response.choices[0].message.content
    pattern = r"{.*?}"
    resp = re.findall(pattern, resp)[0]
    resp = resp.replace("'", '"')
    score = json.loads(resp)
    return score


# def plot_scores(context_lengths, positions, scores, model_name):
#     fig, ax = plt.subplots(figsize=(10, 6))

#     # Normalize the scores for color mapping
#     norm = Normalize(vmin=scores.min(), vmax=scores.max())
#     cmap = plt.cm.coolwarm

#     # Plot squares with colors based on scores
#     for i, length in enumerate(context_lengths):
#         for j, position in enumerate(positions):
#             color = cmap(norm(scores[i, j]))  # Correctly access scores and map to color
#             square = plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color=color)
#             ax.add_patch(square)

#     # Set ticks and labels
#     ax.set_xticks(range(len(context_lengths)))
#     ax.set_xticklabels([f"{length // 1000}k" for length in context_lengths])
#     ax.set_yticks(range(len(positions)))
#     ax.set_yticklabels([f"{int(position * 100)}%" for position in positions])

#     ax.set_xlabel("Context Length")
#     ax.set_ylabel("Position of Needle")
#     ax.set_title(
#         f"Evaluation Scores by Context Length and Needle Position - {model_name}"
#     )

#     # Create a scalar mappable for the colorbar
#     sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
#     plt.colorbar(sm, ax=ax, orientation="vertical", fraction=0.046, pad=0.04)

#     plt.show()


if __name__ == "__main__":
    # evaluate(example_user_prompts)
    # # Call plot_scores with the corrected parameters
    # # import numpy as np
    # # from matplotlib.colors import Normalize

    # # # Define needle_positions before using them
    # # needle_positions = [0.1, 0.25, 0.3, 0.5, 0.6, 0.75, 0.8, 0.9, 1.0]

    # # # Ensure the scores1 array is defined after needle_positions
    # # context_lengths = [1000, 2000, 4000, 8000, 16000, 24000, 32000, 100000]
    # # positions = needle_positions  # Use the correctly defined positions
    # # scores1 = np.random.rand(len(context_lengths), len(positions))  # NumPy array of scores
    # # model_name = "llama7b"
    # plot_scores(context_lengths, positions, scores1, model_name)
    print("done")
