---
title: "Verification Report: Taproot Speedy Trial Activation"
description: "A factual verification of the 2021 Taproot Speedy Trial activation parameters and wording."
date: "2026-06-23"
status: "Verified with wording clarification"
---

# Verification Report: Taproot Speedy Trial Activation

## Executive Summary

Taproot activated on Bitcoin mainnet at block **709,632**.

Taproot's Bitcoin Core activation path used **Speedy Trial**. BIP343 characterizes Speedy Trial as effectively a **BIP8 activation mechanism**, with the exception that the deployment start and timeout were defined using **median time past (MTP)** rather than block heights.

The deployment used **version bit 2**, a **90% signaling threshold**, MTP-based start and timeout timing, and `min_activation_height = 709,632`.

The actual Speedy Trial signaling period was on the order of **three months**, not a short standalone two-week window. The two-week framing refers to Bitcoin's 2,016-block difficulty-retarget period used for threshold evaluation, and also appears in earlier activation proposal language, but it is not an accurate description of the full shipped Speedy Trial window.

## Corrected Summary

Taproot's Speedy Trial activation in 2021 used a roughly three-month signaling window with a 90% threshold, MTP-based start and timeout, version bit 2 signaling, and `min_activation_height = 709,632`. It was specified in BIP341/BIP343 as effectively a BIP8-style activation mechanism using MTP-based timing, with a compatible BIP8(LOT=true) deployment also defined.

## Verification Table

| Item | Verified Fact |
|---|---|
| Mainnet activation height | 709,632 |
| Mechanism used by Bitcoin Core | Speedy Trial |
| BIP343 characterization | Effectively BIP8, except start and timeout used MTP rather than block heights |
| Signaling bit | Bit 2 |
| Miner signaling threshold | 90% |
| Activation signaling start height | 681,408 |
| Minimum activation height | 709,632 |
| Timing basis for start and timeout | Median time past (MTP) |
| Full shipped signaling period | Approximately three months |
| Two-week period | The 2,016-block retarget period used for threshold checks, not the full Speedy Trial window |
| BIP8(LOT=true) deployment | Separately defined and compatible with Speedy Trial for the chosen parameters |

## Terminology

### "Modified BIP9"

Bitcoin Core 0.21.1 describes Speedy Trial as a variation of BIP9 versionbits. BIP341 describes the deployment as versionbits using BIP9 with a lower threshold and `min_activation_height`.

BIP343 describes Speedy Trial as effectively a BIP8 activation mechanism, with one exception: start and timeout were based on MTP rather than block heights. A complete summary should include both points.

### "Short Two-Week Window"

The shipped Speedy Trial deployment did not use a single two-week signaling window. Its signaling period ran for roughly three months.

The two-week concept is relevant because miner signaling was evaluated across 2,016-block retarget periods. It also appears in earlier high-level activation proposal language, but it should not be used as the full description of the deployed Speedy Trial window.

### "90% Instead Of 95%"

Classical BIP9 mainnet deployments used a 95% threshold. Taproot's Speedy Trial used 90%.

The activation rationale for the 90% threshold was that it remained high enough to keep the Taproot chain ahead of invalid chains while being low enough to reduce the risk of a sudden malicious stall by rented or unknown hashrate.

### `min_activation_height`

Speedy Trial included `min_activation_height` so that, even if the signaling threshold was reached early, activation would wait until a set block height. For Taproot mainnet, that height was **709,632**.

### BIP8 Compatibility

Taproot had both the Speedy Trial deployment used by Bitcoin Core and a separately defined BIP8(LOT=true) deployment. The BIP8(LOT=true) path was compatible with Speedy Trial because the selected parameters produced no significant discrepancy between MTP and block-height timing.

## Final Wording

Taproot's Speedy Trial activation in 2021 used a roughly three-month signaling window with a 90% threshold, MTP-based start and timeout, version bit 2 signaling, and `min_activation_height = 709,632`. It was specified in BIP341/BIP343 as effectively a BIP8-style activation mechanism using MTP-based timing, with a compatible BIP8(LOT=true) deployment also defined.

## Sources

1. [BIP341: Taproot deployment parameters](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki)
2. [BIP343: Speedy Trial activation parameters](https://github.com/bitcoin/bips/blob/master/bip-0343.mediawiki)
3. [BIP9: Versionbits baseline threshold](https://github.com/bitcoin/bips/blob/master/bip-0009.mediawiki)
4. [Bitcoin Core 0.21.1 release notes](https://bitcoincore.org/en/releases/0.21.1/)
