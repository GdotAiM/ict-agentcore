Updated: 2026-10-14 09:14 SAST

**Status 14 Oct:** Routines were down 8-14 Oct (out of usage), so the NAS 09:50 forward log has no entries for those days. All three alerts are enabled again. No new backtests since 7 Oct.
**Today's windows (SAST, NY+6):** London SMT EU/GU high side 08:00-11:00 (CONFIRMED, 68% n=63, in progress); Gold 2.0 13:00 (heads-up 12:45; it's Wednesday, not the 0/8 Thursday); NAS 09:50 macro 15:50-16:10 (PROMISING, alert 15:35).

Updated: 2026-10-07 18:31 SAST
# Time Patterns: XAUUSD sweep of the 15:00 NY range (21:00 SAST)
Analysis only, not trade advice. All prices are real OHLC data; nothing invented.

**Data:** TradingView OANDA:XAUUSD (spot CFD, the preferred feed) via tvDatafeed in nologin mode. Timestamps are SAST. The nologin feed limits how much history you get: 5m covers only 2026-09-07 to 2026-10-07 (21 weekdays), and 15m covers 2026-07-01 to 2026-10-07 (68 weekdays, slightly more than 60 days). I did not need yfinance (GC=F is COMEX futures, which trade at a basis to spot and use CME hours). NY = SAST−6h for the whole sample (EDT).
**Rules:** The range is the 15:00-15:15 NY candle (21:00-21:15 SAST). The variant uses the 14:45-15:00 NY candle (20:45-21:00 SAST). A sweep is the first bar that trades beyond the range high or low before **17:00 NY (23:00 SAST)**, the start of OANDA's 17:00-18:00 NY maintenance break. Targets only count if a bar *after* the sweep bar reaches them. T1 = opposite side of the range. T2 = opposite NY-session (08:00-15:00 NY = 14:00-21:00 SAST) extreme. "Move" = distance from the swept edge to the target, in $ (1 point = $1.00 = 100 pips at 0.01). If one bar breaks both sides, it is marked ambiguous and excluded.
**Caveats:** Samples are small. 15:00-17:00 NY is after the COMEX close, so liquidity is thin and spreads are wide. On 15m data a sweep and a target in the same bar can't be ordered. Treat this as hypothesis-level evidence only.

## Results
### 5m sequencing | Range = 15:00-15:15 NY (21:00-21:15 SAST)
- Weekdays with data: 21; sweeps: 19 (high 8, low 11, both-in-one-bar ambiguous 0, no sweep 2)
- Avg range size: $9.40 (median $6.62)
- T1 (opposite side of range): 8/19 = 42% | high-side 6/8, low-side 2/11 | avg distance edge->target all $6.62, hits $5.61 | time sweep->hit avg 34 min, median 25 min
- T2 (opposite NY 08-15 extreme): 1/19 = 5% | high-side 0/8, low-side 1/11 | avg distance edge->target all $26.02, hits $7.97 | time sweep->hit avg 40 min, median 40 min
- Sweep times SAST: median 21:15; within 30 min of range close: 100%
### 5m sequencing | Variant = 14:45-15:00 NY candle (20:45-21:00 SAST)
- Weekdays with data: 21; sweeps: 21 (high 10, low 11, both-in-one-bar ambiguous 0, no sweep 0)
- Avg range size: $8.69 (median $5.45)
- T1 (opposite side of range): 12/21 = 57% | high-side 8/10, low-side 4/11 | avg distance edge->target all $8.69, hits $4.81 | time sweep->hit avg 25 min, median 22 min
- T2 (opposite NY 08-15 extreme): 1/21 = 5% | high-side 1/10, low-side 0/11 | avg distance edge->target all $31.33, hits $9.15 | time sweep->hit avg 25 min, median 25 min
- Sweep times SAST: median 21:00; within 30 min of range close: 95%
### 15m sequencing | Range = 15:00-15:15 NY (21:00-21:15 SAST)
- Weekdays with data: 68; sweeps: 61 (high 28, low 33, both-in-one-bar ambiguous 5, no sweep 2)
- Avg range size: $8.09 (median $6.56)
- T1 (opposite side of range): 25/61 = 41% | high-side 14/28, low-side 11/33 | avg distance edge->target all $7.43, hits $6.21 | time sweep->hit avg 40 min, median 30 min
- T2 (opposite NY 08-15 extreme): 2/61 = 3% | high-side 1/28, low-side 1/33 | avg distance edge->target all $33.67, hits $9.59 | time sweep->hit avg 22 min, median 22 min
- Sweep times SAST: median 21:15; within 30 min of range close: 98%
### 15m sequencing | Variant = 14:45-15:00 NY candle (20:45-21:00 SAST)
- Weekdays with data: 68; sweeps: 54 (high 33, low 21, both-in-one-bar ambiguous 14, no sweep 0)
- Avg range size: $7.03 (median $5.45)
- T1 (opposite side of range): 25/54 = 46% | high-side 18/33, low-side 7/21 | avg distance edge->target all $7.72, hits $5.88 | time sweep->hit avg 34 min, median 30 min
- T2 (opposite NY 08-15 extreme): 3/54 = 6% | high-side 3/33, low-side 0/21 | avg distance edge->target all $34.88, hits $7.21 | time sweep->hit avg 25 min, median 30 min
- Sweep times SAST: median 21:00; within 30 min of range close: 96%

**Takeaways**
- The sweep is nearly certain and happens immediately. 19/21 days on 5m swept the 15:00 range, mostly in the first 5-15 minutes after the range closed (21:15-21:30 SAST). The 14:45 candle gets swept right at 21:00 SAST.
- Reaching the opposite side of the range (T1) is about a coin flip. It was 41-42% for the 15:00 range and 46-57% for the 14:45 variant. Typical move was about $5-6 and the median time about 20-30 min. **High-side sweeps reversed far more often than low-side sweeps** (5m: 6/8 vs 2/11; variant 8/10 vs 4/11). In this sample, buy-side sweeps after 15:00 NY tended to fail and fall back, while sell-side sweeps tended to keep going.
- T2 (opposite NY-session extreme, about $26-35 away) almost never hit before 17:00 NY: 3-6%. Don't use it as a target in this window.

## Next patterns worth testing
1. **Time of daily high/low by NY hour** for XAU, NAS100, EURUSD, GBPUSD. How often is the HOD/LOD set in London KZ (02-05 NY = 08-11 SAST) versus NY KZ (07-09 NY = 13-15 SAST)?
2. **Judas swing:** after the 00:00 NY midnight open (06:00 SAST) or the 08:30/09:30 open, how often does the first move against the daily bias reverse through the open price? Include hit rate and time to reversal.
3. **Silver Bullet (10-11 NY = 16-17 SAST):** how often does a FVG form, how often is it filled, and how often does price reach the nearest liquidity (prior-hour or session high/low)? Split by instrument and by DXY direction.
4. **Day-of-week weekly high/low:** which weekday sets the weekly high/low, and does a Tuesday low or high hold (the "Tuesday/Wednesday" weekly profile)?
5. **Asian range (20:00-00:00 NY = 02:00-06:00 SAST) sweep in London KZ** for EURUSD/GBPUSD, conditioned on DXY sweeping the opposite side (SMT).

## Inputs check
- liquidity.md: updated 2026-10-07 09:46 SAST, current. setups.md: updated 2026-10-07 09:50 SAST, current. Neither is used directly here.
- Script: /workspace/ict-team/scripts/xau_1500ny_sweep.py

## Example chart (added 2026-10-07 09:55 SAST)
charts/xau_1500_example.png. **2026-10-02 (Fri)**, OANDA:XAUUSD 5m. The 15:00-15:15 NY range was H 4149.295 / L 4143.745 ($5.55). It was swept high at 21:30 SAST (bar high 4149.905). T1 (range low) was hit at 21:40 SAST (bar low 4142.865), 10 min later. The NY 08-15 session extremes were H 4227.53 / L 4125.275; T2 was not hit. This was the most recent of 6 high-side T1 hits across both 5m variants.

## Kill zone study: time of daily high/low (added 2026-10-07 09:55 SAST)
**Data:** TradingView (tvDatafeed nologin). Main sample is 1h, 2025-01-02 to 2026-10-06, about 455 weekdays per instrument. A 15m sample from 2026-07-01 (70 days) was used for the 09:30-11:00 split. **Trading day = 18:00 NY prior evening to 17:00 NY.** Timestamps were converted to NY using tz rules for each date, so DST is handled correctly. SAST column assumes EDT (+6h); add 1h during EST (+7h, Nov to Mar). **Asia bucket = 18:00-00:00 NY**, so it includes the daily open (NAS100 index CFD resumes at 18:00). Bucketing is by the hour bar that contains the extreme; 1h bars can't resolve 09:30. Bull day = close > open of the trading day. Chart: charts/killzone_hl.png.

### OANDA:NAS100USD  (1h: 453 days 2025-01-02->2026-10-06; 15m: 70 days from 2026-07-01)
| Bucket (NY) | SAST | % of highs | % of lows |
|---|---|---|---|
| Asia 18-00 (open+Asia) | 00-06 | 18% | 25% |
| 00-02 | 06-08 | 3% | 4% |
| London KZ 02-05 | 08-11 | 7% | 9% |
| 05-07 | 11-13 | 2% | 4% |
| NY AM KZ 07-09 | 13-15 | 7% | 4% |
| 09-10 | 15-16 | 10% | 9% |
| Silver Bullet 10-11 | 16-17 | 7% | 11% |
| 11-13 | 17-19 | 10% | 9% |
| NY PM 13-16 | 19-22 | 25% | 17% |
| 16-17 | 22-23 | 11% | 8% |
- At least one of H/L in London KZ or NY AM KZ: **25%** of days (1h). 15m check: 27% (n=70).
- 09:30-11:00 NY (15:30-17:00 SAST) window, 15m: highs 10%, lows 23%.
- Bullish days 254 (56%): LOD bucket top Asia 18-00 (open+Asia) 43%, London KZ 02-05 15%. Bearish days 199: HOD bucket top Asia 18-00 (open+Asia) 38%, 09-10 14%.
- **CONFIRMED (n>=30, >=60%):** none

### OANDA:XAUUSD  (1h: 455 days 2025-01-02->2026-10-06; 15m: 70 days from 2026-07-01)
| Bucket (NY) | SAST | % of highs | % of lows |
|---|---|---|---|
| Asia 18-00 (open+Asia) | 00-06 | 33% | 40% |
| 00-02 | 06-08 | 4% | 5% |
| London KZ 02-05 | 08-11 | 7% | 7% |
| 05-07 | 11-13 | 4% | 3% |
| NY AM KZ 07-09 | 13-15 | 6% | 5% |
| 09-10 | 15-16 | 6% | 8% |
| Silver Bullet 10-11 | 16-17 | 9% | 9% |
| 11-13 | 17-19 | 12% | 7% |
| NY PM 13-16 | 19-22 | 11% | 10% |
| 16-17 | 22-23 | 9% | 4% |
- At least one of H/L in London KZ or NY AM KZ: **25%** of days (1h). 15m check: 27% (n=70).
- 09:30-11:00 NY (15:30-17:00 SAST) window, 15m: highs 14%, lows 19%.
- Bullish days 249 (55%): LOD bucket top Asia 18-00 (open+Asia) 66%, London KZ 02-05 8%. Bearish days 206: HOD bucket top Asia 18-00 (open+Asia) 65%, 00-02 6%.
- **CONFIRMED (n>=30, >=60%):** bull-day LOD in Asia 18-00 (open+Asia) 66%; bear-day HOD in Asia 18-00 (open+Asia) 65%

### OANDA:EURUSD  (1h: 457 days 2025-01-02->2026-10-06; 15m: 70 days from 2026-07-01)
| Bucket (NY) | SAST | % of highs | % of lows |
|---|---|---|---|
| Asia 18-00 (open+Asia) | 00-06 | 24% | 24% |
| 00-02 | 06-08 | 5% | 4% |
| London KZ 02-05 | 08-11 | 13% | 12% |
| 05-07 | 11-13 | 6% | 3% |
| NY AM KZ 07-09 | 13-15 | 10% | 11% |
| 09-10 | 15-16 | 5% | 8% |
| Silver Bullet 10-11 | 16-17 | 9% | 6% |
| 11-13 | 17-19 | 11% | 12% |
| NY PM 13-16 | 19-22 | 11% | 12% |
| 16-17 | 22-23 | 7% | 7% |
- At least one of H/L in London KZ or NY AM KZ: **42%** of days (1h). 15m check: 54% (n=70).
- 09:30-11:00 NY (15:30-17:00 SAST) window, 15m: highs 10%, lows 13%.
- Bullish days 221 (48%): LOD bucket top Asia 18-00 (open+Asia) 47%, London KZ 02-05 17%. Bearish days 236: HOD bucket top Asia 18-00 (open+Asia) 44%, London KZ 02-05 17%.
- **CONFIRMED (n>=30, >=60%):** none

