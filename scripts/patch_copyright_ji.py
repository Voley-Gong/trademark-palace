# -*- coding: utf-8 -*-
"""Patch copyright-palace.json: add civil / network JI rooms B9–B14."""
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
            "ji-ownership": art(
                "著作权民事司法解释·权属署名",
                "（学习汇编·法释著作权民事解释要点）在作品或者制品上署名的自然人、法人或者非法人组织，视为著作权、与著作权有关权益的权利人，但有相反证明的除外。底稿、原件、合法出版物、著作权登记证书、认证机构出具的证明、取得权利的合同等，可以作为证据。因署名顺序发生纠纷的，有约定按约定；无约定的，可按创作付出的劳动、作品排列、作者姓氏笔画等确定。由不同作者就同一题材创作的作品，表达系独立完成并且有创作性的，应当认定作者各自享有独立著作权。",
                "署名推定权利人（可反证）；底稿登记证书合同等是权属证据；同一题材各自独立创作可各自享有著作权。",
                ["署名为单位但个人举出底稿与创作过程推翻推定"],
                "B0·B9；上接 O5/O1/T1",
            ),
            "ji-similarity": art(
                "著作权民事司法解释·表达相似",
                "（学习汇编）著作权侵权认定常用「接触或接触可能 + 实质性相似」。比对对象是表达，不是思想、主题、创意或公有领域元素；应过滤思想与通用场景后再比独创性表达。同一题材可由不同作者独立创作，只要表达独立完成且有创作性，各自享有著作权；整体欣赏体验不构成实质性相似的，不宜认定侵权。",
                "接触+实质性相似盯表达；先滤思想与公有领域；同题材可并行共存。",
                ["两部同题材剧情节展开与人物性格不同 → 未必实质性相似"],
                "B0·B10；上接 R1/S4",
            ),
            "ji-network-provide": art(
                "信息网络传播权司法解释·提供行为",
                "（学习汇编·法释〔2020〕19号要点）未经许可通过信息网络提供作品、表演、录音录像制品的，除另有规定外构成侵害信息网络传播权。上传至服务器、设置共享文件或利用文件分享软件等，使公众可在其个人选定的时间和地点获得的，属于提供行为。网页快照、缩略图等实质替代他人向公众提供的，可认定提供行为；但不影响正常使用且未不合理损害权利人利益的，可主张未侵害。网络服务提供者与他人分工合作共同提供的，可连带；能证明仅提供自动接入、传输、存储、搜索、链接、文件分享技术等网络服务的，一般不构成共同提供。",
                "交互式「选定时间地点获得」是提供；快照实质替代也算；纯技术中介≠共同提供。",
                ["网盘分享完整影视供任意点播 → 提供行为"],
                "B0·B11；上接 P2/E1/T廊",
            ),
            "ji-network-fault": art(
                "信息网络传播权司法解释·明知应知",
                "（学习汇编·法释〔2020〕19号要点）网络服务提供者教唆或帮助用户侵害信息网络传播权的，应承担侵权责任。过错包括明知或应知；未主动审查不得仅据此认定有过错。应知综合服务性质与管理能力、作品知名度与明显程度、是否选择编辑推荐、预防措施、通知响应、重复侵权处置等判断。对热播影视设榜单目录索引且可直接获得的，可认定应知。从特定作品中直接获得经济利益的，负较高注意义务；一般性广告费服务费除外。接到通知及初步证据未及时采取必要措施的，可认定明知。",
                "应知看红旗与推荐编辑；直接获益抬高注意义务；收通知不处置可推定明知。",
                ["首页置顶热播盗版榜仍不处理 → 应知/明知风险"],
                "B0·B12；上接 T6/T9",
            ),
            "ji-damages": art(
                "著作权民事司法解释·赔偿口径",
                "（学习汇编；顺位对接现行著作权法第54条）赔偿一般按实际损失或违法所得；难以确定的参照权利使用费；故意侵犯著作权或相关权且情节严重的，可按前述方法确定数额的一倍以上五倍以下惩罚性赔偿；仍难确定的，适用五百元以上五百万元以下法定赔偿。确定数额应考虑作品类型、合理使用费、侵权行为性质与后果等。合理开支包括调查取证费用，符合规定的律师费可计入。权利人尽力举证而账簿资料主要由侵权人掌握的，可责令提供；拒不提供或提供虚假的，可参考权利人主张与证据定赔。",
                "损或违法所得→使用费→惩罚性→法定；合理开支含调查取证与合规律师费；账簿可打举证妨碍。",
                ["规模化盗版隐匿账簿 → 惩罚性与举证妨碍叠加"],
                "B0·B13；上接 F3",
            ),
            "ji-limitation": art(
                "著作权民事司法解释·时效持续侵权",
                "（学习汇编）侵害著作权的诉讼时效为三年，自权利人知道或者应当知道权利受到损害以及义务人之日起计算。权利人超过三年起诉，但侵权行为在起诉时仍在持续、且在著作权保护期内的，人民法院应当判决停止侵权；损害赔偿数额自起诉之日起向前推算三年计算。",
                "时效三年；持续侵权仍可判停，赔偿自起诉向前推三年。",
                ["盗版网站从五年前挂到现在 → 停侵可判，赔款通常只算近三年"],
                "B0·B14；上接 F3/F1",
            ),
        }
    )

    floors = {f["id"]: f for f in data["floors"]}
    b0 = floors["copyright-B0-ordinances"]
    b0["name"] = "条例与司法解释补丁层"
    b0["mission"] = "软件/网络条例细则 + 民事权属相似、信息网络提供与过错、赔偿与时效司法解释口径"
    b0["mapAscii"] = (
        "B1-B8条例 → B9权属署名 → B10表达相似 → B11提供行为 → B12明知应知 → B13赔偿 → B14时效"
    )
    b0["commuteMinutes"] = 16

    existing_ids = {r["id"] for r in b0["rooms"]}
    new_rooms = [
        room(
            id="B9",
            order=9,
            zone="ji",
            title="权属署名推定补丁库",
            article="ji-ownership",
            articleLabel="民事解释·权属署名",
            articleRefs=["ji-ownership", "11"],
            relatedArticleRefs=["12", "soft-13"],
            space="署名铜牌推定权利人；旁柜底稿原件登记证书合同；侧签同题材各自独立",
            senses=["铜牌冰凉", "登记章咔哒"],
            sceneHook="署名为单位，个人主张自己才是作者",
            oral30s="作品或制品上署名的主体视为权利人，有相反证明除外。底稿、原件、合法出版物、登记证书、认证证明、权利合同等可作权属证据。署名顺序有约定从约定；无约定可按劳动、排列、姓氏笔画。同一题材独立创作且有创作性的，各自享有著作权。",
            elements=["署名推定", "权属证据清单", "署名顺序", "同题材各自独立"],
            caseAnchor=["署名推定", "登记证书", "同题材独立"],
            links=["O5", "O1", "T1", "B10"],
            drillPrompt="仅有署名、对方举出底稿推翻时，署名推定还能否直接定权属？",
            classicCases=[
                {
                    "name": "署名推定与反证典型裁判口径",
                    "hook": "推定可破",
                    "takeaway": "署名是起点不是终点；反证看创作过程与权属合同。",
                }
            ],
        ),
        room(
            id="B10",
            order=10,
            zone="ji",
            title="接触实质性相似补丁库",
            article="ji-similarity",
            articleLabel="民事解释·表达相似",
            articleRefs=["ji-similarity", "10"],
            relatedArticleRefs=["3", "soft-29"],
            space="双门闸机加深：滤思想公有领域 → 比独创表达；同题材并行灯",
            senses=["荧光笔过滤", "闸机滴滴"],
            sceneHook="同题材两剧像不像、被告称独立创作",
            oral30s="侵权比对常用接触或接触可能加实质性相似。比的是表达不是思想主题创意；先过滤公有领域与通用元素。同一题材不同作者独立完成且有创作性的，各自享有著作权；整体欣赏体验不构成实质性相似的，不宜认定侵权。",
            elements=["接触可能", "实质性相似", "思想表达二分", "同题材可共存"],
            caseAnchor=["实质性相似", "过滤公有领域", "同题材独立"],
            links=["R1", "S4", "B7", "B9"],
            drillPrompt="实质性相似比的是故事题材本身，还是具体表达？",
            classicCases=[
                {
                    "name": "同题材影视实质性相似典型口径",
                    "hook": "题材≠表达",
                    "takeaway": "口诀落地：著作权问表达相似。",
                }
            ],
        ),
        room(
            id="B11",
            order=11,
            zone="ji",
            title="信息网络提供行为补丁库",
            article="ji-network-provide",
            articleLabel="网传解释·提供行为",
            articleRefs=["ji-network-provide"],
            relatedArticleRefs=["10", "net-22"],
            space="服务器上传闸 + 分享软件闸；快照实质替代警示；纯技术中介绿廊",
            senses=["上传进度条"],
            sceneHook="平台称只是链接技术，实际可完整点播",
            oral30s="未经许可通过信息网络提供作品表演录音录像制品，使公众可在个人选定时间和地点获得的，构成侵害信息网络传播权。上传、共享文件、文件分享软件均可构成提供。快照缩略图实质替代也可能构成提供。仅提供接入传输存储搜索链接等技术服务且非分工合作共同提供的，一般不构成共同提供。",
            elements=["选定时间地点获得", "上传共享", "实质替代", "纯技术中介"],
            caseAnchor=["提供行为", "交互式获得", "共同提供"],
            links=["P2", "E1", "T6", "B12"],
            drillPrompt="设置分享使公众随时点播完整片源，是否属于信息网络传播权意义上的提供？",
            classicCases=[
                {
                    "name": "提供行为与技术中介分界典型口径",
                    "hook": "提供vs中介",
                    "takeaway": "能不能选定时间地点拿到内容，是提供行为的关键钩子。",
                }
            ],
        ),
        room(
            id="B12",
            order=12,
            zone="ji",
            title="明知应知与较高注意补丁库",
            article="ji-network-fault",
            articleLabel="网传解释·过错",
            articleRefs=["ji-network-fault", "cc-1197"],
            relatedArticleRefs=["net-22", "net-15"],
            space="应知七因素看板；热播推荐红旗；直接获益高压灯；通知未处置=明知铃",
            senses=["红旗猎猎", "通知铃响"],
            sceneHook="热播盗版置顶推荐且投放贴片广告",
            oral30s="教唆帮助用户侵权应担责。过错含明知应知；未主动审查不得仅据此认有过错。应知综合服务能力、作品知名度、是否编辑推荐、预防与通知响应、重复侵权处置等。热播影视榜单推荐可认定应知；从特定作品直接获益负较高注意义务。接到通知及初步证据未及时必要措施的，可认定明知。",
            elements=["明知应知", "应知因素", "直接获益", "通知后未措施"],
            caseAnchor=["应知", "红旗", "较高注意义务"],
            links=["T6", "T9", "T4", "B11"],
            crossCopyright=None,
            drillPrompt="平台未主动审查，是否因此必然被认定为有过错？",
            classicCases=[
                {
                    "name": "热播推荐应知典型裁判口径",
                    "hook": "榜单红旗",
                    "takeaway": "推荐编辑加直接获益，避风港很难进。",
                }
            ],
        ),
        room(
            id="B13",
            order=13,
            zone="ji",
            title="赔偿与合理开支补丁库",
            article="ji-damages",
            articleLabel="民事解释·赔偿",
            articleRefs=["ji-damages", "54"],
            relatedArticleRefs=["59"],
            space="梯子：损或违法所得→使用费→惩罚阁楼→法定柜台；合理开支抽屉",
            senses=["计算器滴答", "律师费票据"],
            sceneHook="损失和获利都算不清，对方还藏账簿",
            oral30s="赔偿顺位对接第五十四条：实际损失或违法所得，难则使用费，故意且情节严重可一至五倍，再难则五百元至五百万元法定赔偿。综合作品类型、合理使用费、侵权性质后果。合理开支含调查取证，合规律师费可计入。账簿主要由侵权人掌握时可责令提供，拒交可参考权利人主张定赔。",
            elements=["损或违法所得", "使用费", "惩罚性", "法定赔偿", "合理开支", "举证妨碍"],
            caseAnchor=["赔偿梯子", "合理开支", "举证妨碍"],
            links=["F3", "F1", "B14"],
            drillPrompt="实际损失与违法所得都难确定时，下一步通常参照什么？",
            classicCases=[
                {
                    "name": "法定赔偿与合理开支典型口径",
                    "hook": "梯子往下爬",
                    "takeaway": "先穷尽可算基数，再进法定；别忘合理开支。",
                }
            ],
        ),
        room(
            id="B14",
            order=14,
            zone="ji",
            title="时效与持续侵权补丁库",
            article="ji-limitation",
            articleLabel="民事解释·时效",
            articleRefs=["ji-limitation", "54"],
            relatedArticleRefs=["60"],
            space="三年沙漏；持续侵权传送带：停侵全开、赔偿只截近三年",
            senses=["沙漏流沙"],
            sceneHook="盗版从五年前挂到现在才起诉",
            oral30s="诉讼时效三年，自知道或应当知道权利受损及义务人之日起算。超过三年但侵权持续且在保护期内的，仍应判决停止侵权；损害赔偿自起诉之日起向前推算三年。",
            elements=["时效三年", "持续侵权判停", "赔偿向前推三年"],
            caseAnchor=["诉讼时效", "持续侵权", "向前推三年"],
            links=["F3", "F1", "B13"],
            drillPrompt="侵权已持续五年，赔偿一般从何时起向前推算？",
            classicCases=[
                {
                    "name": "持续侵权时效典型口径",
                    "hook": "停全赔三年",
                    "takeaway": "时效过了仍可能停得下来，但钱通常只算近三年。",
                }
            ],
        ),
    ]
    for r in new_rooms:
        if r["id"] not in existing_ids:
            b0["rooms"].append(r)

    # link hubs
    for f in data["floors"]:
        for r in f["rooms"]:
            rid = r["id"]
            if rid == "O5":
                add_link(r, "B9")
            elif rid == "R1":
                add_link(r, "B10")
            elif rid == "T6":
                add_link(r, "B12")
                add_link(r, "B11")
            elif rid == "T9":
                add_link(r, "B12")
            elif rid == "F3":
                add_link(r, "B13")
                add_link(r, "B14")
            elif rid == "P2":
                add_link(r, "B11")
            elif rid == "E1":
                add_link(r, "B11")

    ls = data.setdefault("listenScripts", {})
    ls["motto"] = (
        "一楼钉权属，二楼看平台，三楼看相似与邻接，四楼算代价，地下室查条例与司法解释。"
    )
    by = ls.setdefault("byFloor", {})
    by["copyright-B0-ordinances"] = {
        "intro": "下到著作权馆地下室。前半是软件与网络条例，后半是民事与信息网络传播权司法解释补丁。",
        "motto": "楼上定门牌，地下室对口径；软件走条例，相似与平台过错走司法解释。",
        "bridge": "B9权属署名、B10表达相似、B11提供行为、B12明知应知、B13赔偿、B14时效，常连一楼三楼二楼四楼。",
        "outro": "地下室听完。软件案看软条例，表达相似与平台案记得下井补司法解释。",
    }

    docs = data.setdefault("docs", [])
    for d in [
        "docs/著作权法-司法解释补丁层-记忆宫殿.md",
        "docs/知产诉讼城-司法解释索引.md",
    ]:
        if d not in docs:
            docs.append(d)

    data["description"] = (
        "知产律所实习用：著作权馆全楼层竖切 + 邻接权侧廊 + B0条例与司法解释补丁 + 加密五问 + 加厚听过。"
        "商标问来源混淆，专利问特征落入，著作权问表达相似。"
    )

    # commute drill
    for d in data.get("drills", []):
        if d.get("id") == "drill-commute-copyright-b0":
            d["name"] = "著作权B0通勤16分钟"
            d["steps"] = [f"B{i}" for i in range(1, 15)]
            break
    else:
        data.setdefault("drills", []).append(
            {
                "id": "drill-commute-copyright-b0",
                "name": "著作权B0通勤16分钟",
                "floorId": "copyright-B0-ordinances",
                "steps": [f"B{i}" for i in range(1, 15)],
            }
        )

    data.setdefault("drills", []).append(
        {
            "id": "drill-commute-copyright-ji",
            "name": "著作权司法解释补丁通勤8分钟",
            "floorId": "copyright-B0-ordinances",
            "steps": ["B9", "B10", "B11", "B12", "B13", "B14"],
        }
    )
    # dedupe ji drill if re-run
    seen = set()
    uniq = []
    for d in data["drills"]:
        if d["id"] in seen:
            continue
        seen.add(d["id"])
        uniq.append(d)
    data["drills"] = uniq

    case = {
        "id": "case-ji-similarity-platform",
        "title": "同题材短剧上架平台热播榜",
        "track": "ji",
        "trackLabel": "司法解释向",
        "prompt": "原告短剧上线在先；被告同题材短剧在平台热播榜推荐并可完整点播；平台收贴片广告；原告起诉作者与平台，主张实质性相似与帮助侵权。",
        "closingTip": "口诀：先滤题材比表达；提供行为看选定时间地点获得；热播推荐与直接获益抬高应知注意义务。",
        "suggestedPath": ["B10", "R1", "B11", "B12", "T9", "B13"],
        "questions": [
            {
                "id": "q1",
                "label": "同题材是否当然侵权",
                "floorHint": "B0",
                "roomHints": ["B10"],
                "hint": "表达相似",
                "teach": "同题材可各自享有；关键看独创表达是否实质性相似。",
            },
            {
                "id": "q2",
                "label": "三楼比对总厅",
                "floorHint": "3F",
                "roomHints": ["R1"],
                "hint": "接触+实质性相似",
                "teach": "接触可能加表达层面实质性相似。",
            },
            {
                "id": "q3",
                "label": "完整点播落哪一钉",
                "floorHint": "B0",
                "roomHints": ["B11"],
                "hint": "提供行为",
                "teach": "公众可选定时间地点获得即典型提供。",
            },
            {
                "id": "q4",
                "label": "热播榜+贴片广告",
                "floorHint": "B0",
                "roomHints": ["B12"],
                "hint": "应知/较高注意",
                "teach": "推荐热播可认应知；直接获益负较高注意义务。",
            },
            {
                "id": "q5",
                "label": "赔偿怎么爬梯子",
                "floorHint": "B0",
                "roomHints": ["B13"],
                "hint": "第54条口径",
                "teach": "损或违法所得→使用费→惩罚性→法定；含合理开支。",
            },
        ],
    }
    drills = data.setdefault("caseDrills", [])
    drills = [c for c in drills if c.get("id") != case["id"]]
    drills.append(case)
    data["caseDrills"] = drills

    data["roadmap"] = {
        "done": [
            "1F权属客体",
            "2F程序平台",
            "B0条例补丁",
            "B0民事与网传司法解释",
            "3F侵权认定",
            "邻接权细拆",
            "4F救济",
            "五问加密",
            "听过加厚",
        ],
        "next": ["集体管理细则随案加钉", "游戏规则等办案加钉"],
    }

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    pub.parent.mkdir(parents=True, exist_ok=True)
    pub.write_text(text, encoding="utf-8")
    print(
        "B0 rooms",
        len(b0["rooms"]),
        "articles",
        len(data["articles"]),
        "cases",
        len(data["caseDrills"]),
    )


if __name__ == "__main__":
    main()
