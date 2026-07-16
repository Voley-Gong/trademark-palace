# -*- coding: utf-8 -*-
"""Insert trademark 1F ownership floor into palace JSON and refresh article refs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "data" / "trademark-palace.json"
PUB = ROOT / "trademark-palace-web" / "public" / "data" / "trademark-palace.json"

NEW_ARTICLES = {
    "3": {
        "label": "第三条",
        "text": "经商标局核准注册的商标为注册商标，包括商品商标、服务商标和集体商标、证明商标；商标注册人享有商标专用权，受法律保护。\n\n本法所称集体商标，是指以团体、协会或者其他组织名义注册，供该组织成员在商事活动中使用，以表明使用者在该组织中的成员资格的标志。\n\n本法所称证明商标，是指由对某种商品或者服务具有监督能力的组织所控制，而由该组织以外的单位或者个人使用于其商品或者服务，用以证明该商品或者服务的原产地、原料、制造方法、质量或者其他特定品质的标志。\n\n集体商标、证明商标注册和管理的特殊事项，由国务院工商行政管理部门规定。",
    },
    "4": {
        "label": "第四条",
        "text": "自然人、法人或者其他组织在生产经营活动中，对其商品或者服务需要取得商标专用权的，应当向商标局申请商标注册。不以使用为目的的恶意商标注册申请，应当予以驳回。\n\n本法有关商品商标的规定，适用于服务商标。",
    },
    "7": {
        "label": "第七条",
        "text": "申请注册和使用商标，应当遵循诚实信用原则。\n\n商标使用人应当对其使用商标的商品质量负责。各级工商行政管理部门应当通过商标管理，制止欺骗消费者的行为。",
    },
    "8": {
        "label": "第八条",
        "text": "任何能够将自然人、法人或者其他组织的商品与他人的商品区别开的标志，包括文字、图形、字母、数字、三维标志、颜色组合和声音等，以及上述要素的组合，均可以作为商标申请注册。",
    },
    "9": {
        "label": "第九条",
        "text": "申请注册的商标，应当有显著特征，便于识别，并不得与他人在先取得的合法权利相冲突。\n\n商标注册人有权标明“注册商标”或者注册标记。",
    },
    "10": {
        "label": "第十条",
        "text": "下列标志不得作为商标使用：\n（一）同中华人民共和国的国家名称、国旗、国徽、国歌、军旗、军徽、军歌、勋章等相同或者近似的，以及同中央国家机关的名称、标志、所在地特定地点的名称或者标志性建筑物的名称、图形相同的；\n（二）同外国的国家名称、国旗、国徽、军旗等相同或者近似的，但经该国政府同意的除外；\n（三）同政府间国际组织的名称、旗帜、徽记等相同或者近似的，但经该组织同意或者不易误导公众的除外；\n（四）与表明实施控制、予以保证的官方标志、检验印记相同或者近似的，但经授权的除外；\n（五）同“红十字”、“红新月”的名称、标志相同或者近似的；\n（六）带有民族歧视性的；\n（七）带有欺骗性，容易使公众对商品的质量等特点或者产地产生误认的；\n（八）有害于社会主义道德风尚或者有其他不良影响的。\n\n县级以上行政区划的地名或者公众知晓的外国地名，不得作为商标。但是，地名具有其他含义或者作为集体商标、证明商标组成部分的除外；已经注册的使用地名的商标继续有效。",
    },
    "11": {
        "label": "第十一条",
        "text": "下列标志不得作为商标注册：\n（一）仅有本商品的通用名称、图形、型号的；\n（二）仅直接表示商品的质量、主要原料、功能、用途、重量、数量及其他特点的；\n（三）其他缺乏显著特征的。\n\n前款所列标志经过使用取得显著特征，并便于识别的，可以作为商标注册。",
    },
    "12": {
        "label": "第十二条",
        "text": "以三维标志申请注册商标的，仅由商品自身的性质产生的形状、为获得技术效果而需有的商品形状或者使商品具有实质性价值的形状，不得注册。",
    },
    "15": {
        "label": "第十五条",
        "text": "未经授权，代理人或者代表人以自己的名义将被代理人或者被代表人的商标进行注册，被代理人或者被代表人提出异议的，不予注册并禁止使用。\n\n就同一种商品或者类似商品申请注册的商标与他人在先使用的未注册商标相同或者近似，申请人与该他人具有前款规定以外的合同、业务往来关系或者其他关系而明知该他人商标存在，该他人提出异议的，不予注册。",
    },
    "31": {
        "label": "第三十一条",
        "text": "两个或者两个以上的商标注册申请人，在同一种商品或者类似商品上，以相同或者近似的商标申请注册的，初步审定并公告申请在先的商标；同一天申请的，初步审定并公告使用在先的商标，驳回其他人的申请，不予公告。",
    },
    "32": {
        "label": "第三十二条",
        "text": "申请商标注册不得损害他人现有的在先权利，也不得以不正当手段抢先注册他人已经使用并有一定影响的商标。",
    },
    "39": {
        "label": "第三十九条",
        "text": "注册商标的有效期为十年，自核准注册之日起计算。",
    },
    "40": {
        "label": "第四十条",
        "text": "注册商标有效期满，需要继续使用的，商标注册人应当在期满前十二个月内按照规定办理续展手续；在此期间未能办理的，可以给予六个月的宽展期。每次续展注册的有效期为十年，自该商标上一届有效期满次日起计算。期满未办理续展手续的，注销其注册商标。\n\n商标局应当对续展注册的商标予以公告。",
    },
    "42": {
        "label": "第四十二条",
        "text": "转让注册商标的，转让人和受让人应当签订转让协议，并共同向商标局提出申请。受让人应当保证使用该注册商标的商品质量。\n\n转让注册商标的，商标注册人对其在同一种商品上注册的近似的商标，或者在类似商品上注册的相同或者近似的商标，应当一并转让。\n\n对容易导致混淆或者有其他不良影响的转让，商标局不予核准，书面通知申请人并说明理由。\n\n转让注册商标经核准后，予以公告。受让人自公告之日起享有商标专用权。",
    },
    "43": {
        "label": "第四十三条",
        "text": "商标注册人可以通过签订商标使用许可合同，许可他人使用其注册商标。许可人应当监督被许可人使用其注册商标的商品质量。被许可人应当保证使用该注册商标的商品质量。\n\n经许可使用他人注册商标的，必须在使用该注册商标的商品上标明被许可人的名称和商品产地。\n\n许可他人使用其注册商标的，许可人应当将其商标使用许可报商标局备案，由商标局公告。商标使用许可未经备案不得对抗善意第三人。",
    },
}

FLOOR_1F = {
    "id": "trademark-1F-ownership",
    "level": 1,
    "name": "权属与客体层",
    "mission": "权利是否存在、客体是否适格、权属与处分链条是否清楚",
    "mapAscii": "O1-O2 → O3..O7 → O8-O10 → O11-O13 → 楼梯→3F",
    "commuteMinutes": 10,
    "rooms": [
        {
            "id": "O1",
            "order": 1,
            "zone": "lobby",
            "title": "注册专用权厅",
            "article": "3",
            "articleLabel": "第3条",
            "articleRefs": ["3"],
            "relatedArticleRefs": ["4", "56"],
            "space": "大厅中央注册证铜匣，匣盖刻核准=专用权",
            "senses": ["铜匣冰凉", "启封咔一声"],
            "sceneHook": "未注册有没有专用权？集体/证明商标如何定性？",
            "oral30s": "经商标局核准注册的商标为注册商标，包括商品商标、服务商标和集体商标、证明商标；商标注册人享有商标专用权，受法律保护。",
            "elements": ["核准注册", "注册人", "专用权受保护", "分清商标类型"],
            "exceptions": [],
            "caseAnchor": ["注册取得", "专用权起点", "类型分流"],
            "links": ["O2", "P1", "O11"],
            "peg": 1,
            "drillPrompt": "商标专用权因什么行政行为产生？",
        },
        {
            "id": "O2",
            "order": 2,
            "zone": "lobby",
            "title": "申请入口",
            "article": "4",
            "articleLabel": "第4条",
            "articleRefs": ["4"],
            "relatedArticleRefs": ["7", "3"],
            "space": "申请窗口，上方红灯写恶意驳回",
            "senses": ["排队嘈杂", "红灯刺眼"],
            "sceneHook": "囤积抢注、不以使用为目的的批量申请",
            "oral30s": "生产经营中需要取得专用权的，应当向商标局申请注册。不以使用为目的的恶意商标注册申请，应当予以驳回。商品商标规定适用于服务商标。",
            "elements": ["申请主体适格", "生产经营需要", "恶意不以使用为目的应驳回"],
            "exceptions": [],
            "caseAnchor": ["恶意申请", "使用目的", "驳回"],
            "links": ["O1", "O8", "O9"],
            "peg": None,
            "drillPrompt": "第4条新增的驳回红线八个字核心是什么？",
        },
        {
            "id": "O3",
            "order": 3,
            "zone": "object",
            "title": "标志仓库",
            "article": "8",
            "articleLabel": "第8条",
            "articleRefs": ["8"],
            "relatedArticleRefs": ["9"],
            "space": "文字图形字母数字立体颜色声音货架",
            "senses": ["金属货架碰撞", "声音标短促一响"],
            "sceneHook": "非传统商标、组合标志能否区别来源",
            "oral30s": "任何能够将自然人、法人或其他组织的商品与他人的商品区别开的标志，包括文字、图形、字母、数字、三维标志、颜色组合和声音等以及组合，均可以作为商标申请注册。",
            "elements": ["来源区别可能性", "法定要素或组合"],
            "exceptions": [],
            "caseAnchor": ["可注册标志", "来源区别", "非传统商标"],
            "links": ["O4"],
            "peg": None,
            "drillPrompt": "第8条真正卡的是「要素清单」还是「区别来源」？",
        },
        {
            "id": "O4",
            "order": 4,
            "zone": "object",
            "title": "显著总纲门",
            "article": "9",
            "articleLabel": "第9条",
            "articleRefs": ["9"],
            "relatedArticleRefs": ["10", "11", "32"],
            "space": "双扇门：显著特征 / 不得与在先权利冲突",
            "senses": ["双手同时推门"],
            "sceneHook": "描述性标志又撞别人字号或著作权",
            "oral30s": "申请注册的商标应当有显著特征、便于识别，并不得与他人在先取得的合法权利相冲突。注册人有权标明注册商标或注册标记。",
            "elements": ["显著特征便于识别", "不与在先权利冲突"],
            "exceptions": [],
            "caseAnchor": ["显著+在先", "双门槛"],
            "links": ["O5", "O6", "O9"],
            "peg": None,
            "drillPrompt": "第9条两扇门分别挡住什么风险？",
        },
        {
            "id": "O5",
            "order": 5,
            "zone": "object",
            "title": "禁用红线柜",
            "article": "10",
            "articleLabel": "第10条",
            "articleRefs": ["10"],
            "relatedArticleRefs": ["11"],
            "space": "上锁红柜：国旗国徽官方标志欺骗性不良影响地名",
            "senses": ["红漆刺鼻", "柜锁冰冷"],
            "sceneHook": "国名国旗近似、欺骗性、行政区划地名",
            "oral30s": "若干标志不得作为商标使用；县级以上行政区划地名或公众知晓的外国地名原则上不得作为商标，但有例外。禁用是使用禁令，不只是不给注册。",
            "elements": ["落入禁用清单", "地名原则禁止及例外"],
            "exceptions": ["地名其他含义或集体/证明商标组成部分等例外"],
            "caseAnchor": ["禁用标志", "使用禁令", "地名例外"],
            "links": ["O6"],
            "peg": None,
            "drillPrompt": "第10条与第11条差在「不得使用」还是「不得注册」？",
        },
        {
            "id": "O6",
            "order": 6,
            "zone": "object",
            "title": "禁注三格",
            "article": "11",
            "articleLabel": "第11条",
            "articleRefs": ["11"],
            "relatedArticleRefs": ["9", "59"],
            "space": "三格柜：通用名称、直接描述、其他缺乏显著；底屉第二含义",
            "senses": ["抽屉磨砂使用痕迹"],
            "sceneHook": "纯描述、通用名、用出来了显著性",
            "oral30s": "仅通用名称图形型号，或仅直接表示质量原料功能等，或其他缺乏显著特征的，不得注册；经过使用取得显著特征并便于识别的，可以作为商标注册。",
            "elements": ["三类缺乏显著", "使用取得显著的例外"],
            "exceptions": ["第二含义可注册"],
            "caseAnchor": ["缺乏显著", "第二含义", "仍可注"],
            "links": ["O4", "S2"],
            "peg": None,
            "drillPrompt": "缺乏显著的标志怎样才能跨过第11条？",
        },
        {
            "id": "O7",
            "order": 7,
            "zone": "object",
            "title": "立体禁注角",
            "article": "12",
            "articleLabel": "第12条",
            "articleRefs": ["12"],
            "relatedArticleRefs": ["59"],
            "space": "三个不得注册的立体模型：性质、技术效果、实质价值",
            "senses": ["模型棱角硌手"],
            "sceneHook": "产品外形、技术必需形状、实质价值形状",
            "oral30s": "以三维标志申请注册商标的，仅由商品自身性质产生的形状、为获得技术效果而需有的商品形状或者使商品具有实质性价值的形状，不得注册。",
            "elements": ["性质产生的形状", "技术效果所需形状", "实质价值形状"],
            "exceptions": [],
            "caseAnchor": ["功能性排除", "立体商标"],
            "links": ["S2"],
            "peg": None,
            "drillPrompt": "立体商标三条功能性排除分别防什么？",
        },
        {
            "id": "O8",
            "order": 8,
            "zone": "conflict",
            "title": "抢注暗室",
            "article": "15",
            "articleLabel": "第15条",
            "articleRefs": ["15"],
            "relatedArticleRefs": ["32", "4"],
            "space": "昏暗签约室：代理人名片与注册证叠放",
            "senses": ["纸张摩挲", "门锁咔哒"],
            "sceneHook": "代理抢注；业务往来中明知未注册商标却申请",
            "oral30s": "代理人或代表人以自己名义将被代理人商标注册，被异议的，不予注册并禁止使用。同种或类似商品上，申请人因合同业务等关系明知他人在先未注册商标存在而申请，被异议的，不予注册。",
            "elements": ["代理代表关系", "或合同业务等关系明知", "异议后不予注册"],
            "exceptions": [],
            "caseAnchor": ["代理抢注", "关系人明知", "禁止使用"],
            "links": ["O9", "O2"],
            "peg": None,
            "drillPrompt": "第15条两款分别盯住哪两类「关系人」？",
        },
        {
            "id": "O9",
            "order": 9,
            "zone": "conflict",
            "title": "在先权利墙",
            "article": "32",
            "articleLabel": "第32条",
            "articleRefs": ["32"],
            "relatedArticleRefs": ["9", "15", "59"],
            "space": "石墙嵌著作权姓名字号等铭牌，墙角小龛有一定影响",
            "senses": ["石墙凉意", "铭牌叮当"],
            "sceneHook": "撞著作权姓名字号；抢注已使用并有一定影响的未注册商标",
            "oral30s": "申请商标注册不得损害他人现有的在先权利，也不得以不正当手段抢先注册他人已经使用并有一定影响的商标。",
            "elements": ["在先权利存在", "或在先使用+一定影响+不正当抢注"],
            "exceptions": [],
            "caseAnchor": ["在先权利", "抢注一定影响", "不正当手段"],
            "links": ["O4", "O8", "S2"],
            "peg": None,
            "drillPrompt": "第32条后半句「一定影响」保护的是注册商标还是未注册使用？",
        },
        {
            "id": "O10",
            "order": 10,
            "zone": "conflict",
            "title": "申请在先钟",
            "article": "31",
            "articleLabel": "第31条",
            "articleRefs": ["31"],
            "relatedArticleRefs": ["32"],
            "space": "挂钟停在申请日，旁铃同日使用在先",
            "senses": ["钟摆声", "同日铃声叮"],
            "sceneHook": "两个近似商标撞车谁先申请",
            "oral30s": "同一种或类似商品上以相同或近似商标多人申请的，初步审定并公告申请在先的商标；同一天申请的，初步审定并公告使用在先的商标，驳回其他人的申请。",
            "elements": ["申请在先原则", "同日申请看使用在先"],
            "exceptions": [],
            "caseAnchor": ["申请在先", "同日使用在先"],
            "links": ["O9"],
            "peg": None,
            "drillPrompt": "同日申请时，第31条看的是申请日还是使用事实？",
        },
        {
            "id": "O11",
            "order": 11,
            "zone": "dispose",
            "title": "十年续展台",
            "article": "39",
            "articleLabel": "第39、40条",
            "articleRefs": ["39", "40"],
            "relatedArticleRefs": ["3"],
            "space": "巨日历写十年；左12个月续展窗，右6个月宽展铃",
            "senses": ["翻日历沙沙", "宽展铃轻响"],
            "sceneHook": "权利是否仍有效、过期未续展、宽展期内补办",
            "oral30s": "注册商标有效期十年，自核准注册之日起计算。期满继续使用应在期满前十二个月办理续展；未办可有六个月宽展；每次续展十年；期满未续展注销。",
            "elements": ["有效期十年", "期满前十二个月续展", "六个月宽展", "未续展注销"],
            "exceptions": [],
            "caseAnchor": ["十年有效", "续展宽展", "注销"],
            "links": ["O1", "P1"],
            "peg": None,
            "drillPrompt": "用三个数字说完续展窗口：有效期、办理期、宽展期。",
        },
        {
            "id": "O12",
            "order": 12,
            "zone": "dispose",
            "title": "转让柜",
            "article": "42",
            "articleLabel": "第42条",
            "articleRefs": ["42"],
            "relatedArticleRefs": ["43", "3"],
            "space": "双人签字柜，捆绳勒着应一并转让的近似商标",
            "senses": ["捆绳勒手"],
            "sceneHook": "只转主标不转近似标；转让是否导致混淆",
            "oral30s": "转让须签订协议并共同申请；受让人保证商品质量；同一种商品上的近似商标或类似商品上的相同近似商标应一并转让；易混淆或不良影响的不予核准；核准公告后受让人自公告之日起享有专用权。",
            "elements": ["协议共同申请", "一并转让", "公告日起权属", "质量保证"],
            "exceptions": ["易混淆或不良影响不予核准"],
            "caseAnchor": ["一并转让", "公告日起权属", "质量保证"],
            "links": ["O13", "O1"],
            "peg": None,
            "drillPrompt": "受让人从哪一天起享有商标专用权？",
        },
        {
            "id": "O13",
            "order": 13,
            "zone": "dispose",
            "title": "许可窗",
            "article": "43",
            "articleLabel": "第43条",
            "articleRefs": ["43"],
            "relatedArticleRefs": ["42"],
            "space": "玻璃窗后挂许可合同，便签写备案对抗",
            "senses": ["玻璃反光", "便签胶粘手"],
            "sceneHook": "被许可人能否起诉、未备案、商品未标名称产地",
            "oral30s": "可通过许可合同许可他人使用；许可人监督质量，被许可人保证质量；商品上须标明被许可人名称和产地；许可应报商标局备案公告；未经备案不得对抗善意第三人。",
            "elements": ["许可合同", "质量义务与标注", "备案公告", "未经备案不得对抗善意第三人"],
            "exceptions": [],
            "caseAnchor": ["许可备案", "对抗善意第三人", "质量与标注"],
            "links": ["O12"],
            "peg": None,
            "drillPrompt": "许可未备案的法律效果一句话怎么说？",
        },
    ],
}


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    data["schemaVersion"] = 3
    data["description"] = (
        "知产律所实习用：1F权属客体 + 3F侵权认定 + 4F救济。通勤口述与网页 PalaceRoom/LawNode 共用。"
    )
    data["docs"] = [
        "docs/商标法-权属客体层-记忆宫殿.md",
        "docs/商标法-侵权认定层-记忆宫殿.md",
        "docs/商标法-救济层-记忆宫殿.md",
    ]

    articles = data.setdefault("articles", {})
    articles.update(NEW_ARTICLES)

    # number peg: add 十年 / 宽展提示
    for peg in data.get("numberPegs", []):
        if peg["n"] == 1 and "3专用权因注册" not in peg["bindings"]:
            peg["bindings"] = ["3注册专用权", *peg["bindings"]]
            refs = peg.setdefault("articleRefs", [])
            if "3" not in refs:
                refs.insert(0, "3")
        if peg["n"] == 0:
            pass
    # ensure peg  for 10-year via binding on a note in peg 1 already; add to peg list a soft binding on n=1 for decade
    for peg in data.get("numberPegs", []):
        if peg["n"] == 1 and "39有效期十年" not in peg["bindings"]:
            peg["bindings"].append("39有效期十年（谐音联想：独占十年）")
            if "39" not in peg["articleRefs"]:
                peg["articleRefs"].append("39")

    floors = data.get("floors", [])
    floors = [f for f in floors if f.get("id") != FLOOR_1F["id"]]
    # keep order: 1F, 3F, 4F
    data["floors"] = [FLOOR_1F] + floors

    # fiveQuestions: enrich q1/q2 with ownership rooms
    for q in data.get("fiveQuestions", []):
        if q["id"] == "q1":
            q["floorHint"] = "1F+3F"
            hints = q.get("roomHints", [])
            for rid in ["O1", "O9"]:
                if rid not in hints:
                    hints.insert(0, rid)
            q["roomHints"] = hints
        if q["id"] == "q2":
            q["floorHint"] = "1F"
            q["roomHints"] = ["O1", "O4", "O9", "O11", "E1"]

    # commute drill for 1F
    drills = data.setdefault("drills", [])
    drills = [d for d in drills if d.get("id") != "drill-commute-1f"]
    drills.insert(
        0,
        {
            "id": "drill-commute-1f",
            "name": "1F通勤10分钟",
            "floorId": "trademark-1F-ownership",
            "steps": [r["id"] for r in FLOOR_1F["rooms"]],
        },
    )
    data["drills"] = drills

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    SRC.write_text(text, encoding="utf-8")
    PUB.parent.mkdir(parents=True, exist_ok=True)
    PUB.write_text(text, encoding="utf-8")
    print("1F rooms:", len(FLOOR_1F["rooms"]))
    print("floors:", [f["level"] for f in data["floors"]])
    print("articles:", len(data["articles"]))


if __name__ == "__main__":
    main()
