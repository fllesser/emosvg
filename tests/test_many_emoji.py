import time
import logging
from pathlib import Path

from PIL import Image, ImageFont

emoji_texts = """
表情
😀😁😂😃😄😅😆😉😊😋😎😍😘😗😙😚😇😐😑😶😏😣😥😮😯😪😫😴😌😛😜😝😒😓😔😕😲😷😖😞😟😤😢😭😦😧😨😬😰😱😳😵😡😠
人物
👦👧👨👩👴👵👶👱👮👲👳👷👸💂🎅👰👼💆💇🙍🙎🙅🙆💁🙋🙇🙌🙏👤👥🚶🏃👯💃👫👬👭💏💑👪
手势
💪👈👉👆👇✋👌👍👎✊👊👋👏👐
日常
👣👀👂👃👅👄💋👓👔👕👖👗👘👙👚👛👜👝🎒💼👞👟👠👡👢👑👒🎩🎓💄💅💍🌂
手机
📱📲📶📳📴☎📞📟📠
公共
♻🏧🚮🚰♿🚹🚺🚻🚼🚾⚠🚸⛔🚫🚳🚭🚯🚱🚷🔞💈
动物
🙈🙉🙊🐵🐒🐶🐕🐩🐺🐱😺😸😹😻😼😽🙀😿😾🐈🐯🐅🐆🐴🐎🐮🐂🐃🐄🐷🐖🐗🐽🐏🐑🐐🐪🐫🐘🐭🐁🐀🐹🐰🐇🐻🐨🐼🐾🐔🐓🐣🐤🐥🐦🐧🐸🐊🐢🐍🐲🐉🐳🐋🐬🐟🐠🐡🐙🐚🐌🐛🐜🐝🐞🦋
植物
💐🌸💮🌹🌺🌻🌼🌷🌱🌲🌳🌴🌵🌾🌿🍀🍁🍂🍃
自然
🌍🌎🌏🌐🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜☀🌝🌞⭐🌟🌠☁⛅☔⚡❄🔥💧🌊
饮食
🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍅🍆🌽🍄🌰🍞🍖🍗🍔🍟🍕🍳🍲🍱🍘🍙🍚🍛🍜🍝🍠🍢🍣🍤🍥🍡🍦🍧🍨🍩🍪🎂🍰🍫🍬🍭🍮🍯🍼☕🍵🍶🍷🍸🍹🍺🍻🍴
文体
🎪🎭🎨🎰🚣🛀🎫🏆⚽⚾🏀🏈🏉🎾🎱🎳⛳🎣🎽🎿🏂🏄🏇🏊🚴🚵🎯🎮🎲🎷🎸🎺🎻🎬
恐怖
😈👿👹👺💀☠👻👽👾💣
旅游
🌋🗻🏠🏡🏢🏣🏤🏥🏦🏨🏩🏪🏫🏬🏭🏯🏰💒🗼🗽⛪⛲🌁🌃🌆🌇🌉🌌🎠🎡🎢🚂🚃🚄🚅🚆🚇🚈🚉🚊🚝🚞🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚚🚛🚜🚲⛽🚨🚥🚦🚧⚓⛵🚤🚢✈💺🚁🚟🚠🚡🚀🎑🗿🛂🛃🛄🛅
物品
💌💎🔪💈🚪🚽🚿🛁⌛⏳⌚⏰🎈🎉🎊🎎🎏🎐🎀🎁📯📻📱📲☎📞📟📠🔋🔌💻💽💾💿📀🎥📺📷📹📼🔍🔎🔬🔭📡💡🔦🏮📔📕📖📗📘📙📚📓📃📜📄📰📑🔖💰💴💵💶💷💸💳✉📧📨📩📤📥📦📫📪📬📭📮✏✒📝📁📂📅📆📇📈📉📊📋📌📍📎📏📐✂🔒🔓🔏🔐🔑🔨🔫🔧🔩🔗💉💊🚬🔮🚩🎌💦💨
标志
♠♥♦♣🀄🎴🔇🔈🔉🔊📢📣💤💢💬💭♨🌀🔔🔕✡✝🔯📛🔰🔱⭕✅☑✔✖❌❎➕➖➗➰➿〽✳✴❇‼⁉❓❔❕❗©®™🎦🔅🔆💯🔠🔡🔢🔣🔤🅰🆎🅱🆑🆒🆓ℹ🆔Ⓜ🆕🆖🅾🆗🅿🆘🆙🆚🈁🈂🈷🈶🈯🉐🈹🈚🈲🉑🈸🈴🈳㊗㊙🈺🈵▪▫◻◼◽◾⬛⬜🔶🔷🔸🔹🔺🔻💠🔲🔳⚪⚫🔴🔵
生肖
🐁🐂🐅🐇🐉🐍🐎🐐🐒🐓🐕🐖
星座
♈♉♊♋♌♍♎♏♐♑♒♓⛎
钟表
🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦⌛⏳⌚⏰⏱⏲🕰
心形
💘❤💓💔💕💖💗💙💚💛💜💝💞💟❣
花草
💐🌸💮🌹🌺🌻🌼🌷🌱🌿🍀
树叶
🌿🍀🍁🍂🍃
月亮
🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜🌝
水果
🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓
钱币
💴💵💶💷💰💸💳
交通
🚂🚃🚄🚅🚆🚇🚈🚉🚊🚝🚞🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚚🚛🚜🚲⛽🚨🚥🚦🚧⚓⛵🚣🚤🚢✈💺🚁🚟🚠🚡🚀
建筑
🏠🏡🏢🏣🏤🏥🏦🏨🏩🏪🏫🏬🏭🏯🏰💒🗼🗽⛪🌆🌇🌉
办公
📱📲☎📞📟📠🔋🔌💻💽💾💿📀🎥📺📷📹📼🔍🔎🔬🔭📡📔📕📖📗📘📙📚📓📃📜📄📰📑🔖💳✉📧📨📩📤📥📦📫📪📬📭📮✏✒📝📁📂📅📆📇📈📉📊📋📌📍📎📏📐✂🔒🔓🔏🔐🔑
箭头
⬆↗➡↘⬇↙⬅↖↕↔↩↪⤴⤵🔃🔄🔙🔚🔛🔜🔝
"""


