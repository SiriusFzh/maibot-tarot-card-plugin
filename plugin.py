"""塔罗牌插件 — 随机抽取一张大阿卡那牌，解读运势和建议。"""

import base64
import random
from pathlib import Path
from typing import Any, ClassVar

from maibot_sdk import Command, EventHandler, Field, MaiBotPlugin, PluginConfigBase
from maibot_sdk.types import EventType


IMAGES_DIR = Path(__file__).parent / "images"

TAROT_CARDS = {
    "愚者": {
        "en": "The Fool",
        "meaning": "你正站在全新旅程的起点，内心充满无畏的好奇与期待。不要过度规划，相信直觉，勇敢迈出第一步——最好的冒险往往没有地图。",
    },
    "魔术师": {
        "en": "The Magician",
        "meaning": "你已拥有实现目标所需的一切资源和能力，只是尚未察觉。不必等待完美的时机，现在就是行动的最佳时刻，动手去创造吧。",
    },
    "女祭司": {
        "en": "The High Priestess",
        "meaning": "你的直觉正格外敏锐，有些答案无法从外界获取。静下心来倾听内心的声音吧，给自己一段独处的时间，真相会自然浮现。",
    },
    "皇后": {
        "en": "The Empress",
        "meaning": "丰收与滋养的时期已至，无论是物质还是情感都丰盛而温暖。善待自己，去享受生活中的美好，也别忘了关心身边的人。",
    },
    "皇帝": {
        "en": "The Emperor",
        "meaning": "你正渴望建立秩序与掌控感，用规则和纪律为你的目标保驾护航。但要记得适度放松——真正的权威来自自信而非控制。",
    },
    "教皇": {
        "en": "The Hierophant",
        "meaning": "你正寻求指引与智慧，传统的经验和教诲会给你启发。但知识是用来照亮你的路，不是束缚你的脚步，保持独立思考。",
    },
    "恋人": {
        "en": "The Lovers",
        "meaning": "你正面临一个重要的选择，内心的偏好其实已经有了方向。忠于自己的价值观，而非得失的权衡——无论选哪条路，忠于自己就是最好的决定。",
    },
    "战车": {
        "en": "The Chariot",
        "meaning": "你正以强烈意志推进目标，不达目的不罢休。保持专注稳中求进，同时注意平衡各方关系，胜利在望，继续加油。",
    },
    "力量": {
        "en": "Strength",
        "meaning": "你正用耐心和温柔化解困境，真正的力量是包容而非征服。你比自己想象中更坚韧，温柔地坚持下去就好。",
    },
    "隐士": {
        "en": "The Hermit",
        "meaning": "你需要一段安静的独处时光来沉淀和反思。暂时从喧嚣中抽离吧，很多问题在静心之后自然就有了答案。",
    },
    "命运之轮": {
        "en": "Wheel of Fortune",
        "meaning": "命运的转折点正在到来，变化已在路上。顺应这股力量，当幸运之门打开时勇敢走进去——一切都是最好的安排。",
    },
    "正义": {
        "en": "Justice",
        "meaning": "你正面对一个需要公正裁决的局面，理智与判断力正处于巅峰。以客观态度审视全局，过去的行为正在产生应有的结果。",
    },
    "倒吊人": {
        "en": "The Hanged Man",
        "meaning": "你正处在看似停滞的蓄力期，换个角度看待眼下的困境吧。有时候放下比抓住更需要勇气，这个暂停是为了更大的转变。",
    },
    "死亡": {
        "en": "Death",
        "meaning": "某个阶段正在走向结束，告别虽不舍却是新生的前夜。放下不再适合你的人和事，才有空间迎接全新的可能。这不是终点，而是一场蜕变。",
    },
    "节制": {
        "en": "Temperance",
        "meaning": "你正学着平衡生活中的各个方面，避免走极端才能长久。放慢脚步，融合看似矛盾的力量，你会找到属于自己的和谐节奏。",
    },
    "恶魔": {
        "en": "The Devil",
        "meaning": "你可能正被某些事物束缚感到身不由己，但打破锁链的力量其实就在你手中。诚实审视自己，直面欲望和恐惧，就能挣脱枷锁。",
    },
    "高塔": {
        "en": "The Tower",
        "meaning": "突如其来的变化正在冲击你的生活，虽然过程猛烈，但它摧毁的只是本就不牢固的部分。接受这场洗礼，之后你将拥有更坚实的地基。",
    },
    "星星": {
        "en": "The Star",
        "meaning": "疗愈与平静的时期已经到来，你内心的光芒正重新亮起。保持信念敞开心扉，让希望引领你前行——美好的事情即将发生。",
    },
    "月亮": {
        "en": "The Moon",
        "meaning": "你正处在迷茫与不安之中，看不清前路。但你所恐惧的多半只是内心的投射，冷静区分现实与幻象，穿过迷雾后会比之前更清醒强大。",
    },
    "太阳": {
        "en": "The Sun",
        "meaning": "这是充满活力与成功的灿烂时期！尽情享受这段时光，把快乐传递给身边的人。你会成为自己生命中的太阳，温暖而耀眼。",
    },
    "审判": {
        "en": "Judgement",
        "meaning": "你正经历深层次的觉醒，内心深处有个声音在呼唤你重新开始。清算过去轻装上阵吧，原谅自己、接受过去，然后迈入新的阶段。",
    },
    "世界": {
        "en": "The World",
        "meaning": "一个重要周期即将圆满结束，你的努力得到了回馈。庆祝这份成就，同时也开始思考下一个目标——世界尽在你手中。",
    },
}

