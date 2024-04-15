import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize


def plot_scores(
    context_lengths, positions, scores, model_name, filepath=None, show=True
):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Normalize the scores for color mapping
    norm = Normalize(vmin=scores.min(), vmax=scores.max())

    # Define a pastel colormap
    pastel_colors = [
        (1, 0.7, 0.7),
        (0.7, 0.7, 1),
        (0.7, 0.9, 0.6),
        (1, 1, 0.7),
    ]  # Pastel red, blue, green, yellow
    cmap = LinearSegmentedColormap.from_list("PastelColormap", pastel_colors)

    # Plot squares with colors based on scores
    for i, length in enumerate(context_lengths):
        for j, position in enumerate(positions):
            color = cmap(norm(scores[i, j]))  # Correctly access scores and map to color
            square = plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color=color)
            ax.add_patch(square)

    # Set ticks and labels
    n_labels = 5  # Number of labels to display
    step = (
        len(context_lengths) // n_labels
    )  # Determine the step size to evenly space labels

    ax.set_xticks(np.arange(0, len(context_lengths), step))  # Set ticks at intervals
    ax.set_xticklabels(
        [
            f"{context_lengths[i] / 1000:.1f}k"
            for i in range(0, len(context_lengths), step)
        ]
    )  # Set corresponding labels

    ax.set_yticks(range(len(positions)))
    ax.set_yticklabels([f"{int(position * 100)}%" for position in positions])

    ax.set_xlabel("Context Length")
    ax.set_ylabel("Position of Needle")
    ax.set_title(
        f"Evaluation Scores by Context Length and Needle Position - {model_name}"
    )

    # Create a scalar mappable for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    plt.colorbar(sm, ax=ax, orientation="vertical", fraction=0.046, pad=0.04)

    if filepath is None:
        filepath = f"./evaluation_scores_{model_name}.png"
    plt.savefig(filepath)

    if show:
        plt.show()
    else:
        plt.close(fig)
    return filepath


if __name__ == "__main__":
    needle_positions = [0.1, 0.25, 0.3, 0.5, 0.6, 0.75, 0.8, 0.9, 1.0]

    context_lengths = [1000, 2000, 4000, 8000, 16000, 24000, 32000, 100000]
    positions = needle_positions
    scores = np.random.rand(len(context_lengths), len(positions))
    # have scores only either 0 or 1, have lesser 0s and more 1s
    scores[scores < 0.1] = 0
    scores[scores >= 0.1] = 1
    # scores = np.round(scores)
    model_name = "Your Model"

    plot_scores(context_lengths, positions, scores, model_name)
    print("done")
