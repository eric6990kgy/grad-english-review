"""Backfills flashcards from every passage and question already in the bank.

Usage: python backfill_vocab.py <dir with bank/*.json exported by ArtifactData> <output pack json>
Example sentences are taken from the bank's own text with the same matching rules as the page (exampleFor).
"""
import glob, json, os, re, sys, time

WORDS = """aggravate|v.|加重、使惡化
fabricate|v.|捏造、偽造
speculate|v.|推測；投機
disregard|v.|忽視、不理會
conclusive|adj.|確定的、決定性的
trivial|adj.|瑣碎的、不重要的
subsidy|n.|補貼、補助金
merger|n.|合併（公司）
replicate|v.|複製、重做（實驗）
supply chain|phr.|供應鏈
disruption|n.|中斷、干擾
emerging economy|phr.|新興經濟體
excessive|adj.|過度的
concentrate|v.|專心、集中
startup|n.|新創公司
investor|n.|投資人
pandemic|n.|全球大流行病
logistics|n.|物流
retailer|n.|零售商
verify|v.|核實、查證
output|n.|產出、輸出結果
outperform|v.|表現勝過
competitor|n.|競爭者
insist|v.|堅持（要求）
submission|n.|提交、繳交
regulation|n.|法規、規定
revise|v.|修訂
admissions committee|phr.|招生委員會
applicant|n.|申請人
look forward to|phr.|期待（後接 V-ing）
when it comes to|phr.|談到、說到（後接名詞或 V-ing）
sporadic|adj.|零星的、偶發的
ephemeral|adj.|短暫的、轉瞬即逝的
dispensable|adj.|可有可無的
connectivity|n.|連線能力、連結性
encryption|n.|加密
protocol|n.|協定、規約
data breach|phr.|資料外洩
condone|v.|寬恕、縱容
algorithm|n.|演算法
transparent|adj.|透明的、公開的
versatile|adj.|多功能的、多才多藝的
opaque|adj.|不透明的、難以理解的
robust|adj.|穩健的、強健的
disclose|v.|揭露、公開
transient|adj.|短暫的、一時的
superficial|adj.|表面的、膚淺的
profound|adj.|深遠的、深刻的
compatible|adj.|相容的
analogous|adj.|類似的、可類比的
indifferent|adj.|漠不關心的
vendor|n.|攤販、供應商
bias|n.|偏見、偏差
relinquish|v.|放棄、讓出
commemorate|v.|紀念
expedite|v.|加速處理
innovative|adj.|創新的
tangible|adj.|有形的、具體的
prototype|n.|原型、樣品
durability|n.|耐用性
mass production|phr.|大量生產
safeguard|v.|保護、捍衛
divulge|v.|洩漏（秘密）
refine|v.|改良、精煉
confidential|adj.|機密的
underperforming|adj.|表現不佳的
divest|v.|撤資、出售（資產或部門）
augment|v.|增加、擴大
analyst|n.|分析師
stifle|v.|扼殺、壓制
foster|v.|培養、促進
galvanize|v.|激起、促使行動
lavish|adj.|奢侈的、揮霍的
cursory|adj.|草率的、粗略的
erratic|adj.|不穩定的、反覆無常的
plague|v.|困擾、折磨
sanguine|adj.|樂觀的
apathetic|adj.|冷漠的、無動於衷的
jubilant|adj.|歡欣鼓舞的
restructuring|n.|重組、改組
layoff|n.|裁員
intellectual property|phr.|智慧財產
patent|n.|專利
verdict|n.|判斷、裁決
project|v.|預測、推估
headline inflation|phr.|整體通膨（含能源與食品）
policymaker|n.|決策者
modestly|adv.|小幅地、適度地
resilience|n.|韌性、復原力
under strain|phr.|承受壓力
absorb|v.|吸收；承受（衝擊）
shock|n.|衝擊
uneven|adj.|不均衡的
value chain|phr.|價值鏈
bleak|adj.|黯淡的、令人沮喪的
prospect|n.|前景、展望
ledger|n.|帳簿
productivity|n.|生產力
baseline|n.|基準
forecast|n.|預測
reassessment|n.|重新評估
escalate|v.|升級、加劇
tension|n.|緊張局勢
downside risk|phr.|下行風險
fragile|adj.|脆弱的
public finances|phr.|公共財政
pointed|adj.|直接的、尖銳的（言論）
suppress|v.|壓制、抑制
cost-of-living crisis|phr.|生活成本危機
urge|v.|敦促、力勸
adjust|v.|調整
temporary|adj.|暫時的
targeted|adj.|針對性的、精準的
transfer|n.|移轉（支付）、補助款
fiscal space|phr.|財政空間
physiology|n.|生理學
ion channel|phr.|離子通道
optogenetics|n.|光遺傳學
transform|v.|徹底改變
neuroscience|n.|神經科學
algae|n.|藻類
single-celled|adj.|單細胞的
organism|n.|生物、有機體
respond|v.|回應、產生反應（to）
membrane|n.|薄膜、細胞膜
neuron|n.|神經元
remarkable|adj.|非凡的、顯著的
precision|n.|精確
map|v.|繪製（分布圖）、找出
circuit|n.|迴路、電路
addiction|n.|成癮
application|n.|應用
eventually|adv.|最終
neurological|adj.|神經的
disorder|n.|疾病、失調
recognize|v.|表彰；認出
neglect|v.|忽視
postpone|v.|延後
imitate|v.|模仿
object|v.|反對（to）
contribute|v.|貢獻；促成（to）
physicist|n.|物理學家
observatory|n.|天文台、觀測站
neutrino|n.|微中子
particle|n.|粒子
electric charge|phr.|電荷
interact|v.|相互作用
trace|n.|痕跡
property|n.|特性、性質
messenger|n.|信使
scatter|v.|散射、分散
violent|adj.|劇烈的
detector|n.|偵測器
sensor|n.|感測器
drill|v.|鑽（孔）
collide|v.|碰撞
give off|phr.|發出（光、熱、氣味）
faint|adj.|微弱的
skeptic|n.|懷疑論者
ambitious|adj.|有雄心的、規模宏大的
astrophysical|adj.|天體物理的
origin|n.|起源、來源
cosmos|n.|宇宙
astronomer|n.|天文學家
phenomenon|n.|現象（複數 phenomena）"""


