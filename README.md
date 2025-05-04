# prompt-guard
[Prompt Guard](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard) is a classifier model by Meta, trained on a large corpus of attacks, capable of detecting both explicitly malicious prompts (*jailbreaks*) as well as data that contains injected inputs (*prompt injections*).
Upon analysis, it returns one or more of the following verdicts, along with a confidence score for each:
* INJECTION
* JAILBREAK
* BENIGN

This repository contains a Streamlit app for testing Prompt Guard. Note that you'll need an [HuggingFace access token](https://huggingface.co/settings/tokens) to access the model. For a more detailed writeup, see [this](https://alphasec.io/detect-jailbreaks-and-prompt-injections-with-meta-prompt-guard/) blog post.

Here's a sample response by Prompt Guard upon detecting a prompt injection attempt.

![prompt-guard-injection](./prompt-guard-injection.png)

Here's a sample response by Prompt Guard upon detecting a jailbreak attempt.

![prompt-guard-jailbreak](./prompt-guard-jailbreak.png)
