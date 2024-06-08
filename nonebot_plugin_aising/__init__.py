import asyncio
from time import time
import re
from pathlib import Path
from gradio_client import Client, file
import time
from nonebot.permission import SUPERUSER
from nonebot import require ,on_command ,on_message
import os
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    MessageEvent,
    GroupMessageEvent,
)
from nonebot.params import CommandArg, ArgStr
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata
from functools import partial
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

__plugin_meta__ = PluginMetadata(
    name="ai唱歌",
    description="能让b站任何能搜到素材的角色唱歌",
    usage="让爱丽丝唱冬之花(两边支持bv号) 设置唱歌链接(你的后端公开链接) 设置唱歌开始时间0(默认30秒开始) 设置唱歌音调12(-12到12)",
    supported_adapters={"~onebot.v11"},
    type="application",
    homepage="https://github.com/CCYellowStar2/nonebot-plugin-aising"
)

timee=30
URL = ""
pich=0
init = True
processing = False
filepath: Path = store.get_config_file("aising", "Aising_URL.txt")

REGEX_DICT = "REGEX_DICT"
REGEX_ARG = "REGEX_ARG"


def regex(pattern: str) -> Rule:
    def checker(event: MessageEvent, state: T_State) -> bool:
        msg = event.get_message()
        msg_seg: MessageSegment = msg[0]
        if not msg_seg.is_text():
            return False

        seg_text = str(msg_seg).lstrip()
        matched = re.match(rf"(?:{pattern})", seg_text, re.IGNORECASE)
        if not matched:
            return False

        new_msg = msg.copy()
        seg_text = seg_text[matched.end():].lstrip()
        if seg_text:
            new_msg[0].data["text"] = seg_text
        else:
            new_msg.pop(0)
        state[REGEX_DICT] = matched.groupdict()
        state[REGEX_ARG] = new_msg
        return True

    return Rule(checker)


def RegexArg(key: str):
    async def dependency(state: T_State):
        arg: dict = state[REGEX_DICT]
        return arg.get(key, None)

    return Depends(dependency)

async def async_predict(client, *args, **kwargs):
    fn = partial(client.predict, *args, **kwargs)
    loop = asyncio.get_running_loop()  # 获取当前的事件循环
    return await loop.run_in_executor(None, fn)

async def main(client, *args, **kwargs):
    result = await async_predict(client, *args, **kwargs)
    return result
    
voice = on_message(regex(rf"(?:让|叫)(?P<name>.+?)(?:唱|唱歌)(?P<text>.+?)$"), block=False, priority=5)


@voice.handle()
async def voicHandler(
    bot: Bot, event: MessageEvent,
    name: str = RegexArg("name"),
    text: str = RegexArg("text")
):
    print(name+" "+text)
    global URL
    global pich
    global timee
    global init
    global processing
    if processing:
        await voice.finish("有唱歌正在生成，请稍等...")
        
    if init:
        if os.path.exists(filepath):
            with open(filepath, mode='r', encoding='utf-8', errors='ignore') as f:
                URL = f.read()
            init = False
    if URL == "":
        await voice.finish("请先设置唱歌链接！") 
    substrings = ["ai", "AI"]
    substring_not_in_arg = True
    for sub in substrings:
        if sub in name:
            substring_not_in_arg = False
            break

    if substring_not_in_arg and not name.startswith("BV"):
        name="AI "+name
    aa = time.perf_counter()
    try:
        api = URL
        client = Client(api)
        task = asyncio.create_task(main(
            client,
            timee,	# float  in '起始时间 (秒)' Number component
            text,	# str  in '请填写想要AI翻唱的歌曲或BV号' Textbox component
            name,	# str  in '请填写含有目标音色的歌曲或BV号' Textbox component
            None,	# str (filepath on your computer (or URL) of file) in '从本地上传一段想要AI翻唱的音频。需要为去除伴奏后的音频，此程序将自动提取前45秒的音频；如果您希望通过歌曲名搜索在线音频，请勿在此上传音频文件' Audio component
            None,	# str (filepath on your computer (or URL) of file) in '从本地上传一段音色参考音频。需要为去除伴奏后的音频，建议上传长度为60~90s左右的.wav文件；如果您希望通过歌曲名搜索在线音频，请勿在此上传音频文件' Audio component
            True,	# bool  in '参考音频是否为歌曲演唱，默认为是' Checkbox component
            False,	# bool  in '是否自动预测歌曲人声升降调，默认为是' Checkbox component
            pich,	# float (numeric value between -12 and 12) in '歌曲人声升降调' Slider component
            3,	# float (numeric value between -3 and 3) in '调节人声音量，默认为0' Slider component
            -1,	# float (numeric value between -3 and 3) in '调节伴奏音量，默认为0' Slider component
            api_name="/convert"
        ))
        start_time = asyncio.get_running_loop().time()
        processing = True
        await voice.send(f"开始生成唱歌...")
        result = await task
        print("1")
        end_time = asyncio.get_running_loop().time()
        total_time = end_time - aa 
        location=result
        file_uri = Path(location).as_uri()
        await voice.send(MessageSegment.record(file_uri))
        await voice.send(f"唱歌生成时间：本次用时 {total_time:.2f} seconds.") 
        processing = False
    except Exception as e:
        processing = False
        await voice.finish(f"生成唱歌失败..{type(e)}: {e}")

     
        
set_url = on_command("设置唱歌链接", block=True, permission=SUPERUSER, priority=5)
        
@set_url.handle()
async def _(state: T_State, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["url"] = text
        
@set_url.got("url", prompt="请输入要设定的URL")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("url"),
):  
    global URL
    global filepath
    _url = keyword
    if _url[-1] != "/":
        _url = _url + "/"
    with open(filepath, mode='w', encoding='utf-8', errors="ignore") as f:
        f.write(_url)
    URL = _url
    await set_url.send(f"已设置唱歌链接为{URL}")

set_time = on_command("设置唱歌开始时间", block=True, priority=5)

@set_time.handle()
async def _(state: T_State, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["url"] = text
        
@set_time.got("url", prompt="请输入要设定的时间（秒）")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("url"),
):  
    global timee
    
    timee = int(keyword)
    await set_time.send(f"已设置唱歌时间为{timee}")

set_pich = on_command("设置唱歌音调", block=True, priority=5)

@set_pich.handle()
async def _(state: T_State, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["url"] = text
        
@set_pich.got("url", prompt="请输入要设定的音调（-12到12）")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("url"),
):  
    global pich
    
    pich = int(keyword)
    await set_time.send(f"已设置唱歌音调为{pich}")