### OANDA:GBPUSD  (1h: 457 days 2025-01-02->2026-10-06; 15m: 70 days from 2026-07-01)
| Bucket (NY) | SAST | % of highs | % of lows |
|---|---|---|---|
| Asia 18-00 (open+Asia) | 00-06 | 21% | 24% |
| 00-02 | 06-08 | 4% | 4% |
| London KZ 02-05 | 08-11 | 14% | 15% |
| 05-07 | 11-13 | 7% | 6% |
| NY AM KZ 07-09 | 13-15 | 9% | 12% |
| 09-10 | 15-16 | 7% | 7% |
| Silver Bullet 10-11 | 16-17 | 8% | 6% |
| 11-13 | 17-19 | 10% | 8% |
| NY PM 13-16 | 19-22 | 11% | 11% |
| 16-17 | 22-23 | 8% | 8% |
- At least one of H/L in London KZ or NY AM KZ: **44%** of days (1h). 15m check: 44% (n=70).
- 09:30-11:00 NY (15:30-17:00 SAST) window, 15m: highs 17%, lows 7%.
- Bullish days 229 (50%): LOD bucket top Asia 18-00 (open+Asia) 47%, London KZ 02-05 21%. Bearish days 228: HOD bucket top Asia 18-00 (open+Asia) 42%, London KZ 02-05 21%.
- **CONFIRMED (n>=30, >=60%):** none

### TVC:DXY  (1h: 456 days 2025-01-02->2026-10-06; 15m: 70 days from 2026-07-01)
| Bucket (NY) | SAST | % of highs | % of lows |
|---|---|---|---|
| Asia 18-00 (open+Asia) | 00-06 | 25% | 27% |
| 00-02 | 06-08 | 5% | 5% |
| London KZ 02-05 | 08-11 | 10% | 11% |
| 05-07 | 11-13 | 4% | 6% |
| NY AM KZ 07-09 | 13-15 | 11% | 9% |
| 09-10 | 15-16 | 7% | 5% |
| Silver Bullet 10-11 | 16-17 | 6% | 8% |
| 11-13 | 17-19 | 10% | 11% |
| NY PM 13-16 | 19-22 | 13% | 12% |
| 16-17 | 22-23 | 9% | 6% |
- At least one of H/L in London KZ or NY AM KZ: **39%** of days (1h). 15m check: 49% (n=70).
- 09:30-11:00 NY (15:30-17:00 SAST) window, 15m: highs 7%, lows 14%.
- Bullish days 232 (51%): LOD bucket top Asia 18-00 (open+Asia) 50%, London KZ 02-05 16%. Bearish days 224: HOD bucket top Asia 18-00 (open+Asia) 49%, London KZ 02-05 16%.
- **CONFIRMED (n>=30, >=60%):** none


**Summary for alert routine**
- CONFIRMED (n>=30, >=60%): **XAUUSD only.** On bullish days the LOD formed in the 18:00-00:00 NY window (00:00-06:00 SAST) 66% of the time. On bearish days the HOD formed there 65% of the time. In other words, gold's daily low on up days, or high on down days, is usually already in by the end of Asia. Nothing else passes the threshold.
- Not confirmed: "H or L forms in London/NY AM KZ" happened on only 25% (NAS, XAU) to 44% (GBP) of days on 1h. FX is higher (EUR 42%, GBP 44%; 54%/44% on 15m). FX London KZ has the second-largest share of extremes (12-21%). NAS100 HOD most often formed in NY PM 13-16 (25%). Edges this small are context, not alert triggers.

## Team hypothesis backtest (added 2026-10-07 10:07 SAST)
**Data.** All prices are real TradingView nologin data (OANDA CFDs, TVC:DXY, TVC:US10Y); nothing is invented. NY times are DST-correct from tz-aware timestamps. A trading day runs 17:00 to 17:00 NY. The nologin feed limits history depth:
- **1h:** 2025-01-02 to 2026-10-06, about 450 weekdays.
- **15m:** from 2026-07-01, 68-70 days.
- **5m:** from 2026-09-07, about 21 days (FX about 17).
- **1m:** from 2026-09-28, **about 7 days only.**

Where the spec's timeframe was too short, I also ran an approximation on a longer timeframe, marked *. US10Y intraday exists on TVC at 15m (41 usable days after the 20-day median warm-up) and at 1h.

**Rules applied.**
- Fills are conservative: the stop is checked before the target, and a target touched on the fill bar is ignored.
- One trade per instrument per day.
- R is measured per filled trade. Time exits are booked at the bar open.

**Interpretations where specs were ambiguous.**
- **Bias H1 / LS H2 bias:** prior close > 50% of its range and > the day-before high (mirror for bearish).
- **"Before 10:00":** the extreme forms in a bar starting before 10:00.
- **IM H1 success:** both pairs reach 0.5×Asia range beyond the 02:00 open, against the sweep, during 05-11. Control = both pairs took the same side.
- **LS H2:** "session range so far" = trading-day high/low up to the close-back bar. Control = sweeps without a close-back.
- **Entry H1 bias filter:** daily open vs prior close. "Unswept" = not traded through after the level formed.
- **Scalp H1:** if no 2-bar fractal is found, the post-sweep swing = sweep-to-reclaim extreme.
- **Scalp H2:** "skip if stop > 2× median" uses the in-sample median.
- **TP1 bias:** prior day C>O and today's open ≥ prior close (mirror). Known before Asia.
- **TP2:** "price at 09:30" = 09:30 bar open. "Close above midnight open by 16:00" = 16:00 price > 00:00 open.

| Hypothesis | Data / days | n | Result | Baseline / control | Median time | Verdict |
|---|---|---|---|---|---|---|
| Bias H1 LOD/HOD before 10:00 on bias days | 1h, 438-455 d | 204-217 bias days per inst. | NAS 48%, XAU 63%, EU 58%, GU 62% | all days 49%, 64%, 63%, 65% | - | **REJECTED** (no edge, all below 70%; bias direction correct only 44-49%) |
| Bias H2 London Judas EU/GU | 1h, 455 d | 210 / 204 bias days | success 26% / 30%; extreme held 31% / 48% | non-bias 24% / 27% | - | **REJECTED** |
| IM H1 London SMT EU vs GU | 1h, 457 d | SMT-high 63, SMT-low 48 | reversal ≥0.5×Asia range: **68%** (high), 54% (low) | both took high 33% (n=138), both took low 44% (n=117) | n/a (1h) | **CONFIRMED (SMT-high side)**; low side PROMISING. 15m check (70 d): 62% (n=8), 50% (n=6) |
| IM H2 DXY+US10Y 08:30-09:30 → XAU opposite to DXY 09:30-12:00 | 15m, 41 d | 11 signals | 36% (avg −$3.9 in signal direction) | disagree 64% (n=14) | - | **REJECTED**. 1h* approx 08-09 (384 d): 52% (n=104) vs 55% |
| LS H1 Asia sweep + 5m close-back in 30 min → opposite side before 11:00 | 5m 21 d; 15m* 70 d | 30; 115* | 30%; 30%* (high-side 57% / 38%*, low-side 6% / 22%*) | no close-back 13% (n=38); 18%* (n=109) | 245-278 min | **CONFIRMED vs control (+12 pp, n=115)**, but only 30% absolute; high-side best (NAS 42%*) |
| LS H2 PDH/PDL sweep 07-10 + close-back in 15 min → session mid before 16:00 | 5m 21 d; 15m* 70 d | 27; 72* | 63%; 65%* (PDH 72%, PDL 60%; against-bias 90% n=20, with 78% n=9, neutral 51% n=43) | no close-back 60%; 57%* (n=113). PDH or PDL taken 07-10 on 56-76% of days | 60-105 min | **PROMISING** (+8 pp; "against-bias" subset worth tracking) |
| Entry H1 London sweep+MSS+FVG (2R min) | 5m 21 d; 15m* 70 d | 37 fills (65% fill); 47* | win 14%, **−0.14R**; 15%, −0.28R* | - | 50 min | **REJECTED**. Aligned −0.08R vs not −0.20R; NAS +1.57R on 8 fills (noise) |
| Entry H2 Silver Bullet (2R min) | 1m 7 d; 5m* 21 d | 8 fills; 12* | win 12%, **−0.25R**; 0%, −0.24R* | - | 11 min | **REJECTED** (too few data) |
| Scalp H1 London Asia-sweep scalp | 1m 7 d; 5m* | 6 fills; 10* | 0/6, **−1.0R**; +0.56R* (1 winner of 5R + time exits) | needs ≥100 trades | - | **REJECTED** (1m); 5m* not meaningful |
| Scalp H2 PDH/PDL break continuation 3R | 1m 7 d; 5m* | 3 fills (43% fill); 2* | 0 wins, −0.15R; −0.45R* | DXY split n≤2 | - | **REJECTED** (insufficient data) |
| TP1 XAU Asia extreme holds on bias days | 1h, 451 d | 228 bias days (162 bull / 66 bear) | holds **33%** (bull 36%, bear 27%); bias correct 48% | any-day 36%; if bias was also right: 62% (n=110) vs 65% unconditional | - | **REJECTED** (the 66% needs hindsight about direction) |
| TP2 NAS below midnight open at 09:30 → LOD 09:30-11:00 & close above MO by 16:00 | 15m, 68 d (5m 21 d) | 32 days (9) | LOD in window **34%**; close above MO 25%; both 6% (5m: 22%, 44%, 0%) | LOD in window, all days 24% | median LOD 16:00 SAST | **REJECTED** (<60%) |

**Takeaways.**
- **The only confirmed edge is London SMT on the high side, EU vs GU (IM H1).** If one pair takes the Asia high during 08:00-11:00 SAST and the other doesn't, both pairs dropped at least 0.5× the Asia range below the London open by 17:00 SAST on 68% of days (n=63). When both took the high, this happened 33% of the time. This qualifies for the alert routine. 1h bars can't time the sequence, so check it on 5m before going live.
- **No trade model reaches +0.3R with n≥30.** The 1m specs have only about 7 days of free history, so Entry H2 and Scalp H1/H2 need TradingView login, a broker export, or forward logging.
- **Bias proxies predicted direction no better than chance (44-49%).** That undermines Bias H1/H2 and TP1.
- Scripts: scripts/fetch_data.py, hyp_lib.py, hyp_session.py, hyp_trades.py, hyp_chart.py. Raw results: data/session_results.json, data/trade_results.json. Chart: charts/hypotheses_summary.png.

## Gold 2.0 backtest (added 2026-10-07 11:11 SAST)
**Data.**
- **Primary: Dukascopy free XAUUSD 1m BID candles** (spot, from datafeed.dukascopy.com bi5 files). Covers 2026-06-01 to 2026-10-06: **72 of 92 weekdays**. 20 weekdays are missing because Dukascopy rate-limited downloads (HTTP 429): 06-16, 06-17, 06-24, 06-29, 07-01, 07-07, 07-24, 08-04, 08-06, 08-10, 08-14, 08-18, 08-21, 08-25, 08-26, 08-28, 09-01, 09-02, 09-14, 09-28.
- **Accuracy vs OANDA:** compared with OANDA 1m on 8,371 overlapping bars, Dukascopy averages **$0.32 below** OANDA (median absolute difference $0.31). The structure matches.
- **OANDA on its own reaches only about 7 days of 1m and about 22 of 5m** on the free TradingView feed, so OANDA results are a cross-check only.
- **Costs:** BID prices only, no spread or commission. Effect of spread shown below.

**Rules as implemented.**
- **Range:** the 07:00 NY 1m candle. This is 13:00 SAST throughout the sample, since all dates are in US DST. After 1 Nov 2026 the same 07:00 NY candle is 14:00 SAST.
- **Sweep:** the first trade beyond either side, up to 09:00 NY. If the other side is swept before an MSS, the setup flips to that side. A single bar breaking both sides skips the day.
- **MSS:** a 1m close beyond the most recent confirmed 3-bar fractal on the opposite side.
- **Entry:** first FVG in the shift leg, from the sweep extreme to the MSS bar. If there is none, an IFVG (an opposite FVG within 30 bars that price closed through).
- **Stop:** sweep extreme ± $0.50.
- **Target:** opposite range side if it gives ≥2R; otherwise the nearest untouched 3-bar swing since 00:00 NY that gives ≥2R; otherwise skip.
- **Timing:** no fill after 09:00 NY (15:00 SAST). Time exit at 11:00 NY (17:00 SAST). One trade per day.
- **Conservative fills:** a stop touch on the fill bar is a loss, and a bar touching stop and target is a loss.
- **News days:** taken from the official BLS schedules (NFP, CPI, PPI) and the Fed calendar (FOMC decisions and minutes days).

| Test | Days | Setups | Fills (rate) | Win % | Avg R / expectancy | Avg target R:R | Return / max DD @0.5% | Median fill→target |
|---|---|---|---|---|---|---|---|---|
| **Dukascopy 1m, FVG proximal edge** | 72 | 41 | 38 (93%) | 39% | **+0.31R** | 2.49 | +5.8% / **−3.0%** | 13.5 min |
| **Dukascopy 1m, FVG midpoint** | 72 | 41 | 38 (93%) | 45% | **+0.50R** | 2.56 | +9.9% / **−2.0%** | 13.5 min |
| Proximal + 50% off at 1R, stop to BE | 72 | 41 | 38 | 61% (>0R) | +0.21R | - | DD −2.2% | - |
| Midpoint + 50% at 1R / BE | 72 | 41 | 38 | 55% (>0R) | +0.20R | - | DD −2.2% | - |
| OANDA 1m (TV), proximal / midpoint | 7 | 4 | 3 | 67% | +1.23R / +1.37R | 2.4-2.7 | DD −0.5% | about 9 min |
| OANDA 5m (TV, approx.), proximal / midpoint | 22 | 4 / 5 | 3 / 4 | 0% / 25% | −1.00R / −0.25R | 2.4-2.8 | - | - |

