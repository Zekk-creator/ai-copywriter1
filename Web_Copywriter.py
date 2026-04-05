import streamlit as st
from openai import OpenAI
import time

# ==========================================
# 1. 页面全局配置与手机端适配
# ==========================================
st.set_page_config(page_title="AI 文案全能王", page_icon="✨", layout="centered")

# 隐藏 Streamlit 官方水印，提升商业感
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* 调整按钮样式使其在手机上更易点击 */
            .stButton>button {
                border-radius: 10px;
                height: 50px;
                font-weight: bold;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 初始化页面状态管理 (核心机制：控制用户在哪个页面)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# ==========================================
# 2. 侧边栏：全局配置
# ==========================================
with st.sidebar:
    st.title("⚙️ 引擎配置")
    user_api_key = st.text_input("API Key 秘钥", type="password")
    base_url = st.text_input("接口地址", value="https://v2.aicodee.com/v1")
    st.markdown("---")
    st.success("联系开发者定制：YourWechatHere")

# ==========================================
# 3. 核心大模型调用函数 (避免代码重复)
# ==========================================
def generate_ai_content(system_prompt, user_prompt):
    if not user_api_key:
        st.error("⚠️ 请先在左侧菜单配置 API Key！")
        return None
    
    client = OpenAI(api_key=user_api_key, base_url=base_url)
    
    # 模拟进度条，提升用户体验
    my_bar = st.progress(0, text="AI 正在高速运转中...")
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text="AI 正在高速运转中...")
    my_bar.empty()
    
    with st.spinner("✍️ 正在疯狂码字中..."):
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
            st.error(f"抱歉，系统开小差了：{e}")
            return None

# ==========================================
# 4. 页面路由与 UI 渲染
# ==========================================

# ----------------- 首页：九宫格导航 -----------------
if st.session_state.current_page == 'home':
    st.title("🚀 AI 文案魔法盒")
    st.markdown("请选择你需要使用的功能：")
    
    # 手机端友好的 2x2 网格布局
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📕 小红书种草", use_container_width=True):
            st.session_state.current_page = 'xhs'
            st.rerun()
        if st.button("😎 朋友圈嘴替", use_container_width=True):
            st.session_state.current_page = 'moments'
            st.rerun()
    with col2:
        if st.button("🎬 抖音脚本", use_container_width=True):
            st.session_state.current_page = 'video'
            st.rerun()
        if st.button("💼 闲鱼高转化", use_container_width=True):
            st.session_state.current_page = 'xianyu'
            st.rerun()

# ----------------- 功能页 1：小红书种草 -----------------
elif st.session_state.current_page == 'xhs':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.header("📕 小红书爆款生成器")
    product_name = st.text_input("🎁 产品名称", placeholder="例如：极简风陶瓷水杯")
    product_price = st.text_input("💰 售卖价格", placeholder="例如：¥29.9")
    selling_points = st.text_area("🔥 核心卖点", placeholder="例如：哑光质感、保持恒温", height=100)
    
    if st.button("🚀 一键生成 3 种风格", type="primary", use_container_width=True):
        if product_name and selling_points:
            sys_prompt = "你是一个精通小红书算法的带货专家。文案要带大量Emoji，排版清爽。"
            usr_prompt = f"""
            产品：{product_name}
            价格：{product_price}
            卖点：{selling_points}
            请写 3 篇风格不同（闺蜜分享风、专业评测风、急迫情绪风）的种草文案。
            必须在文案中提及名字和价格。每篇约200字。
            请严格使用“---”来分隔这 3 篇文案。
            """
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                versions = result.split('---')
                st.balloons()
                tab1, tab2, tab3 = st.tabs(["闺蜜分享", "专业评测", "情绪种草"])
                with tab1: st.info(versions[0] if len(versions) > 0 else "生成失败")
                with tab2: st.info(versions[1] if len(versions) > 1 else "生成失败")
                with tab3: st.info(versions[2] if len(versions) > 2 else "生成失败")
        else:
            st.warning("请填写完整信息！")

# ----------------- 功能页 2：抖音短视频脚本 -----------------
elif st.session_state.current_page == 'video':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.header("🎬 黄金3秒短视频脚本")
    video_topic = st.text_input("📌 视频主题", placeholder="例如：教你如何用AI赚钱")
    video_duration = st.selectbox("⏱️ 预估时长", ["30秒以内 (快节奏)", "1分钟左右 (干货局)", "3分钟以上 (深度解析)"])
    
    if st.button("🚀 生成分镜头脚本", type="primary", use_container_width=True):
        if video_topic:
            sys_prompt = "你是百万粉抖音操盘手，深谙短视频完播率和点赞转化逻辑。"
            usr_prompt = f"请为主题为“{video_topic}”的短视频写一份脚本，时长{video_duration}。要求包含：1. 黄金三秒开头（必须抓人眼球）；2. 画面提示；3. 口播台词；4. 引导互动的结尾。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result: st.success("🎉 生成成功！"); st.markdown(result)
        else:
            st.warning("请输入视频主题！")

# ----------------- 功能页 3：朋友圈嘴替 -----------------
elif st.session_state.current_page == 'moments':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.header("😎 朋友圈高情商文案")
    photo_content = st.text_input("🖼️ 照片内容是啥？", placeholder="例如：喝了一下午茶，风景很好")
    mood = st.selectbox("🎭 想表达什么情绪？", ["文艺小清新", "沙雕搞笑", "职场高情商", "深夜emo"])
    
    if st.button("🚀 帮我发圈", type="primary", use_container_width=True):
        if photo_content:
            sys_prompt = "你是一个深谙社交网络心理学的高情商冲浪高手。"
            usr_prompt = f"照片内容是：{photo_content}。需要体现的情绪是：{mood}。请给我 3 句简短、惊艳、适合发朋友圈的文案，不要太长，要像真人发的。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result: st.success("🎉 生成成功！"); st.info(result)
        else:
            st.warning("请描述一下照片内容！")

# ----------------- 功能页 4：闲鱼高转化文案 -----------------
elif st.session_state.current_page == 'xianyu':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.header("💼 闲鱼秒出神仙话术")
    item_name = st.text_input("📦 物品名称", placeholder="例如：九成新 Switch 游戏机")
    reason = st.text_input("😭 出手原因 (越惨越好卖)", placeholder="例如：老婆不让玩了，含泪出")
    
    if st.button("🚀 生成神仙话术", type="primary", use_container_width=True):
        if item_name:
            sys_prompt = "你是闲鱼上卖二手货的顶级大神，文案真实、诚恳，能迅速打消买家疑虑。"
            usr_prompt = f"我要卖：{item_name}。出手原因：{reason}。请帮我写一段闲鱼转卖文案。要求：突出成色好、价格亏本，语气真实自然，带一点个人情绪，最后写明“屠龙刀勿扰，爽快包邮”。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result: st.success("🎉 生成成功！快去复制闲鱼吧！"); st.info(result)
        else:
            st.warning("请输入物品名称！")
