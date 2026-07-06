"""塔罗牌插件 — 随机抽取一张大阿卡那牌，解读运势和建议。"""

import base64
import random
from pathlib import Path
from typing import ClassVar

from maibot_sdk import Command, Field, MaiBotPlugin, PluginConfigBase


IMAGES_DIR = Path(__file__).parent / "images"

TAROT_CARDS = {
    "愚者": {
        "en": "The Fool",
        "situation": "你正处于一个全新的起点，对未来充满好奇与期待。也许你刚做了某个大胆的决定，或正准备踏上一条从未走过的路。虽然前路未卜，但你内心那股无畏的热情正推动着你向前。",
        "advice": "保持开放的心态，相信自己的直觉。不要过度规划，有时候最好的旅程就是那些没有地图的冒险。勇敢迈出第一步吧。",
    },
    "魔术师": {
        "en": "The Magician",
        "situation": "你拥有实现目标所需的全部资源和能力，只是你可能还没有完全意识到。你正处在一个可以将想法变为现实的关键节点，身边的人和事都在为你助力。",
        "advice": "集中精力，专注于你真正想做的事情。你手中的工具已经足够，不需要等待「完美的时机」——现在就是最好的时机，动手去做。",
    },
    "女祭司": {
        "en": "The High Priestess",
        "situation": "你的直觉最近格外敏锐，或许有些事情表面上看不出端倪，但你内心已经有了答案。你可能在等待某个重要的消息，或者正在思考一个深刻的问题。",
        "advice": "相信你的直觉和潜意识。有些答案无法从外界获得，需要你静下心来倾听内心的声音。给自己一些独处的时间，答案会自然浮现。",
    },
    "皇后": {
        "en": "The Empress",
        "situation": "你正处在一个丰收和滋养的时期。无论是物质上的收获还是情感上的满足，你都能感受到生活的丰盛与温暖。也许你最近对美和自然的感受力格外敏锐。",
        "advice": "善待自己，允许自己享受生活中的美好。如果有一直想培养的兴趣爱好，现在是开始的好时候。也别忘了关心身边那些需要你温暖的人。",
    },
    "皇帝": {
        "en": "The Emperor",
        "situation": "你正在建立秩序和掌控感，可能在事业或生活中承担着领导角色。你渴望稳定和规则，希望一切都在掌控之中。但有时候这种掌控欲也会让你感到压力。",
        "advice": "用规则和纪律为你的目标保驾护航，但也要学会适度放松。真正的权威来自于自信而非控制。记住，稳固的根基是长远发展的前提。",
    },
    "教皇": {
        "en": "The Hierophant",
        "situation": "你正在寻求指引或知识，可能在学习新技能、请教前辈或探索精神层面的成长。你渴望找到一套可靠的价值体系来指导自己的生活选择。",
        "advice": "不要排斥向有经验的人请教，传统的智慧往往蕴含着深刻的道理。但同时也要保持独立思考——知识是用来启发你的，不是来束缚你的。",
    },
    "恋人": {
        "en": "The Lovers",
        "situation": "你正面临一个重要的选择，这个选择将影响你未来的方向。可能涉及感情、合作或人生道路的抉择。你内心深处已经有了偏好的方向，只是还需要一点勇气去确认。",
        "advice": "倾听你的内心，而不是只靠理性分析。真正的选择来自于价值观的契合，而非得失的权衡。无论选哪条路，忠于自己就是最好的决定。",
    },
    "战车": {
        "en": "The Chariot",
        "situation": "你正在全力推进某件事，意志力爆棚，有一股不达目的不罢休的冲劲。或许你正面临激烈的竞争或挑战，但你完全没有退缩的打算。",
        "advice": "保持专注，一鼓作气拿下目标。但也要注意平衡各方的力量，不要因为太过强势而伤害了重要的关系。胜利在望，但稳中求进才能走得更远。",
    },
    "力量": {
        "en": "Strength",
        "situation": "你正在用耐心和温柔化解一个棘手的问题。也许你面对的并非外部的敌人，而是自己内心的不安或恐惧。你比自己想象的更有韧性。",
        "advice": "真正的力量不是征服，而是包容。用温柔的方式对待自己和他人，你会发现自己拥有超乎想象的影响力。坚持下去，你比你认为的更强大。",
    },
    "隐士": {
        "en": "The Hermit",
        "situation": "你最近可能需要一些独处的时间，正在向内探索、反思生活的方向。也许你感到有些孤独，但这种孤独是成长的必经之路——你在寻找更深层的意义。",
        "advice": "暂时从喧嚣中抽离，给自己一段安静的时光。沉淀、思考、复盘，你会发现很多问题在静心之后都有了答案。你并不孤单，你只是走在自己的节奏里。",
    },
    "命运之轮": {
        "en": "Wheel of Fortune",
        "situation": "你正处于命运的转折点，一些事情正在发生变化——可能是好运的降临，也可能是一个循环的结束。你会感受到「一切都是安排好的」那种奇妙感觉。",
        "advice": "顺应变化，不要抗拒。命运之轮在转动，好的机会即将到来。保持警觉，当幸运之门打开时，勇敢地走进去。相信一切都是最好的安排。",
    },
    "正义": {
        "en": "Justice",
        "situation": "你正在处理一件涉及公平和真相的事情——可能是一个需要做出的裁决，或者你正在等待一个公正的结果。你的理智和判断力目前处于高峰状态。",
        "advice": "以客观公正的态度面对当前的局势。种瓜得瓜，种豆得豆，你过去的行为正在产生应有的结果。做决定之前，确保你掌握了全部的事实。",
    },
    "倒吊人": {
        "en": "The Hanged Man",
        "situation": "你可能正处在一种「卡住」的状态，有些事情进展缓慢，或者你需要做出一些牺牲来换取更大的收获。换个角度看，这种停滞其实是一种蓄力。",
        "advice": "不要急着挣脱现状，试着从不同的角度看待当前的局面。有时候「放下」比「抓住」更需要勇气。这个暂停期是为了让你准备迎接更大的转变。",
    },
    "死亡": {
        "en": "Death",
        "situation": "你生命中某个阶段正在走向结束——可能是一段关系、一份工作，或者一种旧的生活方式。虽然告别让人不舍，但这个结束将为全新的开始扫清道路。",
        "advice": "接受结束，不要沉溺于过去的模式。放下那些不再适合你的人和事，你才有空间迎接新的可能。这不是终点，而是一场蜕变的前夜。",
    },
    "节制": {
        "en": "Temperance",
        "situation": "你正在学习平衡生活的各个方面——工作与休息、付出与收获、理性与感性。你最近的节奏可能有些忙碌，但你在努力寻找一个让自己舒适的平衡点。",
        "advice": "避免走极端，中庸之道才是长久之计。把看似矛盾的东西融合在一起，你会创造出意想不到的和谐。放慢脚步，用温和的方式处理眼前的事。",
    },
    "恶魔": {
        "en": "The Devil",
        "situation": "你可能正被某些事物所束缚——可能是过度的工作、一段不健康的关系、或者某种成瘾行为。你感到身不由己，但实际上打破锁链的力量就在你手中。",
        "advice": "诚实地审视自己：是什么在控制你的生活？那些你以为「离不开」的东西，往往只是习惯的枷锁。你完全有能力挣脱，关键是要愿意直面自己的欲望和恐惧。",
    },
    "高塔": {
        "en": "The Tower",
        "situation": "你正在经历一场突如其来的变化或冲击，可能是某个计划的中断、一段关系的破裂，或者某个一直掩盖的真相终于曝光。虽然过程痛苦，但这恰恰是必要的「拆旧建新」。",
        "advice": "不要试图维持即将倒塌的东西。虽然改变来得猛烈，但它摧毁的只是那些本就不牢固的部分。接受这场洗礼，之后你将拥有更坚实的地基。",
    },
    "星星": {
        "en": "The Star",
        "situation": "你正处在一个疗愈和恢复的时期。经历了之前的动荡之后，你终于迎来了平静和希望。你内心的光芒正在重新亮起来，对未来充满了期待和信心。",
        "advice": "保持信念，你正在走向光明。这是许愿和规划未来的好时机。敞开心扉，让希望和灵感引导你前行。你的伤口正在愈合，美好的事情即将发生。",
    },
    "月亮": {
        "en": "The Moon",
        "situation": "你可能正处在迷茫和不安中，有些事情看不清真相，或者你被自己的恐惧和想象所困扰。夜晚最暗的时刻，也正是黎明前的最后一刻。",
        "advice": "不要被表面的幻象所迷惑。你所恐惧的事情，多半只是内心的投射。冷静下来，区分现实和想象。穿过这片迷雾，你会比之前更加清醒和强大。",
    },
    "太阳": {
        "en": "The Sun",
        "situation": "你正处于一个充满活力、快乐和成功的阶段！一切都在朝着好的方向发展，你的能量和自信感染着身边的人。这是收获认可和享受生活的好时候。",
        "advice": "尽情享受这段灿烂的时光，把你的快乐和温暖传递给更多人。不要因为太过顺利而掉以轻心，但也不要吝啬庆祝自己的成就。你是自己生命中的太阳。",
    },
    "审判": {
        "en": "Judgement",
        "situation": "你正在经历一次深层次的觉醒或召唤——也许是对过去的一次总结，或者你收到了一个让你重新审视人生的机会。你听到了内心深处「重新开始」的呼声。",
        "advice": "回应这个召唤，不要忽视内心的声音。这是一个清算过去、轻装上阵的时刻。原谅自己、接受过去，然后带着经验和智慧迈向新的阶段。",
    },
    "世界": {
        "en": "The World",
        "situation": "你正在完成一个重要的周期或目标，即将迎来圆满的结局。这是一段旅程的终点，同时也意味着你站在了更高层次的起点上。你的努力得到了回馈。",
        "advice": "庆祝你的成就，你值得这份圆满。但同时也要开始思考下一个目标——世界尽在你的掌握之中，你可以去任何想去的地方。完成感是最好的动力。",
    },
}


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
        description="随机抽取一张塔罗牌",
        pattern=r"^/塔罗$",
    )
    async def handle_tarot(self, stream_id: str = "", **kwargs) -> tuple:
        return await self._draw_card(stream_id)

    @Command(
        "tarot_long",
        description="通过特定短语触发塔罗牌抽取",
        pattern=r"^不属于这个时代的愚者[;；]雾之上的神秘主宰[;；]执掌好运的黄黑之王。请帮我抽一张塔罗牌$",
    )
    async def handle_tarot_long(self, stream_id: str = "", **kwargs) -> tuple:
        return await self._draw_card(stream_id)

    async def _draw_card(self, stream_id: str) -> tuple:
        card_name = random.choice(list(TAROT_CARDS.keys()))
        card = TAROT_CARDS[card_name]

        image_path = IMAGES_DIR / f"{card_name}.png"
        if image_path.exists():
            image_base64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
            await self.ctx.send.image(image_base64, stream_id)

        text = (
            f"你抽到了【{card_name}】（{card['en']}）\n\n"
            f"{card['situation']}\n\n"
            f"建议：{card['advice']}"
        )
        await self.ctx.send.text(text, stream_id)

        return True, f"已抽取 {card_name}", True


def create_plugin() -> TarotCardPlugin:
    return TarotCardPlugin()
