import os
import tempfile
import streamlit as st
import yt_dlp
from pydub import AudioSegment

st.set_page_config(page_title="B站视频转MP3", page_icon="🎵")

st.title("🎵 B站视频 → MP3 转换器")
st.markdown("粘贴哔哩哔哩视频链接，自动提取音频并转为MP3下载")

# 输入框
url = st.text_input("请输入B站视频链接", placeholder="https://www.bilibili.com/video/BV1xx411c7mD")

if st.button("开始转换") and url:
    with st.spinner("正在处理，请稍候..."):
        try:
            # 创建临时目录
            with tempfile.TemporaryDirectory() as tmpdir:
                # 下载音频
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(tmpdir, 'audio.%(ext)s'),
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 查找生成的MP3文件
                mp3_files = [f for f in os.listdir(tmpdir) if f.endswith('.mp3')]
                if mp3_files:
                    mp3_path = os.path.join(tmpdir, mp3_files[0])
                    # 读取文件供下载
                    with open(mp3_path, 'rb') as f:
                        audio_data = f.read()
                    st.success("✅ 转换成功！点击下方按钮下载")
                    st.download_button(
                        label="📥 下载MP3",
                        data=audio_data,
                        file_name=mp3_files[0],
                        mime="audio/mpeg"
                    )
                else:
                    st.error("未找到生成的MP3文件")
        except Exception as e:
            st.error(f"转换失败，请检查链接是否正确或稍后重试。错误信息：{e}")