def test_many_emoji(font_path, cache_dir):
    import emosvg

    font = ImageFont.truetype(font_path, 24)
    # Wrap text into lines
    lines = emosvg.wrap_text(emoji_texts, font, max_width=1000)

    with Image.new("RGB", (1000, 2100), (255, 248, 220)) as image:  # 纸黄背景
        start = time.time()
        emosvg.text_with_wrapped(
            image,
            (10, 10),
            lines,
            font,
            fill=(0, 0, 0),
        )
        end = time.time()
        logging.info(f"[svg] Cont: {end - start:.2f} seconds")
        image.save(cache_dir / "many_emoji.png")


# import pytest


# @pytest.mark.asyncio
# async def test_many_emoji_with_apilmoji(font_path, cache_dir):
#     from PIL import Image, ImageFont
#     from apilmoji import Apilmoji, EmojiStyle, EmojiCDNSource

#     font = ImageFont.truetype(font_path, 24)
#     source = EmojiCDNSource(
#         cache_dir=cache_dir, style=EmojiStyle.FACEBOOK, enable_tqdm=True
#     )
#     with Image.new("RGB", (3000, 2100), (255, 248, 220)) as image:  # 纸黄背景
#         start = time.time()
#         await Apilmoji.text(
#             image, (10, 10), emoji_texts, font, fill=(0, 0, 0), source=source
#         )
#         end = time.time()
#         logging.info(f"[apilmoji] Cont: {end - start:.2f} seconds")
#         image.save(cache_dir / "many_emoji_async.png")


