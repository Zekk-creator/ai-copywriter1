import streamlit as st
from openai import OpenAI
import time
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. 核心配置与安全校验
# ==========================================
try:
    API_KEY = st.secrets["API_KEY"]
    BASE_URL = st.secrets["BASE_URL"]
except:
    st.error("❌ 未检测到后台 Secrets 配置！")
    st.stop()

# ==========================================
# 2. 动效加载工具与页面配置
# ==========================================
st.set_page_config(page_title="AI 文案魔法盒1", page_icon="✨", layout="centered")

# 定义一个加载动画的函数
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp {background-color: #fcfcfc;}
            button[kind="primary"] {
                background: linear-gradient(135deg, #ff4b4b 0%, #ff8f00 100%) !important;
                color: white !important;
                border-radius: 12px !important;
                height: 55px !important;
                font-weight: bold !important;
                box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
            }
            button[kind="secondary"] {
                border-radius: 12px !important;
                border: 1px solid #eaeaea !important;
                height: 60px !important;
                font-weight: 600 !important;
                background-color: white !important;
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
    
    my_bar = st.progress(0, text="✨ AI 灵感引擎正在启动...")
    for p in range(100):
        time.sleep(0.01)
        my_bar.progress(p + 1)
    my_bar.empty()
    
    with st.spinner("✍️ 正在为您疯狂码字中，请稍候..."):
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
            st.error(f"⚠️ 糟糕，AI 开小差了，请重试。（错误代码：{e}）")
            return None

# ==========================================
# 4. 前端界面与功能矩阵
# ==========================================

# ----------------- 首页：功能大厅 -----------------
if st.session_state.current_page == 'home':
    # 【新增】：在标题旁边加上动态插画
    col_title, col_lottie = st.columns([2, 1])
    with col_title:
        st.title("✨ AI 文案魔法盒")
        st.markdown("👇 **请选择您需要的创作场景：**")
    with col_lottie:
        # 这里是一段免费开源的 AI 机器人动画 JSON 链接
        lottie_ai = load_lottieurl("https://lottie.host/8b7d91e0-63eb-4601-bd38-1a06df4ce15e/WWeZlT43gZ.json")
        if lottie_ai:
            st_lottie(lottie_ai, height=120, key="home_anim")
    
    st.write("") 
    
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
    st.caption("💡 商业版定制请联系微信：YourWechatHere")

# ----------------- 后续功能页逻辑保持不变 -----------------
# ----------------- 功能 1：小红书爆款 -----------------
elif st.session_state.current_page == 'xhs':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
    st.header("📕 小红书爆款生成器")
    col1, col2 = st.columns(2)
    with col1: product_name = st.text_input("🎁 产品名称*")
    with col2: product_price = st.text_input("💰 价格*")
    selling_points = st.text_area("🔥 核心卖点*", height=100)
    if st.button("🚀 一键生成 3 种风格", type="primary", use_container_width=True):
        if not product_name or not selling_points:
            st.warning("⚠️ 请填写必填项哦！")
        else:
            res = generate_ai_content("你是小红书专家", f"产品：{product_name}\n价格：{product_price}\n卖点：{selling_points}\n任务：写3篇风格不同（闺蜜、评测、情绪）的文案，用“---”分隔。")
            if res:
                versions = res.split('---')
                tab1, tab2, tab3 = st.tabs(["💅 闺蜜分享", "🔬 专业评测", "🔥 情绪种草"])
                with tab1: st.success(versions[0] if len(versions)>0 else "未生成")
                with tab2: st.success(versions[1] if len(versions)>1 else "未生成")
                with tab3: st.success(versions[2] if len(versions)>2 else "未生成")

# ----------------- 功能 2：短视频脚本 -----------------
elif st.session_state.current_page == 'video':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("🎬 黄金3秒短视频脚本")
    st.caption("自动拆解画面与台词，让完播率飙升！")
    
    video_topic = st.text_input("📌 视频主题*", placeholder="例：普通人如何用 AI 搞钱")
    video_duration = st.selectbox("⏱️ 预估时长", ["30秒以内 (快节奏口播)", "1分钟左右 (干货分享)", "3分钟以上 (深度剧情)"])
    
    if st.button("🚀 生成分镜头脚本", type="primary", use_container_width=True):
        if not video_topic:
            st.warning("⚠️ 请输入视频主题！")
        else:
            sys_prompt = "你是抖音百万粉操盘手，精通短视频完播率算法。"
            usr_prompt = f"主题：{video_topic}\n时长：{video_duration}\n要求：采用清晰的分段输出脚本，包含【黄金三秒开头】、【画面提示】、【口播台词】、【引导点赞结尾】。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.success("🎉 生成成功！"); st.info(result)

# ----------------- 功能 3：朋友圈嘴替 -----------------
elif st.session_state.current_page == 'moments':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("😎 朋友圈高情商嘴替")
    st.caption("不知道配什么文案？告诉 AI 帮你写。")
    
    photo_content = st.text_input("🖼️ 照片拍了啥？*", placeholder="例：一杯咖啡和电脑在加班")
    mood = st.selectbox("🎭 想表达什么情绪？", ["文艺小清新", "沙雕搞笑风", "职场高情商", "深夜Emo"])
    
    if st.button("🚀 帮我发圈", type="primary", use_container_width=True):
        if not photo_content:
            st.warning("⚠️ 描述一下照片内容吧！")
        else:
            sys_prompt = "你是一个深谙社交网络心理学的高情商冲浪高手。"
            usr_prompt = f"照片：{photo_content}\n情绪：{mood}\n任务：给我 3 句简短、惊艳、极具网感的文案。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.success("🎉 生成成功！"); st.info(result)

# ----------------- 功能 4：闲鱼神文案 -----------------
elif st.session_state.current_page == 'xianyu':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("💼 闲鱼秒出神仙话术")
    st.caption("真实自然打消疑虑，加快转卖速度。")
    
    item_name = st.text_input("📦 物品名称*", placeholder="例：九成新 Switch")
    reason = st.text_input("😭 出手原因", placeholder="例：吃灰太久了，回血")
    
    if st.button("🚀 生成高转化话术", type="primary", use_container_width=True):
        if not item_name:
            st.warning("⚠️ 至少告诉我你要卖什么吧！")
        else:
            sys_prompt = "你是闲鱼二手转卖大神，文案真实诚恳。"
            usr_prompt = f"物品：{item_name}\n原因：{reason}\n要求：写一段闲鱼转卖文案。突出成色好、价格亏本，语气真实自然，带免责声明。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.success("🎉 话术已备好！"); st.info(result)
