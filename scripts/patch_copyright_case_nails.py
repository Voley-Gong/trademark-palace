# -*- coding: utf-8 -*-
"""Patch copyright palace: collective management + game expression case nails."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def room(**kwargs):
    kwargs.setdefault("exceptions", [])
    kwargs.setdefault("classicCases", [])
    kwargs.setdefault("peg", None)
    kwargs.setdefault("crossTrademark", None)
    kwargs.setdefault("crossPatent", None)
    kwargs.setdefault("crossCopyright", None)
    return kwargs


def art(label, text, plain, examples, apply):
    return {
        "label": label,
        "text": text,
        "plain": plain,
        "examples": examples,
        "apply": apply,
    }


def add_link(r, target):
    links = r.setdefault("links", [])
    if target not in links:
        links.append(target)


def main():
    path = ROOT / "docs" / "data" / "copyright-palace.json"
    pub = ROOT / "trademark-palace-web" / "public" / "data" / "copyright-palace.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    articles = data.setdefault("articles", {})
    articles.update(
        {
            "cmo-2": art(
                "集体管理条例·第2条",
                "本条例所称著作权集体管理，是指著作权集体管理组织经权利人授权，集中行使权利人的有关权利并以自己的名义进行的下列活动：（一）与使用者订立著作权或者与著作权有关的权利许可使用合同；（二）向使用者收取使用费；（三）向权利人转付使用费；（四）进行涉及著作权或者与著作权有关的权利的诉讼、仲裁等。",
                "集体管理四件事：订许可、收使用费、转付权利人、以自己名义诉讼仲裁。",
                ["音著协就背景音乐批量许可并起诉未获授权的歌厅"],
                "B0·B15；上接 T2",
            ),
            "cmo-standing": art(
                "集体管理诉讼资格口径",
                "（学习汇编）著作权法第八条：依法设立的著作权集体管理组织被授权后，可以自己的名义为权利人主张权利，并可作为当事人参加诉讼、仲裁、调解。民事司法解释：依法成立的著作权集体管理组织根据著作权人的书面授权以自己名义提起诉讼的，人民法院应当受理。前提是授权真实有效、管理权利范围覆盖争议权项；组织本身通常不享有原始著作权。我国现行法未普遍确立延伸性集体管理，一揽子许可不当然覆盖非会员全部作品，使用者仍可能面临非会员维权风险。",
                "书面授权+自己名义可起诉；非延伸管理：一揽子≠全网无死角。",
                ["只拿了会员曲库授权，却用了非会员热歌被诉"],
                "B0·B15",
            ),
            "game-expression": art(
                "游戏规则与表达边界口径",
                "（学习汇编）著作权保护具有独创性的表达，不保护思想、操作方法、玩法规则、数值体系、通用交互模式本身。游戏案件先过滤：规则/玩法/抽象系统 → 思想侧；美术角色场景、文案对白、音乐音效、有独创性的关卡具体编排、计算机软件代码等 → 表达侧，再做接触+实质性相似。玩法高度相似但具体视听与代码表达不同的，著作权常难成立，可评估不正当竞争（数据抓取、仿冒装潢、虚假宣传等）是否另开竞争馆绿灯。",
                "规则玩法不进仓；美术文案音乐代码关卡表达才比对；玩法像可改亮竞争馆。",
                ["两款消除类玩法相同但素材与关卡编排不同 → 先过思想表达关"],
                "B0·B16；上接 O2/R1/S4；跨竞争馆",
            ),
        }
    )

    floors = {f["id"]: f for f in data["floors"]}
    b0 = floors["copyright-B0-ordinances"]
    b0["mapAscii"] = (
        "B1-B8条例 → B9-B14司法解释 → B15集体管理 → B16游戏表达边界"
    )
    b0["commuteMinutes"] = 18
    b0["mission"] = (
        "软件/网络条例 + 民事与网传司法解释 + 集体管理细则 + 游戏表达边界随案补丁"
    )

    existing = {r["id"] for r in b0["rooms"]}
    new_rooms = [
        room(
            id="B15",
            order=15,
            zone="case",
            title="集体管理细则后室",
            article="cmo-2",
            articleLabel="集管条例·诉讼资格",
            articleRefs=["cmo-2", "cmo-standing", "8"],
            relatedArticleRefs=["26", "10"],
            space="四扇柜：订许可、收使用费、转付、诉讼仲裁；墙上书面授权章；侧签非延伸管理警示",
            senses=["授权书撕联", "转付清单打印机"],
            sceneHook="音著协起诉歌厅；使用者称已买一揽子许可却仍被非会员诉",
            oral30s="集体管理经权利人授权，以自己名义做四件事：订许可、收使用费、转付权利人、诉讼仲裁。有书面授权的，可以自己名义起诉。组织不享有原始著作权，授权范围要盖住争议权项。现行法未普遍实行延伸性集体管理，一揽子许可不当然覆盖非会员作品。",
            elements=[
                "四件事",
                "自己名义起诉",
                "书面授权",
                "转付使用费",
                "非延伸管理风险",
            ],
            caseAnchor=["自己名义", "书面授权", "一揽子≠全覆盖"],
            links=["T2", "O4", "F1", "N1"],
            drillPrompt="使用者向集体管理组织买了包年一揽子许可，是否必然不会被非会员权利人起诉？",
            classicCases=[
                {
                    "name": "集体管理一揽子许可与非会员维权典型实践",
                    "hook": "非延伸管理",
                    "takeaway": "办案先核：授权曲目/权项是否覆盖；别迷信一揽子万能。",
                }
            ],
        ),
        room(
            id="B16",
            order=16,
            zone="case",
            title="游戏规则与表达边界柜",
            article="game-expression",
            articleLabel="游戏表达边界",
            articleRefs=["game-expression", "3"],
            relatedArticleRefs=["10", "soft-6", "soft-29"],
            space="双区货架：左红封「规则玩法数值」；右可诉「美术文案音乐代码关卡表达」；侧门通往竞争馆",
            senses=["手柄震动", "荧光笔分拣"],
            sceneHook="对手抄了玩法和经济系统，素材看起来也有点像",
            oral30s="游戏案先分拣：规则、玩法、数值、通用交互多属思想操作方法，著作权一般不保护。美术、文案、音乐、有独创性的关卡具体编排、软件代码等才进表达比对，再走接触加实质性相似。玩法很像但表达不同时，版权常弱，可评估是否改走竞争馆看数据仿冒或混淆。",
            elements=[
                "规则玩法不保护",
                "表达侧清单",
                "接触加实质性相似",
                "竞争馆分流",
            ],
            caseAnchor=["玩法过滤", "表达比对", "跨馆分流"],
            links=["O2", "R1", "S4", "B10", "E2"],
            crossCopyright=None,
            drillPrompt="两款游戏玩法与数值体系高度相似，但美术音乐与代码不同，著作权是否必然成立？",
            classicCases=[
                {
                    "name": "游戏玩法与表达分界典型实践",
                    "hook": "先过滤再比对",
                    "takeaway": "口诀落地：著作权问表达相似；玩法像先别急着告版权。",
                }
            ],
        ),
    ]
    for r in new_rooms:
        if r["id"] not in existing:
            b0["rooms"].append(r)

    for f in data["floors"]:
        for r in f["rooms"]:
            rid = r["id"]
            if rid == "T2":
                add_link(r, "B15")
                r["relatedArticleRefs"] = list(
                    dict.fromkeys((r.get("relatedArticleRefs") or []) + ["cmo-2", "cmo-standing"])
                )
                # thicken T2 oral slightly via scene note in classicCases takeaway already; update oral tip
                if "细则见B15" not in r.get("oral30s", ""):
                    r["oral30s"] = (
                        r["oral30s"].rstrip("。")
                        + "。收费、转付、书面授权范围与一揽子风险等细则下B15。"
                    )
            elif rid == "O2":
                add_link(r, "B16")
            elif rid == "R1":
                add_link(r, "B16")
            elif rid == "S4":
                add_link(r, "B16")
            elif rid == "E2":
                add_link(r, "B16")
            elif rid == "B10":
                add_link(r, "B16")

    ls = data.setdefault("listenScripts", {})
    by = ls.setdefault("byFloor", {})
    by["copyright-B0-ordinances"] = {
        "intro": "下到著作权馆地下室。条例、司法解释之外，还有集体管理与游戏表达两间随案加钉房。",
        "motto": "集体管理看书面授权与四件事；游戏案先滤玩法再比表达。",
        "bridge": "B15接二楼T2；B16接一楼O2、三楼R1与思想表达窗S4，必要时换竞争馆电梯。",
        "outro": "地下室听完。音乐批量许可去B15，游戏抄袭先去B16分拣。",
    }

    docs = data.setdefault("docs", [])
    for d in [
        "docs/著作权法-随案加钉-集体管理与游戏表达.md",
        "docs/知产诉讼城-司法解释索引.md",
    ]:
        if d not in docs:
            docs.append(d)

    # drills
    for d in data.get("drills", []):
        if d.get("id") == "drill-commute-copyright-b0":
            d["name"] = "著作权B0通勤18分钟"
            d["steps"] = [f"B{i}" for i in range(1, 17)]
    data.setdefault("drills", [])
    # replace or append case nails drill
    data["drills"] = [d for d in data["drills"] if d.get("id") != "drill-commute-copyright-case"]
    data["drills"].append(
        {
            "id": "drill-commute-copyright-case",
            "name": "随案加钉通勤6分钟",
            "floorId": "copyright-B0-ordinances",
            "steps": ["B15", "B16"],
        }
    )

    cases = [
        {
            "id": "case-cmo-blanket",
            "title": "歌厅买了一揽子仍被诉",
            "track": "cmo",
            "trackLabel": "集体管理向",
            "prompt": "歌厅向集体管理组织购买包年背景音乐一揽子许可并缴费；某非会员词曲作者仍起诉歌厅与组织管理范围外的曲目使用。",
            "closingTip": "口诀：四件事+书面授权；一揽子≠延伸管理全覆盖。",
            "suggestedPath": ["T2", "B15", "P2", "F1"],
            "questions": [
                {
                    "id": "q1",
                    "label": "集体管理入口厅",
                    "floorHint": "2F",
                    "roomHints": ["T2"],
                    "hint": "第8条",
                    "teach": "先确认是否经授权的集体管理路径。",
                },
                {
                    "id": "q2",
                    "label": "细则后室看什么",
                    "floorHint": "B0",
                    "roomHints": ["B15"],
                    "hint": "非延伸管理",
                    "teach": "核授权曲目与权项是否覆盖争议作品。",
                },
                {
                    "id": "q3",
                    "label": "组织能否自己名义诉",
                    "floorHint": "B0",
                    "roomHints": ["B15"],
                    "hint": "书面授权",
                    "teach": "有书面授权可以自己名义起诉。",
                },
                {
                    "id": "q4",
                    "label": "使用者抗辩焦点",
                    "floorHint": "B0",
                    "roomHints": ["B15"],
                    "hint": "一揽子范围",
                    "teach": "缴费不等于覆盖非会员全部作品。",
                },
                {
                    "id": "q5",
                    "label": "民事入口",
                    "floorHint": "4F",
                    "roomHints": ["F1"],
                    "hint": "主张权利",
                    "teach": "覆盖外作品仍可能走停止侵害与赔偿。",
                },
            ],
        },
        {
            "id": "case-game-rules-filter",
            "title": "消除类玩法相似素材不同",
            "track": "game",
            "trackLabel": "游戏表达向",
            "prompt": "两款消除类手游玩法、数值与经济系统高度相似；美术角色、关卡具体画面与代码模块差异明显；原告主打著作权，并考虑不正当竞争。",
            "closingTip": "口诀：先滤规则玩法，再比表达；版权弱就换竞争馆灯。",
            "suggestedPath": ["O2", "B16", "S4", "R1", "E2"],
            "questions": [
                {
                    "id": "q1",
                    "label": "是不是作品仓先看",
                    "floorHint": "1F",
                    "roomHints": ["O2"],
                    "hint": "独创性表达",
                    "teach": "规则本身通常不是作品仓里的货。",
                },
                {
                    "id": "q2",
                    "label": "分拣柜怎么分",
                    "floorHint": "B0",
                    "roomHints": ["B16"],
                    "hint": "规则/表达",
                    "teach": "玩法数值左柜过滤；美术文案音乐代码右柜比对。",
                },
                {
                    "id": "q3",
                    "label": "思想表达窗",
                    "floorHint": "3F",
                    "roomHints": ["S4"],
                    "hint": "二分",
                    "teach": "操作方法与玩法思想不保护。",
                },
                {
                    "id": "q4",
                    "label": "还要比实质性相似吗",
                    "floorHint": "3F",
                    "roomHints": ["R1"],
                    "hint": "表达层",
                    "teach": "只有进入表达侧的部分才做接触加实质性相似。",
                },
                {
                    "id": "q5",
                    "label": "版权弱怎么分流",
                    "floorHint": "3F",
                    "roomHints": ["E2"],
                    "hint": "竞争馆",
                    "teach": "可评估仿冒、数据或虚假宣传等竞争路径。",
                },
            ],
        },
    ]
    drills = data.setdefault("caseDrills", [])
    ids = {c["id"] for c in cases}
    drills = [c for c in drills if c.get("id") not in ids]
    drills.extend(cases)
    data["caseDrills"] = drills

    data["roadmap"] = {
        "done": [
            "1F权属客体",
            "2F程序平台",
            "B0条例与司法解释",
            "B15集体管理随案钉",
            "B16游戏表达边界随案钉",
            "3F侵权认定",
            "邻接权细拆",
            "4F救济",
            "五问加密",
            "听过加厚",
        ],
        "next": ["合理页面使用细表", "惩罚性四馆对照卡", "电商平台义务合流"],
    }

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    pub.write_text(text, encoding="utf-8")
    print("B0", len(b0["rooms"]), "cases", len(data["caseDrills"]))


if __name__ == "__main__":
    main()
