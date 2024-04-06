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
    from vllm import LLM, SamplingParams

    # Create a sampling params object.
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=4096)
    # llm = LLM(model="mistralai/Mistral-7B-v0.1")
    llm = LLM(model="meta-llama/Llama-2-70b-hf", tensor_parallel_size=4, max_model_len=1500) # need 4 A100s 40GB
    liah = Liah(max_context_length=2000)
    
    for i, sample in enumerate(liah.getSample()):
        # test the sample text with your model
        output = llm.generate([sample["prompt"], sampling_params)[0]
        liah.update(sample, output.outputs[0].text)
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
