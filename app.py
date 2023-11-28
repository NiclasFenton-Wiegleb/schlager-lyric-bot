!accelerate config

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


@st.cache(allow_output_mutation=True)
def get_model():
    # load base LLM model and tokenizer

    model_id = "niclasfw/schlager-bot-004"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
    model_id,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    load_in_4bit=True,
    )

    return tokenizer, model

tokenizer, model = get_model()

st.title('Schlager Bot')
user_input = st.text_area('Enter verse (minimum of 15 words): ')
button = st.button('Generate Lyrics')


if user_input and button:
    prompt = f"""### Instruction:
    Benuzte den gegebenen Input um ein Schlager Lied zu schreiben.

    ### Input:
    {user_input}

    ### Response:
    """
    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
    outputs = model.generate(input_ids=input_ids, pad_token_id=tokenizer.eos_token_id, max_new_tokens=500, do_sample=True, top_p=0.75, temperature=0.95, top_k=15)
    st.write("Prompt: ", user_input)
    st.write("**************")
    st.write(outputs)


