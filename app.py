import os
import tempfile
import streamlit as st
import yt_dlp

# 页面配置
st.set_page_config(page_title="B站视频转MP3", page_icon="🎵")
st.title("🎧 B站视频 → MP3 转换器")
st.markdown("粘贴哔哩哔哩视频链接，自动提取音频并转为 MP3 下载")

# 输入框
link = st.text_input("请输入B站视频链接", placeholder="https://www.bilibili.com/video/BV...")

# 按下按钮时处理
if st.button("开始转换") and link:
    try:
        # 创建临时文件夹（用完自动删除）
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'format': 'bestaudio/best',                     # 下载最优音频
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',               # 用FFmpeg提取音频
                    'preferredcodec': 'mp3',                   # 转成mp3格式
                    'preferredquality': '192',                 # 音质192kbps
                }],
                'quiet': True,
                'no_warnings': True,
            }

            with st.spinner("正在下载并转换音频，请稍候..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    # 获取转换前文件名，推算最终的 mp3 文件路径
                    file_name = ydl.prepare_filename(info)
                    mp3_path = file_name.rsplit('.', 1)[0] + '.mp3'

            # 将转换好的 mp3 提供给用户下载
            with open(mp3_path, 'rb') as f:
                st.download_button(
                    label="📥 下载 MP3",
                    data=f,
                    file_name=os.path.basename(mp3_path),
                    mime="audio/mpeg"
                )
            st.success("转换完成！点击上方按钮下载。")
    except Exception as e:
        st.error(f"转换失败，请检查链接是否正确或稍后重试。错误信息：{e}")