Notes:
- **Skips (Dukascopy):** 14 days had a single bar breaking both sides, 9 had an MSS with no FVG or IFVG, 6 had bad geometry, 2 were under 2R.
- **Entry types (proximal):** FVG 24 trades at +0.53R; IFVG 14 trades at **−0.08R**.
- **Direction (proximal):** longs (low swept) 16 trades at +0.63R; shorts 22 trades at +0.07R.
- **Spread sensitivity:** a $0.20 / $0.35 spread on a median risk of $2.78 cuts proximal to **+0.24R / +0.19R** and midpoint to **+0.43R / +0.38R**.
- **Stability (proximal):** first 19 trades +0.42R, last 19 +0.20R. Midpoint: +0.46R, then +0.55R.
- **5m:** the 07:00 5m bar is 5× wider than the 1m range, and 13 of 22 days were both-sides bars. It is not a usable approximation of a 1m model.

**Weekday (proximal, Dukascopy).** Mon 7 trades +0.80R (57% win). Tue 6, +0.71R. Wed 7, +0.36R. **Thu 8 trades, 0 wins, −1.00R.** Fri 10, +0.72R. Midpoint: Thu −0.62R, the others +0.77 to +0.83R. Every bucket has n<10, so treat the Thursday result as a flag only.

**News vs non-news (proximal).** Non-news days 29 trades, +0.38R (41% win). News days 9 trades, +0.06R (33% win):
- PPI 06-11: loss
- FOMC minutes 07-08: loss
- CPI 07-14: loss
- PPI 07-15: win +2.0R
- NFP 08-07: loss
- CPI 08-12: win +2.5R
- PPI 08-13: loss
- FOMC minutes 08-19: loss
- CPI 09-11: win +2.1R

At midpoint, news days were +0.43R. The 08:30 NY (14:30 SAST) releases fall inside the trade window.

**Compared with the 15:00 NY sweep study.** That study measured reach rates, not trades: 41-57% of sweeps reached the opposite side of the range. Gold 2.0 wins 39-45% of filled trades at about 2.5R, and only fills after a confirmed MSS. This gives positive expectancy even though its hit rate is similar.

**Verdict.**
- **FVG-midpoint entry: CONFIRMED, but marginal** (n=38, +0.50R, still +0.38R after a $0.35 spread, max DD 2.0%).
- **Proximal entry: PROMISING.** +0.31R passes the bar before costs but drops to +0.19-0.24R after spread.
- **The 50%-at-1R / BE variant is worse** (+0.20R) and reduces drawdown only slightly. Not recommended.

Caveats: the data is not OANDA (Dukascopy spot BID), there are 20 missing weekdays, it is a single 4-month period with no out-of-sample test, and the sample is small. Suggested filters to test forward: skip IFVG-only setups; treat Thursdays and NFP/CPI/PPI days with caution. Forward-test before trading live.

Script: scripts/gold20_backtest.py (charts: scripts/gold20_charts.py). Results: data/gold20_results.json and data/gold20_frames.pkl. Charts: charts/gold20_equity.png, charts/gold20_example.png. The example is 2026-07-03 (Fri):
- Sweep above the 13:00 range high (4176.91) at 13:01 SAST.
- MSS at 13:29 SAST; FVG short filled at 13:32 SAST at 4184.07, stop 4186.52.
- Target (range low 4175.41) hit at 14:17 SAST for **+3.53R**.

## PDH/PDL sweep back to the 50% (Tobias Cabrera reel) (added 2026-10-07 16:54 SAST)
**Source.** The reel caption (reel2.info.json, uploaded 2026-09-08) adds only one rule beyond the spec: "if price trades around the 50%, don't trade." That is covered by the chop filter. Video not watched.

**Data.** TradingView OANDA 15m covers 2026-07-01 to 2026-10-06, 67-69 trading days per instrument. A 1h cross-check covers 2025-01-02 to 2026-10-06, 439-456 days; there, "close back inside" means a 1h close. All prices are real; nothing invented.

**Rules as implemented.**
- **Day:** 17:00 to 17:00 NY, DST-correct.
- **Short:** the last 4 closes before the sweep bar are above the prior day's 50%. The first bar trading above PDH is the sweep. Entry is at the first close back below PDH, on the sweep bar or later that day. Stop = highest high from sweep to entry, plus a buffer (NAS 2 pt, XAU $0.50, FX 1 pip). TP1 = 50%, TP2 = PDL. Long is the mirror.
- **Chop filter:** skip if closes crossed the 50% **3 or more times** that day before the sweep, or if the entry close is **within 10% of the prior day's range** from the 50%.
- **Fills and exits:** conservative fills (stop checked first; a bar touching both stop and target counts as a loss). Exit at the 17:00 NY daily close if neither stop nor target is hit. One trade per side per day.
- **TP1 and TP2 are tested as separate single-target trades.** The TP2-only variant is the "E(TP2)" column. Times below are NY+6 = SAST.

**Share of days with a PDH or PDL sweep.**
- 15m: NAS 90%, XAU 93%, EU 83%, GU 81%.
- 1h: 83-89%.

**What filtered setups out.**
- 15m: 137 valid; filtered out: 59 chop, 43 not beyond 50%, 26 no close-back.
- 1h: 511 valid; filtered out: 809 not beyond 50%, 336 no close-back, 60 chop, 31 entry past 50%.

**R:R distribution at TP1.**
- 15m (n=137): <0.5: 3, 0.5-1: 7, 1-1.5: 7, 1.5-2: 8, 2-3: 25, ≥3: 87. 82% have TP1 at 1:2 or better.
- 1h: 54% have TP1 at 1:2 or better.

**R:R distribution at TP2** (15m): <1: 2, 1-2: 7, 2-3: 6, 3-5: 18, ≥5: 104.

### 15m (OANDA, about 70 days)
| Split | n | TP1 hit | TP2 hit | Median R:R TP1/TP2 | TP1 ≥1:2 | E(TP1) R | E(TP2) R | Median min to TP1/TP2 | Max DD @0.5% TP1/TP2 |
|---|---|---|---|---|---|---|---|---|---|
| **Overall** | 137 | 18% | 6% | 3.7 / 8.0 | 82% | **-0.11** | **-0.09** | 300 / 630 | -13.9% / -16.1% |
| Overall, only TP1 R:R ≥ 1:2 | 112 | 12% | 4% | 4.7 / 9.9 | 100% | **-0.12** | **-0.11** | 352 / 750 | -13.2% / -16.1% |
| TP2-only, R:R ≥ 1:2 at TP2 | 128 | 14% | 5% | 4.1 / 8.4 | 88% | **-0.12** | **-0.11** | 322 / 742 | -14.0% / -16.5% |
| EU | 30 | 17% | 7% | 4.1 / 8.8 | 83% | **-0.34** | **-0.38** | 180 / 532 | -6.7% / -6.9% |
| GU | 31 | 23% | 3% | 3.9 / 8.3 | 84% | **+0.45** | **+0.79** | 390 / 735 | -2.1% / -2.1% |
| NAS | 39 | 10% | 3% | 3.3 / 7.3 | 79% | **-0.51** | **-0.52** | 322 / 135 | -11.3% / -10.2% |
| XAU | 37 | 22% | 11% | 4.1 / 8.4 | 81% | **+0.03** | **-0.13** | 300 / 638 | -7.6% / -7.0% |
| EU (R:R≥2) | 25 | 8% | 4% | 4.7 / 9.4 | 100% | **-0.38** | **-0.47** | 262 / 870 | -6.3% / -5.9% |
| GU (R:R≥2) | 26 | 19% | 4% | 5.3 / 10.9 | 100% | **+0.52** | **+0.97** | 525 / 735 | -1.8% / -1.7% |
| NAS (R:R≥2) | 31 | 10% | 3% | 4.6 / 9.6 | 100% | **-0.53** | **-0.53** | 255 / 135 | -9.6% / -9.1% |
| XAU (R:R≥2) | 30 | 13% | 7% | 4.6 / 9.7 | 100% | **-0.02** | **-0.31** | 308 / 795 | -7.4% / -8.3% |
| Asian 20-00 | 63 | 17% | 8% | 4.9 / 10.2 | 90% | **-0.05** | **+0.01** | 360 / 750 | -12.7% / -13.2% |
| London Open 02-05 | 20 | 40% | 15% | 3.7 / 7.7 | 75% | **+0.75** | **+0.69** | 278 / 195 | -1.9% / -1.5% |
| NY AM 07-10 | 24 | 12% | 0% | 2.3 / 4.8 | 58% | **-0.32** | **-0.35** | 30 / - | -4.5% / -4.8% |
| NY PM 13:30-16 | 3 ⚠n<20 | 0% | 0% | 4.7 / 9.4 | 67% | **-0.66** | **-0.66** | - / - | -1.0% / -1.0% |
| Silver Bullet 10-11 | 3 ⚠n<20 | 0% | 0% | 5.4 / 11.6 | 100% | **-1.00** | **-1.00** | - / - | -1.5% / -1.5% |
| other | 24 | 8% | 0% | 3.3 / 7.1 | 88% | **-0.59** | **-0.54** | 278 / - | -6.8% / -6.3% |
| London Close 10-12 (overlaps SB) | 4 ⚠n<20 | 0% | 0% | 4.2 / 8.9 | 100% | **-0.81** | **-0.81** | - / - | -1.6% / -1.6% |
| Fri | 23 | 26% | 0% | 3.9 / 8.3 | 74% | **+0.35** | **+0.09** | 278 / - | -3.9% / -4.3% |
| Mon | 27 | 15% | 0% | 3.5 / 7.5 | 81% | **-0.17** | **-0.33** | 338 / - | -3.2% / -4.4% |
| Thu | 36 | 17% | 11% | 4.4 / 9.3 | 78% | **-0.45** | **-0.16** | 262 / 615 | -8.0% / -6.0% |
| Tue | 29 | 17% | 14% | 3.7 / 7.8 | 90% | **-0.10** | **+0.55** | 525 / 630 | -8.6% / -7.5% |
| Wed | 22 | 14% | 0% | 3.6 / 7.8 | 86% | **+0.03** | **-0.69** | 360 / - | -5.9% / -7.4% |
| short | 68 | 21% | 7% | 4.3 / 8.9 | 84% | **-0.01** | **+0.03** | 300 / 390 | -8.8% / -6.7% |
| long | 69 | 14% | 4% | 3.6 / 7.5 | 80% | **-0.21** | **-0.21** | 292 / 735 | -12.4% / -17.1% |

### 1h cross-check (OANDA, Jan 2025 to Oct 2026, labeled approximation)
| Split | n | TP1 hit | TP2 hit | Median R:R TP1/TP2 | TP1 ≥1:2 | E(TP1) R | E(TP2) R | Median min to TP1/TP2 | Max DD @0.5% TP1/TP2 |
|---|---|---|---|---|---|---|---|---|---|
| **Overall** | 511 | 22% | 7% | 2.2 / 4.7 | 54% | **-0.18** | **-0.10** | 180 / 300 | -37.6% / -26.9% |
| Overall, only TP1 R:R ≥ 1:2 | 276 | 12% | 4% | 4.1 / 8.4 | 100% | **-0.27** | **-0.22** | 300 / 360 | -33.5% / -30.3% |
| TP2-only, R:R ≥ 1:2 at TP2 | 438 | 18% | 6% | 2.5 / 5.4 | 63% | **-0.20** | **-0.13** | 180 / 390 | -37.5% / -28.9% |
| EU | 133 | 23% | 6% | 2.0 / 4.4 | 50% | **-0.15** | **-0.12** | 120 / 510 | -11.6% / -10.7% |
| GU | 147 | 20% | 7% | 2.5 / 5.3 | 59% | **-0.26** | **-0.23** | 240 / 420 | -19.7% / -17.9% |
| NAS | 133 | 25% | 10% | 2.2 / 4.8 | 53% | **-0.07** | **+0.12** | 120 / 180 | -11.7% / -8.0% |
| XAU | 98 | 20% | 5% | 2.1 / 4.6 | 53% | **-0.22** | **-0.17** | 150 / 180 | -10.8% / -10.3% |
| Asian 20-00 | 62 | 10% | 3% | 4.0 / 8.2 | 79% | **-0.66** | **-0.67** | 570 / 540 | -19.5% / -19.3% |
| London Open 02-05 | 128 | 26% | 12% | 2.3 / 5.0 | 56% | **-0.08** | **+0.06** | 300 / 420 | -12.2% / -8.6% |
| NY AM 07-10 | 117 | 33% | 8% | 1.6 / 3.5 | 39% | **+0.17** | **+0.30** | 120 / 120 | -4.6% / -4.8% |
| NY PM 13:30-16 | 12 ⚠n<20 | 8% | 0% | 2.1 / 4.5 | 50% | **-0.09** | **-0.09** | 120 / - | -1.9% / -1.9% |
| Silver Bullet 10-11 | 38 | 18% | 8% | 1.2 / 2.6 | 37% | **-0.14** | **-0.01** | 60 / 60 | -3.8% / -3.8% |
| other | 154 | 18% | 5% | 2.2 / 4.9 | 58% | **-0.34** | **-0.32** | 180 / 330 | -23.5% / -22.7% |
| London Close 10-12 (overlaps SB) | 58 | 19% | 5% | 1.2 / 2.5 | 33% | **-0.13** | **-0.07** | 60 / 60 | -5.4% / -5.4% |
| Fri | 105 | 30% | 9% | 1.8 / 4.3 | 48% | **-0.06** | **+0.05** | 180 / 300 | -7.2% / -7.3% |
| Mon | 76 | 16% | 8% | 2.4 / 5.1 | 63% | **-0.35** | **-0.20** | 270 / 480 | -12.8% / -8.2% |
| Thu | 115 | 17% | 6% | 2.2 / 4.9 | 53% | **-0.18** | **-0.02** | 210 / 360 | -10.6% / -8.1% |
| Tue | 98 | 24% | 6% | 2.5 / 5.2 | 63% | **+0.03** | **-0.06** | 120 / 120 | -11.3% / -9.6% |
| Wed | 117 | 21% | 8% | 1.9 / 4.0 | 47% | **-0.34** | **-0.28** | 120 / 180 | -18.4% / -16.6% |

