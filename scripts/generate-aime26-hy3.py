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
SNAPSHOT_PROBLEMS = tuple(range(1, 16))

MODELS = {
    "local": {
        "name": "Hy3 Chadrock FPX-IFP2 MTP",
        "short": "Local Chadrock",
        "accent": "red",
        "root": RUN / "raw/matharena-full/outputs",
        "runtime": "Local ROCmFPX · Radeon 8060S · native MTP n=2",
    },
    "api": {
        "name": "Hy3 API — Novita (OpenRouter)",
        "short": "Novita API",
        "accent": "cyan",
        "root": RUN / "raw/matharena-api-full/outputs",
        "runtime": "Novita via OpenRouter · third-party · high reasoning",
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
    9: {
        "local": {
            "overview": "Modeled the six rolls as independent face choices, imposed the visibility constraints for stickers 2, 4, and 6, then counted outcomes with exactly five occupied faces.",
            "steps": [
                "Represent the top faces by an ordered sequence f1 through f6.",
                "Require f2 to avoid all later rolls and f4 to avoid rolls 5 and 6.",
                "Fix the distinct faces carrying stickers 2 and 4 and count 480 conditioned assignments.",
                "Count 216 assignments with one blank face, reduce 216/480 to 9/20, and answer 29.",
            ],
            "style": "Detailed occupancy counting with inclusion-exclusion and repeated checks of which stickers remain visible.",
        },
        "api": {
            "overview": "Translated sticker visibility into restrictions on repeated die faces and counted the allowed one-repeat patterns under that condition.",
            "steps": [
                "Treat each roll as an independent uniform choice among six geometric faces.",
                "Enforce that no later sticker covers 2 or 4; sticker 6 is automatically visible.",
                "Classify the valid sequences that occupy exactly five distinct faces.",
                "Obtain conditional probability 9/20 and return 9+20=29.",
            ],
            "style": "Long combinatorial case analysis, ending with a minimal boxed response after several counting cross-checks.",
        },
    },
    10: {
        "local": {
            "overview": "Placed both rotated triangles on their common circumcircle, resolved the orientation condition, and computed the cyclic hexagon area from its central sectors.",
            "steps": [
                "Use the 13-14-15 triangle's area 84 and circumradius 65/8.",
                "Determine the rotation angle and the valid circular order of A, A', C, C', B, and B'.",
                "Express the hexagon as six triangles sharing the circumcenter.",
                "Evaluate the area as 155.7 and round to 156.",
            ],
            "style": "Highly exploratory coordinate and angle analysis with extensive checks against alternate rotations and self-intersecting orders.",
        },
        "api": {
            "overview": "Used exact circumradius and double-angle identities to sum the six central-triangle areas of the rotated cyclic hexagon.",
            "steps": [
                "Compute R=65/8 from Heron's area formula.",
                "Set the selected rotation angle to 90 degrees minus angle C.",
                "Derive the six consecutive central angles and their exact sines.",
                "Apply R squared over 2 times the sine sum to get 155.7, whose nearest integer is 156.",
            ],
            "style": "Compact exact trigonometry with the orientation condition used to select the correct cyclic order.",
        },
    },
    11: {
        "local": {
            "overview": "Used the grid's bipartite coloring and cell degrees to place high values on positive high-degree cells and low values on negative high-degree cells.",
            "steps": [
                "Color the grid like a chessboard so every edge crosses colors.",
                "Put 33 through 64 on one color and 1 through 32 on the other.",
                "Match extreme values to the degree-4, degree-3, and degree-2 cells.",
                "Compute the weighted difference as 3896 and return 896 modulo 1000.",
            ],
            "style": "Careful extremal assignment with explicit degree counts and weighted sums.",
        },
        "api": {
            "overview": "Applied the same bipartite-degree optimization, orienting every edge from the high-number color to the low-number color.",
            "steps": [
                "Use the chessboard partition to separate every adjacent pair.",
                "Assign the largest half to positive coefficients and the smallest half to negative coefficients.",
                "Sort values against each color's matching degree multiset.",
                "Obtain 3896 and reduce it to 896 modulo 1000.",
            ],
            "style": "Compact extremal proof with a coefficient interpretation of the edge sum.",
        },
    },
    12: {
        "local": {
            "overview": "Placed the triangle in coordinates, reflected its centroid across BC, and used the plane through the first three sphere centers to determine the fourth radius.",
            "steps": [
                "Set A=(0,0), B=(6,0), and C=(0,4).",
                "Reflect the centroid across 2x+3y=12 to locate D.",
                "Find the common center plane x+3y−6z+6=0 from radii 1, 2, and 3.",
                "Substitute the center above D to get r=122/39 and answer 161.",
            ],
            "style": "Direct coordinate geometry followed by a linear plane calculation.",
        },
        "api": {
            "overview": "Converted tangency to a linear radius formula over the base plane, then evaluated it at the reflected centroid.",
            "steps": [
                "Represent the first three sphere centers above A, B, and C.",
                "Derive the tangent plane and the radius rule R=x/6+y/2+1.",
                "Reflect the centroid across BC to obtain D=(42/13,124/39).",
                "Evaluate the rule at D to get 122/39 and return 161.",
            ],
            "style": "Efficient affine formulation with coordinate verification at all three known spheres.",
        },
    },
    13: {
        "local": {
            "overview": "Reduced the residue-class binomial sums modulo 503 to a single binomial coefficient, then used Lucas’ theorem to identify the zero range.",
            "steps": [
                "Applied a 502nd-root-of-unity filter over the field with 503 elements.",
                "Transformed the sum to S_r congruent to (-1)^r times C(r+40,40).",
                "Used Lucas’ theorem to find divisibility exactly for r=463 through 501.",
                "Counted those 39 residue classes and answered 39.",
            ],
            "style": "Long finite-field derivation with repeated checks of the endpoint and Lucas-theorem conditions.",
        },
        "api": {
            "overview": "Used the base-503 digits of 10000 and Vandermonde’s identity to collapse each residue sum modulo 503.",
            "steps": [
                "Wrote 10000 as 19 times 503 plus 443.",
                "Applied Lucas’ theorem to each indexed binomial coefficient.",
                "Observed that nonzero terms satisfy a+b at most 462, so no residue wrap occurs.",
                "Obtained C(462,r), leaving exactly 39 zero residues.",
            ],
            "style": "A cleaner Lucas-and-Vandermonde route, followed by careful inclusive endpoint counting.",
        },
    },
    14: {
        "local": {
            "overview": "Encoded the equiangular pentagon with side vectors turning by 72 degrees and related side, diagonal, and perimeter sums.",
            "steps": [
                "Let Q be the side-square sum and split pair products into adjacent and nonadjacent sums.",
                "Used the diagonal-square total to determine the adjacent product sum.",
                "Used vector closure and cosines of 72 and 144 degrees to determine the nonadjacent sum.",
                "Computed the perimeter square as 676 sqrt(5), giving 681.",
            ],
            "style": "Vector geometry with extensive numerical and regular-pentagon sanity checks.",
        },
        "api": {
            "overview": "Used the same cyclic side-vector invariants to recover the two pair-product sums and hence the perimeter.",
            "steps": [
                "Summed the five diagonal-square formulas.",
                "Solved for the adjacent side-product sum using cos(72 degrees).",
                "Applied polygon closure to solve for the nonadjacent product sum.",
                "Simplified the perimeter square to 676 sqrt(5) and answered 681.",
            ],
            "style": "Structured invariant derivation with a coordinate-style numerical check at the end.",
        },
    },
    15: {
        "local": {
            "overview": "Classified loops as solid strips or hollow frames and attempted to count partitions by the number of frames, but omitted valid non-nested frame layouts.",
            "steps": [
                "Converted each loop to an axis-aligned rectangular perimeter.",
                "Split the count into cases with zero through four hollow frames.",
                "Counted nested configurations and some sibling configurations.",
                "Converged on 57, but exhausted the token budget without a boxed answer; the correct count is 83.",
            ],
            "style": "Exhaustive but circular case analysis; a false dismissal of side-by-side frames caused the undercount.",
        },
        "api": {
            "overview": "Explored recursive frame-and-strip tilings for the full token budget but never completed a valid enumeration.",
            "steps": [
                "Modeled loops as solid width-two rectangles or hollow rectangular frames.",
                "Tried to constrain possible tilings using area and nesting arguments.",
                "Revisited several classifications without reaching a complete case count.",
                "Ended without a submitted answer; the correct count is 83.",
            ],
            "style": "Very long exploratory enumeration that remained unfinished at the output limit.",
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
    if problem == 15 and not result["correct"]:
        result["answer"] = "No final answer"
        result["finalResponse"] = "No boxed answer was submitted before the output limit."
    return record, result


def model_status(model_key: str) -> dict:
    records = [load_zst(path) for path in MODELS[model_key]["root"].rglob("*.json.zst")]
    return {
        "completed": len(records),
        "correct": sum(bool(record["correct"][0]) for record in records),
        "total": 30,
    }


def main() -> None:
    problems = []
    for problem in SNAPSHOT_PROBLEMS:
        local_record, local = model_record("local", problem)
        api_record, api = model_record("api", problem)
        if local_record["problem"] != api_record["problem"]:
            raise RuntimeError(f"Question mismatch on problem {problem}")
        problems.append(
            {
                "number": problem,
                "question": local_record["problem"],
                "goldAnswer": str(local_record["gold_answer"]),
                "models": [local, api],
            }
        )

    payload = {
        "title": "Hy3 Chadrock vs Hy3 API — Novita · AIME 2026",
        "snapshotLabel": f"Shared-completion demo · Problems {SNAPSHOT_PROBLEMS[0]}–{SNAPSHOT_PROBLEMS[-1]}",
        "snapshotUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "runStatus": {"local": model_status("local"), "api": model_status("api")},
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
