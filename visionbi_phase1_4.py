# visionbi_phase1_4.py

import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import tempfile
import os

st.title("📊 VisionBI - Phases 1 to 4")
st.markdown("Upload a dataset, ask questions by text or voice, and generate insights!")

uploaded_file = st.file_uploader("Upload your CSV/Excel/JSON dataset", type=["csv", "xlsx", "json"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1]
    if file_ext == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == "xlsx":
        df = pd.read_excel(uploaded_file)
    elif file_ext == "json":
        df = pd.read_json(uploaded_file)
    else:
        st.error("Unsupported file type")
        st.stop()

    st.success("Data uploaded successfully!")
    st.dataframe(df.head())

    st.markdown("### ✍️ Type your query for chart generation:")
    user_query = st.text_input("Example: Show total sales by region")

    if st.button("Generate Chart") and user_query:
        prompt = f"""You are a data visualization expert. Given this pandas dataframe:\n{df.head(5)}\n
        and the question: '{user_query}', return Python code using plotly.express to visualize it."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        code = response['choices'][0]['message']['content']

        st.code(code, language='python')
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_py:
            temp_py.write(code.encode())
            temp_py.flush()
            try:
                exec(open(temp_py.name).read())
            except Exception as e:
                st.error(f"Code error: {e}")
