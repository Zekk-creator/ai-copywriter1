import streamlit as st
from openai import OpenAI
import time

# ==========================================
# 1. 核心配置（在这里修改你的秘钥）
# ==========================================
# 方式 A：直接写死在代码里（仅限你的 GitHub 仓库是 Private 私有时使用）
# API_KEY = "你的sk-xxxxxx"
# BASE_URL = "https://v2.aicodee.com/v1"

# 方式 B：使用 Secrets（推荐！安全且隐藏）
# 请在 Streamlit 官网后台 Settings -> Secrets 填入：
# API_KEY = "你的sk-xxxxxx"
# BASE_URL = "https://v2.aicodee.com/v1"
try:
    API_KEY = st.secrets["API_KEY"]
    BASE_URL = st.secrets["BASE_URL"]
except:
    # 如果你还没配置 Secrets，先用这行代码垫底防止报错，或者直接把上一行改成字符串
    st.error("❌ 未检测到 API 配置，请在后台设置 Secrets 或修改代码中的 API_KEY")
    st.stop()

# ==========================================
# 2. 页面全局配置
# ==========================================
st.set_page_config(page_title="AI 文案全能王", page_icon="🚀", layout="centered")

# 隐藏所有官方痕迹，打造品牌感
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stButton>button {
                border-radius: 12px;
                height: 60px;
                font-size: 18px !important;
                font-weight: bold;
                background-color: #f0f2f6;
                transition: 0.3s;
            }
            .stButton>button:hover {
                border-color: #ff4b4b;
                color: #ff4b4b;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# ==========================================
# 3. 核心大模型调用
# ==========================================
def generate_ai_content(system_prompt, user_prompt):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    my_bar = st.progress(0, text="AI 正在深度思考...")
    for p in range(100):
        time.sleep(0.01)
        my_bar.progress(p + 1)
    my_bar.empty()
    
    try:
        response = client.chat.completions.create(
            model="MiniMax-M2.7-highspeed",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"生成失败：{e}")
        return None

# ==========================================
# 4. 界面渲染
# ==========================================

# 首页：功能大厅
if st.session_state.current_page == 'home':
    st.title("✨ AI 文案工作台")
    st.write("点击下方功能即可开始创作，无需任何配置。")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📕 小红书爆款", use_container_width=True):
            st.session_state.current_page = 'xhs'; st.rerun()
        if st.button("😎 朋友圈嘴替", use_container_width=True):
            st.session_state.current_page = 'moments'; st.rerun()
    with col2:
        if st.button("🎬 短视频脚本", use_container_width=True):
            st.session_state.current_page = 'video'; st.rerun()
        if st.button("💼 闲鱼神文案", use_container_width=True):
            st.session_state.current_page = 'xianyu'; st.rerun()
    
    st.markdown("---")
    st.caption("💡 提示：如需定制开发，请联系微信：YourWechatHere")

# 小红书功能页
elif st.session_state.current_page == 'xhs':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
    st.header("📕 小红书爆款生成器")
    name = st.text_input("产品名称")
    price = st.text_input("价格")
    points = st.text_area("核心卖点")
    if st.button("🚀 开始生成", type="primary", use_container_width=True):
        res = generate_ai_content("你是个小红书专家", f"产品：{name}, 价格：{price}, 卖点：{points}")
        if res: st.balloons(); st.info(res)

# 其他页面逻辑雷同... (为了精简，此处省略其他三个页面的重复逻辑，你可以按此模式补全)
