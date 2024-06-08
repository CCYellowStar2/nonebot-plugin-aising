<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-aising

_✨ 能让b站任何能搜到素材的角色唱歌 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/CCYellowStar2/nonebot-plugin-aising.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-aising">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-aising.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>


## 📖 介绍

使用[NeuCo v2](https://www.bilibili.com/video/BV1fz42127wX/)作为后端，bot作为前端调用的ai唱歌插件，通过爬取b站视频再加上急速训练来做到只要b站上有这个角色的素材就能让这个角色唱b站上有的任何歌，插件可使用```设置唱歌链接```来指定后端链接达到随时更换，后端搭建可以本地也可以[colab](https://colab.research.google.com/drive/102KeOMpmz8Y7m0I3NMSv3orIOBUmNGir?usp=sharing)

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-aising

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-aising
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-aising
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-aising
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-aising
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_aising"]

</details>

### 后端的本地部署
在本地克隆```git clone https://huggingface.co/spaces/CCYellowStar/NeuCoSVC-2```这个项目，随后在这个目录```pip install -r requirements.txt```安装依赖  
解决了各种安装依赖的问题后，就可以```python app_colab.py```运行了

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 让xxx唱xxx | 群员 | 否 | 群聊 | 让b站有素材的任何角色唱b站有的歌 |
| 设置唱歌链接xxx | 超级用户 | 否 | 群聊 | 设置后端运行后输出的公开链接 |
| 设置唱歌开始时间x | 群员 | 否 | 群聊 | 设置唱歌开始秒数 |
| 设置唱歌音调x | 群员 | 否 | 群聊 | 设置唱歌音调 |
### 效果图
![image](https://github.com/CCYellowStar2/nonebot-plugin-aising/assets/149048350/1cd7c8ef-492e-47c8-9913-c7392db00068)

## 💡 鸣谢

### [NeuCoSVC](https://github.com/thuhcsi/NeuCoSVC)
- 后端原项目
### [NeuCo v2](https://www.bilibili.com/video/BV1fz42127wX/)
- 后端项目
### [syagina](https://github.com/syagina)
- 巨大贡献

## 🦜 更新日志

### 2024.06.08

- 音调自动预测改为使用手动设定
- 增加音调调节功能
