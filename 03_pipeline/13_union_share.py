"""봇 ∪ 도구 점유율(합집합) 표. 04 의 bot_share·tool_share 는 각각 따로 계산되어 봇이 롤백으로 되돌린 경우(enwiki ClueBot NG) 두 열에 중복된다.
strict 항등식 Δ = p(F0) × (봇 ∪ 도구 점유율) 과 그림 2 의 X 축은 합집합을 써야 한다.

출력  04_output/union_share.csv : wiki, year(all 포함), n, p_F0_24h, bot_share, tool_share, union_share, rel_delta_strict, rel_delta_replace(표본)
사용법: python 03_pipeline/13_union_share.py
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); O = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]


def inw(sec, w):
    s = sec.astype(float); return s.notna() & (s <= w)


def main():
    rows = []
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_anchors.parquet"),
                            columns=["anchor_rank", "anchor_year", "created_by_self", "anchor_on_allrevs", "is_reverted_d1", "sec_to_revert",
                                     "reverter_is_bot", "reverter_is_tool", "d3_sec_to_revert", "d3nt_sec_to_revert"])
        g = A[(A.anchor_rank == 1) & (A.anchor_year >= 2019) & A.created_by_self.fillna(False).astype(bool)].copy()
        for c in ["reverter_is_bot", "reverter_is_tool"]: g[c] = g[c].fillna(False).astype(bool)
        g["f0"] = g.is_reverted_d1.astype(bool) & inw(g.sec_to_revert, 86400)
        g["bot"] = g.f0 & g.reverter_is_bot; g["tool"] = g.f0 & g.reverter_is_tool; g["union"] = g.bot | g.tool
        s = g[g.anchor_on_allrevs.fillna(False).astype(bool)].copy()
        s["r0"] = inw(s.d3_sec_to_revert, 86400); s["r2"] = inw(s.d3nt_sec_to_revert, 86400)
        def summarize(gg, ss, year):
            nrev = gg.f0.sum()
            if nrev == 0: return None
            p0 = gg.f0.mean()
            return dict(wiki=w, year=year, n=len(gg), n_sample=len(ss), p_F0_24h=p0, bot_share=gg.bot.sum() / nrev, tool_share=gg.tool.sum() / nrev,
                        union_share=gg["union"].sum() / nrev, rel_delta_strict=gg["union"].sum() / nrev,
                        p_F0d3_24h=ss.r0.mean() if len(ss) else float("nan"),
                        rel_delta_replace=((ss.r0.mean() - ss.r2.mean()) / ss.r0.mean()) if len(ss) and ss.r0.mean() > 0 else float("nan"))
        rows.append(summarize(g, s, "all"))
        for y, gg in g.groupby("anchor_year"):
            r = summarize(gg, s[s.anchor_year == y], str(int(y)))
            if r: rows.append(r)
    T = pd.DataFrame([r for r in rows if r]); T.to_csv(os.path.join(O, "union_share.csv"), index=False)
    print(T[T.year == "all"].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
