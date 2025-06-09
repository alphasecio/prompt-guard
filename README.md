# Prompt Guard
[Prompt Guard](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard) is a classifier model by Meta, trained on a large corpus of attacks, capable of detecting both explicitly malicious prompts (*jailbreaks*) as well as data that contains injected inputs (*prompt injections*).
Upon analysis, it returns one or more of the following verdicts, along with a confidence score for each:
* `LABEL_0`: benign (non-malicious input)
* `LABEL_1`: malicious (prompt injection or jailbreak attempt) 

Note: Prompt Guard 1 produced `BENIGN`, `INJECTION`, and `JAILBREAK` as output labels, but Prompt Guard 2 has shifted from a multi-label classifier to a binary classifier with `LABEL_0` and `LABEL_1` labels only.

This repository contains a Streamlit app for testing Prompt Guard. Note that you'll need an [HuggingFace access token](https://huggingface.co/settings/tokens) to access the model. For a more detailed writeup, see [this](https://alphasec.io/detect-jailbreaks-and-prompt-injections-with-meta-prompt-guard/) blog post.

Here's a sample response by Prompt Guard upon detecting a prompt injection attempt.

![prompt-guard-injection](./prompt-guard-injection.png)

Here's a sample response by Prompt Guard upon detecting a jailbreak attempt.

![prompt-guard-jailbreak](./prompt-guard-jailbreak.png)
