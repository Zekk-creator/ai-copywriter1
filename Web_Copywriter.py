import streamlit as st
from openai import OpenAI
import time

# 1. 页面配置
st.set_page_config(page_title="AI 小红书爆款文案引擎 | Pro版", page_icon="🔥", layout="centered")

# 隐藏水印
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# 2. 侧边栏
with st.sidebar:
    st.title("文案引擎 Pro")
    st.markdown("---")
    with st.expander("⚙️ 开发者配置"):
        user_api_key = st.text_input("API Key", type="password")
        base_url = st.text_input("接口地址", value="https://v2.aicodee.com/v1")
    st.markdown("---")
    st.info("💡 建议：输入详细的卖点，生成的文案会更动人。")
    st.success("微信联系: 你的微信号")

# 3. 主界面
st.title("✨ 小红书爆款文案生成系统")
st.markdown("一次生成 3 种风格，总有一款戳中用户！")

# 输入区域
col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("🎁 产品名称", placeholder="例如：极简风陶瓷水杯")
with col2:
    product_price = st.text_input("💰 售卖价格", placeholder="例如：¥29.9 / 史低价")

target_audience = st.text_input("🎯 目标人群", placeholder="例如：精致打工人、租房党")
selling_points = st.text_area("🔥 核心卖点", placeholder="例如：哑光质感、保持恒温、顺丰包邮", height=100)

# 4. 生成逻辑
if st.button("🚀 启动引擎，一键生成三个版本", use_container_width=True):
    if not user_api_key or not product_name:
        st.error("⚠️ 请确保 API Key 和产品名称已填写！")
    else:
        client = OpenAI(api_key=user_api_key, base_url=base_url)
        
        with st.spinner("AI 正在构思三个不同维度的爆款脚本..."):
            try:
                # 强化提示词：要求包含名称、价格，并输出三个版本
                prompt_content = f"""
                产品名称：{product_name}
                产品价格：{product_price}
                目标人群：{target_audience}
                核心卖点：{selling_points}

                【任务要求】：
                请针对以上信息，撰写 3 篇风格截然不同的小红书种草文案。
                1. 必须在每篇文案中都提到产品名称“{product_name}”和价格“{product_price}”。
                2. 版本1风格：纯分享风（闺蜜语气，真实感强）。
                3. 版本2风格：专业评测风（列数字、讲逻辑，显得很专业）。
                4. 版本3风格：急迫情绪风（痛点切入，不买就亏了的感觉）。
                5. 每篇文案约 200 字，包含大量 Emoji 和标签。
                
                重要：请在每篇文案之间使用“---”这个符号进行分隔，方便我进行排版。
                """
                
                response = client.chat.completions.create(
                    model="MiniMax-M2.7-highspeed",
                    messages=[
                        {"role": "system", "content": "你是一个精通小红书算法的带货专家。"},
                        {"role": "user", "content": prompt_content}
                    ]
                )
                
                full_text = response.choices[0].message.content
                
                # 按 --- 分割成三部分
                versions = full_text.split('---')
                
                st.balloons()
                st.success("🎉 生成完毕！请选择最心仪的版本：")
                
                # 使用 Tabs 标签页展示，显得非常专业
                tab1, tab2, tab3 = st.tabs(["版本一：闺蜜分享", "版本二：专业评测", "版本三：情绪种草"])
                
                with tab1:
                    st.info(versions[0] if len(versions) > 0 else "生成失败")
                with tab2:
                    st.info(versions[1] if len(versions) > 1 else "生成失败")
                with tab3:
                    st.info(versions[2] if len(versions) > 2 else "生成失败")
                    
            except Exception as e:
                st.error(f"出错啦：{e}")
