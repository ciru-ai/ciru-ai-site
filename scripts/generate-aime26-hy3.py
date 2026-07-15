#!/usr/bin/env python3
"""Build the frozen AIME 2026 Hy3 demo data from MathArena artifacts."""

from __future__ import annotations

import io
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import zstandard


RUN = Path(os.environ["AIME26_RUN_DIR"])
OUTPUT = Path(__file__).resolve().parents[1] / "public/aime26/hy3-data.js"
SNAPSHOT_PROBLEMS = tuple(range(1, 9))

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
    4: {
        "local": {
            "overview": "Rewrote the expression as a shifted product, then counted distinct products through 101 by separating even products from odd composites.",
            "steps": [
                "Set N+1=(a+1)(b+1), with two distinct factors at least 2.",
                "Counted the 48 eligible even products from 6 through 100.",
                "Enumerated 22 odd composites with a distinct-factor decomposition.",
                "Added the two classes to obtain 70 representable integers.",
            ],
            "style": "Constructive counting with an explicit odd-composite list and repeated checks for duplicate products.",
        },
        "api": {
            "overview": "Used the shifted-product form and characterized the failures as primes or prime squares, reducing the problem to a short complement count.",
            "steps": [
                "Converted a+b+ab into (a+1)(b+1)-1.",
                "Observed that N+1 needs two distinct nontrivial factors.",
                "Counted 74 composites through 101.",
                "Removed the four prime squares 4, 9, 25, and 49 to get 70.",
            ],
            "style": "Compact complement counting, with care not to exclude composite squares that have another factorization.",
        },
    },
    5: {
        "local": {
            "overview": "Placed the rotations in coordinates, simplified the second rotation to a unit horizontal shift, and solved the resulting distance equation.",
            "steps": [
                "Set B=(0,0), A=(1,0), and A'=(cos theta,sin theta).",
                "Rotated the vector from A' to B clockwise to obtain (-1,0).",
                "Located B' at (cos theta-1,sin theta).",
                "Used AB'^2=5-4 cos theta=16/9 to get cos theta=29/36 and answer 65.",
            ],
            "style": "Coordinate and complex-number reasoning with detailed orientation and acute-angle checks.",
        },
        "api": {
            "overview": "Modeled both rotations with vectors, found B' directly, and reduced the geometry to one Pythagorean identity.",
            "steps": [
                "Normalized the original segment to B=(0,0) and A=(1,0).",
                "Placed A' on the unit circle at angle theta.",
                "Applied the clockwise rotation to obtain B'=(cos theta-1,sin theta).",
                "Solved 5-4 cos theta=16/9 and returned 29+36=65.",
            ],
            "style": "Direct vector geometry followed by an independent orientation sanity check.",
        },
    },
    6: {
        "local": {
            "overview": "Turned the logarithmic radical equation into a quadratic in an exponent, then used Vieta's formula to find the product without solving either root.",
            "steps": [
                "Let a=log base 2026 of x, so x=2026^a.",
                "Converted the equation to a^2-20a-20 log_2026(26)=0.",
                "Used a1+a2=20 to obtain x1x2=2026^20.",
                "Factored 2026^20 as 2^20 times 1013^20 and counted 441 divisors.",
            ],
            "style": "Algebraic reduction with extensive domain, root-count, and primality validation.",
        },
        "api": {
            "overview": "Substituted a base-2026 exponent, used the quadratic root sum, and factored the resulting integer product.",
            "steps": [
                "Write x=2026^t using t=log_2026(x).",
                "Equate base-2026 exponents to form a quadratic in t.",
                "Apply Vieta to show the two solution exponents sum to 20.",
                "Count the divisors of 2^20 times 1013^20 as 21 squared, or 441.",
            ],
            "style": "Straight Vieta shortcut supported by checks that both real roots yield valid positive solutions.",
        },
    },
    7: {
        "local": {
            "overview": "Recognized the onto map as a permutation, translated the sixth-iterate condition into an order constraint, and counted the allowed cycle types.",
            "steps": [
                "Use finiteness to turn surjectivity into bijectivity.",
                "Require the permutation order, the LCM of its cycle lengths, to divide 6.",
                "Count the eight allowable partitions built from cycles of lengths 1, 2, 3, and 6.",
                "Sum their counts to obtain 396.",
            ],
            "style": "Systematic cycle-type enumeration with a complementary count as a cross-check.",
        },
        "api": {
            "overview": "Converted the function problem to S6 and enumerated every cycle decomposition whose lengths divide six.",
            "steps": [
                "Identify each valid function with a permutation of six elements.",
                "Interpret pi^6=id as an order-divides-six condition.",
                "Compute the counts for cycle types 1^6, 2 1^4, 2^2 1^2, 2^3, 3 1^3, 3 2 1, 3^2, and 6.",
                "Add 1+15+45+15+40+120+40+120 to get 396.",
            ],
            "style": "Direct symmetric-group counting with total-order and excluded-cycle sanity checks.",
        },
    },
    8: {
        "local": {
            "overview": "Factored the base into four primes and reduced every divisor modulo 12 to the parity pattern of three exponents.",
            "steps": [
                "Factor 17017 as 7 times 11 times 13 times 17.",
                "Note that 13 contributes 1 modulo 12 and the other three residues square to 1.",
                "Find the two exponent-parity patterns that produce residue 5.",
                "Count 2 times 9 cubed times 18 = 26244 divisors and return 244 modulo 1000.",
            ],
            "style": "Explicit parity-table counting with checks against the total divisor count.",
        },
        "api": {
            "overview": "Used the prime factorization and modulo-12 parity cycles to show exactly one quarter of all divisors have the required residue.",
            "steps": [
                "Represent each divisor by four exponents from 0 through 17.",
                "Discard the 13-exponent from the residue calculation because 13 is 1 modulo 12.",
                "Select parity triples (even,even,odd) and (odd,odd,even).",
                "Evaluate the count as 26244 and reduce it to 244 modulo 1000.",
            ],
            "style": "Concise modular counting, reinforced by a CRT-style parity cross-check.",
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
        "snapshotLabel": f"Shared-completion demo · Problems {SNAPSHOT_PROBLEMS[0]}–{SNAPSHOT_PROBLEMS[-1]}",
        "snapshotUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
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
