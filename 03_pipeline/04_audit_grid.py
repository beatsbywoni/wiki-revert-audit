"""3×3 감사 격자와 go/no-go 보고서.

입력  02_derived/<wiki>_anchors.parquet
출력  04_output/<wiki>_grid.csv, <wiki>_grid_by_year.csv, <wiki>_success_rank.csv, <wiki>_gonogo_report.md

변형(variant):
  strict   덤프 D1 기준, 봇·도구가 첫 되돌림이면 "되돌려지지 않음"으로 처리(흔한 전처리 재현)   F0/F1/F2
  replace  D3(refinery 규칙 재현, 반경 없음)에서 첫 비봇(비도구) 되돌림으로 대체                 F0d3/F1r/F2r
  radius15 D3 를 mwreverts 반경 15 로 계산한 변형(문헌 관행)                                    F0r15/F1r15/F2r15

사용법: python 03_pipeline/04_audit_grid.py kowiki --min-year 2019 --boot 2000
"""
import argparse
import os
import sys
from importlib import import_module

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
schema = import_module("01_schema")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILTERS = ["F0", "F1", "F2"]              # strict 변형(덤프 D1 기준)
FILTERS_REPLACE = ["F0d3", "F1r", "F2r"]  # replace 변형(06 D3 재계산 후 존재)
R = schema.MWREVERTS_RADIUS
FILTERS_R15 = [f"F0r{R}", f"F1r{R}", f"F2r{R}"]
WINDOWS = list(schema.WINDOWS.keys())


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def paired_delta_ci(a, b, boot, rng):
    """같은 앵커 집합에서 mean(a) - mean(b) 의 부트스트랩 CI (앵커 = 편집자 1인 1행이므로 행 단위 재표집 = 편집자 군집)."""
    a = a.astype(float).to_numpy()
    b = b.astype(float).to_numpy()
    n = len(a)
    idx = rng.integers(0, n, size=(boot, n))
    d = (a[idx].mean(axis=1) - b[idx].mean(axis=1)) * 100
    return (a.mean() - b.mean()) * 100, np.percentile(d, 2.5), np.percentile(d, 97.5)


def odds_ratio(flag, outcome):
    t = pd.crosstab(flag.astype(bool), outcome.astype(bool)).reindex(index=[True, False], columns=[True, False], fill_value=0)
    # Haldane-Anscombe 보정(+0.5): 빈 셀이 있을 때 발산 방지. 본 분석에서는 빈 셀이 있으면 각주로 표기.
    a, b = t.loc[True, True] + 0.5, t.loc[True, False] + 0.5
    c, d = t.loc[False, True] + 0.5, t.loc[False, False] + 0.5
    if min(a, b, c, d) < 1:
        return (np.nan, np.nan, np.nan)
    orv = (a * d) / (b * c)
    se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return orv, np.exp(np.log(orv) - 1.96 * se), np.exp(np.log(orv) + 1.96 * se)


def grid_for(df, boot, rng, label="", filters=None, base_f="F0", variant="strict"):
    rows = []
    filters = filters or FILTERS
    for w in WINDOWS:
        base = df[f"{base_f}_{w}"]
        for f in filters:
            col = df[f"{f}_{w}"]
            n, k = len(col), int(col.sum())
            lo, hi = wilson(k, n)
            d, dlo, dhi = (0.0, 0.0, 0.0) if f == base_f else paired_delta_ci(base, col, boot, rng)
            orv, olo, ohi = odds_ratio(col, df["retained_2_60"])
            rev = df[col]
            rows.append(dict(
                label=label, variant=variant, F=f, W=w, n_anchor=n, p_reverted=k / n if n else np.nan,
                ci_lo=lo, ci_hi=hi, delta_vs_F0_pp=d, delta_ci_lo=dlo, delta_ci_hi=dhi,
                or_retention=orv, or_lo=olo, or_hi=ohi,
                bot_share=rev["reverter_is_bot"].mean() if len(rev) else np.nan,
                tool_share=rev["reverter_is_tool"].mean() if len(rev) else np.nan,
            ))
    return pd.DataFrame(rows)


