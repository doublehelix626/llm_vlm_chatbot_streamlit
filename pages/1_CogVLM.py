import json
import requests
import streamlit as st
from streamlit_chat import message
import config
import utils
from pathlib import Path
import openai_api_request_vlm
from PIL import Image
import base64
from io import BytesIO
import re
import cv2
import numpy as np
import uuid

st.set_page_config(
    page_title="cogVLMbot",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"  # 左侧参数框时刻打开
)
# 对于状态值的一个逻辑是如果没有值则初始化一个空值，如果有值则使用当前值，需要写

# ss_list = ["st.session_state.source_img", "st.session_state.task_img",
#            "st.session_state.img_url", "st.session_state.base64_data"]
# for ss in ss_list:
#     if ss not in st.session_state:
#         st.session_state[ss] = ""
if "vlm_history" not in st.session_state:
    st.session_state.vlm_history = [{"role": "assistant",
                                     "content": "你好~,我是cogvlm！！！"}]
if "control_history" not in st.session_state:
    st.session_state.control_history = [{"role": "assistant",
                                         "content": "ptz小能手上线了！！！"}]
if "llm_history" not in st.session_state:
    st.session_state.llm_history = [{"role": "assistant",
                                     "content": "你好~,我是chatglm3！！！"}]
if "source_img" not in st.session_state:
    st.session_state.source_img = ""
if "task_img" not in st.session_state:
    st.session_state.task_img = ""
if "base64_data" not in st.session_state:
    st.session_state.base64_data = ""
if "img_url" not in st.session_state:
    st.session_state.img_url = ""
if "vlm_openai_messages" not in st.session_state:
    st.session_state.vlm_openai_messages = []
if "llm_openai_messages" not in st.session_state:
    st.session_state.llm_openai_messages = []
if "control_message" not in st.session_state:
    st.session_state.control_openai_message = []
if "prompt_flag" not in st.session_state:
    st.session_state.prompt_flag = False
if "input_task" not in st.session_state:
    st.session_state.input_task = ""
if "save_path" not in st.session_state:
    st.session_state.save_path = f"./cache/{st.session_state.input_task}.jpg"
st.title(" CogVLM")
# sidebar
st.sidebar.header("模型参数")

# model options
st.session_state.vlm_stream = st.sidebar.selectbox(
    "响应模式",
    ["非流式响应", "流式响应"]
)
if st.session_state.vlm_stream == "非流式响应":
    use_stream = False
else:
    use_stream = True
st.session_state.vlm_top_p = float(st.sidebar.slider(
    "top_p", 0.00, 1.00, 0.80))
st.session_state.vlm_temperature = float(st.sidebar.slider(
    "temperature", 0.01, 1.00, 0.90))
st.session_state.vlm_max_tokens = int(st.sidebar.slider(
    "Output length", 1, 2048, 2048))

with st.sidebar:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        if st.button("清除历史"):
            st.session_state.vlm_history = [{"role": "assistant",
                                             "content": "你好~,我是cogvlm！！！"}]
            st.session_state.vlm_openai_messages = []
            st.session_state.source_img = ""
            st.session_state.task_img = ""
    button_retry = col2.button("重试")
    if button_retry:
        pass
# image/video options
st.sidebar.header("图像选择")
source_selectbox = st.sidebar.selectbox(
    "Select Source",
    config.SOURCES_LIST
)