LONG_PHRASE_KEY = "不属于这个时代的愚者"


class PluginSection(PluginConfigBase):
    __ui_label__ = "插件"
    __ui_order__ = 0

    enabled: bool = Field(default=True, description="是否启用插件")
    config_version: str = Field(default="1.0.0", description="配置版本")


class TarotConfig(PluginConfigBase):
    plugin: PluginSection = Field(default_factory=PluginSection)


class TarotCardPlugin(MaiBotPlugin):
    config_model: ClassVar[type[PluginConfigBase] | None] = TarotConfig

    async def on_load(self) -> None:
        self.ctx.logger.info("塔罗牌插件已加载，共 %d 张大阿卡那牌", len(TAROT_CARDS))

    async def on_unload(self) -> None:
        self.ctx.logger.info("塔罗牌插件已卸载")

    async def on_config_update(self, scope: str, config_data: dict, version: str) -> None:
        pass

    @Command(
        "tarot",
        description="/塔罗 随机抽取一张塔罗牌",
        pattern=r"^/塔罗$",
    )
    async def handle_tarot(self, stream_id: str = "", **kwargs) -> tuple:
        return await self._draw_card(stream_id)

    @EventHandler(
        "tarot_long_phrase",
        description="检测长触发短语并抽取塔罗牌",
        event_type=EventType.ON_MESSAGE,
    )
    async def handle_long_phrase(self, message: Any = None, stream_id: str = "", **kwargs) -> tuple:
        if not message or not stream_id:
            return True, True, None, None, None

        text = ""
        if isinstance(message, dict):
            text = message.get("plain_text", "") or message.get("processed_plain_text", "") or ""
        else:
            text = str(message)

        if LONG_PHRASE_KEY in text and "抽一张塔罗牌" in text:
            await self._draw_card(stream_id)
            return True, True, "已抽取塔罗牌", None, None

        return True, True, None, None, None

    async def _draw_card(self, stream_id: str) -> tuple:
        card_name = random.choice(list(TAROT_CARDS.keys()))
        card = TAROT_CARDS[card_name]

        image_path = IMAGES_DIR / f"{card_name}.png"
        if image_path.exists():
            image_base64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
            await self.ctx.send.image(image_base64, stream_id)

        text = f"你抽到了「{card_name}」（{card['en']}）\n\n{card['meaning']}"
        await self.ctx.send.text(text, stream_id)

        return True, f"已抽取 {card_name}", True


def create_plugin() -> TarotCardPlugin:
    return TarotCardPlugin()
