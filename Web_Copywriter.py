import streamlit as st
from openai import OpenAI
import time

# ==========================================
# 1. 核心配置与安全校验
# ==========================================
try:
    API_KEY = st.secrets["API_KEY"]
    BASE_URL = st.secrets["BASE_URL"]
except:
    st.error("❌ 致命错误：未检测到后台 Secrets 配置！请在 Streamlit 后台设置 API_KEY 和 BASE_URL。")
    st.stop()

# ==========================================
# 2. 页面全局样式与 H5 适配优化
# ==========================================
st.set_page_config(page_title="AI 文案魔法盒", page_icon="✨", layout="centered")

# 隐藏官方痕迹，美化按钮（特别是手机端点击体验）
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* 提升按钮的质感和点击区域 */
            .stButton>button {
                border-radius: 12px;
                height: 55px;
                font-size: 16px !important;
                font-weight: 600;
                transition: all 0.3s ease;
                border: 1px solid #e0e0e0;
            }
            .stButton>button:active {
                transform: scale(0.98);
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 初始化页面路由状态
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# ==========================================
# 3. 核心 AI 驱动引擎
# ==========================================
def generate_ai_content(system_prompt, user_prompt):
    """统一的 AI 调用接口，带加载动画和错误处理"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    # 制造“AI思考中”的视觉停顿感，提升产品价值感
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
    st.title("✨ AI 文案魔法盒")
    st.markdown("👇 **请选择您需要的创作场景：**")
    st.write("") # 留白
    
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

# ----------------- 功能 1：小红书爆款 -----------------
elif st.session_state.current_page == 'xhs':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("📕 小红书爆款生成器")
    st.caption("一次生成 3 种爆款风格，总有一款戳中粉丝！")
    
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("🎁 产品名称*", placeholder="例：极简风陶瓷水杯")
    with col2:
        product_price = st.text_input("💰 价格*", placeholder="例：¥29.9")
        
    selling_points = st.text_area("🔥 核心卖点*", placeholder="例：哑光质感、保持恒温、送礼首选", height=100)
    
    if st.button("🚀 一键生成 3 种风格", type="primary", use_container_width=True):
        if not product_name or not selling_points:
            st.warning("⚠️ 请至少填写【产品名称】和【核心卖点】哦！")
        else:
            sys_prompt = "你是一个精通小红书算法的带货专家。文案要带大量Emoji，排版清爽，情绪拉满。"
            usr_prompt = f"""
            产品：{product_name}
            价格：{product_price}
            卖点：{selling_points}
            任务：写3篇风格不同（闺蜜分享风、专业评测风、急迫情绪风）的种草文案。
            要求：必须在文中提及名字和价格，每篇约200字，附带热门标签。
            【极其重要】：请严格使用“---”来分隔这3篇文案。
            """
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.balloons()
                versions = result.split('---')
                tab1, tab2, tab3 = st.tabs(["💅 闺蜜分享", "🔬 专业评测", "🔥 情绪种草"])
                with tab1: st.success(versions[0].strip() if len(versions) > 0 else "未生成")
                with tab2: st.success(versions[1].strip() if len(versions) > 1 else "未生成")
                with tab3: st.success(versions[2].strip() if len(versions) > 2 else "未生成")

# ----------------- 功能 2：短视频脚本 -----------------
elif st.session_state.current_page == 'video':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("🎬 黄金3秒短视频脚本")
    st.caption("自动拆解画面与台词，让完播率飙升！")
    
    video_topic = st.text_input("📌 视频主题*", placeholder="例：普通人如何用 AI 搞钱")
    video_duration = st.selectbox("⏱️ 预估时长", ["30秒以内 (快节奏口播)", "1分钟左右 (干货分享)", "3分钟以上 (深度剧情/解析)"])
    
    if st.button("🚀 生成分镜头脚本", type="primary", use_container_width=True):
        if not video_topic:
            st.warning("⚠️ 请输入视频主题！")
        else:
            sys_prompt = "你是抖音/快手百万粉操盘手，精通短视频完播率、互动率算法。"
            usr_prompt = f"主题：{video_topic}\n时长：{video_duration}\n要求：采用表格形式（或清晰的分段）输出分镜头脚本，必须包含【黄金三秒开头】、【画面提示】、【口播台词】、【引导点赞收藏结尾】。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.success("🎉 生成成功！")
                st.info(result)

# ----------------- 功能 3：朋友圈嘴替 -----------------
elif st.session_state.current_page == 'moments':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("😎 朋友圈高情商嘴替")
    st.caption("不知道配什么文案？告诉 AI 帮你写。")
    
    photo_content = st.text_input("🖼️ 照片/视频拍了啥？*", placeholder="例：一杯咖啡和一台电脑在加班")
    mood = st.selectbox("🎭 想表达什么情绪/人设？", ["文艺小清新", "沙雕搞笑风", "职场高情商", "深夜走心Emo"])
    
    if st.button("🚀 帮我发圈", type="primary", use_container_width=True):
        if not photo_content:
            st.warning("⚠️ 描述一下照片内容吧！")
        else:
            sys_prompt = "你是一个深谙社交网络心理学的高情商冲浪高手。"
            usr_prompt = f"照片：{photo_content}\n情绪：{mood}\n任务：给我 3 句简短、惊艳、极具网感的文案。不要长篇大论，要像真人随手发的。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.success("🎉 生成成功，赶紧复制去发圈吧！")
                st.info(result)

# ----------------- 功能 4：闲鱼神文案 -----------------
elif st.session_state.current_page == 'xianyu':
    if st.button("⬅️ 返回首页"):
        st.session_state.current_page = 'home'; st.rerun()
        
    st.header("💼 闲鱼秒出神仙话术")
    st.caption("真实自然打消疑虑，加快二手转卖速度。")
    
    item_name = st.text_input("📦 物品名称*", placeholder="例：九成新 Switch 游戏机")
    reason = st.text_input("😭 出手原因", placeholder="例：吃灰太久了，回点血")
    
    if st.button("🚀 生成高转化话术", type="primary", use_container_width=True):
        if not item_name:
            st.warning("⚠️ 至少告诉我你要卖什么吧！")
        else:
            sys_prompt = "你是闲鱼上卖二手货的顶级大神，文案真实、诚恳，能迅速打消买家疑虑。"
            usr_prompt = f"物品：{item_name}\n原因：{reason}\n要求：帮我写一段闲鱼转卖文案。突出成色好、价格亏本，语气真实自然。最后加上常用的免责声明（如：二手物品售出不退换、屠龙刀勿扰）。"
            result = generate_ai_content(sys_prompt, usr_prompt)
            if result:
                st.success("🎉 话术已备好，祝你早日出单！")
                st.info(result)
