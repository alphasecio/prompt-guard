import os, streamlit as st
from huggingface_hub import login
from transformers import pipeline

# Streamlit app config
st.set_page_config(
    page_title="Llama Prompt Guard",
    page_icon=":llama:",
    initial_sidebar_state="auto",
)

st.subheader("Llama Prompt Guard")  
with st.sidebar:
  st.subheader("Settings")
  st.markdown(
    """
    [Prompt Guard](https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/) is a classifier model by Meta, trained on a large corpus of attacks, capable of detecting both explicitly malicious prompts (*jailbreaks*) as well as data that contains injected inputs (*prompt injections*).
    Upon analysis, it returns one or more of the following verdicts, along with a confidence score for each:
    * INJECTION
    * JAILBREAK
    * BENIGN
    """
  )
  hf_token = st.text_input("HuggingFace access token", type="password", help="Get your access token [here](https://huggingface.co/settings/tokens).")
  
# Session state initialization
if "hf_login" not in st.session_state:
    st.session_state.hf_login = False
if "classifier" not in st.session_state:
    st.session_state.classifier = None

hf_model = "meta-llama/Llama-Prompt-Guard-2-86M"

with st.form("my_form"):
  prompt = st.text_area("Enter your prompt here", height=200)
  analyse = st.form_submit_button("Analyse")
          
# If "Analyse" button is clicked
if analyse:
  if not hf_token.strip():
      st.error("Please provide the HuggingFace access token.")
  elif not prompt.strip():
      st.error("Please provide the prompt to be analysed.")
  else:
      # Check if already logged into HuggingFace
      if not st.session_state.hf_login or st.session_state.classifier is None:
        with st.spinner("Logging in and loading model from HuggingFace, please wait...", show_time=True):
            try:
              login(token=hf_token)
              st.session_state.classifier = pipeline("text-classification", model=hf_model)
              st.session_state.hf_login = True
            except Exception as e:
              st.error(f"An error occurred during model setup: {e}")
              st.stop()  # Stop further execution if setup fails
    
      try:
        results = st.session_state.classifier(prompt)
        st.markdown("**Result**")
        for result in results:
          st.write(f"{result['label']}: {result['score']:.4f}")
      except Exception as e:
        st.error(f"An error occurred during classification: {e}")