**Reading.**
- **The rule as specified loses money overall.** 15m: TP1 hit only 18% before the stop, E(TP1) **−0.11R**, E(TP2) **−0.09R**, max DD −14% / −16% at 0.5% risk. 1h: E −0.18 / −0.10R over 511 trades.
- **Requiring 1:2 at TP1 makes it worse** (15m −0.12R; 1h −0.27R). The wide-R:R setups have the tightest stops, and those get run.
- **Positive pockets on 15m:**
  - GBPUSD: +0.45R / +0.79R, n=31. The 1h check says −0.26R.
  - London Open 02-05 NY (08-11 SAST): +0.75R / +0.69R, n=20, TP1 hit 40%. The 1h check says −0.08 / +0.06R over 128 trades.
  - NY AM 07-10 is positive only on 1h (+0.17 / +0.30R, n=117) and negative on 15m (−0.32R, n=24).
  - **None of these pockets agree across both timeframes**, so they are probably noise.
- **TP1 takes time when it is hit:** median 300 min (5 h) on 15m. TP2 median 630 min. Most trades end at the stop or at the daily close.

**Verdict: REJECTED** as specified, overall and for the 1:2-filtered version: n=137 (15m) and 511 (1h), expectancy negative. **London Open 15m and GBPUSD are PROMISING-at-best leads.** Each is n≤31 and contradicted by the 1h data. Track them forward before acting on them.

Script: scripts/pdhl_50_backtest.py (charts: scripts/pdhl_50_charts.py). Results: data/pdhl50_results.json. Charts: charts/pdhl50_summary.png, charts/pdhl50_example.png.

**Example (XAUUSD short, Fri 2026-10-02):**
- PDH 4193.1 swept, and the 15m bar closed back inside at 08:00 SAST.
- Entry 4192.20, stop 4197.40.
- TP1 (50%, 4166.18) hit at 12:15 SAST for **+5.0R**.
- The TP2 version (PDL 4139.27) was stopped out first: price spiked to about 4227 at about 14:30 SAST (NFP day; release 08:30 NY = 14:30 SAST), then fell to PDL.

## Phase (phase4o4) Classic & Ping-Pong backtest (added 2026-10-07 17:32 SAST)
**Data.**
- **OANDA** (TradingView): 15m for liquidity/trend/OTE, plus 5m for shift/entry. NAS 2026-09-06 to 10-07; XAU same; EU/GU 09-13 to 10-07. About 17-22 trading days per instrument.
- **Dukascopy XAUUSD 1m** (spot BID), with 15m resampled from it: 2026-05-31 to 10-06, **104 trading days**.
- **Dukascopy FX/NAS is not used.** EURUSD, GBPUSD and USATECHIDXUSD downloads were blocked by Dukascopy rate-limiting (HTTP 429) throughout this run, so FX/NAS results are OANDA 5m only.
- All prices are real.

**Rules made mechanical.**
- **Pools:**
  - PDH/PDL.
  - Asia H/L (20:00-00:00 NY, active after 00:00).
  - London H/L (02:00-05:00 NY, active after 05:00).
  - Unswept 15m fractal swing highs/lows (2 bars each side) from the last 3 days.
- **Sweep:** an LTF bar trading beyond an active pool.
- **Shift (MSS):** an LTF close beyond the most recent 3-bar LTF fractal on the opposite side, within 60 minutes of the sweep.
- **Ping-Pong confirmations.** Each is also tested stand-alone. The model takes whichever limit fills first.
  - OTE: limit at 0.705 of the shift leg.
  - OB: last opposite-colour candle within 6 bars before the extreme; limit at its proximal edge.
  - IFVG: an FVG in the sweep direction, within 20 bars, that price closed through at the MSS; limit at its proximal edge.
  - Unicorn: a shift-leg FVG overlapping the OB/breaker candle; limit at the proximal edge of the overlap.
- **Ping-Pong stop and target:** stop = sweep extreme + buffer (NAS 2 pt, XAU $0.50, FX 1 pip). Target = nearest unswept opposite pool.
- **Second leg:** a trade whose swept pool was the target of the previous winning trade that day.
- **Retry rule:** at most 3 trades and 2 losses per day per model (one retry after a loss).
- **Counter-trend label:** direction against the 15m BOS trend.
- **Classic, trend:** 15m BOS trend. Impulse = from the swing anchor to the running extreme. HTF OTE = 0.618-0.786 of the impulse.
- **Classic, entry:** needs an LTF sweep of a pool with the sweep price inside the HTF OTE and not beyond 1.0, then an LTF shift. Limit at 0.705 of the LTF shift leg.
- **Classic, stop and target:** stop beyond the LTF sweep extreme. Target = HTF impulse extreme (opposing HTF liquidity). Variant "nearest pool" targets the nearest opposite pool instead. Partials were not modelled.
- **Fill window:** 60 minutes after the MSS. No fills after 15:00 NY (21:00 SAST). **Time exit 16:00 NY (22:00 SAST)** at bar open.
- **Fills:** conservative. A stop touch on the fill bar is a loss, and a bar touching stop and target is a loss.
- **Kill zone:** by fill time. Times below are SAST = NY+6.
- **Day caps are used up early:** on 1m, Asia/early-London sweeps usually use up the day's 3-trade / 2-loss allowance before NY. So the NY kill zones are thin.


### Ping-Pong: OANDA 15m+5m, 4 instruments, about 21 days
| Split | Setups | Fills | Fill % | Win % | Avg R = expectancy | Median R:R | R:R ≥2 | Median / avg min to target | Max DD @0.5% |
|---|---|---|---|---|---|---|---|---|---|
| **All setups** | 442 | 195 | 44% | 35% | **-0.02** | 2.1 | 53% | 30 / 60 | -12.0% |
| **Only R:R ≥ 1:2** | 254 | 104 | 41% | 19% | **-0.17** | 3.9 | 100% | 58 / 87 | -14.5% |
| 2nd-leg reversal (all) | 18 | 11 ⚠n<20 | 61% | 45% | **-0.05** | 1.4 | 27% | 10 / 24 | -2.5% |
| 2nd-leg reversal R:R≥2 | 6 | 3 ⚠n<20 | 50% | 33% | **+0.00** | 3.2 | 100% | 5 / 5 | -1.0% |
| Counter-trend (vs 15m BOS) | 296 | 128 | 43% | 38% | **+0.06** | 2.1 | 53% | 30 / 66 | -7.1% |
| With trend | 146 | 67 | 46% | 30% | **-0.17** | 2.1 | 54% | 28 / 44 | -10.3% |
| IFVG only (stand-alone) | 228 | 108 | 47% | 38% | **+0.06** | 1.7 | 44% | 25 / 65 | -8.9% |
| OB only (stand-alone) | 365 | 160 | 44% | 32% | **-0.06** | 2.2 | 55% | 30 / 59 | -11.4% |
| OTE only (stand-alone) | 442 | 139 | 31% | 21% | **-0.12** | 4.1 | 88% | 35 / 49 | -12.0% |
| Unicorn only (stand-alone) | 93 | 45 | 48% | 33% | **+0.11** | 2.4 | 60% | 50 / 77 | -4.2% |
| IFVG only, R:R≥2 | 112 | 47 | 42% | 26% | **+0.13** | 3.2 | 100% | 45 / 91 | -5.1% |
| OB only, R:R≥2 | 228 | 88 | 39% | 19% | **-0.17** | 3.8 | 100% | 60 / 97 | -13.2% |
| OTE only, R:R≥2 | 412 | 123 | 30% | 19% | **-0.13** | 4.6 | 100% | 35 / 52 | -11.9% |
| Unicorn only, R:R≥2 | 67 | 27 | 40% | 33% | **+0.36** | 3.6 | 100% | 60 / 81 | -3.4% |
| EU | 89 | 43 | 48% | 35% | **-0.13** | 1.6 | 40% | 25 / 52 | -3.6% |
| GU | 61 | 37 | 61% | 30% | **-0.29** | 1.8 | 41% | 25 / 72 | -5.3% |
| NAS | 138 | 55 | 40% | 33% | **-0.04** | 2.2 | 62% | 32 / 62 | -7.4% |
| XAU | 154 | 60 | 39% | 42% | **+0.25** | 2.5 | 63% | 20 / 56 | -3.4% |
| EU R:R≥2 | 49 | 17 ⚠n<20 | 35% | 18% | **-0.16** | 4.6 | 100% | 120 / 117 | -3.0% |
| GU R:R≥2 | 28 | 15 ⚠n<20 | 54% | 7% | **-0.75** | 3.4 | 100% | 360 / 360 | -5.5% |
| NAS R:R≥2 | 86 | 34 | 40% | 21% | **-0.17** | 4.0 | 100% | 40 / 54 | -9.1% |
| XAU R:R≥2 | 91 | 38 | 42% | 24% | **+0.04** | 3.5 | 100% | 55 / 72 | -5.4% |
| KZ Asian 20-00 | 69 | 69 | 100% | 41% | **+0.03** | 1.7 | 43% | 38 / 64 | -8.3% |
| KZ London Open 02-05 | 27 | 27 | 100% | 48% | **+0.18** | 1.7 | 41% | 25 / 37 | -2.4% |
| KZ NY AM 07-10 | 7 | 7 ⚠n<20 | 100% | 0% | **-1.00** | 3.4 | 71% | - / - | -3.4% |
| KZ NY PM 13:30-16 | 1 | 1 ⚠n<20 | 100% | 100% | **+2.14** | 2.1 | 100% | 70 / 70 | 0.0% |
| KZ Silver Bullet 10-11 | 3 | 3 ⚠n<20 | 100% | 0% | **-0.12** | 2.6 | 100% | - / - | -1.0% |
| KZ other | 88 | 88 | 100% | 31% | **-0.07** | 2.3 | 61% | 30 / 65 | -10.0% |
| KZ London Close 10-12 (overlaps SB) | 3 | 3 ⚠n<20 | 100% | 0% | **-0.12** | 2.6 | 100% | - / - | -1.0% |
| Fri | 36 | 36 | 100% | 36% | **+0.26** | 2.3 | 64% | 80 / 93 | -4.9% |
| Mon | 33 | 33 | 100% | 27% | **-0.29** | 2.1 | 55% | 20 / 46 | -5.4% |
| Thu | 32 | 32 | 100% | 34% | **-0.00** | 3.3 | 59% | 50 / 57 | -5.6% |
| Tue | 45 | 45 | 100% | 42% | **+0.12** | 1.7 | 44% | 25 / 77 | -3.6% |
| Wed | 49 | 49 | 100% | 35% | **-0.19** | 1.8 | 49% | 20 / 23 | -7.0% |

### Classic (target = HTF impulse extreme): OANDA 15m+5m, 4 instruments, about 21 days
| Split | Setups | Fills | Fill % | Win % | Avg R = expectancy | Median R:R | R:R ≥2 | Median / avg min to target | Max DD @0.5% |
|---|---|---|---|---|---|---|---|---|---|
| **All setups** | 89 | 29 | 33% | 10% | **-0.17** | 6.8 | 93% | 90 / 83 | -4.0% |
| **Only R:R ≥ 1:2** | 87 | 27 | 31% | 7% | **-0.22** | 7.0 | 100% | 80 / 80 | -4.4% |
| EU | 17 | 8 ⚠n<20 | 47% | 12% | **+0.04** | 5.4 | 100% | 100 / 100 | -1.5% |
| GU | 13 | 6 ⚠n<20 | 46% | 17% | **-0.34** | 5.2 | 83% | 60 / 60 | -1.5% |
| NAS | 35 | 4 ⚠n<20 | 11% | 0% | **-1.00** | 11.0 | 100% | - / - | -2.0% |
| XAU | 24 | 11 ⚠n<20 | 46% | 9% | **+0.06** | 7.0 | 91% | 90 / 90 | -3.0% |
| EU R:R≥2 | 17 | 8 ⚠n<20 | 47% | 12% | **+0.04** | 5.4 | 100% | 100 / 100 | -1.5% |
| GU R:R≥2 | 12 | 5 ⚠n<20 | 42% | 20% | **-0.21** | 6.4 | 100% | 60 / 60 | -1.0% |
| NAS R:R≥2 | 35 | 4 ⚠n<20 | 11% | 0% | **-1.00** | 11.0 | 100% | - / - | -2.0% |
| XAU R:R≥2 | 23 | 10 ⚠n<20 | 43% | 0% | **-0.11** | 9.5 | 100% | - / - | -3.0% |
| KZ Asian 20-00 | 10 | 10 ⚠n<20 | 100% | 10% | **-0.59** | 5.4 | 90% | 100 / 100 | -3.0% |
| KZ London Open 02-05 | 4 | 4 ⚠n<20 | 100% | 0% | **-1.00** | 6.1 | 100% | - / - | -2.0% |
| KZ NY AM 07-10 | 2 | 2 ⚠n<20 | 100% | 50% | **+0.39** | 4.4 | 50% | 90 / 90 | -0.5% |
| KZ NY PM 13:30-16 | 2 | 2 ⚠n<20 | 100% | 0% | **-1.00** | 7.8 | 100% | - / - | -1.0% |
| KZ Silver Bullet 10-11 | 1 | 1 ⚠n<20 | 100% | 0% | **-1.00** | 6.2 | 100% | - / - | -0.5% |
| KZ other | 10 | 10 ⚠n<20 | 100% | 10% | **+0.71** | 8.8 | 100% | 60 / 60 | -2.0% |
| KZ London Close 10-12 (overlaps SB) | 2 | 2 ⚠n<20 | 100% | 0% | **-1.00** | 8.0 | 100% | - / - | -1.0% |
| Fri | 4 | 4 ⚠n<20 | 100% | 0% | **-1.00** | 12.8 | 100% | - / - | -2.0% |
| Mon | 8 | 8 ⚠n<20 | 100% | 12% | **+0.04** | 6.3 | 100% | 100 / 100 | -2.5% |
| Thu | 3 | 3 ⚠n<20 | 100% | 33% | **+3.29** | 10.0 | 100% | 60 / 60 | -0.5% |
| Tue | 7 | 7 ⚠n<20 | 100% | 14% | **-0.60** | 7.7 | 86% | 90 / 90 | -2.5% |
| Wed | 7 | 7 ⚠n<20 | 100% | 0% | **-1.00** | 5.1 | 86% | - / - | -3.4% |

