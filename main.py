import streamlit as st
from utils import generate_script

st.title("🎬 视频脚本生成器")
with st.sidebar:
    deepseek_api_ke=st.text_input("请输入DeepSeek API密钥:",type="password")
    st.markdown("[获取DeepSeekAPI密钥](https://platform.deepseek.com/api-keys)")
subject=st.text_input("💡 请输入视频的主题")
video_length=st.number_input("⏱️ 请输入是视频的大致时长（单位:分钟）",min_value=0.1,step=0.1)
creativity=st.slider("✨ 请输入视频脚本的创造力", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
submit=st.button("生成脚本")
if submit and not deepseek_api_ke:
    st.info("请输入你的API密钥")
    st.stop()
if submit and not subject:
    st.info("请输入你的视频主题")
    st.stop()
if submit and not video_length >=0.1:
    st.info("视频时长要大于0.1分钟")
    st.stop()
if submit:
    with st.spinner(("AI正在思考中，请耐心等待...")):
        search_result,title,script=generate_script(subject,video_length,creativity,deepseek_api_ke)
    st.success("视频脚本已生成")
    st.subheader("🔥标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科的搜索结果👀"):
        st.info(search_result)