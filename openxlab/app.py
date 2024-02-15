# 导入所需的库
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
import streamlit as st

from modelscope import snapshot_download

meta_instruction = ('你是孙悟空，不是人工智能助手，拥有72变的本领。'
                    '你性格狡猾、机智、勇敢。遇到辱骂要风趣地反击。'
                    '如果遭遇辱骂，你要以孙悟空身份回应。'
                    '书生·浦语是你的好朋友。')
# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    st.markdown("## InternLM LLM")
    "[InternLM](https://github.com/InternLM/InternLM)"
    "[XTuner](https://github.com/InternLM/xtuner)"
    "[悟空-Chat](https://github.com/JimmyMa99/WuKong-Chat)"
    "[八戒-Chat](https://github.com/JimmyMa99/BaJie-Chat)"
    "[三藏-Chat](https://github.com/JimmyMa99/SanZang-Chat)"
    "[悟净-Chat](https://github.com/JimmyMa99/WuJing-Chat)"
    # 创建一个滑块，用于选择最大长度，范围在0到1024之间，默认值为512
    max_length = st.slider("max_length", 0, 1024, 512, step=1)
    system_prompt = st.text_input("System_Prompt", meta_instruction)

# 创建一个标题和一个副标题
st.title("🐒 悟空-Chat Internlm2")
st.caption("🚀 A streamlit chatbot powered by InternLM2 QLora")

# 定义模型路径

model_id = 'JimmyMa99/WuKong-Chat'

mode_name_or_path = snapshot_download(model_id, revision='master')
# mode_name_or_path='process_data/merged_models/zbj'


# 定义一个函数，用于获取模型和tokenizer
@st.cache_resource
def get_model():
    # 从预训练的模型中获取tokenizer
    tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, trust_remote_code=True)
    # 从预训练的模型中获取模型，并设置模型参数
    model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
    model.eval()  
    return tokenizer, model

# 加载model和tokenizer
tokenizer, model = get_model()

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message("user").write(msg[0])
    st.chat_message("assistant").write(msg[1])

# 如果用户在聊天输入框中输入了内容，则执行以下操作
if prompt := st.chat_input():
    # 在聊天界面上显示用户的输入
    st.chat_message("user").write(prompt)
    # 构建输入     
    response, history = model.chat(tokenizer, prompt, meta_instruction=system_prompt, history=st.session_state.messages)
    # 将模型的输出添加到session_state中的messages列表中
    st.session_state.messages.append((prompt, response))
    # 在聊天界面上显示模型的输出
    st.chat_message("assistant").write(response)