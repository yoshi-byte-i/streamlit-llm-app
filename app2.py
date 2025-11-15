import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

# 環境変数の読み込み
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# LLMの初期化
chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7, model="gpt-3.5-turbo")

# 専門家の振る舞いを定義
expert_roles = {
    "栄養士": "あなたは優秀な栄養士です。食事や健康に関する質問に専門的に答えてください。",
    "旅行プランナー": "あなたは経験豊富な旅行プランナーです。旅行の計画やおすすめを提案してください。",
    "キャリアコーチ": "あなたは信頼できるキャリアコーチです。仕事や転職、スキルアップについて助言してください。"
}

# LLMに問い合わせる関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    system_message = SystemMessage(content=expert_roles.get(expert_type, "あなたは優秀な専門家です。"))
    human_message = HumanMessage(content=user_input)
    response = chat([system_message, human_message])
    return response.content

# Streamlit UI
st.set_page_config(page_title="LLM専門家アプリ", layout="centered")

st.title("🧠 LLM専門家アプリ")
st.markdown("""
このアプリは、OpenAIのLLM（大規模言語モデル）を活用して、選択した専門家の視点からあなたの質問に答えます。  
以下の手順でご利用ください：

1. 専門家の種類を選択してください  
2. 質問や相談内容を入力してください  
3. 「送信」ボタンを押すと、専門家からの回答が表示されます
""")

# ラジオボタンで専門家選択
expert_type = st.radio("専門家の種類を選んでください：", list(expert_roles.keys()))

# 入力フォーム
user_input = st.text_area("質問・相談内容を入力してください：", height=150)

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("専門家が回答中です..."):
            response = get_llm_response(user_input, expert_type)
            st.success("専門家からの回答：")
            st.write(response)