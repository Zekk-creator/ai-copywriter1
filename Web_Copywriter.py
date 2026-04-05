import streamlit as st
from google import genai
import time

# 1. 设置页面全局属性 (宽屏展示更大气)
st.set_page_config(page_title="AI 小红书爆款文案引擎 | Pro版", page_icon="🔥", layout="centered")

# 2. 核心包装术：隐藏 Streamlit 官方的水印和菜单
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. 侧边栏：商业化与高级配置
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/bot.png", width=60)
    st.title("文案引擎 Pro")
    st.markdown("---")
    
    with st.expander("⚙️ 开发者底层配置 (普通用户勿动)"):
        user_api_key = st.text_input("API Key 秘钥", type="password")
        base_url = st.text_input("接口调用地址", value="https://v2.aicodee.com")
    
    st.markdown("---")
    st.markdown("### 💼 商业合作")
    st.info("本系统支持私有化部署。如需购买源码或定制专属 AI 员工，请联系开发者。")
    st.success("微信: 请替换成你的微信号")

# 4. 主界面：注重用户体验 (UX)
st.title("✨ 小红书爆款文案生成系统")
st.markdown("输入产品基础信息，AI 将自动融合`痛点引流`、`情绪价值`与`促单话术`，10秒输出爆款种草文案。")

# 使用分栏让界面更专业
col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("🎁 产品名称 (必填)", placeholder="例如：极简风陶瓷水杯")
with col2:
    target_audience = st.text_input("🎯 目标人群 (选填)", placeholder="例如：打工人、学生党、宝妈")

selling_points = st.text_area("🔥 核心卖点 (必填)", placeholder="例如：哑光质感、保持恒温、极简主义美学、送礼首选", height=100)

# 生成按钮
if st.button("🚀 启动爆款引擎，一键生成", use_container_width=True):
    if not user_api_key:
        st.error("⚠️ 请先在左侧侧边栏【开发者底层配置】中输入 API Key！")
    elif not product_name or not selling_points:
        st.warning("请填写完整产品名称和核心卖点哦~")
    else:
        # 【修正点1】：换回你测试成功的 google-genai 客户端引擎
        client = genai.Client(
            api_key=user_api_key,
            http_options={'base_url': base_url}
        )
        
        progress_text = "AI 正在分析小红书底层流量逻辑..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()
        
        with st.spinner("✍️ 正在疯狂码字中..."):
            try:
                # 组合提示词
                prompt_content = f"""
                你是一个深谙小红书流量密码的百万粉带货博主。请根据以下信息写一篇爆款种草文案。
                【产品】：{product_name}
                【人群】：{target_audience}
                【卖点】：{selling_points}
                【要求】：痛点抓得准，情绪价值高，排版清爽，多用Emoji，并在文末附带4-6个热门标签。字数250字左右。
                """
                
                # 【修正点2】：使用你测试成功的模型名称
                response = client.models.generate_content(
                    model='MiniMax-M2.7-highspeed',
                    contents=prompt_content,
                )
                
                # 【修正点3】：换回正确的解析方式
                result = response.text
                
                st.balloons()
                st.success("🎉 生成成功！请复制下方文案：")
                st.info(result)
                
            except Exception as e:
                st.error(f"抱歉，系统开小差了：{e}")