emoji_texts2 = "#⃣0⃣1⃣2⃣3⃣4⃣5⃣6⃣7⃣8⃣9⃣emoji_u002a_20e3©®‼⁉™ℹ↔↕↖↗↘↙↩↪⌚⌛⌨⏏⏩⏪⏫⏬⏭⏮⏯⏰⏱⏲⏳⏸⏹⏺Ⓜ▪▫▶◀◻◼◽◾☀☁☂☃☄☎☑☔☕☘☝☝🏻☝🏼☝🏽☝🏾☝🏿☠☢☣☦☪☮☯☸☹☺♀♂♈♉♊♋♌♍♎♏♐♑♒♓♟♠♣♥♦♨♻♾♿⚒⚓⚔⚕⚖⚗⚙⚛⚜⚠⚡⚧⚪⚫⚰⚱⚽⚾⛄⛅⛈⛎⛏⛑⛓⛔⛩⛪⛰⛱⛲⛳⛴⛵⛷⛸⛹⛹‍♀⛹‍♂⛹🏻⛹🏻‍♀⛹🏻‍♂⛹🏼⛹🏼‍♀⛹🏼‍♂⛹🏽⛹🏽‍♀⛹🏽‍♂⛹🏾⛹🏾‍♀⛹🏾‍♂⛹🏿⛹🏿‍♀⛹🏿‍♂⛺⛽✂✅✈✉✊✊🏻✊🏼✊🏽✊🏾✊🏿✋✋🏻✋🏼✋🏽✋🏾✋🏿✌✌🏻✌🏼✌🏽✌🏾✌🏿✍✍🏻✍🏼✍🏽✍🏾✍🏿✏✒✔✖✝✡✨✳✴❄❇❌❎❓❔❕❗❣❤❤‍🔥❤‍🩹➕➖➗➡➰➿⤴⤵⬅⬆⬇⬛⬜⭐⭕〰〽㊗㊙🀄🃏🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅🌆🌇🌈🌉🌊🌋🌌🌍🌎🌏🌐🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜🌝🌞🌟🌠🌡🌤🌥🌦🌧🌨🌩🌪🌫🌬🌭🌮🌯🌰🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🍽🍾🍿🎀🎁🎂🎃🎄🎅🎅🏻🎅🏼🎅🏽🎅🏾🎅🏿🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎖🎗🎙🎚🎛🎞🎟🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏂🏻🏂🏼🏂🏽🏂🏾🏂🏿🏃🏃‍♀🏃‍♂🏃🏻🏃🏻‍♀🏃🏻‍♂🏃🏼🏃🏼‍♀🏃🏼‍♂🏃🏽🏃🏽‍♀🏃🏽‍♂🏃🏾🏃🏾‍♀🏃🏾‍♂🏃🏿🏃🏿‍♀🏃🏿‍♂🏄🏄‍♀🏄‍♂🏄🏻🏄🏻‍♀🏄🏻‍♂🏄🏼🏄🏼‍♀🏄🏼‍♂🏄🏽🏄🏽‍♀🏄🏽‍♂🏄🏾🏄🏾‍♀🏄🏾‍♂🏄🏿🏄🏿‍♀🏄🏿‍♂🏅🏆🏇🏇🏻🏇🏼🏇🏽🏇🏾🏇🏿🏈🏉🏊🏊‍♀🏊‍♂🏊🏻🏊🏻‍♀🏊🏻‍♂🏊🏼🏊🏼‍♀🏊🏼‍♂🏊🏽🏊🏽‍♀🏊🏽‍♂🏊🏾🏊🏾‍♀🏊🏾‍♂🏊🏿🏊🏿‍♀🏊🏿‍♂🏋🏋‍♀🏋‍♂🏋🏻🏋🏻‍♀🏋🏻‍♂🏋🏼🏋🏼‍♀🏋🏼‍♂🏋🏽🏋🏽‍♀🏋🏽‍♂🏋🏾🏋🏾‍♀🏋🏾‍♂🏋🏿🏋🏿‍♀🏋🏿‍♂🏌🏌‍♀🏌‍♂🏌🏻🏌🏻‍♀🏌🏻‍♂🏌🏼🏌🏼‍♀🏌🏼‍♂🏌🏽🏌🏽‍♀🏌🏽‍♂🏌🏾🏌🏾‍♀🏌🏾‍♂🏌🏿🏌🏿‍♀🏌🏿‍♂🏍🏎🏏🏐🏑🏒🏓🏔🏕🏖🏗🏘🏙🏚🏛🏜🏝🏞🏟🏠🏡🏢🏣🏤🏥🏦🏧🏨🏩🏪🏫🏬🏭🏮🏯🏰🏳🏳‍⚧🏳‍🌈🏴🏴‍☠🏵🏾🏿🐀🐁🐂🐃🐄🐅🐆🐇🐈🐈‍⬛🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐕‍🦺🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐻‍❄🐼🐽🐾🐿👀👁👁‍🗨👂👂🏻👂🏼👂🏽👂🏾👂🏿👃👃🏻👃🏼👃🏽👃🏾👃🏿👄👅👆👆🏻👆🏼👆🏽👆🏾👆🏿👇👇🏻👇🏼👇🏽👇🏾👇🏿👈👈🏻👈🏼👈🏽👈🏾👈🏿👉👉🏻👉🏼👉🏽👉🏾👉🏿👊👊🏻👊🏼👊🏽👊🏾👊🏿👋👋🏻👋🏼👋🏽👋🏾👋🏿👌👌🏻👌🏼👌🏽👌🏾👌🏿👍👍🏻👍🏼👍🏽👍🏾👍🏿👎👎🏻👎🏼👎🏽👎🏾👎🏿👏👏🏻👏🏼👏🏽👏🏾👏🏿👐👐🏻👐🏼👐🏽👐🏾👐🏿👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥👦👦🏻👦🏼👦🏽👦🏾👦🏿👧👧🏻👧🏼👧🏽👧🏾👧🏿👨👨‍⚕👨‍⚖👨‍✈👨‍❤‍👨👨‍❤‍💋‍👨👨‍🌾👨‍🍳👨‍🍼👨‍🎓👨‍🎤👨‍🎨👨‍🏫👨‍🏭👨‍👦👨‍👦‍👦👨‍👧👨"  # noqa: E501


