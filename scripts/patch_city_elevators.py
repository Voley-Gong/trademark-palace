# -*- coding: utf-8 -*-
"""Attach crossPalaceLinks from city-elevators.json into each palace pack."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    src = ROOT / "docs" / "data" / "city-elevators.json"
    pub = ROOT / "trademark-palace-web" / "public" / "data" / "city-elevators.json"
    text = src.read_text(encoding="utf-8")
    pub.write_text(text, encoding="utf-8")

    city = json.loads(text)
    node_by_id = {n["id"]: n for n in city["nodes"]}

    outgoing = defaultdict(list)
    for e in city["edges"]:
        pairs = [(e["from"], e["to"])]
        if e.get("bidirectional"):
            pairs.append((e["to"], e["from"]))
        for a, b in pairs:
            na, nb = node_by_id[a], node_by_id[b]
            label = f"{nb.get('floorHint', '')}·{nb['label']}".lstrip("·")
            outgoing[(na["palaceId"], na["roomId"])].append(
                {
                    "palaceId": nb["palaceId"],
                    "roomId": nb["roomId"],
                    "label": label,
                    "reason": e["label"],
                    "edgeId": e["id"],
                }
            )

    def dedupe(links):
        seen = set()
        out = []
        for link in links:
            key = (link["palaceId"], link["roomId"], link["reason"])
            if key in seen:
                continue
            seen.add(key)
            out.append(link)
        return out

    palace_files = {
        "trademark": ROOT / "docs" / "data" / "trademark-palace.json",
        "patent": ROOT / "docs" / "data" / "patent-palace.json",
        "copyright": ROOT / "docs" / "data" / "copyright-palace.json",
        "competition": ROOT / "docs" / "data" / "competition-palace.json",
    }

    oral_patch = {
        ("trademark", "S1"): (
            "将他人注册商标、未注册驰名商标作为企业名称中的字号使用，误导公众，构成不正当竞争的，"
            "依照反不正当竞争法处理。乘跨馆电梯可直达竞争馆字号·关键词厅与分流台。"
        ),
        ("copyright", "E2"): (
            "作品性弱但存在有一定影响的装潢、名称混淆或虚假宣传时，应考虑改走商标或反不正当竞争路径。"
            "乘跨馆电梯可直达竞争馆分流台、混淆总厅与装潢厅。"
        ),
        ("competition", "O2"): (
            "注册商标核准冲突走商标馆；作品表达抄袭走著作权馆；有一定影响的装潢字号域名关键词攀附、"
            "商业秘密、虚假宣传、网络干扰走本馆。可乘电梯回商标边界厅或著作权作品门。"
        ),
    }

    for pid, path in palace_files.items():
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data["cityElevators"] = {
            "title": city["title"],
            "motto": city["motto"],
            "blurb": city["blurb"],
            "nodeIds": [n["id"] for n in city["nodes"] if n["palaceId"] == pid],
        }
        for floor in data.get("floors", []):
            for room in floor.get("rooms", []):
                links = outgoing.get((pid, room["id"]))
                if links:
                    room["crossPalaceLinks"] = dedupe(links)
                elif "crossPalaceLinks" in room:
                    del room["crossPalaceLinks"]
                patch = oral_patch.get((pid, room["id"]))
                if patch:
                    room["oral30s"] = patch

        out_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(out_text, encoding="utf-8")
        pub_path = ROOT / "trademark-palace-web" / "public" / "data" / path.name
        pub_path.write_text(out_text, encoding="utf-8")
        count = sum(
            1
            for f in data["floors"]
            for r in f["rooms"]
            if r.get("crossPalaceLinks")
        )
        print(pid, "rooms with elevators", count)

    print("city elevators synced")


if __name__ == "__main__":
    main()
