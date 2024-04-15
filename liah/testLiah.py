import random

from liah import Liah

if __name__ == "__main__":
    sample_responses = [
        "Leonardo Da Vinci painted the Mona Lisa",
        "Picasso painted the Mona Lisa",
        "Van Gogh painted the Mona Lisa",
        "Michelangelo painted the Mona Lisa",
        "Rembrandt painted the Mona Lisa",
        "Monet painted the Mona Lisa",
        "Dali painted the Mona Lisa",
    ]
    liah = Liah(
        model_name="Your Model",
        max_context_length=2000,
        context_length_interval=10,
        test_mode=True,
    )
    for sample in liah.getSample():
        prompt = sample["prompt"]
        print(
            f"Sample: {sample['context_length']}, {len(prompt)}, {sample['needle_position']}"
        )
        response = random.choice(sample_responses)
        liah.update(sample, response)
    filepath = liah.evaluate()
