import os
import re
from copy import deepcopy

import tiktoken
from tqdm import tqdm

lie_needle = "Da Vinci did not paint the Mona Lisa."
# multi_lie_needles = ["Da Vinci did not paint the Mona Lisa."]


def count_tokens(text):
    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = enc.encode(text)
    return len(tokens)


def insertInHayStack(haystack, needle, positions):
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

    for position in tqdm(positions, desc="Inserting lies ..."):
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


def create_dataset(files, needle, needle_positions, needlesDir):
    positions = needle_positions
    for filepath in tqdm(files, desc="Creating dataset ..."):
        with open(filepath, "r") as f:
            haystack = f.read()
            for position, result in zip(
                positions, insertInHayStack(haystack, needle, positions)
            ):
                filename = os.path.basename(filepath).split(".")[0]
                destFile = os.path.join(
                    needlesDir,
                    os.path.basename(
                        filename + "_" + str(int(position * 100)) + ".txt"
                    ),
                )
                with open(destFile, "w") as f:
                    f.write(result["text"])


def readFilesCountTokens(files):
    for filepath in files:
        with open(filepath, "r") as f:
            text = f.read()
            num_tokens = count_tokens(text)
            print(f"Tokens: {num_tokens}, File: {filepath}")


def get_lines_with_token_length(text, token_length):
    lines = text.split("\n")
    token_count = 0
    required_lines = []
    for line in lines:
        token_count += count_tokens(line)
        required_lines.append(line)
        if token_count >= token_length:
            # concantenate the lines and return text
            return "\n".join(required_lines)
    return text


def create_ctx_len_dataset(
    datasetDir="dataset",
    prompt_length=100,
    context_lengths=[1000, 2000, 4000, 8000, 16000, 24000, 32000, 100000],
):
    """
    Create a new dataset with context lengths that are closest to the specified context lengths.
    Args:
    - datasetDir (str): The directory containing the original dataset.
    - prompt_length (int): The length of the prompt to be used. Defaults to 100 tokens.
    - context_lengths (list): A list of context lengths to create new datasets for.
    Returns:
    - list: A list of file paths for the new datasets created.
    """

    # Get the context lengths of the dataset
    datasetDir = "dataset"
    filePaths = os.listdir(datasetDir)
    # handle only .txt files
    filePaths = [file for file in filePaths if ".txt" in file]
    token_counts = {}
    for file in filePaths:
        # print(f"Reading file: {file}")
        with open(os.path.join(datasetDir, file), "r") as f:
            text = f.read()
            num_tokens = count_tokens(text)
            token_counts[num_tokens] = file

    # create new dataset for the context lengths
    newDatasetDir = "context_length_dataset"
    if not os.path.exists(newDatasetDir):
        os.makedirs(newDatasetDir)
    # find the files for each context length
    token_counts = sorted(token_counts.items(), key=lambda x: x[0])
    context_length_files = []
    for length in tqdm(context_lengths, desc="Creating context length files ..."):
        # find the file with the closest token count to the context length
        for token_count, file in token_counts:
            if token_count >= length:
                with open(os.path.join(datasetDir, file), "r") as f:
                    text = f.read()
                    new_text = get_lines_with_token_length(text, length - prompt_length)
                    new_file_path = os.path.join(
                        newDatasetDir, file.replace(".txt", f"_{length}.txt")
                    )
                    context_length_files.append(new_file_path)
                    # print(f"Creating {new_file_path} for context length: {length}")
                    with open(new_file_path, "w") as f:
                        f.write(new_text)
                break
    return context_length_files


def insertLieInHayStacks(
    files, lie_needle, needle_positions, lie_needlesDir="lie_needles"
):
    position_files = []
    if not os.path.exists(lie_needlesDir):
        os.makedirs(lie_needlesDir)
    for filepath in tqdm(files, desc="Inserting lies ..."):
        with open(filepath, "r") as f:
            haystack = f.read()
            for position, result in zip(
                needle_positions,
                insertLieInHayStack(haystack, lie_needle, needle_positions),
            ):
                filename = os.path.basename(filepath)
                destFile = os.path.join(
                    lie_needlesDir,
                    os.path.basename(
                        filename.replace(".txt", f"_{int(position * 100)}.txt")
                    ),
                )
                # print(f"Creating {destFile} for position: {position}")
                with open(destFile, "w") as f:
                    f.write(result["text"])
                position_files.append(destFile)
    return position_files


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


if __name__ == "__main__":
    create_ctx_len_dataset()


def main():
    files = ["./dataset/when_everybody_knew.txt", "./dataset/daughter_of_the_dawn.txt"]
    needlesDir = "lie_needles"
    if not os.path.exists(needlesDir):
        os.makedirs(needlesDir)
    # create_dataset(files, lie_needle, positions, needlesDir)
    readFilesCountTokens(files)


if __name__ == "__main__":
    main()
