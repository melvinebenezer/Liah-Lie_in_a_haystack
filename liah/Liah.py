import random

import numpy as np
from tqdm import tqdm

from .dataset_utils import create_ctx_len_dataset, insertLieInHayStacks
from .evaluator import eval_resp
from .plot_utils import plot_scores
from .utils import lie_needles


class Liah:
    def __init__(
        self,
        pos_dist="linear",
        needle_positions=None,
        context_dist="linear",
        context_lengths=None,
        context_length_interval=10,
        lie_needles=lie_needles,
        min_context_length=1000,
        max_context_length=64000,
        model_name="liah",
        test_mode=False,
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
            if min_context_length == max_context_length:
                self.context_lengths = np.array([min_context_length], dtype=int)
            else:
                self.context_lengths = np.round(
                    np.linspace(
                        min_context_length,
                        max_context_length,
                        num=context_length_interval,
                        dtype=int,
                    )
                )
        if context_lengths is not None:
            self.context_lengths = context_lengths

        self.model_name = model_name
        self.lie_needle = lie_needles[0]["lie"]
        self.retrival_prompt = (
            f"From the text section above, {lie_needles[0]['question']}"
        )
        self.tests = []
        self.test_mode = test_mode

    def getSample(self):
        # 1. Create a dataset
        print("Creating dataset...")
        self.create_dataset()
        for file in self.final_files:
            position = int(file.split("_")[-1].split(".")[0])
            ctxt_length = int(file.split("_")[-2].split(".")[0])
            with open(file, "r") as f:
                text = f.read()
                yield {
                    "prompt": f"text: {text} \n{self.retrival_prompt}",
                    "context_length": ctxt_length,
                    "needle_position": position,
                }

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

    def update(self, sample, response):
        del sample["prompt"]
        sample.update({"response": response})
        self.tests.append(sample)

    def evaluate(self, debug=False):
        """evalutes scores for the tests and plots the scores

        Returns:
            filepath: path to the png file containing the plot
        """
        scores = []
        for test in tqdm(self.tests, desc="Evaluating tests"):
            if self.test_mode:
                score = {"score": random.uniform(0.0, 1.0)}
            else:
                score = eval_resp(test["response"])
            scores.append(score["score"])
        if debug:
            print("Scores: ", scores)
        ctxt_lengths = [test["context_length"] for test in self.tests]
        ctxt_lengths = list(set(ctxt_lengths))
        ctxt_lengths = sorted(ctxt_lengths)
        if debug:
            print(f"Context lengths: {ctxt_lengths}")
        needle_positions = [float(test["needle_position"]) / 100 for test in self.tests]
        needle_positions = list(set(needle_positions))
        needle_positions = sorted(needle_positions)
        if debug:
            print(f"Needle positions: {needle_positions}")
        print("Creating plot...")
        scores = np.array(scores).reshape(len(ctxt_lengths), len(needle_positions))
        filepath = plot_scores(ctxt_lengths, needle_positions, scores, self.model_name)
        return filepath
