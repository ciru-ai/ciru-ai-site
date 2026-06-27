---
name: italianclownz-blueprint-theme
description: "Create polished @Italianclownz / charlie12345 technical webpages, reports, profile pages, release notes, and research artifacts using the dark/light blue Blueprint theme: high-contrast blue gradients, deep cut-corner cards, angled technical composition, friendly top-right profile/contact treatment, transparent RGBA image assets, strict attribution boundaries, first-person personal-report voice when requested, and Python-generated ECharts data. Use when Codex is asked to make pages or reports for Italianclownz, charlie12345, ROCmFP4, ROCmFPX, MTP, speculative decoding, or related AMD inference work in this visual style."
---

# Italianclownz Blueprint Theme

## Overview

Use this skill to build a distinctive technical page family for Italianclownz
(`@Italianclownz`, `charlie12345`). The look should feel like a precision AMD
inference workbench: dark/light blue gradients, hard angles, cut corners,
transparent blue technical ornaments, and readable evidence-first content.

## Workflow

1. Start from the content goal: profile page, development report, release page,
   artifact index, or benchmark summary.
2. Use the Theme Spec and Content Integrity Rules below. If this skill is
   installed as a full folder and includes `references/theme-spec.md`, read that
   file before designing or coding.
3. Copy the reusable assets from `assets/` into the project, preserving
   filenames unless the target project already has a naming scheme.
4. Put the profile/contact module near the top right on desktop and near the
   top on mobile. Include:
   - X: `https://x.com/Italianclownz`
   - GitHub: `https://github.com/charlie12345`
   - Profile image: `assets/italianclownz-pfp.jpg`
5. Use the RGBA ornaments as floating, non-rectangular visual assets:
   - `engine-core-rgba.png` for hero or major section emphasis
   - `token-ribbon-rgba.png` for motion/timeline emphasis
   - `profile-orbit-rgba.png` around or behind the contact/profile treatment
6. Build cards with cut corners and depth. Do not use rounded pastel cards or
   generic SaaS panels.
7. For charts, generate the data/options from Python and render with ECharts.
   If `pyecharts` is unavailable, write ECharts option JSON/JS from Python and
   initialize it in the page with the ECharts runtime.
8. Verify the page in a browser at desktop and mobile widths. Fix overlapping
   text, cramped cards, blank charts, and rectangular-looking transparent image
   placements before finishing.

## Content Integrity Rules

- When a requested report is meant to be from Italianclownz's perspective, write
  in first person. Use `I`, `my`, and `the work I maintained` rather than
  third-person profile language.
- Attribute work only to public `charlie12345` repositories, commits authored
  as `caf`, his X/GitHub profile, or sources the user explicitly says are his.
- Do not attribute unrelated organization work, model-card releases, benchmark
  notes, local artifacts, or user-created artifacts to Italianclownz unless a
  source explicitly shows he authored them.
- For a "meaningful moment" development report, prefer repo-visible artifacts:
  ROCmFPX/ROCmFP4 format work, AMD build support, model-family coverage,
  backend decode paths, speculative/MTP support, docs, profiles, and benchmark
  tables that live in the `charlie12345` repos.
- If external artifacts are included for comparison or impact context, label
  them as external and do not write as if Italianclownz created them.

## Non-Negotiables

- Use dark blue, light blue, cyan, and near-white contrast.
- Use angular composition: diagonal bands, clipped panels, beveled rules,
  offset shadows, and cut-corner geometry.
- Keep text factual and source-grounded. Make the page feel like a technical
  producer artifact, not fan art.
- Keep cards at `8px` radius or less; cut corners should carry the shape.
- Do not use decorative gradient blobs, beige palettes, purple-dominant
  gradients, or generic stock hero layouts.
- Do not put a card inside another card.
- Do not embed square/rectangular generated-image backgrounds. Use RGBA PNGs
  as irregular overlays or ornaments.

## Theme Spec

- Primary surfaces: `#050b18`, `#07172d`, and `#0a2d56`.
- Accent gradients: `#0a6dff`, `#18c8ff`, and `#84eaff`.
- Text: `#eef8ff`; secondary text: `#9dc4e9`.
- Cards use cut corners, one-pixel cyan/blue translucent borders, deep navy
  shadows, and small cyan highlights. Use `clip-path` geometry rather than
  rounded pastel panels.
- Use full-width bands and unframed layouts for page structure. Cards are for
  repeated facts, evidence items, compact profile/contact modules, and charts.
- Hero layout should have a direct title, one-paragraph thesis, top-right
  profile/contact module, and an oversized irregular RGBA ornament.
- Generate chart data/options with Python. Render with Apache ECharts in the
  browser, using transparent backgrounds, cyan/blue series colors, low-contrast
  grid lines, and readable mobile labels.

## Assets

Use these bundled files directly:

- `assets/engine-core-rgba.png`
- `assets/token-ribbon-rgba.png`
- `assets/profile-orbit-rgba.png`
- `assets/italianclownz-pfp.jpg`

When creating additional generated images, request a flat chroma-key background
and remove it locally so the final project asset is an RGBA PNG with
transparent corners and an irregular silhouette.