### Classic, nearest-pool target: OANDA 15m+5m, 4 instruments, about 21 days
| Split | Setups | Fills | Fill % | Win % | Avg R = expectancy | Median R:R | R:R ≥2 | Median / avg min to target | Max DD @0.5% |
|---|---|---|---|---|---|---|---|---|---|
| **All setups** | 90 | 30 | 33% | 17% | **-0.18** | 5.0 | 93% | 45 / 47 | -4.9% |
| **Only R:R ≥ 1:2** | 87 | 28 | 32% | 14% | **-0.22** | 5.1 | 100% | 42 / 48 | -4.9% |

### Ping-Pong: Dukascopy XAUUSD 1m, 104 days
| Split | Setups | Fills | Fill % | Win % | Avg R = expectancy | Median R:R | R:R ≥2 | Median / avg min to target | Max DD @0.5% |
|---|---|---|---|---|---|---|---|---|---|
| **All setups** | 433 | 198 | 46% | 18% | **+0.07** | 4.7 | 87% | 54 / 71 | -21.1% |
| **Only R:R ≥ 1:2** | 322 | 172 | 53% | 17% | **+0.15** | 5.3 | 100% | 56 / 80 | -18.2% |
| 2nd-leg reversal (all) | 24 | 21 | 88% | 19% | **+0.30** | 3.9 | 90% | 40 / 34 | -4.6% |
| 2nd-leg reversal R:R≥2 | 22 | 19 ⚠n<20 | 86% | 16% | **+0.35** | 4.8 | 100% | 49 / 44 | -4.9% |
| Counter-trend (vs 15m BOS) | 252 | 113 | 45% | 17% | **+0.04** | 4.8 | 87% | 54 / 71 | -16.0% |
| With trend | 181 | 85 | 47% | 19% | **+0.11** | 4.4 | 87% | 51 / 72 | -9.0% |
| IFVG only (stand-alone) | 222 | 113 | 51% | 18% | **+0.05** | 3.9 | 88% | 59 / 76 | -14.8% |
| OB only (stand-alone) | 293 | 162 | 55% | 18% | **+0.12** | 5.0 | 88% | 54 / 66 | -21.4% |
| OTE only (stand-alone) | 433 | 175 | 40% | 10% | **-0.15** | 7.5 | 99% | 60 / 56 | -32.1% |
| Unicorn only (stand-alone) | 90 | 40 | 44% | 18% | **+0.17** | 5.7 | 90% | 63 / 64 | -8.4% |
| IFVG only, R:R≥2 | 167 | 99 | 59% | 18% | **+0.12** | 4.4 | 100% | 62 / 83 | -13.7% |
| OB only, R:R≥2 | 249 | 142 | 57% | 16% | **+0.17** | 5.7 | 100% | 54 / 75 | -20.4% |
| OTE only, R:R≥2 | 420 | 174 | 41% | 10% | **-0.14** | 7.6 | 100% | 60 / 56 | -31.7% |
| Unicorn only, R:R≥2 | 64 | 36 | 56% | 19% | **+0.25** | 6.4 | 100% | 63 / 64 | -7.9% |
| XAU | 433 | 198 | 46% | 18% | **+0.07** | 4.7 | 87% | 54 / 71 | -21.1% |
| XAU R:R≥2 | 322 | 172 | 53% | 17% | **+0.15** | 5.3 | 100% | 56 / 80 | -18.2% |
| KZ Asian 20-00 | 65 | 65 | 100% | 17% | **+0.37** | 7.3 | 97% | 54 / 96 | -13.4% |
| KZ London Open 02-05 | 5 | 5 ⚠n<20 | 100% | 0% | **-1.00** | 8.3 | 100% | - / - | -2.5% |
| KZ other | 128 | 128 | 100% | 19% | **-0.04** | 3.6 | 81% | 52 / 60 | -10.1% |
| KZ London Close 10-12 (overlaps SB) | 0 | 0 | | | | | | | |
| Fri | 40 | 40 | 100% | 15% | **-0.20** | 3.4 | 88% | 65 / 78 | -12.4% |
| Mon | 35 | 35 | 100% | 11% | **-0.02** | 5.9 | 89% | 90 / 87 | -9.8% |
| Thu | 45 | 45 | 100% | 27% | **+0.46** | 5.2 | 82% | 51 / 77 | -3.5% |
| Tue | 41 | 41 | 100% | 12% | **-0.10** | 4.7 | 88% | 65 / 53 | -8.3% |
| Wed | 37 | 37 | 100% | 22% | **+0.17** | 4.8 | 89% | 32 / 62 | -6.0% |

### Classic (target = HTF impulse extreme): Dukascopy XAUUSD 1m, 104 days
| Split | Setups | Fills | Fill % | Win % | Avg R = expectancy | Median R:R | R:R ≥2 | Median / avg min to target | Max DD @0.5% |
|---|---|---|---|---|---|---|---|---|---|
| **All setups** | 130 | 72 | 55% | 6% | **-0.41** | 10.6 | 100% | 86 / 94 | -15.7% |
| **Only R:R ≥ 1:2** | 130 | 72 | 55% | 6% | **-0.41** | 10.6 | 100% | 86 / 94 | -15.7% |
| XAU | 130 | 72 | 55% | 6% | **-0.41** | 10.6 | 100% | 86 / 94 | -15.7% |
| XAU R:R≥2 | 130 | 72 | 55% | 6% | **-0.41** | 10.6 | 100% | 86 / 94 | -15.7% |
| KZ Asian 20-00 | 15 | 15 ⚠n<20 | 100% | 13% | **+0.52** | 10.6 | 100% | 105 / 105 | -4.9% |
| KZ London Open 02-05 | 10 | 10 ⚠n<20 | 100% | 0% | **-1.00** | 10.6 | 100% | - / - | -4.9% |
| KZ NY AM 07-10 | 9 | 9 ⚠n<20 | 100% | 0% | **-1.00** | 10.8 | 100% | - / - | -4.4% |
| KZ NY PM 13:30-16 | 5 | 5 ⚠n<20 | 100% | 0% | **-1.00** | 14.9 | 100% | - / - | -2.5% |
| KZ Silver Bullet 10-11 | 3 | 3 ⚠n<20 | 100% | 0% | **-1.00** | 7.3 | 100% | - / - | -1.5% |
| KZ other | 30 | 30 | 100% | 7% | **-0.35** | 10.4 | 100% | 82 / 82 | -9.1% |
| KZ London Close 10-12 (overlaps SB) | 6 | 6 ⚠n<20 | 100% | 0% | **-1.00** | 9.1 | 100% | - / - | -3.0% |
| Fri | 18 | 18 ⚠n<20 | 100% | 6% | **-0.50** | 10.4 | 100% | 90 / 90 | -6.8% |
| Mon | 12 | 12 ⚠n<20 | 100% | 17% | **+0.90** | 10.3 | 100% | 105 / 105 | -3.4% |
| Thu | 16 | 16 ⚠n<20 | 100% | 0% | **-1.00** | 12.1 | 100% | - / - | -7.7% |
| Tue | 15 | 15 ⚠n<20 | 100% | 7% | **-0.30** | 8.3 | 100% | 75 / 75 | -4.4% |
| Wed | 11 | 11 ⚠n<20 | 100% | 0% | **-1.00** | 13.4 | 100% | - / - | -5.4% |

### Classic, nearest-pool target: Dukascopy XAUUSD 1m, 104 days
| Split | Setups | Fills | Fill % | Win % | Avg R = expectancy | Median R:R | R:R ≥2 | Median / avg min to target | Max DD @0.5% |
|---|---|---|---|---|---|---|---|---|---|
| **All setups** | 128 | 70 | 55% | 6% | **-0.45** | 10.0 | 100% | 86 / 91 | -16.5% |
| **Only R:R ≥ 1:2** | 128 | 70 | 55% | 6% | **-0.45** | 10.0 | 100% | 86 / 91 | -16.5% |

**Reading.**
- **Ping-Pong, OANDA (4 instruments, n=195):** −0.02R overall. R:R≥2 gives −0.17R over 104 trades, win 19%, DD −14%.
  - XAU +0.27R (n=57).
  - London Open 02-05 +0.16R (n=28).
  - Counter-trend +0.06R vs with-trend −0.17R.
  - Unicorn-only at R:R≥2: **+0.37R, n=30, win 33%**. This is the best confirmation type.
- **Ping-Pong, Dukascopy XAU 1m (n=198):** +0.07R. R:R≥2 gives **+0.15R over 172 trades**, win 17%, median R:R 5.3, DD −18%.
  - Unicorn-only at R:R≥2: +0.25R (n=36).
  - OB +0.17R; IFVG +0.12R; OTE-only −0.14R.
  - Second leg at R:R≥2: +0.35R but n=19 (⚠).
  - Asian-session fills +0.37R (n=65); Thursday +0.46R (n=45).
- **Classic:** OANDA −0.17R (n=29; R:R≥2 −0.22R). Dukascopy XAU −0.41R (n=72, win 6%; the median target is about 10R away). Nearest-pool variant −0.18R / −0.45R. **Waiting for the HTF OTE plus a sweep plus an LTF shift rarely reaches the HTF target before 16:00 NY.**

**Verdicts.**
- **Classic: REJECTED** (n=29-72, expectancy negative on both sources).
- **Ping-Pong as a whole: REJECTED** at the +0.3R bar. Best result is +0.15R at R:R≥2 (XAU 1m, n=172); OANDA is negative.
- **Ping-Pong, Unicorn confirmation only, R:R≥2: PROMISING.**
  - OANDA: +0.37R, n=30. This meets the CONFIRMED bar on one source.
  - Dukascopy XAU 1m: +0.25R, n=36, which does not meet it.
  - It is not confirmed across both sources, and OANDA covers only 21 days.
- **Second-leg reversal: PROMISING at best** (+0.35R, n=19 on XAU 1m; OANDA n=11, −0.05R).
- The reels' 2-17R claims are not reproduced. Real wins average about 2-5R with 17-35% win rates.

Script: scripts/pingpong_backtest.py (charts: scripts/pingpong_charts.py; Dukascopy fetcher: scripts/duka_fetch.sh). Results: data/pingpong_results.json, data/pingpong_trades.pkl.

Charts: charts/pingpong_summary.png, charts/pingpong_example.png, charts/classic_example.png.
- **Ping-Pong example** (NAS100 5m, 2026-10-07): sweep of a 15m swing high at 02:25 SAST, MSS at 02:45, OB short filled at 03:40 (31292, stop 31303.8), target pool 31268.4 hit at 03:45 for +2.0R.
- **Classic example** (GBPUSD 5m, 2026-09-24): downtrend; sweep of a 15m swing high inside the HTF OTE at 18:15 SAST, MSS at 18:50, OTE short filled at 19:00 (1.32334, stop 1.32414), target 1.32097 hit at 20:00 for +2.95R.

## Prior-day Volume Profile POC/VAH/VAL rejection (@julianmerrow reel) (added 2026-10-07 17:53 SAST)
**Data.**
- OANDA via TradingView, with **tick volume**. Main test: 30m signal bars built from OANDA 15m, **70 trading days** (2026-07-01 to 10-06). Cross-check: 1h signal bars and 1h-based profiles, **448 trading days** (2025-01-02 to 2026-10-06).
- Profile per prior trading day (17:00-17:00 NY) from that day's OANDA bars (15m for the main test, 1h for the cross-check). Each bar's volume is spread evenly across its high-low in 200 bins. POC = top bin. Value area = 70%, expanded outward from the POC.
- Dukascopy and 5m were not used for the profile, to keep one consistent OANDA source over 70 days; 5m covers only about 21 days.
- **Tick-volume caveat:** OANDA volume is a count of price updates, not traded contracts. Spot FX/CFD has no central volume, so the POC is only a proxy for the futures POC.

