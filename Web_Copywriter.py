import streamlit as st
import pandas as pd
import time
import io
from openai import OpenAI

# ==========================================
# 🎨 页面全局配置 (让网页看起来更高大上)
# ==========================================
st.set_page_config(page_title="爆款文案生成引擎", page_icon="🔥", layout="wide")

# ==========================================
# ⚙️ 左侧边栏：配置中心
# ==========================================
with st.sidebar:
    st.header("⚙️ 引擎配置中心")
    st.markdown("请填写你的接口信息")
    
    # 密码框设计，防止别人偷看你的 Key
    api_key = st.text_input("🔑 API Key", type="password", help="sk-676c72b728b1e40ec0ecec48a6b77203")
    base_url = st.text_input("🌐 接口地址", value="https://v2.aicodee.com/v1")
    model_name = st.text_input("🤖 模型名称", value="MiniMax-M2.7-highspeed")
    
    st.markdown("---")
    st.markdown("💡 **操作指南**：\n1. 在左侧配好秘钥。\n2. 在右侧上传包含 `产品名称` 和 `核心卖点` 的表格。\n3. 点击开始生成！")

# ==========================================
# 🧠 AI 核心生成逻辑
# ==========================================
def generate_copy(client, product_name, selling_points):
    prompt = f"""
    你是一个深谙小红书流量密码的百万粉带货博主。请根据以下信息，写一篇爆款种草文案。
    
    【产品名称】：{product_name}
    【核心卖点】：{selling_points}
    
    【写作要求】：
    1. 标题：吸引眼球，使用痛点/猎奇/干货/数字等爆款标题结构，加Emoji。
    2. 引入：直接切入目标人群痛点，引发共鸣。
    3. 正文：将干瘪的【核心卖点】转化为生动的【情绪价值】和【使用场景】。
    4. 结尾：加入强烈的购买号召。
    5. 格式：多用空行，视觉清爽，大量使用小红书风格的 Emoji 符号。
    6. 标签：在文末生成 4-6 个相关的热门话题标签。
    
    字数控制在 250 字左右。
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个专业的小红书营销文案专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {e}"

# ==========================================
# 🖥️ 主界面 UI 设计
# ==========================================
st.title("🔥 小红书/短视频爆款文案批量生成器")
st.markdown("告别手动码字！上传商品表格，AI 自动为你批量产出带情绪价值的高转化文案。")

# 1. 文件上传组件
uploaded_file = st.file_uploader("📂 请在此拖入或选择您的 Excel 数据表 (.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 2. 读取并预览数据
    df = pd.read_excel(uploaded_file)
    st.write("👀 **数据预览：**")
    st.dataframe(df.head(), use_container_width=True)

    # 3. 数据格式校验
    if "产品名称" not in df.columns or "核心卖点" not in df.columns:
        st.error("❌ 格式错误：您的表格中缺少 `产品名称` 或 `核心卖点` 列，请修改后重新上传！")
    else:
        # 4. 生成按钮
        if st.button("🚀 启动自动化生成", type="primary", use_container_width=True):
            if not api_key:
                st.warning("⚠️ 滴滴滴！产品经理，你忘记在左侧输入 API Key 啦！")
            else:
                # 初始化大模型客户端
                client = OpenAI(api_key=api_key, base_url=base_url)
                
                # 设置进度条和状态提示
                progress_bar = st.progress(0)
                status_text = st.empty()
                generated_copies = []
                
                total_items = len(df)
                
                # 开始循环处理
                for i, row in df.iterrows():
                    product = row['产品名称']
                    features = row['核心卖点']
                    
                    # 更新状态文本
                    status_text.info(f"⏳ 正在为【{product}】施展爆款魔法... ({i+1}/{total_items})")
                    
                    # 调用 AI
                    copy = generate_copy(client, product, features)
                    generated_copies.append(copy)
                    
                    # 更新进度条
                    progress_bar.progress((i + 1) / total_items)
                    time.sleep(1) # 稍微停顿，防止并发过高被封 IP
                    
                # 处理完成，将结果写回表格
                df['爆款文案生成结果'] = generated_copies
                status_text.success("🎉 大功告成！所有爆款文案已生成完毕，请点击下方按钮下载！")
                
                # 5. 生成 Excel 内存文件供下载
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                processed_data = output.getvalue()
                
                st.download_button(
                    label="📥 立即下载结果表格 (Excel)",
                    data=processed_data,
                    file_name="产品文案批量生成结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )