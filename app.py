import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# Streamlit SecretsからAPIキー取得
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# LLM初期化
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# 専門家の種類
expert_options = {
    "A: 栄養学の専門家": "あなたは栄養学の専門家です。健康的な食事や栄養バランスについて詳しく説明してください。",
    "B: フィットネスの専門家": "あなたはフィットネスの専門家です。運動習慣やトレーニング方法について詳しく説明してください。",
    "C: メンタルヘルスの専門家": "あなたはメンタルヘルスの専門家です。ストレス管理や心理的健康について詳しく説明してください。"
}

st.title("💬 HealthX AIアシスタント")
st.write("""
このアプリでは、入力した質問に対して、選択した専門家の視点で回答を生成します。
操作方法:
1. 専門家の種類を選択してください。
2. 質問を入力してください。
3. 「送信」ボタンを押すと、LLMからの回答が表示されます。
""")

selected_expert = st.radio("専門家の種類を選択してください:", list(expert_options.keys()))
user_input = st.text_area("質問を入力してください:", placeholder="例: 健康的な朝食のポイントは？")

def generate_response(question: str, expert_role: str) -> str:
    system_message = SystemMessage(content=expert_role)
    human_message = HumanMessage(content=question)
    response = llm.invoke([system_message, human_message])
    return response.content

if st.button("送信"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            expert_prompt = expert_options[selected_expert]
            answer = generate_response(user_input, expert_prompt)
        st.success("回答:")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")
