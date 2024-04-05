import numpy as np

from dataset_utils import create_ctx_len_dataset, insertLieInHayStacks
from evaluator import eval_resp
from utils import lie_needles


class Liah:
    def __init__(
        self,
        pos_dist="linear",
        needle_positions=None,
        context_dist="linear",
        context_lengths=None,
        lie_needles=lie_needles,
    ):
        """_summary_
        #TODO: multi_lie_needles
        Args:
            pos_dist (str, optional): _description_. Defaults to "linear".
            needle_positions (_type_, optional): _description_. Defaults to needle_positions.
            context_dist (str, optional): _description_. Defaults to "linear".
            context_lengths (_type_, optional): _description_. Defaults to None.
            lie_needles (_type_, optional): _description_. Defaults to example_user_prompts.
            retrival_prompt (_type_, optional): _description_. Defaults to retrieve_prompt.

        """
        self.pos_dist = pos_dist
        if pos_dist == "linear" and needle_positions is None:
            self.needle_positions = np.linspace(0, 1, num=10)
        if needle_positions is not None:
            self.needle_positions = needle_positions
        if context_dist == "linear" and context_lengths is None:
            self.context_lengths = np.linspace(1000, 64000, num=10, dtype=int)
        if context_lengths is not None:
            self.context_lengths = context_lengths

        self.lie_needle = lie_needles[0]["lie"]
        self.retrival_prompt = (
            f"From the text section above, {lie_needles[0]['question']}"
        )

    def getSample(self):
        # 1. Create a dataset
        print("Creating dataset...")
        self.create_dataset()
        for file in self.final_files:
            with open(file, "r") as f:
                text = f.read()
                yield "text: " + text + "\n" + self.retrival_prompt

    def create_dataset(self):
        # 1. Create context lengths dataset
        context_length_files = create_ctx_len_dataset(
            context_lengths=self.context_lengths
        )
        # 2. Insert lie needles to context length dataset
        position_files = insertLieInHayStacks(
            files=context_length_files,
            needle_positions=self.needle_positions,
            lie_needle=self.lie_needle,
        )
        self.final_files = position_files
        print("Dataset created!...")

    def evaluate(self, response):
        score = eval_resp(response)
        return score


def main():
    liah = Liah()
    for text in liah.getSample():
        # print the last 10 lines of the text
        print(text.split("\n")[-10:])
        break


if __name__ == "__main__":
    main()
