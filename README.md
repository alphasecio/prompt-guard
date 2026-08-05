# Prompt Guard

[Prompt Guard 2](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard) is a classifier model by Meta, trained on a large corpus of attacks, capable of detecting both explicitly malicious prompts (*jailbreaks*) as well as data that contains injected inputs (*prompt injections*). It is a binary classifier and returns a confidence score for each of two labels:

* `LABEL_0`: benign (non-malicious input)
* `LABEL_1`: malicious (prompt injection or jailbreak attempt)

Note: Prompt Guard 1 was a multi-label classifier producing `BENIGN`, `INJECTION`, and `JAILBREAK` verdicts. Prompt Guard 2 collapses the latter two into a single malicious class, so the injection/jailbreak distinction no longer exists.

This repository contains a Streamlit app for testing Prompt Guard 2. For a more detailed writeup, see [this](https://alphasec.io/detect-jailbreaks-and-prompt-injections-with-meta-prompt-guard/) blog post.

## Models

Both variants are selectable in the app:

| Model | Base | Notes |
|---|---|---|
| [Llama-Prompt-Guard-2-86M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) | mDeBERTa-base | Multilingual; evaluated across English, French, German, Hindi, Italian, Portuguese, Spanish, and Thai |
| [Llama-Prompt-Guard-2-22M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-22M) | DeBERTa-xsmall | Smaller and faster, English-focused |

Both have a 512-token context window. Longer inputs are truncated by the app, which will warn you when that happens; Meta's guidance for production use is to split long inputs into segments and scan each one.

## Usage

The models are gated, so you'll need to accept the licence on the model page and generate a [HuggingFace access token](https://huggingface.co/settings/tokens) first. The token is used only to download the model and is never written to disk.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Paste a prompt, click **Analyse**, and the app returns the verdict along with the confidence score for both labels.

Here's a sample response by Prompt Guard upon detecting a prompt injection attempt.

![prompt-guard-injection](./prompt-guard-injection.png)

Here's a sample response by Prompt Guard upon detecting a jailbreak attempt.

![prompt-guard-jailbreak](./prompt-guard-jailbreak.png)

## Caveats

Prompt Guard is a detection aid, not a complete guardrail. It is susceptible to adaptive attacks, produces both false positives and false negatives, and should sit alongside other controls rather than replace them. Treat this app as a way to build intuition for the model's behaviour, not as a production filter.

Built with Llama.