**Rules as implemented.**
- **Bias:** prior close vs prior-day midpoint; above = bullish.
- **Long rejection at a level:** the 30m bar opens at or above the level, wicks below it, and closes above it. Short is the mirror. Tested "with bias" (only trades in the bias direction) vs "no bias filter" (both directions).
- **Entry and stop:** entry at the rejection close. Stop beyond the wick + buffer (NAS 2 pt, XAU $0.50, FX 1 pip).
- **Targets, each tested separately:**
  - 2R and 3R.
  - Opposite VA edge: long → VAH, or PDH if entry is already above VAH; short mirror.
  - PDH/PDL.
- **One trade per level (POC, VAH, VAL) per day**, at the first rejection.
- **Timing:** no entries after 16:00 NY. Time exit at 17:00 NY at the last bar close.
- **Fills:** managed on 15m bars (main) or 1h bars (cross-check). A bar touching both stop and target counts as a loss.
- **Kill zones:** by entry time in NY. SAST = NY+6.


### 30m (OANDA 15m, ~70 d)
| Split | n | Win | Avg R | Max DD @0.5% | Median min to target | Median R:R (share ≥1:2) |
|---|---|---|---|---|---|---|
| no bias filter, target 2R | 506 | 25% | **-0.18** | -42.7% | 75 | 2.0 (100% ≥1:2) |
| no bias filter, target 3R | 506 | 19% | **-0.15** | -41.9% | 128 | 3.0 (100% ≥1:2) |
| no bias filter, target VA | 493 | 26% | **-0.10** | -36.0% | 75 | 3.1 (70% ≥1:2) |
| no bias filter, target VA RR>=2 | 347 | 14% | **-0.14** | -33.2% | 180 | 4.9 (100% ≥1:2) |
| no bias filter, target PD | 493 | 16% | **-0.12** | -49.5% | 165 | 5.6 (84% ≥1:2) |
| no bias filter, target PD RR>=2 | 416 | 12% | **-0.11** | -45.0% | 300 | 6.8 (100% ≥1:2) |
| with bias, target 2R | 281 | 25% | **-0.19** | -30.3% | 60 | 2.0 (100% ≥1:2) |
| with bias, target 3R | 281 | 19% | **-0.17** | -31.9% | 105 | 3.0 (100% ≥1:2) |
| with bias, target VA | 274 | 28% | **-0.13** | -25.2% | 68 | 2.6 (65% ≥1:2) |
| with bias, target VA RR>=2 | 178 | 13% | **-0.26** | -23.6% | 158 | 4.5 (100% ≥1:2) |
| with bias, target PD | 274 | 20% | **-0.10** | -31.3% | 128 | 4.2 (80% ≥1:2) |
| with bias, target PD RR>=2 | 218 | 15% | **-0.10** | -26.8% | 255 | 5.5 (100% ≥1:2) |
| with bias, 2R, level: POC | 101 | 23% | **-0.29** | -19.2% | 60 | 2.0 (100% ≥1:2) |
| with bias, 2R, level: VAH | 89 | 22% | **-0.23** | -14.0% | 68 | 2.0 (100% ≥1:2) |
| with bias, 2R, level: VAL | 91 | 31% | **-0.02** | -8.8% | 60 | 2.0 (99% ≥1:2) |
| with bias, 2R, inst: EU | 61 | 26% | **-0.13** | -9.6% | 60 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: GU | 75 | 24% | **-0.22** | -11.8% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: NAS | 71 | 30% | **-0.09** | -6.9% | 75 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: XAU | 74 | 22% | **-0.28** | -12.3% | 45 | 2.0 (99% ≥1:2) |
| with bias, 2R, kz: Asian 20-00 | 74 | 27% | **-0.19** | -10.5% | 45 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: London Open 02-05 | 51 | 31% | **-0.06** | -7.3% | 68 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: NY AM 07-10 | 23 | 30% | **+0.20** | -2.5% | 60 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: NY PM 13:30-16 | 5 ⚠n<20 | 0% | **-0.37** | -1.1% | - | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: Silver Bullet 10-11 | 10 ⚠n<20 | 20% | **-0.21** | -1.5% | 90 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: other | 118 | 22% | **-0.30** | -21.7% | 75 | 2.0 (99% ≥1:2) |
| with bias, 2R, kz: London Close 10-12 (overlap) | 21 | 10% | **-0.42** | -4.3% | 90 | 2.0 (95% ≥1:2) |
| no bias filter, 2R, level: POC | 175 | 25% | **-0.23** | -24.6% | 60 | 2.0 (99% ≥1:2) |
| no bias filter, 2R, level: VAH | 160 | 25% | **-0.18** | -16.5% | 75 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, level: VAL | 171 | 27% | **-0.13** | -14.2% | 75 | 2.0 (99% ≥1:2) |
| no bias filter, 2R, inst: EU | 131 | 27% | **-0.14** | -13.4% | 75 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: GU | 122 | 21% | **-0.28** | -19.7% | 135 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: NAS | 121 | 29% | **-0.10** | -10.8% | 75 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: XAU | 132 | 25% | **-0.19** | -16.4% | 60 | 2.0 (98% ≥1:2) |
| no bias filter, 2R, kz: Asian 20-00 | 141 | 32% | **-0.04** | -9.1% | 60 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: London Open 02-05 | 80 | 30% | **-0.06** | -12.1% | 75 | 2.0 (99% ≥1:2) |
| no bias filter, 2R, kz: NY AM 07-10 | 45 | 20% | **-0.22** | -7.0% | 75 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: NY PM 13:30-16 | 14 ⚠n<20 | 0% | **-0.63** | -4.5% | - | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: Silver Bullet 10-11 | 19 ⚠n<20 | 16% | **-0.21** | -3.0% | 60 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: other | 207 | 23% | **-0.28** | -28.7% | 98 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: London Close 10-12 (overlap) | 40 | 12% | **-0.33** | -6.4% | 60 | 2.0 (98% ≥1:2) |

### 1h (OANDA 1h, Jan 2025+)
| Split | n | Win | Avg R | Max DD @0.5% | Median min to target | Median R:R (share ≥1:2) |
|---|---|---|---|---|---|---|
| no bias filter, target 2R | 2908 | 28% | **-0.04** | -49.6% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, target 3R | 2908 | 20% | **-0.01** | -49.7% | 180 | 3.0 (100% ≥1:2) |
| no bias filter, target VA | 2775 | 30% | **-0.03** | -53.7% | 120 | 2.6 (59% ≥1:2) |
| no bias filter, target VA RR>=2 | 1640 | 17% | **-0.03** | -39.5% | 180 | 4.3 (100% ≥1:2) |
| no bias filter, target PD | 2775 | 21% | **-0.00** | -57.5% | 180 | 4.2 (77% ≥1:2) |
| no bias filter, target PD RR>=2 | 2134 | 13% | **+0.02** | -42.9% | 300 | 5.7 (100% ≥1:2) |
| with bias, target 2R | 1634 | 28% | **-0.04** | -35.3% | 120 | 2.0 (100% ≥1:2) |
| with bias, target 3R | 1634 | 19% | **-0.03** | -41.0% | 180 | 3.0 (100% ≥1:2) |
| with bias, target VA | 1541 | 32% | **-0.04** | -44.7% | 120 | 2.2 (54% ≥1:2) |
| with bias, target VA RR>=2 | 835 | 18% | **-0.04** | -29.9% | 180 | 4.0 (100% ≥1:2) |
| with bias, target PD | 1541 | 23% | **-0.06** | -54.3% | 120 | 3.4 (71% ≥1:2) |
| with bias, target PD RR>=2 | 1101 | 15% | **-0.04** | -46.1% | 240 | 4.7 (100% ≥1:2) |
| with bias, 2R, level: POC | 603 | 29% | **-0.05** | -20.2% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, level: VAH | 510 | 28% | **-0.02** | -19.3% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, level: VAL | 521 | 27% | **-0.05** | -18.6% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: EU | 419 | 28% | **-0.01** | -14.9% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: GU | 432 | 28% | **-0.07** | -17.4% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: NAS | 385 | 26% | **-0.09** | -19.5% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, inst: XAU | 398 | 29% | **+0.01** | -13.7% | 120 | 2.0 (99% ≥1:2) |
| with bias, 2R, kz: Asian 20-00 | 446 | 31% | **-0.06** | -22.5% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: London Open 02-05 | 213 | 31% | **+0.01** | -12.2% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: NY AM 07-10 | 143 | 34% | **+0.14** | -5.0% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: NY PM 13:30-16 | 56 | 11% | **-0.08** | -4.4% | 60 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: Silver Bullet 10-11 | 83 | 23% | **-0.01** | -4.2% | 60 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: other | 693 | 26% | **-0.08** | -27.9% | 120 | 2.0 (100% ≥1:2) |
| with bias, 2R, kz: London Close 10-12 (overlap) | 187 | 16% | **-0.13** | -12.3% | 120 | 2.0 (99% ≥1:2) |
| no bias filter, 2R, level: POC | 1033 | 29% | **-0.05** | -30.9% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, level: VAH | 939 | 27% | **-0.04** | -22.7% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, level: VAL | 936 | 29% | **-0.02** | -24.4% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: EU | 749 | 29% | **+0.00** | -18.3% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: GU | 755 | 28% | **-0.07** | -27.5% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: NAS | 688 | 26% | **-0.11** | -34.0% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, inst: XAU | 716 | 31% | **+0.03** | -14.1% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: Asian 20-00 | 833 | 32% | **-0.03** | -26.3% | 180 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: London Open 02-05 | 385 | 35% | **+0.11** | -11.4% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: NY AM 07-10 | 249 | 28% | **-0.03** | -11.2% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: NY PM 13:30-16 | 84 | 11% | **-0.16** | -6.6% | 60 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: Silver Bullet 10-11 | 151 | 20% | **-0.05** | -6.6% | 90 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: other | 1206 | 27% | **-0.08** | -41.2% | 120 | 2.0 (100% ≥1:2) |
| no bias filter, 2R, kz: London Close 10-12 (overlap) | 303 | 16% | **-0.10** | -15.4% | 120 | 2.0 (100% ≥1:2) |

**Reading.**
- **Every configuration is negative or flat.**
  - 30m: −0.10 to −0.26R across all targets and filters. Max DD −24% to −50% at 0.5% risk.
  - 1h over 448 days: −0.06R to +0.02R; the best is no-bias PD at R:R≥2, +0.02R over 2,134 trades.
- **The bias filter does not help:** 30m with-bias 2R −0.19R vs no filter −0.18R.
- **Levels:** POC is worst (30m −0.23 / −0.29R). VAL is near flat with bias (−0.02R, n=91).
- **Only mildly positive pocket:** NY AM 07-10 NY (13-16 SAST) with bias at 2R. 30m +0.20R (n=23); 1h +0.14R (n=143), win 34%. Same sign on both timeframes, but below +0.3R.
- **Times:** 2R targets that hit took a median 60-75 min (30m) or 120 min (1h).

**Verdict: REJECTED** for every configuration. No target or filter reaches +0.3R with n≥30. NY AM with bias is the only lead worth watching (+0.14 to +0.20R), and it is not tradable at Hilda's bar.

Script: scripts/vp_poc_backtest.py (charts: scripts/vp_charts.py; tick-volume fetch: scripts/fetch_vol.py). Results: data/vp_results.json. Charts: charts/vp_summary.png, charts/vp_example.png.

Example: EURUSD 2026-10-07. Prior-day POC 1.12577, VAH 1.12718, VAL 1.12278. A bullish-bias 30m rejection of VAL closed at 07:30 SAST (01:30 NY). Long 1.12286, stop 1.12267; the 2R target of 1.12324 was hit within 30 minutes.

## goldhunter_ict "One Setup for life" in ICT macro windows (added 2026-10-07 17:58 SAST)
**Data (trading days with data).**
- **Dukascopy 1m (spot BID):** XAUUSD 90 days (Jun to Oct 2026); EURUSD only **25 days**, a partial download because Dukascopy still rate-limits (HTTP 429). The "Dukascopy 1m" rows pool XAU and EU; per-instrument rows are below. **GBPUSD and NAS Dukascopy: not available.**
- **OANDA 5m:** NAS/XAU 23 days, EU/GU 18 days.
- **OANDA 1m:** 8 days, all four instruments.
- All prices are real.

**Rules made mechanical (bearish; bullish is the mirror).**
- **Premium:** the sweep price is above the 50% of the prior-day range (PDH-PDL dealing range). FVG/OB premium was not required.
- **Swing:** 5-bar fractal (2 bars each side), confirmed, unswept, within the last **N = 60 min** (60 bars on 1m, 12 on 5m). The highest one is used.
- **Sweep:** a bar inside a macro window (NY: 07:50-08:10, 08:50-09:10, 09:50-10:10, 10:50-11:10, 11:50-12:10, 13:20-13:40, 14:50-15:10, 15:15-15:45, 15:50-16:10) trades above it.
- **E1:** the last bullish FVG formed in the 60 minutes up to the sweep is inverted (a close below its bottom). Enter at the next bar open.
- **E2 (breaker):** a close below the lowest low between the swept swing and the sweep bar. Enter at the next bar open.
- **Entry deadline:** 30 min after the window ends. **Time exit:** 90 min after the window ends, at bar open.
- **Stops:**
  - Stop A = sweep extreme (updated to entry) + buffer (NAS 2, XAU $0.50, FX 1 pip).
  - Stop B ("zone") = E1: FVG top + buffer; E2: high of the breaker (swing-low) candle + buffer.
