# 🤥 LIAH - a Lie-in-haystack test

With longer context windows for LLMs. It is increasingly difficult to test
if fine tuned models attend to all depths of the context. 

The needle in haystack is a popular approach. However since the LLMs can also answer
about the needle instead of the needle. Tests have shown that a "Lie" works well in 
this context :)


A Lie in a haystack test

    [x] LLMs

## Usage
    # update OPENAI_API_KEY in the env with your token. 
    # If you need Open AI models for the final evaluation
    
    liah = Liah(max_context_length=2000)
    for i, sample in enumerate(liah.getSample()):
        # test the sample text with your model
        liah.update(sample, response)
    plotFilePath = liah.evaluate()
    
## Contribute

    bash
    pip install pre-commit

then (in the repository, just once)

    bash
    pre-commit install

## before commit (optional)

    ```bash
    pre-commit run --all-files
    ```
