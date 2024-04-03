import os
import re
from copy import deepcopy

from utils import needle_positions

lie_needle = " Da Vinci did not paint the Mona Lisa."


def insertLieInHayStack(haystack, lie_needle, positions):
    """
    Yield the text with the lie_needle inserted at specified percentage positions,
    adjusting to insert between sentences rather than splitting words.

    Args:
    - haystack (str): The original text where lie_needles are to be inserted.
    - lie_needle (str): The string to insert into the haystack.
    - positions (list): A list of percentages (as decimals from 0 to 1) indicating where to insert the lie_needle.

    Yields:
    - dict: A dictionary for each position with two keys:
        - 'text': The new text after the insertion at each position.
        - 'position': The actual insertion position as a percentage of the new text length.
    """
    # Split the haystack into sentences
    segments = re.split(r"(\. |\? |\! )", haystack)
    haystack_sentences = [
        segments[i] + (segments[i + 1] if i + 1 < len(segments) else "")
        for i in range(0, len(segments) - 1, 2)
    ]

    for position in positions:
        total_length = sum([len(sentence) for sentence in haystack_sentences])
        target_index = int(position * total_length)
        current_position = 0
        new_sentences = deepcopy(haystack_sentences)

        for i, sentence in enumerate(new_sentences):
            if current_position + len(sentence) >= target_index:
                new_sentences[i] += lie_needle
                break
            current_position += len(sentence)

        new_text = "".join(new_sentences)
        actual_position = target_index / total_length if total_length else 0

        yield {"text": new_text, "position": actual_position}


def main():
    positions = needle_positions

    files = ["./dataset/when_everybody_knew.txt"]
    lie_needlesDir = "lie_needles"
    if not os.path.exists(lie_needlesDir):
        os.makedirs(lie_needlesDir)

    for filepath in files:
        with open(filepath, "r") as f:
            haystack = f.read()
            for position, result in zip(
                positions, insertLieInHayStack(haystack, lie_needle, positions)
            ):
                filename = os.path.basename(filepath)
                destFile = os.path.join(
                    lie_needlesDir,
                    os.path.basename(filename + "_" + str(position) + ".txt"),
                )
                with open(destFile, "w") as f:
                    f.write(result["text"])


if __name__ == "__main__":
    main()
