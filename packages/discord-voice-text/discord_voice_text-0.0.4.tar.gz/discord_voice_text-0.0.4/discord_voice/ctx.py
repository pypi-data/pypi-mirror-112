from discord.ext import commands as c
from discord import FFmpegPCMAudio, ui, Message
from asyncpgw import general
from typing import Optional
from asyncio import sleep
from datetime import datetime

from aiohttp import ClientSession, BasicAuth

from .embed import *

import numpy as np

import os
import re

__all__ = ["VoiceTextContext", "get_folder", "voice_purge"]

bot_channels = """bot_channels(
    server bigint,
    vc bigint,
    opt bigint,
    join_time timestamp with time zone

)"""


class Speaker(ui.View):
    def __init__(self, ctx, number: int, *, timeout: Optional[float]):
        super().__init__(timeout=timeout)
        self.number = number
        self.user_voices = general.Pg(ctx.bot, "user_voices")
        self.author = ctx.author

        self.params = {
            "member": ctx.author.id,
            "set_number": number
        }

    @ui.button(label="男性1", custom_id="boy1")
    async def boy_one(self, button, interaction):
        await self.user_voices.update(speaker="show", **self.params)

    @ui.button(label="男性2", custom_id="boy2")
    async def boy_two(self, button, interaction):
        await self.user_voices.update(speaker="takeru", **self.params)

    @ui.button(label="女性1", custom_id="girl1")
    async def girl_one(self, button, interaction):
        await self.user_voices.update(speaker="haruka", **self.params)

    @ui.button(label="女性2", custom_id="girl2")
    async def girl_two(self, button, interaction):
        await self.user_voices.update(speaker="hikari", **self.params)

    @ui.button(label="サンタ", custom_id="santa")
    async def santa(self, button, interaction):
        await self.user_voices.update(speaker="santa", **self.params)

    @ui.button(label="凶暴な熊", custom_id="bear")
    async def bear(self, button, interaction):
        await self.user_voices.update(speaker="bear", **self.params)


class Emotion(ui.View):
    def __init__(self, ctx, number: int, *, timeout: Optional[float]):
        super().__init__(timeout=timeout)
        self.number = number
        self.user_voices = general.Pg(ctx.bot, "user_voices")
        self.author = ctx.author

        self.params = {
            "member": ctx.author.id,
            "set_number": number
        }

    async def send(self, button, interaction):
        await interaction.response.send_message(f"{self.author.mention}の感情の設定を{button.label}にしたよ！")

    @ui.button(label="喜", custom_id="happiness")
    async def boy_one(self, button, interaction):
        await self.user_voices.update(speaker="happiness", **self.params)

    @ui.button(label="怒", custom_id="anger")
    async def boy_one(self, button, interaction):
        await self.user_voices.update(speaker="anger", **self.params)

    @ui.button(label="悲", custom_id="sadness")
    async def boy_one(self, button, interaction):
        await self.user_voices.update(speaker="sadness", **self.params)


def get_folder(mes) -> str:
    """wavファイルを保存するフォルダーを返す

    params:
        mes: discord.Message, 送信されたメッセージ

    return:
        folder: wavファイルを保存するフォルダー
    """

    if not os.path.isdir(f"voice"):
        os.mkdir(f"voice")

    if not os.path.isdir(f"voice/{mes.author.id}"):
        os.mkdir(f"voice/{mes.author.id}")

    return f"voice/{mes.author.id}/"