- **Targets:** fixed 2R, and opposing liquidity (nearest unswept 5-bar fractal low from today below entry, else PDL).
- **Conservative fills:** stop checked first; a bar touching both stop and target is a loss.
- **Trade limit:** one setup per window per instrument (first premium sweep). E1 and E2 are evaluated separately.
- **Bias:** prior close vs prior-day midpoint.

**Setups and fills (E1 / E2).**
- Dukascopy 1m: {'E1': 192, 'E2': 190} → triggered {'E1': 123, 'E2': 60}.
- OANDA 5m: {'E1': 130, 'E2': 156} → {'E1': 42, 'E2': 29}.
- OANDA 1m: {'E1': 72, 'E2': 71} → {'E1': 41, 'E2': 26}.


### Dukascopy 1m
| Split | n | Win | Avg R | Max DD @0.5% | Median min to target | Median R:R (share ≥1:2) |
|---|---|---|---|---|---|---|
| stop=sweep, tgt=2R | 183 | 13% | **-0.08** | -13.0% | 34 | 2.00 (100%) |
| stop=zone, tgt=2R | 183 | 27% | **-0.12** | -13.6% | 11 | 2.00 (100%) |
| stop=sweep, tgt=liq | 183 | 64% | **-0.06** | -6.4% | 6 | 0.35 (1%) |
| stop=sweep, tgt=liq, RR>=2 | 1 ⚠n<20 | 0% | **-1.00** | -0.5% | - | 2.19 (100%) |
| stop=zone, tgt=liq | 183 | 44% | **-0.11** | -10.4% | 4 | 1.17 (25%) |
| stop=zone, tgt=liq, RR>=2 | 46 | 17% | **-0.22** | -9.6% | 12 | 3.08 (100%) |
| sweep stop, 2R: E1 | 123 | 14% | **-0.06** | -8.6% | 31 | 2.00 (100%) |
| sweep stop, 2R: E2 | 60 | 10% | **-0.12** | -5.2% | 50 | 2.00 (100%) |
| sweep stop, 2R: macro 07:50-08:10 NY (13:50-14:10 SAST) | 26 | 12% | **-0.18** | -3.6% | 33 | 2.00 (100%) |
| sweep stop, 2R: macro 08:50-09:10 NY (14:50-15:10 SAST) | 24 | 8% | **-0.20** | -2.4% | 56 | 2.00 (100%) |
| sweep stop, 2R: macro 09:50-10:10 NY (15:50-16:10 SAST) | 26 | 27% | **+0.27** | -2.0% | 38 | 2.00 (100%) |
| sweep stop, 2R: macro 10:50-11:10 NY (16:50-17:10 SAST) | 18 ⚠n<20 | 11% | **-0.23** | -3.0% | 46 | 2.00 (100%) |
| sweep stop, 2R: macro 11:50-12:10 NY (17:50-18:10 SAST) | 20 | 5% | **-0.46** | -4.8% | 19 | 2.00 (100%) |
| sweep stop, 2R: macro 13:20-13:40 NY (19:20-19:40 SAST) | 22 | 23% | **+0.08** | -2.4% | 25 | 2.00 (100%) |
| sweep stop, 2R: macro 14:50-15:10 NY (20:50-21:10 SAST) | 19 ⚠n<20 | 5% | **-0.06** | -2.1% | 42 | 2.00 (100%) |
| sweep stop, 2R: macro 15:15-15:45 NY (21:15-21:45 SAST) | 12 ⚠n<20 | 17% | **+0.22** | -1.0% | 52 | 2.00 (100%) |
| sweep stop, 2R: macro 15:50-16:10 NY (21:50-22:10 SAST) | 16 ⚠n<20 | 0% | **-0.17** | -2.0% | - | 2.00 (100%) |
| sweep stop, 2R: EU | 29 | 21% | **+0.26** | -2.5% | 42 | 2.00 (100%) |
| sweep stop, 2R: XAU | 154 | 11% | **-0.15** | -12.6% | 33 | 2.00 (100%) |
| sweep stop, 2R: against bias | 94 | 11% | **-0.25** | -11.3% | 36 | 2.00 (100%) |
| sweep stop, 2R: with bias | 89 | 15% | **+0.10** | -4.8% | 33 | 2.00 (100%) |

### OANDA 5m
| Split | n | Win | Avg R | Max DD @0.5% | Median min to target | Median R:R (share ≥1:2) |
|---|---|---|---|---|---|---|
| stop=sweep, tgt=2R | 71 | 4% | **-0.01** | -4.6% | 45 | 2.00 (100%) |
| stop=zone, tgt=2R | 71 | 21% | **+0.03** | -5.3% | 15 | 2.00 (100%) |
| stop=sweep, tgt=liq | 71 | 61% | **+0.09** | -1.6% | 10 | 0.41 (3%) |
| stop=sweep, tgt=liq, RR>=2 | 2 ⚠n<20 | 0% | **-0.83** | -0.8% | - | 3.71 (100%) |
| stop=zone, tgt=liq | 71 | 48% | **+0.09** | -2.8% | 5 | 0.93 (18%) |
| stop=zone, tgt=liq, RR>=2 | 13 ⚠n<20 | 8% | **-0.02** | -2.0% | 5 | 4.41 (100%) |
| sweep stop, 2R: E1 | 42 | 7% | **-0.04** | -3.8% | 45 | 2.00 (100%) |
| sweep stop, 2R: E2 | 29 | 0% | **+0.02** | -1.3% | - | 2.00 (100%) |
| sweep stop, 2R: macro 07:50-08:10 NY (13:50-14:10 SAST) | 9 ⚠n<20 | 11% | **-0.45** | -3.0% | 5 | 2.00 (100%) |
| sweep stop, 2R: macro 08:50-09:10 NY (14:50-15:10 SAST) | 5 ⚠n<20 | 20% | **+0.64** | 0.0% | 45 | 2.00 (100%) |
| sweep stop, 2R: macro 09:50-10:10 NY (15:50-16:10 SAST) | 11 ⚠n<20 | 9% | **+0.03** | -1.6% | 45 | 2.00 (100%) |
| sweep stop, 2R: macro 10:50-11:10 NY (16:50-17:10 SAST) | 9 ⚠n<20 | 0% | **+0.23** | -0.8% | - | 2.00 (100%) |
| sweep stop, 2R: macro 11:50-12:10 NY (17:50-18:10 SAST) | 6 ⚠n<20 | 0% | **-0.49** | -1.5% | - | 2.00 (100%) |
| sweep stop, 2R: macro 13:20-13:40 NY (19:20-19:40 SAST) | 6 ⚠n<20 | 0% | **-0.21** | -0.8% | - | 2.00 (100%) |
| sweep stop, 2R: macro 14:50-15:10 NY (20:50-21:10 SAST) | 9 ⚠n<20 | 0% | **-0.24** | -1.4% | - | 2.00 (100%) |
| sweep stop, 2R: macro 15:15-15:45 NY (21:15-21:45 SAST) | 12 ⚠n<20 | 0% | **+0.21** | -0.5% | - | 2.00 (100%) |
| sweep stop, 2R: macro 15:50-16:10 NY (21:50-22:10 SAST) | 4 ⚠n<20 | 0% | **+0.34** | 0.0% | - | 2.00 (100%) |
| sweep stop, 2R: EU | 19 ⚠n<20 | 5% | **+0.01** | -1.2% | 5 | 2.00 (100%) |
| sweep stop, 2R: GU | 11 ⚠n<20 | 9% | **+0.36** | -0.5% | 45 | 2.00 (100%) |
| sweep stop, 2R: NAS | 22 | 5% | **+0.01** | -1.9% | 45 | 2.00 (100%) |
| sweep stop, 2R: XAU | 19 ⚠n<20 | 0% | **-0.28** | -2.9% | - | 2.00 (100%) |
| sweep stop, 2R: against bias | 44 | 5% | **-0.02** | -4.3% | 25 | 2.00 (100%) |
| sweep stop, 2R: with bias | 27 | 4% | **-0.01** | -2.6% | 45 | 2.00 (100%) |

### OANDA 1m
| Split | n | Win | Avg R | Max DD @0.5% | Median min to target | Median R:R (share ≥1:2) |
|---|---|---|---|---|---|---|
| stop=sweep, tgt=2R | 67 | 10% | **-0.18** | -9.1% | 15 | 2.00 (100%) |
| stop=zone, tgt=2R | 67 | 27% | **-0.15** | -8.8% | 8 | 2.00 (100%) |
| stop=sweep, tgt=liq | 67 | 63% | **-0.06** | -4.0% | 4 | 0.38 (1%) |
| stop=sweep, tgt=liq, RR>=2 | 1 ⚠n<20 | 0% | **-1.00** | -0.5% | - | 2.52 (100%) |
| stop=zone, tgt=liq | 67 | 46% | **-0.18** | -7.5% | 2 | 1.00 (24%) |
| stop=zone, tgt=liq, RR>=2 | 16 ⚠n<20 | 6% | **-0.56** | -5.8% | 6 | 2.77 (100%) |
| sweep stop, 2R: E1 | 41 | 12% | **-0.20** | -6.1% | 15 | 2.00 (100%) |
| sweep stop, 2R: E2 | 26 | 8% | **-0.15** | -3.7% | 12 | 2.00 (100%) |
| sweep stop, 2R: macro 07:50-08:10 NY (13:50-14:10 SAST) | 10 ⚠n<20 | 10% | **-0.14** | -2.0% | 1 | 2.00 (100%) |
| sweep stop, 2R: macro 08:50-09:10 NY (14:50-15:10 SAST) | 8 ⚠n<20 | 0% | **-0.64** | -3.0% | - | 2.00 (100%) |
| sweep stop, 2R: macro 09:50-10:10 NY (15:50-16:10 SAST) | 4 ⚠n<20 | 0% | **-1.00** | -2.0% | - | 2.00 (100%) |
| sweep stop, 2R: macro 10:50-11:10 NY (16:50-17:10 SAST) | 7 ⚠n<20 | 14% | **+0.24** | -1.0% | 21 | 2.00 (100%) |
| sweep stop, 2R: macro 11:50-12:10 NY (17:50-18:10 SAST) | 10 ⚠n<20 | 10% | **-0.18** | -1.5% | 85 | 2.00 (100%) |
| sweep stop, 2R: macro 13:20-13:40 NY (19:20-19:40 SAST) | 7 ⚠n<20 | 0% | **-0.34** | -1.7% | - | 2.00 (100%) |
| sweep stop, 2R: macro 14:50-15:10 NY (20:50-21:10 SAST) | 6 ⚠n<20 | 0% | **-0.47** | -1.7% | - | 2.00 (100%) |
| sweep stop, 2R: macro 15:15-15:45 NY (21:15-21:45 SAST) | 7 ⚠n<20 | 43% | **+0.40** | -1.0% | 15 | 2.00 (100%) |
| sweep stop, 2R: macro 15:50-16:10 NY (21:50-22:10 SAST) | 8 ⚠n<20 | 12% | **+0.10** | -1.0% | 7 | 2.00 (100%) |
| sweep stop, 2R: EU | 13 ⚠n<20 | 8% | **-0.55** | -3.5% | 1 | 2.00 (100%) |
| sweep stop, 2R: GU | 17 ⚠n<20 | 6% | **-0.30** | -3.0% | 85 | 2.00 (100%) |
| sweep stop, 2R: NAS | 21 | 19% | **+0.09** | -3.5% | 16 | 2.00 (100%) |
| sweep stop, 2R: XAU | 16 ⚠n<20 | 6% | **-0.11** | -2.9% | 7 | 2.00 (100%) |
| sweep stop, 2R: against bias | 45 | 11% | **-0.23** | -6.6% | 15 | 2.00 (100%) |
| sweep stop, 2R: with bias | 22 | 9% | **-0.08** | -3.8% | 14 | 2.00 (100%) |

**Reading.**
- **No configuration is positive enough.**
  - Main deep test (Dukascopy 1m, n=183): 2R with sweep stop **−0.08R** (win 13%); 2R with zone stop −0.12R.
  - OANDA 5m (n=71): −0.01R / +0.03R. OANDA 1m (n=67): −0.18R / −0.15R.
- **Opposing liquidity is usually too close.** With the sweep stop, the median R:R to the nearest opposing pool is only 0.35-0.41, and 1-3% of setups reach 1:2. With the zone stop, 18-25% reach 1:2, and those filtered trades are negative (Dukascopy −0.22R, n=46).
- **E1 (FVG inversion) vs E2 (breaker):** Dukascopy −0.06R (n=123) vs −0.12R (n=60). OANDA 5m −0.04R vs +0.02R.
- **With vs against bias** (Dukascopy): with bias **+0.10R** (n=89) vs against −0.25R (n=94). The direction is consistent on OANDA 1m (−0.08 vs −0.23R), but nothing reaches +0.3R.
- **Macro windows** (Dukascopy, sweep stop, 2R):
  - 09:50-10:10 NY (15:50-16:10 SAST): +0.27R, n=26, win 27%.
  - 13:20-13:40 NY (19:20-19:40 SAST): +0.08R, n=22.
  - 15:15-15:45 NY: +0.22R, n=12 (⚠).
  - 11:50-12:10 NY is the worst: −0.46R, n=20.
  - On OANDA, every window has n<20.
