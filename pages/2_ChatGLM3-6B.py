import json
import requests
import streamlit
import streamlit as st
from streamlit_chat import message
from openai import OpenAI
import openai_api_request_glm
import base64
import cv2

st.set_page_config(
    page_title="ChatApp",
    page_icon=" ",
    layout="wide",
)
st.title(" ChatGLM3-6B")
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
# sidebar
st.sidebar.header("模型参数")

# model options
st.session_state.llm_stream = st.sidebar.selectbox(
    "响应模式",
    ["非流式响应", "流式响应"]
)
if st.session_state.llm_stream == "非流式响应":
    use_stream = False
else:
    use_stream = True
st.session_state.llm_top_p = float(st.sidebar.slider(
    "top_p", 0.00, 1.00, 0.80))
st.session_state.llm_temperature = float(st.sidebar.slider(
    "temperature", 0.01, 1.00, 0.80))
st.session_state.llm_max_tokens = int(st.sidebar.slider(
    "Output length", 1, 2048, 256))

with st.sidebar:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        if st.button("清除历史"):
            st.session_state.llm_history = [{"role": "assistant",
                                             "content": "你好~,我是chatglm3！！！"}]
            st.session_state.llm_openai_messages = []
            st.session_state.source_img = ""
            st.session_state.task_img = ""
    button_retry = col2.button("重试")
    if button_retry:
        pass

with (st.container(height=700, border=None)):
    col3, col4 = st.columns([1, 60])
    with col3.container(height=560):
        pass
        # if st.session_state.source_img is not None:
        #     # bytes_data = st.session_state.source_img.getvalue()
        #     # st.session_state.base64_data = base64.b64encode(bytes_data).decode("utf-8")
        #     # st.session_state.img_url = f"data:image/jpeg;base64,{st.session_state.base64_data}"
        #     st.image(image=st.session_state.source_img, width=444)
        #     st.image(image=st.session_state.task_img, width=444)
        # 拉取rtsp的流
        # rtsp_url = "rtsp://admin:zmh123456@192.168.1.64:554"
        # cap = cv2.VideoCapture(rtsp_url)
        # ret, frame = cap.read()
        # height, width, channels = frame.shape
        # canvas = st.empty()
        # while True:
        #     ret, frame = cap.read()
        #     if not ret:
        #         st.warning("Error reading frame from video stream.")
        #         break
        #     # Resize the frame to fit the Streamlit canvas
        #     resized_frame = cv2.resize(frame, (int(width / 2), int(height / 2)))
        #     # Display the resized frame on the Streamlit canvas
        #     ·canvas.image(resized_frame, channels="BGR")
        #     # Release the VideoCapture object and close the Streamlit app
        # cap.release()
    with col4.container(height=560):
        st.markdown("历史记录")

        for message in st.session_state.llm_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
                    # if st.session_state.source_img != "":
                    #     st.image(image=st.session_state.source_img)
            if message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
                    # if st.session_state.source_img != "" and message[
                    #     "content"] != "张明皓你这个臭傻逼，又来问我问题了是吧":
                    #     st.image(image=st.session_state.task_img)

        # user_input接收用户的输入
        if user_input := col4.chat_input("Chat with ChatGLM3-6B: "):  # 注意只要是col4，就不会受到col4中其他container的影响(乱序插入)
            # 在历史记录上显示用户的输入内容
            with st.chat_message("user"):  # 是那个对话的头像元素
                st.markdown(user_input)
                # st.image(image=st.session_state.source_img)
            st.session_state.llm_history.append({"role": "user", "content": user_input})
            st.session_state.llm_openai_messages.append({
                "role": "user",
                "content": user_input
            })
        if st.session_state.llm_history[-1]["role"] == "user":
            with st.chat_message("assistant"):  # 这是一个container元素，所以加入历史记录不能放在这个with里
                print(st.session_state.llm_temperature)
                print(st.session_state.llm_max_tokens)
                print(st.session_state.llm_top_p)
                response_raw = openai_api_request_glm.client.chat.completions.create(model="chatglm3-6b",
                                                                                     messages=st.session_state.llm_openai_messages,
                                                                                     stream=use_stream,
                                                                                     max_tokens=st.session_state.llm_max_tokens,
                                                                                     temperature=st.session_state.llm_temperature,
                                                                                     presence_penalty=1.1,
                                                                                     top_p=st.session_state.llm_top_p)
                response = response_raw.choices[0].message.content
                print(response_raw)
                st.markdown(response)
                # result = re.findall(r"\[\[(.*?)\]\]", response)
                # if result:
                #     img = base64.b64decode(st.session_state.base64_data)
                #     img_array = np.fromstring(img, np.uint8)
                #     print(type(result))
                #     for match in result:
                #         result_num = re.findall("\d+", match)
                #         if result_num:
                #             a = []
                #             for match_n in result_num:
                #                 match_int = int(match_n)
                #                 a.append(match_int)
                #             pt1 = (a[0], a[1])
                #             pt2 = (a[2], a[3])
                #
                #             img_array = cv2.rectangle(img_array, pt1, pt2, (0, 255, 0), 2)
                #     st.session_state.task_img = Image.fromarray(img_array)
                # st.image(image=st.session_state.task_img)
            st.session_state.llm_history.append({"role": "assistant", "content": response})
            st.session_state.llm_openai_messages.append({"role": "assistant", "content": response})
            # if len(st.session_state.history) > 20:
            #     st.session_state.messages = st.session_state.messages[-20:]