def sentences_of(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", str(text or "")) if len(s.strip()) > 20]


def example_for(word, sentences):
    w = word.lower()
    parts = [re.escape(p) for p in re.split(r"[\s-]+", w)]
    # exact (space or hyphen between words), then inflected words (breaches, urges, looking, mitigated)
    tries = [re.compile(r"\b" + r"[\s-]+".join(parts) + r"\b", re.I)]
    infl = [re.escape(re.sub(r"(e|y)$", "", p)) + r"(?:e|y)?(?:s|es|d|ed|ing|ies|ied|er|est|ier|iest)?" for p in re.split(r"[\s-]+", w)]
    tries.append(re.compile(r"\b" + r"[\s-]+".join(infl) + r"\b", re.I))
    for rx in tries:
        for s in sentences:
            if rx.search(s):
                return s if len(s) <= 240 else s[:237] + "…"
    return ""


src, out_path = sys.argv[1], sys.argv[2]
packs = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(src, "bank", "*.json")))]
known, sentences = set(), []
for p in packs:
    # cloze answers go back into their blanks, in question order
    fills = {}
    for it in p["items"]:
        if it["type"] == "mc" and it.get("section") == "cloze" and it.get("passage"):
            fills.setdefault(it["passage"], []).append(it["options"][it["answer"]])
    for it in p["items"]:
        if it["type"] == "vocab":
            known.add(it["word"].strip().lower())
        elif it["type"] == "passage":
            ans = fills.get(it["key"], [])
            text = re.sub(r"__\((\d+)\)__", lambda m: ans[int(m.group(1)) - 1] if int(m.group(1)) <= len(ans) else "___", it["text"])
            sentences += sentences_of(text)
        elif it["type"] == "mc":
            stem = it["stem"]
            if it.get("section") in ("vocab", "grammar"):
                stem = re.sub(r"_{2,}", it["options"][it["answer"]], stem, count=1)
            sentences += sentences_of(stem)

# first match is the wrong sense (noun "project" vs. verb "projects")
OVERRIDE = {"project": "Global growth, the Fund projects, will slow to 3.1 percent this year before recovering to 3.4 percent in 2027."}
items, skipped = [], []
for line in WORDS.strip().splitlines():
    w, pos, zh = line.split("|")
    if w.lower() in known:
        skipped.append(w)
        continue
    known.add(w.lower())
    items.append(dict(type="vocab", word=w, pos=pos, zh=zh, example=OVERRIDE.get(w) or example_for(w, sentences), source="題庫補抽"))

pack = dict(title=f"題庫補抽單字（{len(items)} 字）", source="題庫補抽", kind="seed", createdAt=int(time.time() * 1000), items=items)
json.dump(pack, open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
no_ex = [i["word"] for i in items if not i["example"]]
print(f"new={len(items)} skipped_existing={len(skipped)} {skipped}")
print(f"without example={len(no_ex)}: {no_ex}")