- **EURUSD** (Dukascopy partial, 25 days): +0.26R, n=29. Not confirmed elsewhere: OANDA 1m EU −0.55R (n=13).

**Verdict: REJECTED.** No configuration reaches n≥30 with +0.3R at 1:2 or better. Leads to watch, not trade:
- With-bias only, +0.10R.
- 09:50-10:10 NY macro, +0.27R, n=26.

Script: scripts/macro_setup_backtest.py (charts: scripts/macro_charts.py). Results: data/macro_results.json, data/macro_trades.pkl. Charts: charts/macro_summary.png, charts/macro_example.png.

**Example (Dukascopy XAUUSD 1m, 2026-09-23, 13:20-13:40 NY macro, with bias):**
- Long. A 1m low swept the swing low at 4275.39 at 19:39 SAST.
- The bearish FVG was inverted. Entry 4279.01 at 19:41 SAST, stop 4273.72.
- 2R (4289.59) hit 7 min later.

## 2026-10-07 — NAS100 09:50-10:10 NY macro (15:50-16:10 SAST) deep-dive
Source: histdata.com NSXUSD M1, 2025-01-01 → 2026-10-02 (546 days; trades in 2025-01 → 2026-09). Timestamps verified empirically to be NY local incl. DST (1h return corr vs OANDA 0.98–0.99 at lag 0 in both EST and EDT periods; the "EST fixed" doc assumption was wrong by 1h in DST and the first run was discarded). 1m overlap vs OANDA:NAS100USD (2026-09-27→10-02, 6,677 bars): return corr 0.997, same direction 97%, basis ≈ +39–40 pts (level offset only). Dukascopy USATECHIDXUSD: heavy 429s, only a few days fetched, not used. yfinance NQ=F only 1m from 2026-09-30 / 5m from 2026-07-29, not needed. OANDA-only cross-check n≤3 (too short).
Scripts: scripts/nas_0950_study.py, scripts/nas0950_charts.py. Charts: charts/nas0950_summary.png, charts/nas0950_example.png (2026-09-02 zone/2R win).
Test 1 — One Setup rules unchanged (macro_setup_backtest.py), 09:50-10:10 only, 0.5% risk, conservative fills:
- sweep stop / 2R: n=220, WR 14.1%, −0.13R, maxDD −22.6%, t_med 19m. H1 −0.22 / H2 −0.05.
- zone stop / 2R: n=219, WR 33.3%, +0.03R, DD −9.1%, t_med 7m. H1 −0.07 / H2 +0.12.
- zone stop / liq (all): n=218, −0.10R. Only RR≥2: n=78, WR 17.9%, −0.07R, DD −10.8%; H1 +0.34 (n=36) / H2 −0.42 (n=42), so it fails out-of-sample.
- sweep stop / liq: all n=219, −0.04R; RR≥2 n=7 (n<20).
- Splits for zone/2R: E1 +0.01 (139), E2 +0.06 (80); with bias −0.10 (69) vs against +0.09 (150); Thu +0.36 (43), Mon +0.15, Tue −0.22, Wed −0.15, Fri 0.00; news days 0.00 (27) vs 0.03; every month n<20 except 2026-06 (+0.80, n=20).
- Neighbour windows, zone/2R: 08:50 +0.19 (227), 10:50 +0.04 (147).
Test 2 — behaviour (n≈450 days per window; random = 25 starts from 08:00-11:00, n=11,238). Columns: Judas/reversal, opposite 10-11 vs 09:30-09:50, macro extreme = 09:30-12:00 session extreme, avg range, median |move| in the 60m after:
- 08:50: 13.5% | 53.4% | 12.6% | 52 pts | 77 pts
- 09:50: 11.6% | 47.9% | 22.5% | 111 pts | 58 pts
- 10:50: 12.9% | 49.1% | 23.8% | 82 pts | 42 pts
- random: 19.4% | 50.6% | 21.8% | 79 pts | 53 pts
The 09:50 window has the largest range but its Judas rate is lower than random, its directional flip is a coin toss, and its session-extreme rate equals random. Halves and news-day results are stable (Judas 12.3% / 11.0%).
VERDICT: REJECTED. No variant has n≥30 with ≥+0.3R at 1:2 that also holds out-of-sample. Earlier Dukascopy lead (+0.27R, n=26) did not survive the larger sample. Only notable fact: the window is volatile (range 1.4× random), which is not an edge.

## 2026-10-07 — 4H PD array + 15m rejection block
Sources:
- Deep test: histdata.com 1m for EURUSD, GBPUSD, XAUUSD and NSXUSD, 2025-01-01 → 2026-10-02. Timestamps are NY local time incl. DST for all four (hourly return corr vs OANDA 0.99–1.00 at lag 0 in both EST and EDT periods; scripts/hd_tzcheck.py). Fills ordered on 1m.
- Dukascopy XAU 1m, 2026-05-31 → 10-06.
- OANDA 15m, 2026-06-30 → 10-07 (4H built from OANDA 1h back to 2025). 15m only, so no intrabar ordering.
Rules (mechanical; see the docstring of scripts/pd4h_rb15_backtest.py):
- 4H bars start 17/21/01/05/09/13 NY. Swings are 3-bar fractals.
- OB: the last opposite candle within the 10 bars before a displacement candle (body ≥50% of range) that closes beyond the latest swing. Zone is its full range. MT is its 50% line.
- FVG: the 3-bar gap.
- A level is dead after a 4H close or a 15m close beyond its far edge, and fires only once.
- Rejection: the 15m candle trades into the level, closes back outside it, and the wick on the level side is ≥50% of its range.
- Entry: limit at 50% of the wick, valid for 4 or 8 bars.
- Stops: (a) wick tip + buffer (NAS 2, XAU 0.5, FX 1 pip); (b) fixed: NAS 10, XAU 2.18, EU 1.55 pips, GU 2.05 pips, scaled by the median wick stop (NAS 16.1 / XAU 3.52 / EU 2.5 / GU 3.3 pips).
- Fills: same-bar stop+target counts as a loss. Time exit at 17:00 NY (23:00 SAST in US DST).
Results, histdata all 4 instruments (2,448 signals):
- 8-bar expiry: fill rate 77%, n=1,890.
  - wick stop: 2R WR 30.2% −0.09R DD −60%, t_med 15m; 3R 21.6% −0.13R; 6R 10.3% −0.20R DD −86%, t_med 89m.
  - fixed stop: 2R 29.6% −0.11R; 3R 22.7% −0.08R; 6R 12.5% −0.10R.
- 4-bar expiry: fill rate 70%, n=1,724, results similar (−0.09 to −0.18R).
- Halves (cut 2025-11-27): every config is negative in both halves; best is IS −0.05 / OOS −0.12.
- Splits (8-bar, wick stop, 2R):
  - type: OB −0.05 (564), MT −0.18 (448), FVG −0.07 (878).
  - instrument: GU +0.01 (489), XAU −0.07, EU −0.12, NAS −0.17.
  - bias: with −0.09 (1,092), against −0.08 (798).
  - kill zone: Asian +0.03 (277), NY AM −0.01 (377), Silver Bullet −0.13, London Close −0.13, London Open −0.14, NY PM −0.41 (135), other −0.07.
- Dukascopy XAU (n=69), fixed stop 2R: +0.30R. But histdata XAU over the same Jun–Oct 2026 window gives only +0.10R (n=81), and over the full 21 months histdata XAU fixed 2R is −0.11R in both halves. So the Dukascopy result is a lucky recent window.
- OANDA 15m, 8-bar: −0.29 to −0.43R (n=316). The 15m-only conservative fills make this worse.
Reel claim check: a 90% WR at 6R would mean +5.3R per trade. Breakeven at 6R needs 14.3% (33.3% at 2R). Observed at 6R: 10.3% (wick) / 12.5% (fixed). Observed at 2R: about 30%. Both are below breakeven.
VERDICT: REJECTED.
Scripts: pd4h_rb15_backtest.py, pd4h_report.py, pd4h_charts.py, hd_tzcheck.py, histdata_fetch_pair.sh. Charts: charts/pd4h_summary.png, charts/pd4h_example.png (XAU 2026-09-24 12:30 NY / 18:30 SAST, OB short, 2R hit in 4 min).

## NAS 09:50 macro: direction predictors (2026-10-07)
Analysis only. Data: histdata NSXUSD 1m (Jan 2025 to Oct 2026, NY-local timestamps, tracks OANDA:NAS100USD at 0.997 correlation). SPXUSD 1m from histdata for SMT, with lag-0 correlation to NAS of 0.87-0.93. EURUSD 1m from histdata stands in for inverse DXY, because TVC:DXY 1m doesn't go back to 2025. Its timestamps check out: correlation with OANDA is 0.98, and its biggest move in Jan 2026 is at 08:30 NY. Window: 09:50 to 10:10 NY (15:50-16:10 SAST in US summer, 16:50-17:10 in winter), plus 09:50 to 11:10 NY (to 17:10 / 18:10 SAST). Sample: 446 weekdays. In-sample (IS) is 2025, 254 days. Out-of-sample (OOS) is 2026, 192 days. Script: `scripts/nas0950_direction.py`. Chart: `charts/nas0950_direction.png`. Tables: `data/nas0950_dir_*.csv`.

**Base rates:** price was up at 10:10 on 51.8% of days and up at 11:10 on 54.3%. The average absolute move was 55pt by 10:10 and 95pt by 11:10. News days (n=53) moved no more than other days, at 51pt vs 56pt.

**Single predictors** (20 predictors x 2 targets; hit = share of days where the predictor's sign matched the move's sign). None is significant in both halves.
| Predictor | 10:10 hit IS / OOS | 11:10 hit IS / OOS | Note |
|---|---|---|---|
| Toward nearest unswept PDH/PDL | 57.1% (n245, p=.03) / 53.0% | 55.7% / 49.7% | best single predictor; fades OOS |
| Price vs 08:30 open | 56.2% (p=.06) / 54.2% | 51.6 / 50.0 | weak, same sign in both halves |
| Gap at 09:30 (fade it) | 49.0 / 56.8 | 57.9% (p=.01) / 50.5% | IS only |
| Swept PDH/PDL (trade the reversal) | 54.7 / 51.8 | 56.6 (p=.09) / 48.9 | IS only |
| SMT NAS vs SPX at 09:50 | 36.8% (n57, p=.06) / 50.0% | 56 / 50 | small sample, flips |
| Daily bias (prior close vs midpoint) | 48.2 / 55.7 | 47.2 / 54.7 | no edge |
| EUR (inverse DXY) since midnight / 09:30-09:50 | 51 / 54 | 50 / 47-54 | no edge |
| 09:50-09:55 Judas push (trade from 09:55) | 51.4 / 50.0 | 46.9 / 51.6 | no edge, in either direction |
| Midnight, 09:30 and weekly open; overnight direction; premium/discount; ON and London sweeps; 09:30-09:50 high or low first; size of 09:30 move | all 47-55% | all 46-56% | no edge |

**Combos:** 2,280 tests of 2-factor and 3-factor agreement, about 2,320 tests in total. In-sample, 60 met n>=60 and p<.05, which is fewer than the ~115 you'd expect by chance alone. Only **1** held its direction OOS at p<.10: **price on the same side of the weekly open as the nearest unswept PDH/PDL** (long when price is above the weekly open and PDH is the nearer unswept level, and the mirror for shorts). It hit 61.9% IS (n84, p=.04) and 61.9% OOS (n63, p=.08) for the 09:50-10:10 move, an average of +22pt and +17pt. The other IS winners failed OOS, for example "08:30 open + unswept" went from 63.9% to 56.1%, and "weekly open + gap" went from 67.6% to 51.4%.

**As trades** (enter at the 09:50 open, exit by 11:10 at the latest, no spread; NAS spread is about 1-2pt):
| Rule | Stop / target | IS n, win, avgR, maxDD | OOS n, win, avgR, maxDD |
|---|---|---|---|
| Weekly open + unswept | 09:30-09:50 range extreme (min 10pt), 2R | 84, 50%, +0.14R, −3.4% | 63, 49%, +0.16R, −4.5% |
| same | range stop, 3R | 84, 48%, +0.08R, −3.4% | 63, 48%, +0.18R, −3.5% |
| same | fixed 40pt, 2R | 84, 44%, +0.24R, −4.2% | 63, 37%, +0.09R, −4.0% |
| same | fixed 40pt, 3R | 84, 43%, +0.35R, −4.5% | 63, 33%, +0.19R, −4.5% |
| 08:30 open + unswept | range stop, 2R | 119, 53%, +0.20R, −3.0% | 107, 46%, +0.05R, −7.3% |
| Weekly open + gap (to 11:10) | range stop, 3R | 74, 45%, −0.02R | 74, 47%, +0.20R |
Max DD is at 0.5% risk per trade. Wins include trades closed in profit at 11:10.

**Verdict:**
- Single predictors: **REJECTED**. The 09:50 direction is close to a coin flip on everything known by 09:50, including DXY (via EUR), SMT, the Judas push, sweeps and bias.
- Weekly open + nearest unswept PDH/PDL: **PROMISING**, not confirmed. It's positive in both halves, but OOS reaches only +0.16R to +0.19R, below the +0.3R bar, at n=63. It was picked out of about 2,320 tests, so luck can't be ruled out. Forward-test it before risking money.