if source_selectbox == config.SOURCES_LIST[0]:  # Image
    st.session_state.source_img = st.sidebar.file_uploader(
        label="Choose an image...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    st.session_state.task_img = st.session_state.source_img
    # print(st.session_state.task_img)
    # print(type(st.session_state.task_img))
    # if st.session_state.task_img is not None:
    #     print(st.session_state.task_img.getvalue())
elif source_selectbox == config.SOURCES_LIST[1]:  # Video
    pass
elif source_selectbox == config.SOURCES_LIST[2]:  # Webcam
    pass
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")
st.sidebar.header("对齐与提示语")
st.session_state.prompt_flag = st.sidebar.checkbox("Grounding")
st.session_state.prompt = st.sidebar.selectbox(
    "可供选择的提示语",
    config.PROMPT_LIST
)
with (st.container(height=700, border=None)):
    col3, col4 = st.columns([1, 1.35])
    with col3.container(height=620):
        if st.session_state.source_img is not None:
            bytes_data = st.session_state.source_img.getvalue()
            st.session_state.base64_data = base64.b64encode(bytes_data).decode("utf-8")
            st.session_state.img_url = f"data:image/jpeg;base64,{st.session_state.base64_data}"
            st.image(image=st.session_state.source_img, width=444)
            st.image(image=st.session_state.task_img, width=444)
    with col4.container(height=560):
        st.markdown("历史记录")

        for message in st.session_state.vlm_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
                    if st.session_state.source_img != "":
                        st.image(image=st.session_state.source_img)
            if message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
                    if st.session_state.source_img != "" and message[
                        "content"] != "你好~,我是cogvlm！！！":
                        st.image(image=st.session_state.save_path)

        # user_input接收用户的输入
        if user_input := col4.chat_input("Chat with cogVLM: "):  # 注意只要是col4，就不会受到col4中其他container的影响(乱序插入)
            # 在历史记录上显示用户的输入内容
            with st.chat_message("user"):  # 是那个对话的头像元素
                if st.session_state.prompt_flag:
                    if (st.session_state.prompt == config.PROMPT_LIST[0]) or (
                            st.session_state.prompt == config.PROMPT_LIST[1]) or (
                            st.session_state.prompt == config.PROMPT_LIST[2]):
                        input_content = st.session_state.prompt.replace("<TASK>", user_input)
                        st.session_state.input_task = user_input
                        st.markdown(input_content)
                        st.image(image=st.session_state.source_img)
                    else:
                        input_content = st.session_state.prompt
                        st.markdown(input_content)
                        st.image(image=st.session_state.source_img)
                else:
                    input_content = user_input
                    st.markdown(input_content)
                    st.image(image=st.session_state.source_img)
            st.session_state.vlm_history.append({"role": "user", "content": input_content})
            st.session_state.vlm_openai_messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": input_content,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": st.session_state.img_url
                        },
                    },
                ],
            })
        if (st.session_state.vlm_history[-1]["role"] == "user") and (st.session_state.img_url != ""):
            with st.chat_message("assistant"):  # 这是一个container元素，所以加入历史记录不能放在这个with里
                # print(st.session_state.vlm_temperature)
                # print(st.session_state.vlm_max_tokens)
                # print(st.session_state.vlm_top_p)
                response = openai_api_request_vlm.create_chat_completion("cogvlm-chat-17b",
                                                                         messages=st.session_state.vlm_openai_messages,
                                                                         temperature=st.session_state.vlm_temperature,
                                                                         max_tokens=st.session_state.vlm_max_tokens,
                                                                         top_p=st.session_state.vlm_top_p,
                                                                         use_stream=use_stream)
                # print(response)
                st.markdown(response)
                if st.session_state.prompt_flag:
                    if st.session_state.input_task:
                        coordinate_dict = utils.draw_coordinate_object(st.session_state.input_task, response)
                        print(coordinate_dict)
                        print(type(coordinate_dict))
                        img = utils.draw_bbox(st.session_state.source_img.getvalue(),
                                              coordinate_dict)
                        print("完成！！！")
                        # print(type(st.session_state.task_img))
                        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
                        st.session_state.save_path = f"./cache/{st.session_state.input_task}.jpg"  # 将这个路径替换为你想要保存图像的实际路径
                        cv2.imwrite(st.session_state.save_path, img)
                        st.image(image=st.session_state.save_path)
                        # st.session_state.input_task = ""
                    else:
                        unique_id = uuid.uuid4()
                        # st.session_state.input_task = unique_id
                        coordinate_dict = utils.draw_coordinate_all_object(response)
                        img = utils.draw_bbox(st.session_state.source_img.getvalue(), coordinate_dict)
                        # st.image(image=st.session_state.task_img)
                        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
                        st.session_state.save_path = f"./cache/{unique_id}.jpg"  # 将这个路径替换为你想要保存图像的实际路径
                        cv2.imwrite(st.session_state.save_path, img)
                        st.image(image=st.session_state.save_path)
                        # st.session_state.input_task = ""
                else:
                    st.image(image=st.session_state.task_img)
            st.session_state.vlm_history.append({"role": "assistant", "content": response})
            st.session_state.vlm_openai_messages.append({"role": "assistant", "content": response})
