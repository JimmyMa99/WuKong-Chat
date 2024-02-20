# 数据获取

⚙️基于API的数据获取与处理

## 需要准备的

1. OpenAI格式的api
2. python环境（参考快速开始中的环境配置环节）

## 数据的组成

项目数据组成分为以下三部分，三个部分都需要 api ，任意选择其中两个即可做出不错的效果

- 基础问题重复询问：使用API，让Chat-GPT扮演角色，提供一定的prompt让其模仿语气问答
- 原文短对话提取（参照[葱老师](https://github.com/KMnO4-zx)的[extract-dialogue](https://github.com/KMnO4-zx/extract-dialogue)）但作者进行了一定的修改
- 原文长对话提取

## 数据的获取

### 1.基础问题重复询问

提供脚本 `q2a_api.py` 但需要自行填入 `api_key` 和 `api_base_url` 以及 `base_prompt`

注意：base_prompt 会影响回复的质量

💬以下是唐三藏的 prompt

```shell

base_prompt='孙悟空，亦称美猴王，是中国古典名著《西游记》中的核心角色之一，原为花果山水帘洞的石猴，因修炼成仙而拥有变化莫测的神通和72变的本领。他拜菩提祖师为师，学得了一身好武艺和法术，其中包括筋斗云，能一跃十万八千里。孙悟空性格狡猾、机智、勇敢，不畏强权，曾一度大闹天宫，被封为“齐天大圣”。后因佛祖降伏，成为唐僧取经路上的第一位弟子，负责保护师傅西行取经，途中斗妖除魔，展现出非凡的智慧和力量。孙悟空忠诚勇敢，无论遇到多大的困难和危险，都毫不退缩，用他的聪明才智和无比的武艺保护唐僧安全。他的性格虽然有时候显得轻狂和不羁，但他对师傅的忠诚以及对正义的坚持不懈，赢得了众多读者的喜爱。孙悟空的言行充满了对自由和正义的追求，他的故事激励了无数人勇敢面对困难，坚持自我。作为一位神通广大的仙猴，他的话语中既有俏皮和幽默，也充满了对生命和宇宙奥秘的探索与思考。在对待敌人时，他既有慈悲为怀的一面，也有果断严厉的一面，这体现了他复杂而丰富的性格特点。请你扮演孙悟空回答我的问题，尽量保持回答的自然回答，当然你也可以适当穿插一些文言文，尽可能贴合原著，注意孙悟空一般以“俺老孙”作为第一人称回答但不一定，我的问题是：'


```

本质是借助已经训练好的 LLM 进行角色扮演。

运行脚本 `q2a_api.py`

```shell

pythontools/get_data/Q2A/q2a_api.py--questions_path{your_question}--save_path{save_path}--repeat5

```

参数说明：

`--questions_path` : 基础问题，可以从 Chat-GPT 等模型中获取，项目提供了955个基础问题用于提问。

`--save_path` :保存路径，一般是 output/xxx.jsonl，脚本会整理好 xtuner 可训练的格式。

`--repeat` :重复次数，西游系列的四个模型重复询问了5次。

### 2.原文短对话提取

原 repo 链接：**[extract-dialogue](https://github.com/KMnO4-zx/extract-dialogue)**

1.从原文中获取对话（以孙悟空为例）

    首先需要在`tools/get_data/extract-dialogue/OpenAI_LLM.py` 中配置 api

    然后运行脚本

```shell

python tools/get_data/extract-dialogue/main.py --path {novel_path} --roles 孙悟空,悟空,石猴,美猴王,孙大圣,齐天大圣,行者,孙行者

```

参数说明：

`--path` :小说路径，一般是 *.txt

`--roles` :角色可能的称呼，注意用英文逗号隔开

完成后会在 `tools/get_data/extract-dialogue/output` 下生成两个文件 *.json 就是对话内容

2.将对话内容转换为 xtuner 可用格式

```shell

python tools/get_data/extract-dialogue/process_data.py --raw_data {output.json} --save_path {swk.jsonl} --role 孙悟空

```

参数说明：

`--raw_data` :提取的对话

`--save_path` :保存的路径

`--role` :角色名称

### 3.长对话提取（此模块脚本可能需要优化）

  此脚本与方法1中脚本类似 同样需要配置 api ，具体prompt修改如下

```shell

base_prompt='你是一个对话整理大师，以下内容为《西游记》节选，请你整理出角色“唐三藏”，“孙悟空”，“猪八戒”，“沙悟净”四人的对话内容，当然，这四人在小说中可能以别的名字出现，如：唐三藏->金蝉子，孙悟空->猴王->行者等人物需要你根据理解自行判别，直接返回对话内容，返回格式为：唐三藏：{对话内容}，孙悟空：{对话内容}，猪八戒：{对话内容}，沙悟净：{对话内容}，某人说：{对话内容}；若内容中无对话，则直接回答“无对话内容”无需提及人物，若对话不完整或者你没法确定对话的人物关系，你可以放弃整理，直接回复“无对话内容”无需提及人物，若出现非四人内任务与四人对话，非四人内的以“某人说”记录，请保持对话的准确性，不要修改和翻译，请不要解释。以下为节选片段：'

```

  运行脚本

```shell

python tools/get_data/long-dialogue/q2a_api.py --file_path {novel_path} --save_path {save_path}

```

  完成后会生成由 GPT 生成的对话整理

  接下来运行脚本提取长对话

```shell

python tools/get_data/long-dialogue/get_data.py --data_path {conversation.txt} --save_path {outputpath}

```

  该脚本一次可以生成多个角色的符合 xtuner 的训练数据

三个方法完成后需要整理到同一个 .jsonl 文件下，即可进行下一步使用 XTuner 微调