class VoiceTextContext(c.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.base_url = "https://api.voicetext.jp/v1/tts"

        self.api = os.environ.get('VOICE_TEXT_WEB_API')

        self.base_role = general.Pg(self.bot, 'base_role')

        self.user_voice = general.Pg(self.bot, "user_voice")  # IDと使用番号
        self.user_voices = general.Pg(self.bot, "user_voices")  # IDとセット番号と声の設定
        self.bot_channels = general.Pg(self.bot, 'bot_voices')  # IDと声の設定の一覧
        self.user_dict = general.Pg(self.bot, 'user_dict')
        self.ment = general.Pg(self.bot, 'ment')

        self.default_params = {
            "server": self.guild.id,
            "vc": self.author.voice.channel.id,
            "tc": self.channel.id,
            "opt": self.bot.user.id
        }

        # 話者
        self.speaker = {
            "show": "男性1",
            "takeru": "男性2",
            "haruka": "女性1",
            "hikari": "女性2",
            "santa": "サンタ",
            "bear": "凶暴な熊"
        }

        # 感情
        self.emotion = {
            'happiness': '喜',
            'anger': '怒',
            'sadness': '悲'
        }

        self.speakers = tuple(self.speaker.keys())
        self.emotions = tuple(self.emotion.keys())

    async def join(self) -> None:

        if not await self.bot_channels.fetch(**self.default_params):
            await self.bot_channels.insert(**self.default_params)

        await self.read_voice.update(tc=self.channel.id, **self.default_params)

        await self.read_voice.update(join_time=datetime.now(), **self.default_params)


    async def leave(self):
        await self.bot_channels.update(tc=None, **self.default_params)

    async def load_data(self) -> dict:
        """ユーザーのデータを取得する

        return:

            speaker, emotion, emotion_level, pitch, speed, volume, 
            ユーザーのデーター　
        """
        if not (data := await self.user_voice.fetch(member=self.author.id)):
            params = self.set_random_data()

            params["member"] = self.author.id

            await self.user_voices.insert(**params)
            await self.user_voice.insert(member=self.author.id)

            number = 1

        else:
            number = data["use_number"]

        data = await self.user_voices.fetch(member=self.author.id, set_number=number)

        data = dict(data)

        del data["member"]

        if data['speaker'] == 'show':
            del data['emotion']
            del data['emotion_level']

        return data

    async def set_speaker(self) -> str:
        """
        話者の設定
        """

        if not (data := await self.base_role.fetch(server=self.guild.id)):
            speaker = np.random.choice(tuple(self.speaker.keys()))
        else:
            boy_role = self.guild.get_role(data['base_boy_role'])
            girl_role = self.guild.get_role(data['base_girl_role'])

            if boy_role in self.author.roles:
                speaker = "haruka"
            elif girl_role in self.author.roles:
                speaker = "takeru"

            return speaker

    async def set_random_data(self) -> dict:
        """ユーザーの声の初期設定を登録する時に使用
        ランダムな設定を返す

        return:
            speaker: 話者
            emotion: 感情
            emotion_level: 感情レベル
            pitch: 音程
            speed: 速さ
            volume: 音量
        """

        params = {}

        # 話者
        params["speaker"] = await self.set_speaker()

        # 感情
        if "show" != params["speaker"]:
            params["emotion"] = np.random.choice(tuple(self.emotion.keys()))
            params["emotion_level"] = np.random.randint(1, 5)

        # 音程
        params["pitch"] = np.random.randint(50, 201)
        # 速度
        params["speed"] = np.random.randint(50, 401)
        # 音量
        params["speed"] = np.random.randint(50, 201)

        return params

    async def fixed(self) -> dict:
        """ユーザーのデータを修正する

        return:
            member: discord.Member
            set_number: int
            speaker: str
            emotion: str
            emotion_level: int
            pitch: int
            speed: int
            volume: int
        """

        fixed_items = {}

        data = await self.load_data()

        params = {
            "member": self.author.id,
            "set_number": data["set_number"]
        }

        if data["speaker"] not in self.speakers:
            speaker = await self.set_speaker()
            await self.user_voices.update(speaker=speaker, **params)
            fixed_items["話者"] = self.speaker[speaker]

        if data["speaker"] != "show":
            if data["emotion"] not in self.emotions:
                emotion = np.random.choice(self.emotions)
                await self.user_voices.update(emotion=emotion, **params)
                fixed_items["感情"] = self.emotion[emotion]

            if data["emotion_level"] not in (levels := tuple(range(1, 5))):
                emotion_level = np.random.choice(levels)
                await self.user_voices.update(emotion_level=emotion_level, **params)
                fixed_items["感情レベル"] = emotion_level

        if data["pitch"] not in (pitchs := tuple(range(50, 201))):
            pitch = np.random.choice(pitchs)
            await self.user_voices.update(pitch=pitch, **params)
            fixed_items["音程"] = pitch

        if data["speed"] not in (speeds := tuple(range(50, 401))):
            speed = np.random.choice(speeds)
            await self.user_voices.update(speed=speed, **params)
            fixed_items["速度"] = speed

        if data["volume"] not in (volumes := tuple(range(50, 201))):
            volume = np.random.choice(volumes)
            await self.user_voices.update(volume=volume, **params)
            fixed_items["音量"] = volume

        if fixed_items != {}:
            e = normal(
                title='以下の項目にエラーがあったので修正したよ',
                description='\n'.join(f'{k}: {v}' for k, v in fixed_items.items())
            )
            await self.send(embed=e)

        data = await self.get_data()
        return dict(data)

    # メッセージを読み上げるか
    async def is_read(self) -> str:
        """メッセージを読み上げるか"""

        if self.message.author.bot:
            return

        if self.command:
            return

        if 'http' in self.message.content:
            return

        if self.message.content.isnumeric():
            return

        if self.message.content == '':
            return

        if ':' in self.message.content:
            return

        # 役職
        for m in re.finditer(r'<@&(?P<role_id>[0-9]+)>', self.message.content, re.MULTILINE):
            g = m.groups()[0]
            for w in g.splitlines():
                self.message.content = self.message.content.replace(g, self.guild.get_role(int(w)).name).replace("@&", "")
        # ユーザー
        for m in re.finditer(r'<@!?(?P<user_id>[0-9]+)>', self.message.content, re.MULTILINE):
            g = m.groups()[0]
            for w in g.splitlines():
                self.message.content = self.message.content.replace(g, self.guild.get_member(int(w)).display_name).replace("@", "")
        # チャンネル
        for m in re.finditer(r'<#(?P<channel_id>[0-9]+)>', self.message.content, re.MULTILINE):
            g = m.groups()[0]
            for w in g.splitlines():
                self.message.content = self.message.content.replace(g, self.guild.get_channel(int(w)).name).replace("#", "")

        self.message.content = re.sub('[w|W|ｗ|W|笑|爆笑]+', 'わら', self.message.content)

        return self.message.content

    # 読み方を変更
    async def replace(self) -> str:
        """ユーザー辞書が登録されてたらその読み方に変更する

        return:
            変換されたメッセージ
        """

        if not (datas := await self.user_dict.fetch(member=self.author.id)):
            return self.message.content

        replacemes = {data["before_word"]: data["after_word"] for data in datas if data["before_word"]}

        key = tuple(replacemes.keys())

        if len(key) == 0:
            return self.message.content

        replace_mes = re.sub('({})'.format('|'.join(map(re.escape, replacemes.keys()))), lambda m: replacemes[m.group()], self.message.content)

        return replace_mes

    async def _save_wav_file(self) -> None:
        "wavファイルに保存"
        content = await self.replace()

        params = await self.fixed()

        del params["set_number"]

        params["text"] = content

        folder = get_folder(self.message)

        async with ClientSession() as s:
            async with s.post(self.base_url, params=params, auth=BasicAuth(self.api)) as data:
                if data.status != 200:
                    return

                if data.status == 503:
                    if not (data := await self.ment.fetch(server=self.guild.id)):
                        await self.ment.insert(server=self.guild.id)

                    if data['enable']:
                        return

                    e = normal(
                        title='現在読み上げをサポートしてるサーバーがメンテナンス中です。メンテナンスが終わるまで暫くお待ちください'
                    )
                    if not await self.ment.fetch(server=self.guild.id):
                        await self.ment.insert(server=self.guild.id)
                    await self.ment.update(enable=True, server=self.guild.id)
                    return await self.channel.send(embed=e)

                if data.status == 200:
                    await self.ment.update(enable=False)

                with open(f"{folder}{self.message.id}.wav", 'wb') as f:
                    f.write(await data.content.read())

    async def speak(self) -> None:
        "読み上げ関数"
        if not await self.is_read():
            return

        folder = get_folder(self.message)

        while self.guild.voice_client.is_playing():
            await sleep(1)

        self.guild.voice_client.play(FFmpegPCMAudio(f"{folder}{self.message.id}.wav"))

        await sleep(1)

        try:
            os.remove(f'{folder}{self.message.id}.wav')
        except:
            return

    async def _error(self):
        e = error("一度読み上げ機能を使ってからこのコマンドを実行してね")
        return await self.send(embed=e)

    async def save_speaker(self) -> None:
        if not (data := await self.user_voice.fetch(member=self.author.id)):
            return await self._error()

        e = normal(
            title="下のボタンからどの話者に設定するか選んでね！"
        )
        return await self.send(embed=e, view=Speaker(self.ctx, data["use_number"]))

    async def save_emotion(self):
        if not (data := await self.user_voice.fetch(member=self.author.id)):
            return await self._error()

        e = normal(
            title="下のボタンからどの感情に設定するか選んでね！"
        )
        return await self.send(embed=e, view=Emotion(self.ctx, data["use_number"]))

    async def get_number(self, opt):
        if opt == "emotion_level":
            limit = range(1, 5)
        elif opt == "pitch":
            limit = range(50, 201)
        elif opt == "speed":
            limit = range(50, 401)
        elif opt == "volume":
            limit = range(50, 201)

        def check(m):
            return m.author == self.author and \
                m.channel.id == self.channel.id and \
                m.content in limit

        m = await self.bot.wait_for("message", check=check)

        return m

    async def save_number(self, opt, jpn_opt, min: int, max: int):
        if not (data := await self.user_voice.fetch(member=self.author.id)):
            return await self._error()

        e = normal(
            desc=f"{jpn_opt}を\n```{min}~{max + 1}```\nで入力してね！"
        )

        await self.send(embed=e)

        number = await self.get_number(opt)

        params = {
            "member": self.author.id,
            "set_number": data["use_number"]
        }

        await self.user_voices.update(emotion_level=number, **params)

    async def save_emotion_level(self):
        await self.save_number("emotion_level", "感情レベル", 1, 4)

    async def save_pitch(self):
        await self.save_number("pitch", "音程", 50, 200)

    async def save_speed(self):
        await self.save_number("speed", "速度", 50, 400)

    async def save_volume(self):
        await self.save_number("volume", "音量", 50, 200)

    async def show(self) -> dict:
        "声の一覧"
        if not (data := await self.user_voice.fetch(member=self.author.id)): return await self._error()
        
        number = data["use_number"]

        if not (data := await self.user_voices.fetch(member=self.author.id, set_number=number)): return await self._error()

        params = {
            "話者": self.speaker[data["speaker"]],
            "音程": data["pitch"],
            "速度": data["speed"],
            "音量": data["volume"]
        }

        if data["speaker"] != "show":
            params["感情"] = self.emotion[data["emotion"]]
            params["感情レベル"] = data["emoion_level"]

        return params

async def voice_purge(bot, member):
    auto_delete = general.Pg(bot, 'voice_auto_delete')
    bot_channels = general.Pg(bot, 'bot_voices')

    default_params = {
        "server": member.guild.id,
        "vc": member.voice.channel.id,
        "opt": bot.user.id
    }

    if not (data := await auto_delete.fetch(member=member.id)): return

    time_data = await bot_channels.fetch(**default_params)

    if not data["enable"]: return

    channel = time_data["tc"]

    await channel.purge(limit=None, after=time_data["join_time"])