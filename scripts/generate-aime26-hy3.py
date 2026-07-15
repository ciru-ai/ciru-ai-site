#!/usr/bin/env python3
"""Build the frozen AIME 2026 Hy3 demo data from MathArena artifacts."""

from __future__ import annotations

import io
import json
import os
from pathlib import Path

import zstandard


RUN = Path(os.environ["AIME26_RUN_DIR"])
OUTPUT = Path(__file__).resolve().parents[1] / "public/aime26/hy3-data.js"
SNAPSHOT_PROBLEMS = (1, 2, 3)

MODELS = {
    "local": {
        "name": "Hy3 Chadrock FPX-IFP2 MTP",
        "short": "Local Chadrock",
        "accent": "red",
        "root": RUN / "raw/matharena-full/outputs",
        "runtime": "Local ROCmFPX · Radeon 8060S · native MTP n=2",
    },
    "api": {
        "name": "Tencent Hy3 API",
        "short": "API Hy3",
        "accent": "cyan",
        "root": RUN / "raw/matharena-api-full/outputs",
        "runtime": "OpenRouter · Novita · high reasoning",
    },
}

SUMMARIES = {
    1: {
        "local": {
            "overview": "Turned the staggered departures into equal-distance equations, solved for travel time and Patrick’s speed, then reduced the distance fraction.",
            "steps": [
                "Set Patrick’s speed to p and common arrival time to T.",
                "Equated pT, (p+2)(T−1), and (p+9)(T−2).",
                "Derived T = 14/5 and p = 18/5.",
                "Computed 252/25 miles and returned 252 + 25 = 277.",
            ],
            "style": "Methodical algebra with repeated checks of the departure-time interpretation and fraction reduction.",
        },
        "api": {
            "overview": "Built the same timeline model, used Patrick–Tanya and Patrick–Jose equations, and independently checked the resulting speeds and distance.",
            "steps": [
                "Placed departures at hours 0, 1, and 2.",
                "Expressed all three trips using one arrival time.",
                "Solved the linear relationships for T = 14/5 and p = 18/5.",
                "Verified the common distance is 252/25 and answered 277.",
            ],
            "style": "Direct algebra followed by sanity checks against all three travelers.",
        },
    },
    2: {
        "local": {
            "overview": "Used parity to eliminate even-length palindromes, then counted valid left halves as ordered compositions.",
            "steps": [
                "Observed that paired digits make every even-length digit sum even.",
                "For odd length, wrote 2(a₁+⋯+aₖ)+m = 13.",
                "Mapped middle digits 1, 3, 5, 7, 9 to left-half sums 6, 5, 4, 3, 2.",
                "Summed 2^(S−1) over those five sums to get 62.",
            ],
            "style": "Combinatorial derivation with extensive edge-case checks on digit bounds, length, and uniqueness.",
        },
        "api": {
            "overview": "Reduced the palindrome to its free half and center digit, counted compositions, and cross-checked the result with generating-function reasoning.",
            "steps": [
                "Ruled out even lengths because the target digit sum is odd.",
                "Constrained the left-half sum A to {2,3,4,5,6}.",
                "Counted each ordered positive composition of A as one palindrome.",
                "Added 2 + 4 + 8 + 16 + 32 to obtain 62.",
            ],
            "style": "A composition count backed by a second generating-function verification.",
        },
    },
    3: {
        "local": {
            "overview": "Converted the solid-containment question into a center-distance inequality, then turned the allowable placements into a smaller disk.",
            "steps": [
                "Placed the hemisphere center at the origin and the small sphere center at (x,y,42).",
                "Required the farthest small-sphere point to remain within radius 200.",
                "Solved √(x²+y²+42²)+42 ≤ 200, giving x²+y² ≤ 23200.",
                "Compared disk areas: 23200/40000 = 29/50, so p+q = 79.",
            ],
            "style": "Highly exploratory geometry: it repeatedly tested interpretations of “inside the hemisphere” before locking the containment proof.",
        },
        "api": {
            "overview": "Modeled the hemisphere as the upper half-ball and used the standard ball-in-ball containment condition for the tangent sphere.",
            "steps": [
                "Set the placement radius to ρ and the small sphere center height to 42.",
                "Used |OC| + 42 ≤ 200 as the exact containment condition.",
                "Derived ρ² ≤ (158²−42²) = 23200.",
                "Reduced the area ratio to 29/50 and returned 79.",
            ],
            "style": "Long-form geometric validation with explicit checks of the flat base, upper-half constraint, and farthest-point argument.",
        },
    },
}


def load_zst(path: Path) -> dict:
    with path.open("rb") as raw:
        with zstandard.ZstdDecompressor().stream_reader(raw) as reader:
            with io.TextIOWrapper(reader, encoding="utf-8") as text:
                return json.load(text)


def artifact(root: Path, problem: int) -> Path:
    matches = list(root.rglob(f"{problem}.json.zst"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one artifact for problem {problem} under {root}, got {matches}")
    return matches[0]


def model_record(model_key: str, problem: int) -> tuple[dict, dict]:
    config = MODELS[model_key]
    record = load_zst(artifact(config["root"], problem))
    messages = record["messages"][0]
    thinking = next(m["content"] for m in messages if m.get("type") == "cot")
    answer = next(m["content"] for m in messages if m.get("type") == "response")
    cost = record["detailed_costs"][0]
    seconds = float(cost.get("request_time") or cost.get("time") or 0)
    tokens = int(cost.get("output_tokens") or 0)
    result = {
        "key": model_key,
        "name": config["name"],
        "short": config["short"],
        "accent": config["accent"],
        "runtime": config["runtime"],
        "answer": record["answers"][0],
        "correct": bool(record["correct"][0]),
        "tokens": tokens,
        "thinkingChars": len(thinking),
        "seconds": round(seconds, 1),
        "summary": SUMMARIES[problem][model_key],
        "thinking": thinking,
        "finalResponse": answer,
    }
    return record, result


def main() -> None:
    problems = []
    for problem in SNAPSHOT_PROBLEMS:
        local_record, local = model_record("local", problem)
        api_record, api = model_record("api", problem)
        if local_record["problem"] != api_record["problem"]:
            raise RuntimeError(f"Question mismatch on problem {problem}")
        if not (local["correct"] and api["correct"]):
            raise RuntimeError(f"Frozen demo requires two correct completed answers for problem {problem}")
        problems.append(
            {
                "number": problem,
                "question": local_record["problem"],
                "goldAnswer": str(local_record["gold_answer"]),
                "models": [local, api],
            }
        )

    payload = {
        "title": "Hy3 vs Hy3 · AIME 2026",
        "snapshotLabel": "Shared-completion demo · Problems 1–3",
        "snapshotUtc": "2026-07-15T06:21:55Z",
        "problems": problems,
    }
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "// Generated from frozen MathArena artifacts.\nwindow.AIME_HY3_DATA=" + encoded + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes; {len(problems)} problems)")


if __name__ == "__main__":
    main()
