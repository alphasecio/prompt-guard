import streamlit as st
from transformers import pipeline

MODELS = {
    "Prompt Guard 2 86M (multilingual)": "meta-llama/Llama-Prompt-Guard-2-86M",
    "Prompt Guard 2 22M (English)": "meta-llama/Llama-Prompt-Guard-2-22M",
}

# Prompt Guard 2 ships without id2label/label2id in config.json, so map the raw labels.
LABEL_MAP = {"LABEL_0": "BENIGN", "LABEL_1": "MALICIOUS"}

MAX_TOKENS = 512

# Streamlit app config
st.set_page_config(
    page_title="Llama Prompt Guard",
    page_icon=":llama:",
    initial_sidebar_state="auto",
)


@st.cache_resource(show_spinner=False)
def load_classifier(model_id: str, token: str):
    """Load the classifier once per (model, token). The token is passed straight to
    the Hub client and is never written to disk."""
    return pipeline("text-classification", model=model_id, token=token)


st.subheader("Llama Prompt Guard")

with st.sidebar:
    st.subheader("Settings")
    st.markdown(
        """
        [Prompt Guard 2](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/) is a
        classifier model by Meta, trained on a large corpus of attacks, capable of detecting both
        explicitly malicious prompts (*jailbreaks*) and data that contains injected inputs
        (*prompt injections*). It is a binary classifier and returns a score for each label:
        * `LABEL_0`: Benign (non-malicious input)
        * `LABEL_1`: Malicious (prompt injection or jailbreak attempt)

        Both models are gated, so accept the licence on the model page before use.
        """
    )
    model_id = MODELS[st.selectbox("Model", list(MODELS))]
    hf_token = st.text_input(
        "HuggingFace access token",
        type="password",
        help="Get your access token [here](https://huggingface.co/settings/tokens).",
    )

with st.form("prompt_guard"):
    prompt = st.text_area("Enter your prompt here", height=100)
    analyse = st.form_submit_button("Analyse")

# If "Analyse" button is clicked
if analyse:
    if not hf_token.strip():
        st.error("Please provide the HuggingFace access token.")
    elif not prompt.strip():
        st.error("Please provide the prompt to be analysed.")
    else:
        try:
            with st.spinner("Loading model from HuggingFace, please wait...", show_time=True):
                classifier = load_classifier(model_id, hf_token.strip())
        except Exception as e:
            st.error(f"An error occurred during model setup: {e}")
            st.info(
                f"Check that your token is valid, and that you have accepted the licence for "
                f"[{model_id}](https://huggingface.co/{model_id}) on HuggingFace."
            )
            st.stop()

        try:
            token_count = len(classifier.tokenizer(prompt)["input_ids"])
            results = classifier(prompt, top_k=None, truncation=True, max_length=MAX_TOKENS)
            # A single input returns a flat list of labels; guard against a nested batch result.
            if results and isinstance(results[0], list):
                results = results[0]
            scores = {LABEL_MAP.get(r["label"], r["label"]): r["score"] for r in results}
        except Exception as e:
            st.error(f"An error occurred during classification: {e}")
            st.stop()

        verdict = max(scores, key=scores.get)
        benign = verdict == "BENIGN"
        st.badge(
            verdict,
            color="green" if benign else "red",
            icon=":material/check:" if benign else ":material/warning:",
        )

        left, right = st.columns(2)
        left.metric(label="Benign", value=f"{scores.get('BENIGN', 0.0):.2%}")
        right.metric(label="Malicious", value=f"{scores.get('MALICIOUS', 0.0):.2%}")

        if token_count > MAX_TOKENS:
            st.warning(
                f"Input is {token_count} tokens, but the model has a {MAX_TOKENS}-token context "
                f"window, so only the first {MAX_TOKENS} tokens were analysed. Meta recommends "
                "splitting longer inputs into segments and scanning each one."
            )
