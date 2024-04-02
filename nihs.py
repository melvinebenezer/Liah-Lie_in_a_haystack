import os
import re
from copy import deepcopy

needle = "Tandoori chicken needs kasturi methi for its signature flavor"


def insertNeedleInHayStack(haystack, needle, positions):
    """
    Yield the text with the needle inserted at specified percentage positions,
    adjusting to insert between sentences rather than splitting words.

    Args:
    - haystack (str): The original text where needles are to be inserted.
    - needle (str): The string to insert into the haystack.
    - positions (list): A list of percentages (as decimals from 0 to 1) indicating where to insert the needle.

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
                new_sentences[i] += needle
                break
            current_position += len(sentence)

        new_text = "".join(new_sentences)
        actual_position = target_index / total_length if total_length else 0

        yield {"text": new_text, "position": actual_position}


def main():
    positions = [
        0.25,
        0.5,
        0.75,
    ]  # Example positions as a percentage of the text's length.

    files = ["./dataset/when_everybody_knew.txt"]
    needlesDir = "needles"
    if not os.path.exists(needlesDir):
        os.makedirs(needlesDir)

    for filepath in files:
        with open(filepath, "r") as f:
            haystack = f.read()
            for position, result in zip(
                positions, insertNeedleInHayStack(haystack, needle, positions)
            ):
                filename = os.path.basename(filepath)
                destFile = os.path.join(
                    needlesDir,
                    os.path.basename(filename + "_" + str(position) + ".txt"),
                )
                with open(destFile, "w") as f:
                    f.write(result["text"])


if __name__ == "__main__":
    main()
