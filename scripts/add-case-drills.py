# -*- coding: utf-8 -*-
"""Add caseDrills: infringement + procedure-oriented five-question cases."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "data" / "trademark-palace.json"
PUB = ROOT / "trademark-palace-web" / "public" / "data" / "trademark-palace.json"

CASE_DRILLS = [
    {
        "id": "case-seller",
        "title": "电商销售近似标",
        "track": "infringement",
        "trackLabel": "侵权救济向",
        "prompt": "电商卖同品类近似标鞋；卖家称有进货发票且不知情；权利人近三年无明显使用证据；商品链接可能随时下架。",
        "closingTip": "口诀：上三楼定门牌，下四楼算代价。",
        "suggestedPath": ["P1", "P2", "R2", "R3", "S2", "F5", "F3", "F7"],
        "questions": [
            {
                "id": "q1",
                "label": "请求权基础首先落哪",
                "floorHint": "1F+3F",
                "roomHints": ["O1", "P1", "R2"],
            },
            {
                "id": "q2",
                "label": "是否构成商标性使用与近似混淆",
                "floorHint": "3F",
                "roomHints": ["P2", "R2"],
            },
            {
                "id": "q3",
                "label": "销售者责任与抗辩",
                "floorHint": "3F+4F",
                "roomHints": ["R3", "F5", "S2"],
            },
            {
                "id": "q4",
                "label": "赔偿还是免赔",
                "floorHint": "4F",
                "roomHints": ["F5", "F3"],
            },
            {
                "id": "q5",
                "label": "证据可能灭失时怎么办",
                "floorHint": "4F",
                "roomHints": ["F7", "F6"],
            },
        ],
    },
    {
        "id": "case-oppose-then-invalid",
        "title": "初审异议与抢注无效",
        "track": "procedure",
        "trackLabel": "程序向",
        "prompt": "你方品牌「青禾」在茶饮门店使用多年、有一定影响但未注册。对手「青禾里」在咖啡馆服务上进入初步审定公告，异议期还剩约二十天。若错过异议，对方可能获准注册；即便获准，你仍可能考虑后续无效。",
        "closingTip": "口诀：先看表（三月窗），再看门（32/15），输了异议转无效（45）。",
        "suggestedPath": ["O9", "T5", "T7", "T8", "T10", "T11"],
        "questions": [
            {
                "id": "q1",
                "label": "此刻最该抢哪扇程序门",
                "floorHint": "2F",
                "roomHints": ["T5"],
            },
            {
                "id": "q2",
                "label": "异议实体理由主要挂哪",
                "floorHint": "1F+2F",
                "roomHints": ["O9", "O8", "T5"],
            },
            {
                "id": "q3",
                "label": "若异议失败被准予注册，下一步常转哪",
                "floorHint": "2F",
                "roomHints": ["T7", "T10"],
            },
            {
                "id": "q4",
                "label": "获准注册后权利起算与追溯怎么想",
                "floorHint": "2F",
                "roomHints": ["T8"],
            },
            {
                "id": "q5",
                "label": "相对无效有没有五年闸，谁可能例外",
                "floorHint": "2F",
                "roomHints": ["T10", "E1"],
            },
        ],
    },
    {
        "id": "case-reject-and-badfaith",
        "title": "驳回复审与绝对无效",
        "track": "procedure",
        "trackLabel": "程序向",
        "prompt": "你方新申请被引证商标驳回。同时尽调发现：引证商标注册人短期内囤积大量商标、无明显真实使用意图，且该引证标本身描述性极强。你既要救自己的申请，也想削弱对方权利。",
        "closingTip": "口诀：驳回走复审电梯；绝对瑕疵进无效熔炉；烧穿后看自始空洞。",
        "suggestedPath": ["T4", "T6", "O2", "O6", "T9", "T11"],
        "questions": [
            {
                "id": "q1",
                "label": "不服驳回先开哪间",
                "floorHint": "2F",
                "roomHints": ["T6", "T4"],
            },
            {
                "id": "q2",
                "label": "驳回通知里的「撞车」对应哪扇闸",
                "floorHint": "2F",
                "roomHints": ["T4"],
            },
            {
                "id": "q3",
                "label": "对方恶意囤标、不以使用为目的，实体回哪",
                "floorHint": "1F",
                "roomHints": ["O2", "O6"],
            },
            {
                "id": "q4",
                "label": "攻击已注册引证标的绝对事由走哪炉",
                "floorHint": "2F",
                "roomHints": ["T9"],
            },
            {
                "id": "q5",
                "label": "无效成功后权利状态怎么理解",
                "floorHint": "2F",
                "roomHints": ["T11"],
            },
        ],
    },
    {
        "id": "case-cancel3-and-damages",
        "title": "撤三攻防与索赔免赔",
        "track": "procedure",
        "trackLabel": "程序向",
        "prompt": "对手商标注册已满四年，市场上几乎看不到真实使用。你方计划推出近似品牌，同时你方自有注册商标遭到仿冒销售，准备索赔；对方可能反过来说你也没怎么用。",
        "closingTip": "口诀：攻他走撤三磨坊；守己备三年使用；赔不赔看免赔窗。",
        "suggestedPath": ["T12", "P2", "F5", "F3", "O11"],
        "questions": [
            {
                "id": "q1",
                "label": "攻击对方「注而不用」走哪",
                "floorHint": "2F",
                "roomHints": ["T12"],
            },
            {
                "id": "q2",
                "label": "什么叫商标法上的「使用」证据",
                "floorHint": "3F",
                "roomHints": ["P2", "T12"],
            },
            {
                "id": "q3",
                "label": "你方索赔时对方提「你没用过」抗辩",
                "floorHint": "4F",
                "roomHints": ["F5"],
            },
            {
                "id": "q4",
                "label": "若能赔，数额梯子怎么爬",
                "floorHint": "4F",
                "roomHints": ["F3"],
            },
            {
                "id": "q5",
                "label": "自己商标会不会因过期未续展先塌掉",
                "floorHint": "1F",
                "roomHints": ["O11", "O1"],
            },
        ],
    },
]


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    data["schemaVersion"] = max(int(data.get("schemaVersion") or 5), 6)
    data["caseDrills"] = CASE_DRILLS

    # keep legacy fiveQuestions as alias of first case for compatibility
    data["fiveQuestions"] = CASE_DRILLS[0]["questions"]

    # update peg flash to include 6
    for d in data.get("drills", []):
        if d.get("id") == "drill-peg-flash":
            d["pegs"] = [0, 1, 2, 3, 5, 6]
        if d.get("id") == "drill-hypothetical-seller":
            d["caseId"] = "case-seller"

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    SRC.write_text(text, encoding="utf-8")
    PUB.write_text(text, encoding="utf-8")
    print("caseDrills:", len(CASE_DRILLS))


if __name__ == "__main__":
    main()