def h1_window_test(df, boot, rng, f0="F0d3", f2="F2r"):
    """H1(2026-10-27 확정): replace 변형에서 D = Δ(W24h) − Δ(W∞) > 0 의 단측 부트스트랩 CI(편집자 군집)와 비율 R = Δ(W∞)/Δ(W24h)."""
    need = [f"{f0}_W24h", f"{f2}_W24h", f"{f0}_Winf", f"{f2}_Winf"]
    if not all(c in df.columns for c in need):
        return None
    sub = df[df["anchor_on_allrevs"].fillna(False).astype(bool)] if "anchor_on_allrevs" in df.columns else df
    if len(sub) < 50:
        return None
    a24 = (sub[f"{f0}_W24h"].astype(float) - sub[f"{f2}_W24h"].astype(float)).to_numpy()
    ainf = (sub[f"{f0}_Winf"].astype(float) - sub[f"{f2}_Winf"].astype(float)).to_numpy()
    n = len(a24)
    idx = rng.integers(0, n, size=(boot, n))
    d24 = a24[idx].mean(axis=1); dinf = ainf[idx].mean(axis=1)
    D = (d24 - dinf) * 100
    R = np.where(d24 > 0, dinf / np.where(d24 > 0, d24, np.nan), np.nan)
    return dict(n=n, delta24_pp=a24.mean() * 100, deltainf_pp=ainf.mean() * 100,
                D_pp=(a24.mean() - ainf.mean()) * 100, D_ci90_lo=np.percentile(D, 5), D_ci95_lo=np.percentile(D, 2.5), D_ci95_hi=np.percentile(D, 97.5),
                R=ainf.mean() / a24.mean() if a24.mean() > 0 else np.nan, R_ci_lo=np.nanpercentile(R, 2.5), R_ci_hi=np.nanpercentile(R, 97.5))


