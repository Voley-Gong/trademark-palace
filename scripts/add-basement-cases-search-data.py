# -*- coding: utf-8 -*-
"""Add basement patches, classic cases on rooms, and more case drills."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "data" / "trademark-palace.json"
PUB = ROOT / "trademark-palace-web" / "public" / "data" / "trademark-palace.json"

PATCH_ARTICLES = {
    "ji-civil": {
        "label": "商标民事纠纷司法解释（要点汇编）",
        "text": "【学习补丁·非逐字法条】最高人民法院关于审理商标民事纠纷案件适用法律若干问题的解释等文件的实务要点：商标相同/近似判断看音形义与整体；商品类似看功能用途原料销售渠道消费对象等；商标法意义上的使用强调识别来源；销售者合法来源抗辩需证明合法取得并说明提供者；赔偿可参考许可费倍数；停止侵害、销毁等民事责任可并用。",
        "plain": "打侵权官司时的「操作手册」：怎么判断近似/类似、什么叫使用、销售者怎么免赔、赔多少怎么说。",
        "examples": [
            "比对两个标：不能只拆开看一个字，要看整体给相关公众的印象。",
            "超市卖侵权货：发票齐全、上家清晰、确不知情 → 常走合法来源免赔思路。",
        ],
        "apply": "3F/4F 读案时，把本补丁当「裁判口径说明书」，与第57、63、64条对照用。",
    },
    "ji-wellknown": {
        "label": "驰名商标保护司法解释（要点汇编）",
        "text": "【学习补丁】驰名商标按需认定、个案认定；考虑知晓程度、持续使用、宣传范围、受保护记录等；跨类保护看是否误导公众致使驰名商标注册人利益可能受损；禁止把「驰名商标」字样用于广告宣传。",
        "plain": "驰名不是荣誉墙，是案子需要时才认定；跨类保护更严，要证明误导和损害可能。",
        "examples": [
            "普通侵权能用第57条解决，就不必强行认定驰名。",
            "包装印「中国驰名商标」做广告 → 违法。",
        ],
        "apply": "只有跨类攀附或未注册驰名保护时，才认真打开本补丁 + 第13、14条。",
    },
    "ji-grant": {
        "label": "商标授权确权行政案件规定（要点汇编）",
        "text": "【学习补丁】授权确权案件中恶意申请、囤积、欺骗不正当手段、绝对/相对事由的审查口径；在先权利范围（姓名、著作权、字号等）；一定影响的判断看使用时间、区域、销售与宣传等。",
        "plain": "异议、无效、驳回复审行政诉讼里，法官怎么看「恶意」和「在先权利」的说明书。",
        "examples": [
            "大量申请热门词汇却无真实使用安排 → 恶意/囤积论证常引用确权口径。",
            "主张「有一定影响」：准备区域销售、媒体报道、持续时间证据。",
        ],
        "apply": "2F 程序案写理由时，实体问题回 1F，口径问题打开本补丁。",
    },
    "ji-punitive": {
        "label": "惩罚性赔偿裁判要点（汇编）",
        "text": "【学习补丁】惩罚性赔偿通常要求「故意/恶意」+「情节严重」；考量侵权时间规模、屡教不改、伪造隐匿证据、侵权获利等；基数为实际损失、侵权获利或许可费倍数等，再乘一倍以上五倍以下。",
        "plain": "想主张惩罚性赔偿，不能只喊「恶意」，要同时把「情节严重」的故事讲圆。",
        "examples": [
            "重复侵权、拒不提供账簿、假冒规模大 → 更容易支撑惩罚性。",
            "偶发销售、情节轻微 → 即便构成侵权，惩罚性也难。",
        ],
        "apply": "写第63条惩罚性诉请时，单独列「恶意事实」和「严重情节」两组证据。",
    },
    "ji-evidence": {
        "label": "知识产权证据规则要点（汇编）",
        "text": "【学习补丁】书证提出命令、举证妨碍、电子数据与公证、诉前证据保全；权利人尽力举证后可责令掌握账簿的一方提交，拒不提交或虚假提交可参考权利人主张。",
        "plain": "证据在对方手里时怎么「撬」：申请提出命令、固定电子证据、打举证妨碍。",
        "examples": [
            "侵权网店后台数据可能被删 → 诉前证保 + 公证并行。",
            "被告掌握进销存却拒不交 → 可主张举证妨碍。",
        ],
        "apply": "对接第63条第二款、第66条；诉前策略与赔偿策略一起设计。",
    },
    "ji-online": {
        "label": "网络侵权与平台责任要点（汇编）",
        "text": "【学习补丁】网络服务提供者知道或应知侵权仍提供便利，可能构成帮助侵权；「通知—删除」规则影响平台过错判断；仓储、物流、引流账号等故意提供便利可落入第57条第六项口径。",
        "plain": "平台、代发、仓储不是绝对免责：知道还帮，或通知后装死，风险上升。",
        "examples": [
            "多次投诉同一店铺售假，平台未采取必要措施 → 过错论证空间大。",
            "专门为假货提供隐藏仓储 → 帮助侵权。",
        ],
        "apply": "被告是平台/服务商时，先第57(6)，再补本补丁看过错与通知记录。",
    },
    "ji-injunction": {
        "label": "行为保全/诉前禁令要点（汇编）",
        "text": "【学习补丁】诉前责令停止有关行为需考量侵权可能性、难以弥补的损害、损益平衡、公共利益，并通常需要担保；情况紧急可申请诉前措施。",
        "plain": "想「先停再说」，法院会问：有没有侵权苗头、拖下去损不损得起、担保拿出来没。",
        "examples": [
            "展会明日开展、假冒样机已到场 → 典型紧急保全场景。",
            "证据不足且损害可金钱弥补 → 禁令难获支持。",
        ],
        "apply": "对接第65条；申请书结构按「可能性—损害—担保—紧急」四段写。",
    },
    "ji-use3y": {
        "label": "三年使用与合法来源裁判要点（汇编）",
        "text": "【学习补丁】请求赔偿时，被告可以「权利人未使用」抗辩，法院可要求权利人提供此前三年内实际使用证据；使用应足以维持商标识别功能。销售者合法来源抗辩强调合法取得并说明提供者；免赔不等于免停。",
        "plain": "索赔前先自查：近三年有没有真把商标当来源标识用过；卖家免赔仍可能要停售。",
        "examples": [
            "仅有商标注册证、无销售宣传生产记录 → 三年使用抗辩风险高。",
            "进货合同+付款凭证+上家信息 → 合法来源抗辩更完整。",
        ],
        "apply": "对接第64、48、49条；攻击撤三与防守索赔是同一套使用证据体系。",
    },
}

BASEMENT = {
    "id": "trademark-B0-basement",
    "level": 0,
    "name": "司法解释补丁层",
    "mission": "把法条接到裁判口径：近似、驰名、确权恶意、惩罚性、证据、网络、禁令、三年使用",
    "mapAscii": "B1民事 → B2驰名 → B3确权 → B4惩罚性 → B5证据 → B6网络 → B7禁令 → B8三年使用",
    "commuteMinutes": 12,
    "rooms": [
        {
            "id": "B1",
            "order": 1,
            "zone": "patch",
            "title": "民事纠纷补丁库",
            "article": "ji-civil",
            "articleLabel": "民事司法解释要点",
            "articleRefs": ["ji-civil"],
            "relatedArticleRefs": ["57", "63", "64"],
            "space": "地下室第一库房：贴满近似比对表与类似商品坐标图",
            "senses": ["纸库霉味", "荧光笔味"],
            "sceneHook": "近似怎么比、类似商品怎么定、销售者免赔口径",
            "oral30s": "民事司法解释补丁：近似看整体音形义；类似商品看功能用途渠道对象；使用强调识别来源；合法来源与赔偿口径与第57、63、64条联动。",
            "elements": ["近似整体观察", "商品类似多因素", "使用与赔偿口径"],
            "exceptions": [],
            "caseAnchor": ["近似比对", "类似商品", "合法来源"],
            "classicCases": [
                {
                    "name": "「非诚勿扰」商标案",
                    "hook": "服务商标近似与混淆",
                    "takeaway": "相关公众混淆可能性是近似判断的核心落点。",
                }
            ],
            "links": ["R2", "F3", "F5"],
            "peg": None,
            "drillPrompt": "近似判断能不能只盯一个汉字是否相同？",
        },
        {
            "id": "B2",
            "order": 2,
            "zone": "patch",
            "title": "驰名认定补丁库",
            "article": "ji-wellknown",
            "articleLabel": "驰名保护解释要点",
            "articleRefs": ["ji-wellknown"],
            "relatedArticleRefs": ["13", "14"],
            "space": "保险柜门上写「按需认定」，禁止广告贴纸被撕下",
            "senses": ["保险柜冷金属", "撕贴纸声"],
            "sceneHook": "要不要认定驰名、跨类保护证明什么",
            "oral30s": "驰名按需、个案认定；跨类看误导公众与利益受损可能；禁止驰名商标字样广告化。",
            "elements": ["按需认定", "跨类误导损害", "禁止广告使用驰名字样"],
            "exceptions": [],
            "caseAnchor": ["按需认定", "跨类保护"],
            "classicCases": [
                {
                    "name": "驰名商标按需认定系列实践",
                    "hook": "能用普通条款就不用强行驰名",
                    "takeaway": "先问第57条够不够，再决定是否启动第13条电梯。",
                }
            ],
            "links": ["E1"],
            "peg": None,
            "drillPrompt": "为什么说驰名是事实认定不是荣誉称号？",
        },
        {
            "id": "B3",
            "order": 3,
            "zone": "patch",
            "title": "授权确权补丁库",
            "article": "ji-grant",
            "articleLabel": "确权行政案件要点",
            "articleRefs": ["ji-grant"],
            "relatedArticleRefs": ["4", "32", "44", "45"],
            "space": "档案架标「恶意」「一定影响」「在先权利」",
            "senses": ["档案袋尘土", "印泥味"],
            "sceneHook": "异议无效理由怎么写才像「确权语言」",
            "oral30s": "确权补丁：恶意囤积与不正当手段、在先权利类型、一定影响的证据结构，服务异议无效驳回复审。",
            "elements": ["恶意认定口径", "在先权利", "一定影响证据"],
            "exceptions": [],
            "caseAnchor": ["恶意申请", "在先权利", "一定影响"],
            "classicCases": [
                {
                    "name": "乔丹商标行政纠纷案",
                    "hook": "姓名权与抢注",
                    "takeaway": "在先权利可包括姓名权等；恶意与关联性是关键评价点。",
                }
            ],
            "links": ["T5", "T9", "T10", "O9"],
            "peg": None,
            "drillPrompt": "主张第32条「一定影响」，最少要准备哪三类事实？",
        },
        {
            "id": "B4",
            "order": 4,
            "zone": "patch",
            "title": "惩罚性赔偿补丁库",
            "article": "ji-punitive",
            "articleLabel": "惩罚性赔偿要点",
            "articleRefs": ["ji-punitive"],
            "relatedArticleRefs": ["63"],
            "space": "阁楼模型：恶意旋钮 × 情节严重仪表",
            "senses": ["仪表滴滴响", "热风"],
            "sceneHook": "主张一至五倍惩罚性时缺哪一块",
            "oral30s": "惩罚性补丁：故意/恶意与情节严重双要件；基数乘一至五倍；证据看规模、重复、隐匿等。",
            "elements": ["恶意", "情节严重", "基数与倍数"],
            "exceptions": [],
            "caseAnchor": ["惩罚性", "情节严重"],
            "classicCases": [
                {
                    "name": "惩罚性赔偿适用典型案例（各地法院）",
                    "hook": "重复假冒+拒不举证",
                    "takeaway": "把「明知故犯」和「情节恶劣」写成可核对的事实清单。",
                }
            ],
            "links": ["F3"],
            "peg": 5,
            "drillPrompt": "只有「故意」没有「情节严重」，惩罚性能不能稳？",
        },
        {
            "id": "B5",
            "order": 5,
            "zone": "patch",
            "title": "证据与妨碍补丁库",
            "article": "ji-evidence",
            "articleLabel": "证据规则要点",
            "articleRefs": ["ji-evidence"],
            "relatedArticleRefs": ["63", "66"],
            "space": "铁抽屉与封条公证袋并排",
            "senses": ["封条脆响", "抽屉空回声"],
            "sceneHook": "账簿在对方、链接要消失",
            "oral30s": "证据补丁：书证提出、举证妨碍、电子数据与诉前证保，撬开赔偿与事实固定。",
            "elements": ["提出命令", "举证妨碍", "电子证据固定"],
            "exceptions": [],
            "caseAnchor": ["举证妨碍", "诉前证保"],
            "classicCases": [
                {
                    "name": "证据保全与举证妨碍典型实践",
                    "hook": "拒交账簿",
                    "takeaway": "权利人尽力举证后，妨碍可转化对赔偿数额的不利推定。",
                }
            ],
            "links": ["F3", "F7"],
            "peg": None,
            "drillPrompt": "举证妨碍启动前，原告自己要先做到哪一步？",
        },
        {
            "id": "B6",
            "order": 6,
            "zone": "patch",
            "title": "网络帮助补丁库",
            "article": "ji-online",
            "articleLabel": "网络与平台要点",
            "articleRefs": ["ji-online"],
            "relatedArticleRefs": ["57"],
            "space": "服务器机柜贴着「通知—删除」流程图",
            "senses": ["风扇嗡鸣", "键盘声"],
            "sceneHook": "告平台、告代发、告仓储",
            "oral30s": "网络补丁：知道或应知仍提供便利、通知删除影响过错、帮助侵权与第57条第六项对接。",
            "elements": ["知道或应知", "通知删除", "提供便利"],
            "exceptions": [],
            "caseAnchor": ["平台责任", "帮助侵权"],
            "classicCases": [
                {
                    "name": "电商平台商标侵权通知删除类案件",
                    "hook": "必要措施是否及时",
                    "takeaway": "通知内容与平台反应时点，是过错认定的证据主轴。",
                }
            ],
            "links": ["R6"],
            "peg": None,
            "drillPrompt": "告平台时，优先固定哪两类证据？",
        },
        {
            "id": "B7",
            "order": 7,
            "zone": "patch",
            "title": "诉前禁令补丁库",
            "article": "ji-injunction",
            "articleLabel": "行为保全要点",
            "articleRefs": ["ji-injunction"],
            "relatedArticleRefs": ["65"],
            "space": "急诊通道墙上四块板：可能性、损害、平衡、担保",
            "senses": ["警灯闪", "担保函纸张涩手"],
            "sceneHook": "展会前能否先责令停止",
            "oral30s": "禁令补丁：侵权可能性、难以弥补损害、损益平衡、公共利益与担保，对接第65条。",
            "elements": ["侵权可能性", "难以弥补", "担保", "紧急情况"],
            "exceptions": [],
            "caseAnchor": ["诉前禁令", "担保"],
            "classicCases": [
                {
                    "name": "展会/新品发布前行为保全实践",
                    "hook": "情况紧急",
                    "takeaway": "证据与担保准备越完整，紧急措施越可行。",
                }
            ],
            "links": ["F6"],
            "peg": None,
            "drillPrompt": "申请诉前禁令，四段式结构怎么写？",
        },
        {
            "id": "B8",
            "order": 8,
            "zone": "patch",
            "title": "三年使用补丁库",
            "article": "ji-use3y",
            "articleLabel": "使用与合法来源要点",
            "articleRefs": ["ji-use3y"],
            "relatedArticleRefs": ["64", "48", "49"],
            "space": "三年台历与进货单钉在一起",
            "senses": ["台历撕页", "发票油墨"],
            "sceneHook": "索赔被反杀三年未使用；撤三攻防",
            "oral30s": "使用补丁：三年实际使用证据、识别来源标准、合法来源免赔不免停，打通第48、49、64条。",
            "elements": ["三年使用", "合法来源", "免赔不免停"],
            "exceptions": [],
            "caseAnchor": ["三年使用", "合法来源"],
            "classicCases": [
                {
                    "name": "撤三与三年使用抗辩关联实践",
                    "hook": "同一套使用证据两用",
                    "takeaway": "攻击撤三与防守第64条，证据结构高度同构。",
                }
            ],
            "links": ["F5", "T12", "P2"],
            "peg": 3,
            "drillPrompt": "为什么说撤三证据和64条抗辩是一套体系？",
        },
    ],
}

# classic cases to merge into existing rooms by id
CLASSIC_BY_ROOM = {
    "O1": [{"name": "注册取得原则通说实践", "hook": "核准注册产生专用权", "takeaway": "先核对注册证与权利人，再谈侵权。"}],
    "O2": [{"name": "恶意囤积商标驳回/无效典型案", "hook": "不以使用为目的", "takeaway": "批量抢注无使用安排，可走第4条+确权恶意口径。"}],
    "O9": [{"name": "乔丹商标案", "hook": "在先姓名权", "takeaway": "第32条在先权利不限于商标权。"}],
    "O8": [{"name": "代理抢注典型行政案", "hook": "第15条关系人", "takeaway": "先证关系与明知，再谈不予注册禁止使用。"}],
    "R1": [{"name": "假冒注册商标刑事/民事交叉案", "hook": "双重相同", "takeaway": "同品同标常是刑民衔接高发区。"}],
    "R2": [{"name": "「非诚勿扰」商标案", "hook": "混淆可能性", "takeaway": "近似判断落在相关公众是否容易混淆。"}],
    "R5": [{"name": "「枫叶」与鳄鱼撕标案（反向假冒经典）", "hook": "更换商标再投入市场", "takeaway": "撕标换标切断来源识别，落入第57条第五项。"}],
    "R6": [{"name": "提供仓储物流帮助侵权案", "hook": "故意提供便利", "takeaway": "主观故意+便利行为是帮助侵权双轴。"}],
    "S1": [{"name": "字号与商标冲突反法规制案", "hook": "第58条换轨", "takeaway": "字号攀附优先评估不正当竞争路径。"}],
    "S2": [{"name": "描述性正当使用抗辩典型案", "hook": "第59条", "takeaway": "能说明是描述产地/特征，而非商标性使用。"}],
    "E1": [{"name": "驰名商标跨类保护典型案", "hook": "误导公众", "takeaway": "跨类不是自动保护，要证误导与损害可能。"}],
    "T5": [{"name": "初审公告期异议攻防实践", "hook": "三个月窗口", "takeaway": "监控公告+期限管理决定程序成败。"}],
    "T10": [{"name": "恶意抢注突破五年限制实践", "hook": "驰名所有人例外", "takeaway": "五年闸不是绝对墙，恶意+驰名可能例外。"}],
    "T12": [{"name": "连续三年不使用撤销案", "hook": "撤三", "takeaway": "使用证据要指向核定商品上的识别来源使用。"}],
    "F3": [{"name": "惩罚性赔偿与法定赔偿裁量案", "hook": "第63条梯子", "takeaway": "先定基数方法，再谈倍数或法定封顶。"}],
    "F5": [{"name": "销售者合法来源免赔案", "hook": "第64条第二款", "takeaway": "免赔不等于可以继续销售。"}],
    "F6": [{"name": "诉前行为保全支持/驳回对比案", "hook": "难以弥补的损害", "takeaway": "紧急+担保+侵权可能性缺一不可。"}],
}

NEW_CASES = [
    {
        "id": "case-reverse-passing-off",
        "title": "撕标换标反向假冒",
        "track": "infringement",
        "trackLabel": "侵权救济向",
        "prompt": "你方正品被经销商买走后撕掉原注册商标，换贴经销商自己的商标再销售。你方要停止该行为并索赔。",
        "closingTip": "口诀：撕标换标进暗室；使用与来源识别被切断。",
        "suggestedPath": ["P2", "R5", "F3", "F1"],
        "questions": [
            {"id": "q1", "label": "最直接的侵权门牌", "floorHint": "3F", "roomHints": ["R5"]},
            {"id": "q2", "label": "为何仍要确认商标性使用语境", "floorHint": "3F", "roomHints": ["P2", "R5"]},
            {"id": "q3", "label": "救济路径怎么选", "floorHint": "4F", "roomHints": ["F1", "F3"]},
            {"id": "q4", "label": "若只告销售渠道还涉及哪项", "floorHint": "3F", "roomHints": ["R3", "R5"]},
            {"id": "q5", "label": "要高额赔时证据补丁去哪", "floorHint": "B0", "roomHints": ["B4", "B5", "F3"]},
        ],
    },
    {
        "id": "case-tradename-antiunfair",
        "title": "字号攀附转反法",
        "track": "infringement",
        "trackLabel": "侵权救济向",
        "prompt": "对方把你的注册商标拿去当企业字号突出使用，招牌和宣传都在强化该字号，相关公众容易以为有关联。对方抗辩「我依法登记了字号」。",
        "closingTip": "口诀：字号侧门换轨反法，别硬塞57。",
        "suggestedPath": ["S1", "P1", "B1", "E1"],
        "questions": [
            {"id": "q1", "label": "程序/请求权换轨落哪扇侧门", "floorHint": "3F", "roomHints": ["S1"]},
            {"id": "q2", "label": "是否还要核对商标权利边界", "floorHint": "3F", "roomHints": ["P1", "O1"]},
            {"id": "q3", "label": "若主张未注册驰名被作字号", "floorHint": "3F", "roomHints": ["S1", "E1"]},
            {"id": "q4", "label": "混淆误导的民事口径补丁", "floorHint": "B0", "roomHints": ["B1"]},
            {"id": "q5", "label": "若同时存在商标性使用近似", "floorHint": "3F", "roomHints": ["R2", "S1"]},
        ],
    },
    {
        "id": "case-wellknown-crossclass",
        "title": "驰名跨类攀附",
        "track": "procedure",
        "trackLabel": "程序向",
        "prompt": "你方商标在手机上已注册且全国知名。对方在马桶盖类别申请高度摹仿的标志并已初审公告。商品不类似，普通第57条路径吃力。",
        "closingTip": "口诀：不类似先乘驰名电梯；程序上抢异议窗。",
        "suggestedPath": ["E1", "B2", "T5", "T10", "T7"],
        "questions": [
            {"id": "q1", "label": "实体保护入口乘哪部电梯", "floorHint": "3F", "roomHints": ["E1"]},
            {"id": "q2", "label": "驰名认定补丁库", "floorHint": "B0", "roomHints": ["B2"]},
            {"id": "q3", "label": "公告期程序动作", "floorHint": "2F", "roomHints": ["T5"]},
            {"id": "q4", "label": "若已注册后的相对无效", "floorHint": "2F", "roomHints": ["T10", "T7"]},
            {"id": "q5", "label": "确权理由写作口径", "floorHint": "B0", "roomHints": ["B3", "B2"]},
        ],
    },
]


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    data["schemaVersion"] = max(int(data.get("schemaVersion") or 6), 7)
    data["description"] = (
        "知产律所实习用：1F权属 + 2F程序 + 3F认定 + 4F救济 + 地下室司法解释补丁。"
        "含五问办案、通勤听过、发霉复习与搜索。"
    )

    docs = data.get("docs", [])
    doc_b = "docs/商标法-司法解释补丁层-记忆宫殿.md"
    if doc_b not in docs:
        docs.append(doc_b)
    data["docs"] = docs

    articles = data.setdefault("articles", {})
    articles.update(PATCH_ARTICLES)

    # classic cases on existing rooms
    for floor in data.get("floors", []):
        for room in floor.get("rooms", []):
            extras = CLASSIC_BY_ROOM.get(room["id"])
            if not extras:
                continue
            existing = room.get("classicCases") or []
            names = {c.get("name") for c in existing}
            for c in extras:
                if c["name"] not in names:
                    existing.append(c)
            room["classicCases"] = existing
            # soft links to basement
            links = room.setdefault("links", [])
            if room["id"] in ("R2", "F5", "F3") and "B1" not in links:
                links.append("B1")
            if room["id"] == "E1" and "B2" not in links:
                links.append("B2")
            if room["id"] in ("T5", "T9", "T10", "O9") and "B3" not in links:
                links.append("B3")
            if room["id"] == "F3" and "B4" not in links:
                links.append("B4")
            if room["id"] in ("F3", "F7") and "B5" not in links:
                links.append("B5")
            if room["id"] == "R6" and "B6" not in links:
                links.append("B6")
            if room["id"] == "F6" and "B7" not in links:
                links.append("B7")
            if room["id"] in ("F5", "T12", "P2") and "B8" not in links:
                links.append("B8")

    floors = [f for f in data.get("floors", []) if f.get("id") != BASEMENT["id"]]
    by_level = {f["level"]: f for f in floors}
    by_level[0] = BASEMENT
    data["floors"] = [by_level[lv] for lv in sorted(by_level)]

    # case drills merge
    cases = data.get("caseDrills") or []
    ids = {c["id"] for c in cases}
    for c in NEW_CASES:
        if c["id"] not in ids:
            cases.append(c)
    data["caseDrills"] = cases

    drills = [d for d in data.get("drills", []) if d.get("id") != "drill-commute-b0"]
    drills.append(
        {
            "id": "drill-commute-b0",
            "name": "地下室通勤12分钟",
            "floorId": "trademark-B0-basement",
            "steps": [r["id"] for r in BASEMENT["rooms"]],
        }
    )
    data["drills"] = drills

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    SRC.write_text(text, encoding="utf-8")
    PUB.write_text(text, encoding="utf-8")
    print("floors", [(f["level"], len(f["rooms"])) for f in data["floors"]])
    print("caseDrills", len(data["caseDrills"]))
    print("patch articles", len(PATCH_ARTICLES))


if __name__ == "__main__":
    main()
