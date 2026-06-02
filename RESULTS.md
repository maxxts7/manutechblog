# Cross-Axis Capping — Qwen3-32B full run

Run directory: `Qwen3-32B_L46-L53_nj250_nb100_tok256_pca_optimal75_2026-04-17T19-16-29`

## Configuration

| Field | Value |
|---|---|
| Model | Qwen/Qwen3-32B |
| Cap layers | L46–L53 (8 layers) |
| Prompts | 250 jailbreak + 100 benign |
| Max new tokens | 256 |
| Axis method | PCA |
| Compliance threshold | optimal75 (= mean_compliant + 0.75·(mean_refusing − mean_compliant)) |
| Cross-detect method | benign-p1 (assistant-axis firing gate trained on benign pool) |
| n_detect_cal | 50 |
| Orthogonalize | false |
| cos(assistant, compliance) | 0.156 |
| Judge | claude-sonnet-4-6 (anthropic backend) |

## Headline — jailbreak defense lift

Percentages are over **judgeable rows** (NaN = correction never fired; `error` = judge abstained). Error bands are 95% bootstrap CIs (N=10,000 resamples of prompts, same judge/labels fixed).

| Mode | Fire rate | Refusal (95% CI) | Partial refusal | Compliance | Degraded |
|---|---|---|---|---|---|
| assistant-cap (n_judged=219 / 250) | 100% | **32.9%** [26.6, 39.3] | 1.8% [0.4, 3.7] | 65.3% [58.9, 71.7] | 0% |
| cross-cap (n_judged=204 / 250) | 92.4% | **54.5%** [47.5, 61.4] | 3.4% [1.0, 6.2] | 41.6% [34.8, 48.5] | 0.5% [0, 1.5] |

**Paired lift (cross-cap − assistant-cap, same prompts):**

- Refusal only: **+21.5 pp** [+15.1, +28.0], P(lift > 0) = 100.0%.
- Refusal + partial_refusal: **+23.1 pp** [+16.7, +29.7], P(lift > 0) = 100.0%.

The CIs do not overlap zero, and every one of the 10,000 bootstrap samples showed positive lift — cross-cap is very clearly the stronger defense on this run.

Raw counts (all rows, including judge-errors and no-fires):

- `assistant_cap_jailbreak` (250 rows, 100% fire): refusal 72, partial 4, compliance 143, error 31.
- `cross_cap_jailbreak` (250 rows, 231 fires): refusal 111, partial 7, compliance 85, degraded 1, error 27, NaN (no-fire) 19.

## Utility — benign prompts

Percentages are over rows where correction fired. Error bands are 95% bootstrap CIs.

| Mode | Fire rate | Unchanged (95% CI) | False refusal | Degraded (95% CI) |
|---|---|---|---|---|
| assistant-cap (fired n=100) | 100% | 90.0% [84.0, 95.0] | 0% [0, 0] | 10.0% [5.0, 16.0] |
| cross-cap (fired n=67) | 67% | 91.0% [83.6, 97.0] | 0% [0, 0] | 9.0% [3.0, 16.4] |

Both modes preserve output quality on benigns: **zero false refusals** in either mode, ~9–10% output degradation among fired rows. The two modes' unchanged/degraded CIs overlap heavily — no detectable utility difference between them. Cross-cap's detect gate leaves 33% of benigns completely untouched (correction never fires); of the 67% where it does fire, the capped output is still clean.

Raw counts (cross-cap benign, n=100): benign_unchanged 61, benign_degraded 6, NaN (no-fire) 33.

## Layer activation details

Per-layer fire totals (summed over all prompts × all generated tokens).

### cross-cap jailbreaks (231 / 250 prompts fired)

| Layer | Fires | Share |
|---|---|---|
| L46 | 9,696 | 41.0% |
| L47 | 5,325 | 22.5% |
| L48 | 2,323 | 9.8% |
| L49 | 2,552 | 10.8% |
| L50 | 1,184 | 5.0% |
| L51 | 1,729 | 7.3% |
| L52 | 313 | 1.3% |
| L53 | 547 | 2.3% |
| **Total** | **23,669** | |

Fires concentrate in the early cap layers (L46–L47 = 63.5% of all fires). Per-prompt fire density is heavy-tailed: mean 102.5 fires/prompt, median 8, max 1,133, min 1 — a handful of prompts with sustained correction dominate the totals.

### cross-cap benigns (67 / 100 prompts fired)

| Layer | Fires | Share |
|---|---|---|
| L46 | 153 | 36.5% |
| L47 | 242 | 57.8% |
| L48 | 3 | 0.7% |
| L49 | 0 | — |
| L50 | 0 | — |
| L51 | 11 | 2.6% |
| L52 | 10 | 2.4% |
| L53 | 0 | — |
| **Total** | **419** | |

Two orders of magnitude fewer fires than on jailbreaks (419 vs 23,669), almost entirely in L46–L47. Per-prompt density: mean 6.3, median 3, max 67. When benigns do cross the detect gate, they get a light, brief correction — which matches the 91% unchanged / 0% false-refusal outcome.

### assistant-cap (both files)

Assistant-cap fires on every row by design (paper-style "always apply" mode) — no fire-density table meaningful.

## Interpretation

- Cross-cap behaves the way the decoupled-axis design hopes: heavy, sustained correction on jailbreak prompts (23.7k fires) vs a light touch on benigns (0.4k fires) — a ~56× gap in total intervention.
- The jailbreak refusal lift (33% → 54%) comes with no extra false-refusal cost on benigns (0 in both modes) and essentially the same degradation rate (~9–10%).
- Fires are front-loaded in the cap window: L46–L47 carry the majority of intervention effort in both distributions, with tail layers (L52–L53) seeing much less.
- Unlike the Llama-3.3-70B runs, the compliance axis on Qwen3-32B is doing real defensive work — the lift is not a judge artefact (same judge for both modes, same prompts).

## Bootstrap details

- N = 10,000 resamples, percentile 95% CI (2.5 / 97.5).
- Jailbreak paired lift: resample prompt indices with replacement, then compute each mode's refusal rate over the *resampled* judgeable rows; take the difference. Preserves per-prompt pairing across modes.
- Rates are over judgeable rows only; NaN (no-fire) and `error` (judge abstain) are excluded — matches how the headline percentages are computed.
- Raw output: `bootstrap.txt` in this directory.

## Artifacts in this directory

- `metadata.json` — run config
- `RESULTS.md` — this file
- `bootstrap.txt` — raw bootstrap numbers
- `assistant_cap_{jailbreak,benign}_reclassified.csv` — 250 / 100 rows, Claude-judged
- `cross_cap_{jailbreak,benign}_reclassified.csv` — 250 / 100 rows, Claude-judged; benign labels include manual corrections
- `*_reclassified.csv` columns: `prompt_idx, prompt_text, baseline_text, correction_applied, layers, capped_text, fires_per_layer (cross-cap only), push_trace (cross-cap only), llm_label, llm_judge_model`