def confirmatory_tests(df, boot, rng):
    """등록 검정 H2(대체율 S)·H3(정의 일치)·H4(OR 최대/최소 비). H1 은 h1_window_test."""
    out = {}
    sub = df[df["anchor_on_allrevs"].fillna(False).astype(bool)] if "anchor_on_allrevs" in df.columns else df.iloc[0:0]
    # H2: S = 1 − Δ(F2r,24h)/Δ(F2 strict,24h), 같은 D3 표본에서. 단측 95% 상한.
    if len(sub) >= 50 and "F2r_W24h" in sub.columns:
        ds = (sub["F0_W24h"].astype(float) - sub["F2_W24h"].astype(float)).to_numpy()
        dr = (sub["F0d3_W24h"].astype(float) - sub["F2r_W24h"].astype(float)).to_numpy()
        n = len(ds); idx = rng.integers(0, n, size=(boot, n))
        bs, br = ds[idx].mean(axis=1), dr[idx].mean(axis=1)
        S = 1 - br / np.where(bs > 0, bs, np.nan)
        out.update(h2_n=n, h2_delta_strict_pp=ds.mean() * 100, h2_delta_replace_pp=dr.mean() * 100,
                   h2_S=(1 - dr.mean() / ds.mean()) if ds.mean() > 0 else np.nan,
                   h2_S_ci95_hi_onesided=np.nanpercentile(S, 95), h2_S_ci_lo=np.nanpercentile(S, 2.5), h2_S_ci_hi=np.nanpercentile(S, 97.5))
    # H3: 앵커 2020-08-01 이후, D2 vs D3r15 일치율; D1=1,D2=0 중 반경 15 밖 비율
    if "d3r_is_reverted" in sub.columns:
        g = sub[sub["anchor_ts"] >= pd.Timestamp("2020-08-01", tz="UTC")]
        if len(g) >= 50:
            d1 = g["is_reverted_d1"].astype(bool); d2 = g["is_reverted_d2"].astype(bool); r15 = g["d3r_is_reverted"].astype(bool)
            x = g[d1 & ~d2]
            out.update(h3_n=len(g), h3_agree_d2_d3r15=(d2 == r15).mean(), h3_agree_d1_d2=(d1 == d2).mean(),
                       h3_n_d1only=len(x), h3_d1only_beyond_radius=(~x["d3r_is_reverted"].astype(bool)).mean() if len(x) else np.nan)
    # H4: strict 9셀 OR 최대/최소 비, 부트스트랩(boot//4) 95% 하한 (numpy 로 빠르게)
    cells = [(f, w) for w in WINDOWS for f in FILTERS]
    flags = np.stack([df[f"{f}_{w}"].astype(bool).to_numpy() for f, w in cells], axis=1)  # n × 9
    ret = df["retained_2_60"].astype(bool).to_numpy()
    def or_ratio(rows):
        fl = flags[rows]; rt = ret[rows][:, None]
        a_ = (fl & rt).sum(0) + 0.5; b_ = (fl & ~rt).sum(0) + 0.5
        c_ = (~fl & rt).sum(0) + 0.5; d_ = (~fl & ~rt).sum(0) + 0.5
        ors = (a_ * d_) / (b_ * c_)
        return ors.max() / ors.min()
    n = len(df); all_rows = np.arange(n)
    rr = or_ratio(all_rows)
    nb = max(100, boot // 4)
    ratios = [or_ratio(rng.integers(0, n, size=n)) for _ in range(nb)]
    out.update(h4_or_ratio=rr, h4_or_ratio_ci_lo=np.nanpercentile(ratios, 2.5), h4_or_ratio_ci_hi=np.nanpercentile(ratios, 97.5), h4_boot=nb)
    # 음성 대조(봇 축): 연도별 셀 중 봇 점유율 < 1% 인 셀의 Δ(F0d3 − F1r, 24h) CI
    neg = []
    if "F1r_W24h" in sub.columns:
        for y, g in sub.groupby("anchor_year"):
            if len(g) < 50:
                continue
            rev = g[g["F0_W24h"]]
            bot_share = rev["reverter_is_bot"].mean() if len(rev) else np.nan
            if bot_share < 0.01:
                d, lo, hi = paired_delta_ci(g["F0d3_W24h"], g["F1r_W24h"], max(200, boot // 10), rng)
                neg.append(dict(year=int(y), n=len(g), bot_share=bot_share, delta_pp=d, ci_lo=lo, ci_hi=hi, within_0p5=(abs(lo) <= 0.5 and abs(hi) <= 0.5)))
    return out, pd.DataFrame(neg)


def success_rank(df):
    """첫 90일 ≥10 편집 편집자의 success rate: F0 vs F2, W24h·Winf 에서 순위 상관과 하위 10% 이동."""
    e = df[df["n_edits_90d"].fillna(0) >= 10].copy()
    out = []
    for w in ["W24h", "Winf"]:
        s0 = 1 - e[f"n_rv_F0_{w}"] / e["n_edits_90d"]
        s2 = 1 - e[f"n_rv_F2_{w}"] / e["n_edits_90d"]
        rho = s0.rank().corr(s2.rank())  # Spearman (scipy 불필요)
        q = 0.10
        top0 = set(e.index[s0 <= s0.quantile(q)])   # 되돌림 많은 하위 10%(success 낮음)
        top2 = set(e.index[s2 <= s2.quantile(q)])
        moved = 1 - len(top0 & top2) / max(len(top0), 1)
        out.append(dict(W=w, n_editors=len(e), spearman_F0_vs_F2=rho, bottom10_moved_share=moved,
                        mean_sr_F0=s0.mean(), mean_sr_F2=s2.mean()))
    return pd.DataFrame(out)


def all_grids(df, boot, rng, label):
    """strict 는 전체 앵커, replace·radius 변형은 D3 를 계산한 앵커(anchor_on_allrevs; enwiki 는 표본)에서만."""
    parts = [grid_for(df, boot, rng, label=label)]
    if "anchor_on_allrevs" in df.columns:
        sub = df[df["anchor_on_allrevs"].fillna(False).astype(bool)]
        if len(sub) >= 50:
            # 같은 표본에서 strict 도 다시 산출해 변형 간 비교가 같은 앵커 집합이 되게 한다
            parts.append(grid_for(sub, boot, rng, label=label, variant="strict_d3sample"))
            if all(f"{f}_Winf" in sub.columns for f in FILTERS_REPLACE):
                parts.append(grid_for(sub, boot, rng, label=label, filters=FILTERS_REPLACE, base_f="F0d3", variant="replace"))
            if all(f"{f}_Winf" in sub.columns for f in FILTERS_R15):
                parts.append(grid_for(sub, boot, rng, label=label, filters=FILTERS_R15, base_f=FILTERS_R15[0], variant=f"radius{R}"))
    return pd.concat(parts, ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki")
    ap.add_argument("--min-year", type=int, default=2019, help="태그 가용 이후만(V3 결과로 조정)")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261026)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    d = os.path.join(ROOT, "02_derived")
    o = os.path.join(ROOT, "04_output")
    os.makedirs(o, exist_ok=True)
    anchors = pd.read_parquet(os.path.join(d, f"{a.wiki}_anchors.parquet"))
    first = anchors[(anchors["anchor_rank"] == 1) & (anchors["anchor_year"] >= a.min_year)].copy()
    first = first[first["created_by_self"].fillna(False)]  # 주 분석: self-created
    has_replace = all(f"{f}_Winf" in first.columns for f in FILTERS_REPLACE)

    grid = all_grids(first, a.boot, rng, label=f"{a.wiki}_{a.min_year}+_self")
    grid.to_csv(os.path.join(o, f"{a.wiki}_grid.csv"), index=False)
    by_year = pd.concat([all_grids(g, max(200, a.boot // 10), rng, label=str(y))
                         for y, g in first.groupby("anchor_year") if len(g) >= 50])
    by_year.to_csv(os.path.join(o, f"{a.wiki}_grid_by_year.csv"), index=False)
    sr = success_rank(first)
    sr.to_csv(os.path.join(o, f"{a.wiki}_success_rank.csv"), index=False)
    h1 = h1_window_test(first, a.boot, rng)
    conf, neg = confirmatory_tests(first, a.boot, rng)
    pd.DataFrame([{**(h1 or {}), **conf}]).to_csv(os.path.join(o, f"{a.wiki}_confirmatory.csv"), index=False)
    if len(neg):
        neg.to_csv(os.path.join(o, f"{a.wiki}_negative_control.csv"), index=False)
    h1_lines = []
    if h1:
        h1_lines = [f"- H1 창 간 차이(replace, D3 앵커 n={h1['n']:,}): Δ(24h) = {h1['delta24_pp']:.2f}pp, Δ(∞) = {h1['deltainf_pp']:.2f}pp, "
                    f"D = {h1['D_pp']:.2f}pp [단측 95% 하한 {h1['D_ci90_lo']:.2f}; 양측 95% {h1['D_ci95_lo']:.2f}, {h1['D_ci95_hi']:.2f}], "
                    f"R = Δ(∞)/Δ(24h) = {h1['R']:.3f} [{h1['R_ci_lo']:.3f}, {h1['R_ci_hi']:.3f}] → "
                    + ("H1 지지" if h1['D_ci90_lo'] > 0 else "H1 미지지") + (", R ≥ 0.75(대부분 잔존)" if h1['R'] >= 0.75 else ", R < 0.75")]

    # go/no-go 판정 (02_plan/timeline_and_gonogo.md 기준)
    g = grid[grid["variant"].isin(["strict", "replace"])].set_index(["F", "W"])
    fjudge = "F2r" if has_replace else "F2"   # H1 의 정식 검정 대상은 replace 변형
    d24 = abs(g.loc[(fjudge, "W24h"), "delta_vs_F0_pp"])
    d7 = abs(g.loc[(fjudge, "W7d"), "delta_vs_F0_pp"])
    dinf_lo, dinf_hi = g.loc[(fjudge, "Winf"), ["delta_ci_lo", "delta_ci_hi"]]
    rho24 = sr.set_index("W").loc["W24h", "spearman_F0_vs_F2"]
    moved24 = sr.set_index("W").loc["W24h", "bottom10_moved_share"]
    cond1 = (d24 >= 5) or (d7 >= 5) or (rho24 < 0.95) or (moved24 >= 0.15)
    cond2 = (abs(dinf_lo) <= 2) and (abs(dinf_hi) <= 2)
    verdict = "GO" if cond1 else "NO-GO(둔감)"
    note = "창 대비 패턴 성립(H1 서술 유지)" if cond2 else "W∞도 움직임(H1 서술 수정 필요)"
    lines = [
        f"# go/no-go 보고 — {a.wiki} (앵커 {a.min_year}년 이후, self-created, n={len(first):,})", "",
        f"**판정: {verdict}** · {note} · 판정 기준 필터: {fjudge}"
        + ("" if has_replace else " (replace 변형 없음: 06_recompute_reverts_d3.py 실행 후 재판정 권장)"), "",
        f"- |Δp| F0−F2 W24h = {d24:.2f}pp, W7d = {d7:.2f}pp, W∞ CI = [{dinf_lo:.2f}, {dinf_hi:.2f}]pp",
        f"- success rate Spearman(F0 vs F2, W24h) = {rho24:.3f}, 하위 10% 이동 = {moved24:.1%}",
        *h1_lines,
        (f"- H2 대체율 S(D3 표본 n={conf['h2_n']:,}): Δ strict {conf['h2_delta_strict_pp']:.2f}pp, Δ replace {conf['h2_delta_replace_pp']:.2f}pp, "
         f"S = {conf['h2_S']:.3f} [단측 95% 상한 {conf['h2_S_ci95_hi_onesided']:.3f}; 양측 {conf['h2_S_ci_lo']:.3f}, {conf['h2_S_ci_hi']:.3f}] → "
         + ("H2 지지(S < 0.25)" if conf['h2_S_ci95_hi_onesided'] < 0.25 else "H2 미지지")) if "h2_S" in conf else "- H2: D3 표본 없음",
        (f"- H3 정의 일치(앵커 2020-08+, n={conf['h3_n']:,}): D2 vs D3r15 {conf['h3_agree_d2_d3r15']:.4f}, D1 vs D2 {conf['h3_agree_d1_d2']:.4f}; "
         f"D1만 되돌림 {conf['h3_n_d1only']:,}건 중 반경 15 밖 {conf['h3_d1only_beyond_radius']:.3f} → "
         + ("H3 지지" if (conf['h3_agree_d2_d3r15'] >= 0.95 and conf['h3_d1only_beyond_radius'] > 0.5) else "H3 미지지")) if "h3_n" in conf else "- H3: 해당 앵커 없음",
        f"- H4 OR 최대/최소 비(strict 9셀): {conf['h4_or_ratio']:.3f} [{conf['h4_or_ratio_ci_lo']:.3f}, {conf['h4_or_ratio_ci_hi']:.3f}] (boot {conf['h4_boot']}) → "
        + ("H4 지지" if (conf['h4_or_ratio'] >= 1.5 and conf['h4_or_ratio_ci_lo'] > 1.0) else "H4 미지지"),
        (f"- 음성 대조(봇 점유율 < 1% 연도 셀 {len(neg)}개): ±0.5pp 안 {int(neg['within_0p5'].sum())}개" if len(neg) else "- 음성 대조: 봇 점유율 < 1% 셀 없음"),
        f"- 되돌린 쪽 join 실패 = {int(first['reverter_join_failed'].sum()):,} / 되돌림 {int(first['is_reverted_d1'].sum()):,}",
        (f"- D3 계산 앵커 {int(first['anchor_on_allrevs'].sum()):,} / {len(first):,}; D1≠D3 불일치 비율 = "
         f"{first.loc[first['anchor_on_allrevs'], 'd1_d3_mismatch'].mean():.5f} "
         f"(되돌린 revision 까지 비교 {first.loc[first['anchor_on_allrevs'], 'd1_d3_rev_mismatch'].mean():.5f})"
         if has_replace else "- D3 재계산 미실행"),
        "", "## 격자", grid.round(4).to_markdown(index=False), "", "## success rate", sr.round(4).to_markdown(index=False),
        "", "주의: 이 보고는 파일럿이며 확증 분석은 다른 위키에서 사전등록 후 수행한다.",
    ]
    with open(os.path.join(o, f"{a.wiki}_gonogo_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("\n".join(lines[:8]))


if __name__ == "__main__":
    main()