def test_many_emoji2(lxgw_font_path: Path, cache_dir: Path):
    import emosvg

    width = 500
    font = ImageFont.truetype(lxgw_font_path, 24)
    lines = emosvg.wrap_text(emoji_texts2, font, width)
    height = len(lines) * emosvg.get_font_height(font)
    image = Image.new("RGB", (width, height), (255, 255, 255))
    emosvg.text_with_wrapped(image, (10, 10), lines, font, fill=(0, 0, 0))
    image.save(cache_dir / "test_many_emoji2.png")


multi_line_text = """
这篇文章看完 立刻想起某人🐷和我聊过达尔文进化论  霍金天体物理黑洞辐射 到现在马斯克的人机接口
再回头看一遍《普罗米修斯》中文版 有了新的理解 不枉我上映当天在新加坡电影院看了2.5小时原声（同学都睡着了）
《超验骇客》德普的，也会觉得没那么不可思议 灵魂可以永生了 脑电波 💻控制all
甚至再看一遍裘·德洛《人工智能》[苦涩]留住一缕头发 可以再见亲人
还有《第五元素》DNA复制人可以 快速🔜学习语言与各种知识
但都离不开要学习📑 下一代有多需要学习力
"""  # noqa: E501


def test_multi_line_text(font_path: Path, cache_dir: Path):
    import emosvg

    width = 300
    font = ImageFont.truetype(font_path, 24)
    lines = emosvg.wrap_text(multi_line_text, font, width)
    height = len(lines) * emosvg.get_font_height(font)
    image = Image.new("RGB", (width, height), (255, 255, 255))
    emosvg.text_with_wrapped(image, (0, 10), lines, font, fill=(0, 0, 0))
    image.save(cache_dir / "test_multi_line_text.png")
