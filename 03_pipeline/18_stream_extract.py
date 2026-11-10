"""Targeted re-extraction from the mediawiki_history dumps WITHOUT storing them (post-review round 2; exploratory).

The raw dumps were deleted after the first pass. Two things asked for in review need fields that were not kept:
  (1) the user groups held by the account that made each recorded revert, at the time of the revert
      (event_user_groups_historical), to test directly whether untagged reverts come from accounts without an
      autopatrol-carrying group;
  (2) block events of cohort accounts (user / alterblocks), so that blocked newcomers can be separated in the retention comparison.

The script streams each dump file of the SAME version (2026-09) through curl | bzip2 -dc and keeps only
  revision rows whose revision_id is in 02_derived/<wiki>_target_revs.txt        -> 02_derived/<wiki>_revgroups.tsv
  user alterblocks rows whose user_id is in 02_derived/<wiki>_cohort_users.txt   -> 02_derived/<wiki>_blocks.tsv
Nothing else is written. Files are processed one at a time with a .done marker, so the run can be interrupted and resumed.
Local copies in 01_raw/<wiki>/ are used when present. Only files from 2019 onward are read (all recorded reverts and all
cohort accounts date from 2019 or later).

Usage: python 03_pipeline/18_stream_extract.py jawiki [--from 2019]
"""
import argparse
import os
import re
import subprocess
import sys
import time
import urllib.request
from importlib import import_module

sys.path.insert(0, os.path.dirname(__file__))
C = import_module("01_schema").COLUMNS
IX = {c: i for i, c in enumerate(C)}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); RAW = os.path.join(ROOT, "01_raw")
BASE = "https://dumps.wikimedia.org/other/mediawiki_history"; VER = "2026-09"
REV_COLS = ["revision_id", "event_timestamp", "event_user_id", "event_user_is_anonymous", "event_user_is_temporary",
            "event_user_groups_historical", "event_user_groups", "event_user_is_bot_by_historical", "event_user_revision_count", "revision_tags"]
BLK_COLS = ["user_id", "event_timestamp", "event_user_id", "user_blocks_historical", "user_blocks"]


def file_list(wiki, start):
    req = urllib.request.Request(f"{BASE}/{VER}/{wiki}/", headers={"User-Agent": "wiki-revert-audit research script"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    files = sorted(set(re.findall(rf"{VER}\.{wiki}\.[0-9a-z-]+\.tsv\.bz2", html)))
    if not files:
        sys.exit(f"version {VER} is no longer listed for {wiki}; this extraction must use the same dump version")
    keep = []
    for f in files:
        tok = f[len(f"{VER}.{wiki}."):-len(".tsv.bz2")]
        if tok == "all-time" or tok >= start:
            keep.append(f)
    return keep


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("wiki"); ap.add_argument("--from", dest="start", default="2019"); a = ap.parse_args()
    wiki = a.wiki
    revs = set(int(x) for x in open(os.path.join(D, f"{wiki}_target_revs.txt")).read().split())
    users = set(int(x) for x in open(os.path.join(D, f"{wiki}_cohort_users.txt")).read().split())
    print(f"[{wiki}] target revisions {len(revs):,}; cohort users {len(users):,}", flush=True)
    out_r = os.path.join(D, f"{wiki}_revgroups.tsv"); out_b = os.path.join(D, f"{wiki}_blocks.tsv")
    mark = os.path.join(D, f"{wiki}_stream_done.txt")
    done = set(open(mark).read().split()) if os.path.exists(mark) else set()
    if not done:
        open(out_r, "w").write("\t".join(REV_COLS) + "\n"); open(out_b, "w").write("\t".join(BLK_COLS) + "\n")
    ri = [IX[c] for c in REV_COLS]; bi = [IX[c] for c in BLK_COLS]; rid_i = IX["revision_id"]; uid_i = IX["user_id"]
    local = os.path.join(RAW, wiki)
    files = sorted(f for f in os.listdir(local) if f.endswith(".tsv.bz2")) if os.path.isdir(local) and any(f.endswith(".tsv.bz2") for f in os.listdir(local)) else None
    if files is not None:
        files = [f for f in files if f[len(f"{VER}.{wiki}."):-len(".tsv.bz2")] >= a.start or "all-time" in f]
    else:
        files = file_list(wiki, a.start)
    t0 = time.time(); nr = nb = 0
    for f in files:
        if f in done:
            continue
        path = os.path.join(local, f)
        cmd = f"bzip2 -dc '{path}'" if os.path.exists(path) else f"curl -fsSL --retry 5 --retry-delay 10 '{BASE}/{VER}/{wiki}/{f}' | bzip2 -dc"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1 << 22)
        rows_r, rows_b, n = [], [], 0
        for raw in p.stdout:
            n += 1
            fl = raw.decode("utf-8", "replace").rstrip("\n").split("\t")
            if len(fl) != len(C):
                continue
            ent = fl[2]
            if ent == "revision":
                v = fl[rid_i]
                if v and int(v) in revs:
                    rows_r.append("\t".join(fl[i] for i in ri))
            elif ent == "user" and fl[3] == "alterblocks":
                v = fl[uid_i]
                if v and int(v) in users:
                    rows_b.append("\t".join(fl[i] for i in bi))
        rc = p.wait()
        if rc != 0:
            sys.exit(f"stream failed for {f} (exit {rc}); rerun to resume")
        with open(out_r, "a") as fh:
            fh.write("".join(r + "\n" for r in rows_r))
        with open(out_b, "a") as fh:
            fh.write("".join(r + "\n" for r in rows_b))
        with open(mark, "a") as fh:
            fh.write(f + "\n")
        nr += len(rows_r); nb += len(rows_b)
        print(f"  {f}: rows {n:,}; kept revisions {len(rows_r):,}, block events {len(rows_b):,}; {time.time()-t0:,.0f}s", flush=True)
    print(f"[{wiki}] stream extraction done: revisions {nr:,} of {len(revs):,} targets, block events {nb:,}; {time.time()-t0:,.0f}s", flush=True)


if __name__ == "__main__":
    main()
