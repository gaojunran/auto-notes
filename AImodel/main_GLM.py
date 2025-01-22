# This file is used to call api of GLM model.
# 使用了uv来管理这个文件的运行环境

# 输入输出文件
input_file = '行列式输入.txt'
output_file1 = '行列式输出.md'
output_file2 = '行列式输出.json'

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

model_str = ChatOpenAI(
    model='glm-4-flash',
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    max_tokens=2000,
    temperature=0.1
)
prompt_template_str = ChatPromptTemplate.from_messages(
    [
        ('system','用户输入一堂课的录音文本，你被要求先优化识别错误的内容，然后根据处理后的文本，以文本形式输出课程主题，课程摘要，和详细的课程笔记(每个要点都要有根据课堂内容的解释或例子），最后附上几个关键词及对应的参考网站'),
        ('human','{record_text}')
    ]
)

with open(input_file, 'r', encoding='utf-8') as f:
    record_text = f.read()

print("读取输入文件成功")

chain_str = prompt_template_str|model_str

note_text = chain_str.invoke(input = {'record_text': record_text}).content
print(type(note_text))
print(note_text)

note_text = note_text.replace('{', '{{').replace('}', '}}')

with open(output_file1, 'w', encoding='utf-8') as f:
    f.write(note_text)

model_json = ChatOpenAI(
    model='glm-4-flash',
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    max_tokens=3000
)

model_json_massage = ("接下来把用户输入的课堂笔记进行拆分并输出一个json文件，包含：1.课程主题，2.课程摘要，3.详细的课程笔记中的每一个要点及对应的解释或例子，4.关键词及对应的参考网站，要点中用markdown格式。示例如下："
                    "{{'主题'：'区块链', '摘要'：'区块链是一种分布式数据库技术，它利用密码学、共识算法、智能合约等技术，为用户提供安全、透明、可靠的价值存储和交换服务。', '要点'：[{{'标题'：'#什么是区块链？', '内容'：'**区块链**是一种分布式数据库技术，它利用密码学、共识算法、智能合约等技术，为用户提供安全、透明、可靠的价值存储和交换服务。'}}, {{'标题'：'#区块链的应用场景', '内容'：'区块链的应用场景主要有以下几种：1. 价值存储和交换。2. 身份认证}}],"
                    "‘参考网站’:[{{‘标题’：‘区块链白皮书’，‘链接’：‘https://baike.baidu.com/item/%E5%8C%BA%E5%9D%97%E9%93%BE/10281957?fr=aladdin’}}, {{‘标题’：‘区块链技术指南’，‘链接’：‘https://baike.baidu.com/item/%E5%8C%BA%E5%9D%97%E9%93%BE%E6%8A%80%E6%9C%AF%E6%8C%87%E5%8D%97/2022877?fr=aladdin’}}]}})")

prompt_template_json = ChatPromptTemplate.from_messages(
    [
        ('system',model_json_massage),
        ('human',note_text)
    ]
)
chain_json = prompt_template_json|model_json
json_text = chain_json.invoke({}).content
print(json_text)

json_text = json_text.replace('```json','').replace('```','')

with open(output_file2, 'w', encoding='utf-8') as f:
    f.write(json_text)