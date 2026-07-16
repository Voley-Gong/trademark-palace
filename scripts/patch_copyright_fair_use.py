# -*- coding: utf-8 -*-
"""Patch copyright palace: fair use detailed table B17."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART24_FULL = (
    "在下列情况下使用作品，可以不经著作权人许可，不向其支付报酬，但应当指明作者姓名或者名称、作品名称，"
    "并且不得影响该作品的正常使用，也不得不合理地损害著作权人的合法权益：\n"
    "（一）为个人学习、研究或者欣赏，使用他人已经发表的作品；\n"
    "（二）为介绍、评论某一作品或者说明某一问题，在作品中适当引用他人已经发表的作品；\n"
    "（三）为报道新闻，在报纸、期刊、广播电台、电视台等媒体中不可避免地再现或者引用已经发表的作品；\n"
    "（四）报纸、期刊、广播电台、电视台等媒体刊登或者播放其他报纸、期刊、广播电台、电视台等媒体已经发表的关于政治、经济、宗教问题的时事性文章，但著作权人声明不许刊登、播放的除外；\n"
    "（五）报纸、期刊、广播电台、电视台等媒体刊登或者播放在公众集会上发表的讲话，但作者声明不许刊登、播放的除外；\n"
    "（六）为学校课堂教学或者科学研究，翻译、改编、汇编、播放或者少量复制已经发表的作品，供教学或者科研人员使用，但不得出版发行；\n"
    "（七）国家机关为执行公务在合理范围内使用已经发表的作品；\n"
    "（八）图书馆、档案馆、纪念馆、博物馆、美术馆、文化馆等为陈列或者保存版本的需要，复制本馆收藏的作品；\n"
    "（九）免费表演已经发表的作品，该表演未向公众收取费用，也未向表演者支付报酬，且不以营利为目的；\n"
    "（十）对设置或者陈列在公共场所的艺术作品进行临摹、绘画、摄影、录像；\n"
    "（十一）将中国公民、法人或者非法人组织已经发表的以国家通用语言文字创作的作品翻译成少数民族语言文字作品在国内出版发行；\n"
    "（十二）以阅读障碍者能够感知的无障碍方式向其提供已经发表的作品；\n"
    "（十三）法律、行政法规规定的其他情形。\n"
    "前款规定适用于对与著作权有关的权利的限制。"
)


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
    articles["24"] = {
        "label": "第二十四条",
        "text": ART24_FULL,
        "plain": "合理使用=对号入座十三项情形之一，且过三句总闸：指明作者作品名；不影响正常使用；不不合理损害权益。可不经许可、不付报酬；也适用于邻接权限制。",
        "examples": [
            "书评适当引用并署名 → 常走第二项。",
            "短视频整片搬运打广告还称个人欣赏 → 难过第一项与总闸。",
            "课堂教学少量复制供师生 ≠ 出版发行整书网售。",
        ],
        "apply": "3F·S1 总厅；细表 B0·B17；对照 S2 法定许可仍要付酬。",
    }
    articles["fair-use-table"] = art(
        "合理使用十三项细表（学习汇编）",
        "（学习汇编）办案两步：①对号入座第24条十三项；②过三句总闸。高频：①个人使用限于私域，公开传播难靠；②适当引用须引用为辅且有介绍评论说明，整片搬运难过；③新闻报道看「不可避免」；⑥课堂科研不得出版发行；⑨免费表演须不收费、不向表演者付酬且非营利。④⑤注意权利人/作者声明不许。与第25条教科书法定许可区分：后者通常仍须付酬。",
        "先对号，再过闸；个人≠公开传；引用≠搬运；课堂≠出版；免费演≠商场营利场。",
        [
            "知识区讲全书并卖课 → 难靠②或⑥",
            "新闻剪必要现场画面 → 可评估③",
        ],
        "B0·B17；上接 S1",
    )

    floors = {f["id"]: f for f in data["floors"]}
    b0 = floors["copyright-B0-ordinances"]
    b0["mapAscii"] = (
        "B1-B8条例 → B9-B14司法解释 → B15集管 → B16游戏 → B17合理使用细表"
    )
    b0["commuteMinutes"] = 20
    b0["mission"] = (
        "软件/网络条例 + 司法解释 + 集体管理/游戏表达/合理使用细表随案补丁"
    )

    existing = {r["id"] for r in b0["rooms"]}
    if "B17" not in existing:
        b0["rooms"].append(
            room(
                id="B17",
                order=17,
                zone="case",
                title="合理使用十三项细表柜",
                article="fair-use-table",
                articleLabel="第24条细表",
                articleRefs=["fair-use-table", "24"],
                relatedArticleRefs=["25", "10"],
                space="十三格抽屉柜：①个人②引用③新闻④时事文章⑤集会讲话⑥课堂⑦公务⑧馆藏⑨免费演⑩公地艺术⑪民语译⑫无障碍⑬其他；柜顶三句总闸烫金",
                senses=["抽屉拉出咔哒", "总闸横幅烫手"],
                sceneHook="短视频称适当引用；网盘称个人欣赏；商场称免费表演",
                oral30s="合理使用先对号入座二十四条十三项，再过三句总闸：指明作者与作品名，不影响正常使用，不不合理损害权益。个人学习难覆盖公开传播；适当引用不是整片搬运；课堂教学不得出版发行；免费表演要未收费、未付表演者酬且非营利。法定许可教科书仍要付酬，走S2。",
                elements=[
                    "十三项对号",
                    "三句总闸",
                    "个人≠公开传",
                    "引用≠搬运",
                    "课堂≠出版",
                    "免费演三要件",
                    "对照法定许可",
                ],
                caseAnchor=["适当引用", "个人学习", "三句总闸", "免费表演"],
                links=["S1", "S2", "R3", "R1"],
                crossTrademark="S2",
                drillPrompt="整部影视搬运到短视频并插广告，主张「介绍评论适当引用」，细表上最可能卡在哪？",
                classicCases=[
                    {
                        "name": "适当引用与整片搬运分界典型实践",
                        "hook": "引用为辅",
                        "takeaway": "没有独立评论说明、引用变正文时，第二项很难过。",
                    },
                    {
                        "name": "个人欣赏公开传播典型争议",
                        "hook": "私域边界",
                        "takeaway": "①盯个人使用；面向不特定公众分享常破闸。",
                    },
                ],
            )
        )

    for f in data["floors"]:
        for r in f["rooms"]:
            if r["id"] == "S1":
                add_link(r, "B17")
                add_link(r, "S2")
                r["oral30s"] = (
                    "符合第24条所列情形，可不经许可、不付报酬，但应指明作者与作品名称，"
                    "且不得影响作品正常使用、不得不合理损害合法权益。前款也适用于邻接权限制。"
                    "办案先对号入座十三项，再过三句总闸；细表下B17。"
                )
                r["space"] = "十三格情形柜入口，顶上三句总闸横幅；侧门通往B17细表抽屉"
                notes = r.setdefault("sideNotes", [])
                if not any(n.get("id") == "S1-b17" for n in notes):
                    notes.append(
                        {
                            "id": "S1-b17",
                            "article": "24",
                            "oneLiner": "十三项能过/难过对照与互联网卡点见B17细表",
                        }
                    )
            elif r["id"] == "S2":
                add_link(r, "B17")
                add_link(r, "S1")

    ls = data.setdefault("listenScripts", {})
    by = ls.setdefault("byFloor", {})
    prev = by.get("copyright-B0-ordinances", {})
    by["copyright-B0-ordinances"] = {
        "intro": prev.get(
            "intro",
            "下到著作权馆地下室。",
        ).replace("两间随案加钉房", "随案加钉房，含合理使用细表")
        if "随案" in prev.get("intro", "")
        else "下到著作权馆地下室。条例、司法解释与随案加钉房都在这里，合理使用细表在B17。",
        "motto": "合理使用先对号再过闸；个人不等于公开传，引用不等于搬运。",
        "bridge": "B17接三楼S1；和S2法定许可对照：一个常不付酬，一个常要付酬。",
        "outro": "地下室听完。抗辩合理使用时，记得下井拉开十三格抽屉。",
    }
    # thicken 3F listen bridge
    f3 = by.get("copyright-3F-infringement", {})
    if f3:
        f3["bridge"] = (
            "主走廊走完接触加实质性相似后，抗辩先过S1三句总闸，细表下B17；"
            "邻接权进R4到N廊。"
        )
        by["copyright-3F-infringement"] = f3

    docs = data.setdefault("docs", [])
    for d in [
        "docs/著作权法-合理使用细表-记忆宫殿.md",
        "docs/知产诉讼城-司法解释索引.md",
    ]:
        if d not in docs:
            docs.append(d)

    for d in data.get("drills", []):
        if d.get("id") == "drill-commute-copyright-b0":
            d["name"] = "著作权B0通勤20分钟"
            d["steps"] = [f"B{i}" for i in range(1, 18)]
    data["drills"] = [
        d for d in data.get("drills", []) if d.get("id") != "drill-commute-copyright-fairuse"
    ]
    data["drills"].append(
        {
            "id": "drill-commute-copyright-fairuse",
            "name": "合理使用通勤5分钟",
            "floorId": "copyright-3F-infringement",
            "steps": ["S1", "S2"],
        }
    )
    data["drills"].append(
        {
            "id": "drill-commute-copyright-fairuse-b0",
            "name": "合理使用细表通勤4分钟",
            "floorId": "copyright-B0-ordinances",
            "steps": ["B17"],
        }
    )
    # dedupe drills
    seen = set()
    uniq = []
    for d in data["drills"]:
        if d["id"] in seen:
            continue
        seen.add(d["id"])
        uniq.append(d)
    data["drills"] = uniq

    case = {
        "id": "case-fair-use-quote",
        "title": "短视频「解说」整片搬运",
        "track": "fairuse",
        "trackLabel": "合理使用向",
        "prompt": "账号以「五分钟看完电影」为名，将院线片主要情节画面连续剪辑上传并插广告；被告主张介绍评论适当引用与个人欣赏。",
        "closingTip": "口诀：先对号再过闸；引用为辅才像②；整片加广告难过总闸。",
        "suggestedPath": ["P2", "R1", "S1", "B17", "F3"],
        "questions": [
            {
                "id": "q1",
                "label": "先勾哪项财产权",
                "floorHint": "3F",
                "roomHints": ["P2"],
                "hint": "信息网络传播权",
                "teach": "交互式提供完整或主要情节，先勾权项。",
            },
            {
                "id": "q2",
                "label": "相似还要不要过",
                "floorHint": "3F",
                "roomHints": ["R1"],
                "hint": "实质性相似",
                "teach": "连续剪辑主要情节通常过表达相似。",
            },
            {
                "id": "q3",
                "label": "抗辩总厅",
                "floorHint": "3F",
                "roomHints": ["S1"],
                "hint": "三句总闸",
                "teach": "即使主张情形，也要指明来源且不不合理损害。",
            },
            {
                "id": "q4",
                "label": "细表最可能落哪项",
                "floorHint": "B0",
                "roomHints": ["B17"],
                "hint": "②适当引用",
                "teach": "介绍评论要引用为辅；整片搬运不像适当。",
            },
            {
                "id": "q5",
                "label": "①个人欣赏能否救",
                "floorHint": "B0",
                "roomHints": ["B17"],
                "hint": "个人≠公开传",
                "teach": "面向公众传播并插广告，难靠第一项。",
            },
        ],
    }
    drills = [c for c in data.get("caseDrills", []) if c.get("id") != case["id"]]
    drills.append(case)
    data["caseDrills"] = drills

    data["roadmap"] = {
        "done": [
            "1F权属客体",
            "2F程序平台",
            "B0条例与司法解释",
            "B15集体管理",
            "B16游戏表达",
            "B17合理使用细表",
            "3F侵权认定",
            "邻接权细拆",
            "4F救济",
        ],
        "next": ["惩罚性四馆对照卡", "电商平台义务合流"],
    }

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    pub.write_text(text, encoding="utf-8")
    print("B0", len(b0["rooms"]), "art24_len", len(articles["24"]["text"]))


if __name__ == "__main__":
    main()
