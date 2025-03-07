# GPT-SoVITS推理

本仓库是[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)的推理版本，一个功能强大的少样本语音克隆框架。

## 概述

GPT-SoVITS是一个创新型的文本到语音解决方案，可以用仅仅1分钟的训练数据克隆语音。这个仓库专注于原始项目的推理部分，使得使用训练好的模型进行语音合成变得更容易。

## 特点

- 少样本语音克隆能力
- 支持多种语言：
  - 中文
  - 英文
  - 日文
  - 混合语言支持（中文-英文，日文-英文，多语言）
- 带参考音频的文本到语音
- 无参考模式可用
- 多种文本切割方法以提高合成质量

## 入门

### 环境要求

- Python 3.8 - Python 3.10
- 兼容CUDA的GPU（推荐）
- Windows/Linux/MacOS

### 安装

1. 克隆这个仓库：
```bash
git clone [your-repository-url]
cd GPT-SoVITS
```

2. 安装依赖项：
```bash
pip install -r requirements.txt
```

3. 下载所需模型：
   - 将GPT模型放在`GPT_weights/`中
   - 将SoVITS模型放在`SoVITS_weights/`中
   - 对于中文ASR：从Damo ASR/VAD/Punc下载模型，并将其放在`tools/asr/models/`中
   - 对于英文/日文ASR：下载Faster Whisper Large V3，并将其放在`tools/asr/models/`中

### 使用

1. 启动WebUI：
```bash
python inference_webui.py
```

2. 使用界面：
   - 上传3-10秒的参考音频
   - 输入参考音频的文本
   - 选择参考音频的语言
   - 输入要合成的文本
   - 选择目标语言
   - 如果需要，选择文本切割方法
   - 点击“生成”以创建语音

### 文本切割方法

对于长文本，提供了多种切割方法：
- 按4句分组
- 按50个字符切割
- 按中文句号（。）切割
- 按英文句号（.）切割
- 按标点符号切割

### 高级设置

- 无参考模式：当参考文本不清晰或不可用时启用
- GPT采样参数：
  - top_k：控制多样性（1-100）
  - top_p：控制随机性（0-1）
  - temperature：控制创造性（0-1）

##鸣谢

本项目基于原始[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)项目。所有鸣谢归功于原始作者和贡献者。

## 许可证

本项目根据限制性许可证进行许可，该许可证禁止商业用途。以下条件适用：

1. 您只能为个人和研究目的使用本软件。
2. 任何形式的商业用途都是严格禁止的。
3. 您必须包括本许可证通知和对原始项目的归属。
4. 您不能将软件用于任何非法目的或生成误导性内容。

对于学术或研究用途，请引用原始[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)项目。

## 免责声明

使用本软件或分发本软件生成的语音的用户承担全部责任。如果您不同意这些条款，您不能使用或引用软件包中的任何代码和文件。任何滥用本软件以生成误导或有害内容的行为都是严格禁止的。 