Updated: 2026-10-14 15:15 SAST (newest section at the bottom; first section written 09:50)
Probability Bot | London Open KZ, Wed 14 Oct 2026. First run (late; 07:36 routine not yet live).
Sources: time_patterns.md (backtests), review.md, setups.md, confluence.md, bias.md, timeframes.md, orderflow.md (all dated today). Fresh check: OANDA:NAS100USD 5m via tvDatafeed (nologin), 2026-09-18 to 2026-10-14 09:45 SAST. No prices invented. Small samples are flagged; nothing here is a trade instruction.

## Hilda's own record (review.md)
- n=1 logged trade (7 Oct XAUUSD short, +2.19R). 8-13 Oct not logged. **No personal base rate possible yet**; backfill from broker history.

## Base rates by instrument / kill zone (time_patterns.md, 1h, ~455 days)
| Inst | Day H or L forms in London KZ (08-11 SAST) | in NY AM KZ (13-15) | H/L in London or NY AM | Confirmed edge |
|---|---|---|---|---|
| NAS100 | H 7% / L 9% | H 7% / L 4% | 25% (15m: 27%, n=70) | none; HOD most often NY PM 19-22 (25%) |
| XAUUSD | 7% / 7% | 6% / 5% | 25% | bull-day LOD / bear-day HOD in Asia 00-06 SAST: 66% / 65% (CONFIRMED) |
| EURUSD | 13% / 12% | 10% / 11% | 42% (15m 54%) | none |
| GBPUSD | 14% / 15% | 9% / 12% | 44% (15m 44%) | none |
Read: for NAS, today's low 30519.6 (London) being the day's low is historically a ~9% bucket; most NAS lows are Asia/open (25%) or NY PM (17%).

## Base rates by setup (time_patterns.md)
| Setup | Sample | Win % | Expectancy | Status |
|---|---|---|---|---|
| London sweep+MSS+FVG, 2R min (all inst) | 37 fills, 5m 21d; 47 fills 15m 70d | 14% / 15% | **-0.14R / -0.28R** | REJECTED (NAS +1.57R on 8 fills = noise) |
| Silver Bullet 2R | 8-12 fills | 0-12% | -0.25R | REJECTED (too few) |
| XAU 07:00 NY 1m range sweep+MSS+FVG (NY AM) | 38 fills, 72d | 39% prox / 45% mid | **+0.31R / +0.50R** (spread: +0.19 to +0.43R) | positive; longs +0.63R (n=16), shorts +0.07R (n=22); Wed +0.36R (n=7); Thu -1.00R (n=8, flag) |
| EU vs GU London SMT (high side) | n=63 | 68% reversal >=0.5x Asia range | - | CONFIRMED |
| Asia sweep + 5m close-back -> opposite side by 11:00 | n=115 | 30% | - | vs control +12pp, low absolute |
| PDH/PDL sweep 13-16 SAST + close-back -> session mid | n=72 | 65% (against-bias 90%, n=20) | - | PROMISING |
| Bias-direction proxy | 204-217 days/inst | 44-49% correct | - | no better than chance |

## Scored: NAS100 Idea A LONG, COUNTER-TREND (confluence.md; limit 30576, stop 30517, target 30704; risk 59 / reward 128 = 2.17R; cancel 11:00 SAST)
Context: last 30614.8 (09:45 bar), 38.8 pts above the limit. Confluence 2/5 (down from 3). timeframes.md 4H bear in control, orderflow.md 1H bear, weekly bear retrace, daily neutral/lean bear, price in PREMIUM (~73%). Fill needs a break of 30585.5/30588.4, which setups.md reads as a bearish MSS.
1. **P(fill by 11:00): ~50%.** Analog: on 18 recent weekdays, price fell >=36 pts from the 09:40-09:45 close within 09:45-10:59 on 9 days (n=18; 29 pts: 10/18).
2. **P(target before stop | fill): ~20-30%.** Analog: of those 9 fills, +128 before -59 (to 18:00, conservative same-bar = stop) hit 2, stop 7 = **22% (n=9, very small)**. Driftless barrier model: 59/187 = **32%**. Break-even win rate at 2.17R = 31.5%.
3. **EV per fill: about -0.30R (analog) to ~0.00R (random-walk model).** Per order placed (x ~50% fill): about -0.15R to 0R. No positive edge shown; the closest tested setup (London sweep+MSS+FVG) is REJECTED at -0.14/-0.28R.
4. **Counter-trend caveat:** a fill here is itself the bearish MSS through 30585.5 against a 4H/1H bear — the fills that happen are the ones where sellers are winning, which is why the analog stop rate is high. The only support is bias.md's London Judas lean bull and the PDH/Asia-high draw (4/5 as a draw).
5. **Correlation:** same USD-soft / risk-on unit as EUR B3 (already filled). If B3 is on, Idea A is not a fresh 0.5%. DXY bouncing (102.114 -> 102.15) works against both.
**Score: 2/5 probability. Verdict: negative-to-flat expectancy; passes 1:2 on geometry only. If taken, it is COUNTER-TREND and should share B3's risk unit.** Upgrade only if a fresh raid near 30519.6 reclaims with a 5m close above 30629.6 (setups.md long trigger) and DXY loses 102.114.

## Disagreements
- confluence.md/bias.md treat Idea A as valid at 2.17R; base rates here say no demonstrated edge (EV <= 0). Flagged, not hidden.
- Analog n=9 is too small to overrule the model; treat 22% as a warning, not a rate.

## Data notes
- tvDatafeed nologin gives ~18 weekdays of NAS 5m; 5m bars cannot resolve intrabar order, so same-bar stop/target was scored a loss.

---
Updated: 2026-10-14 09:55 SAST

## Agreed gate conditions (team, 14 Oct)
- **NAS100 COUNTER-TREND long (Idea A) is valid only after a 15m close above 30677.** Until then it's NOT VALID. That fits the 2/5 score above. Note: a 15m close above 30677 leaves only ~27 pts to the 30704 target. The 30576 limit with a 30704 target would then need a pullback after the gate, so re-score the geometry once the gate is met.
- **Gold stays bearish unless there is a 15m close above 4170.5 or a 1H close above 4156.** Any gold long toward 4173.2 is a COUNTER-TREND scalp.
- **The DXY bearish read is off on a 1H close above 102.22.**

## Scored: XAUUSD Idea B / setups.md B1 SHORT, trend-aligned
Sell 4148.17, FILLED 09:37. Stop 4152.6 per confluence.md (setups.md uses 4152.4; risk 4.43 vs 4.23). TP1 4138.3 = 2.23R; runner 4131.8 (Fri low) = 3.70R. **US CPI is at 14:30 SAST, so the trade must be flat by 14:30.**
Status (OANDA 5m to 09:45): last 4148.78, high since fill 4148.98, low 4145.59. Neither stop nor target has been hit, so the trade is about -0.1R.
1. **P(fill): 100%** (already filled).
2. **P(TP1 before stop, by 14:30): ~31-33%.** On 18 recent weekdays (OANDA 5m, 2026-09-18 to 10-13), a short at the 09:35-09:40 close with a +4.43 stop and a -9.87 target reached the target first on 6 days and the stop first on 12. That gives **33% (n=18)**, with 0 timed out by 14:30. A same-bar touch of both was scored as a loss. A driftless barrier model gives 4.43/14.30 = **31%**. The break-even win rate at 2.23R is 31%.
3. **EV: about 0R to +0.08R** (analog 0.33x2.23-0.67 = +0.08R; model ~0R). Spread on a $4.4 stop (~$0.2-0.35) costs about 0.05-0.08R, so **net ≈ 0R**. The positive gold backtest in time_patterns.md (+0.31/+0.50R, n=38) is the NY AM 07:00 NY range model. It does **not** apply to this London entry. The tested London sweep+MSS+FVG model is REJECTED (-0.14R/-0.28R).
4. **Trend support:** M/W/D bear, the bearish gate is intact (price is well under 4156 1H and 4170.5 15m), DXY is bouncing from 102.114, and a 1H close above 102.22 would end the DXY bear read, which favours this short. Time patterns: on bear days gold's HOD forms in Asia 65% of the time (CONFIRMED, n=206). Today's Asia high is 4170.49, so that is consistent with a bear day.
5. **Caveats:**
   - Price is in daily DISCOUNT (~25%), so take TP1 and don't count on the runner.
   - London is a weak bucket for gold extremes (7%).
   - A sell-side sweep and reclaim of 4143.255 was logged, and the 1m bullish shift is the bounce risk.
   - A 5m close above 4149.06 is a 5m bullish MSS: exit early (matches setups.md's 4148.505 1m rule).
   - The trade is the same risk unit as the GBP B2 short.
   - **Hard flat at 14:30 SAST (CPI).** Any open runner is closed at market before then.
**Score: 3/5 probability. Trend-aligned, inside the bearish gate. Expectancy ≈ breakeven-to-slightly-positive (n=18). Manage it: TP1 4138.3, early exit on a 5m close above 4149.06, flat by 14:30.** Invalidation of the theme: a 1H close above 4156 or a 15m close above 4170.5.

---
Updated: 2026-10-14 10:10 SAST
Probability Bot | London Open KZ, Wed 14 Oct 2026. Kill-zone scoring run (10:07 fire).
Sources: setups.md 10:00, confluence.md 10:05, time_patterns.md, bias.md, live OANDA 5m via tvDatafeed (nologin) to 10:05 SAST. No prices invented. Small samples flagged.

## Outcome updates (already scored)
- **NAS100 Idea A LONG, COUNTER-TREND:** still NOT VALID. Gate (15m close >30677) unmet (10:00 15m close 30615.8; live 5m high 30651.4). Limit 30576 should stay cancelled. Prior score 2/5 / EV ≤0 unchanged.
- **XAUUSD Idea B / B1 SHORT:** CLOSED by exit rule (~−0.3R to −0.4R). Live 10:05 last 4153.34 / high 4153.96 traded through the 4152.015 raid high after the exit — hard stop 4152.6 would also have been at risk. Prior 3/5 score is historical only.
- **EURUSD B3 LONG, COUNTER-TREND:** STOPPED 09:55, −1R (never separately scored here; London sweep+MSS+FVG base rate REJECTED). Same USD-soft unit as Ping-Pong EU long (also −1R).

## Scored: GBPUSD B2 SHORT, COUNTER-TREND, London Open (setups.md; Charter M12)
Sell limit 1.32665, stop 1.32748, TP1 1.32538 / TP2 1.32480 / TP3 1.32390. Alerted 09:26, **still unfilled** at 10:05 (last 1.32638, high since 09:44 1.32644). Cancel if 1.32538 prints first, stop trades first, or 11:00 SAST. Flat before CPI 14:30 SAST.
Geometry: risk 8.3 pips. **TP1 = 1.53R (fails Hilda's 1:2 min)**; TP2 = 2.23R (passes); TP3 = 3.31R. ict_mentor safer stop ~1.32765 → TP2 only 1.85R (fails 1:2) / TP3 2.75R — if using the safer stop, target must be TP3.
1. **P(fill by 11:00): ~60-80%.** Live: only ~2.7 pips to the limit, ~10 pips to the cancel. Analog on 18 recent weekdays (OANDA 5m, Sep 14–Oct 7): from a 10:05-like close, +2.7 pips before −10 pips by 11:00 filled **14/18 = 78%**. At the earlier 7.5-pip gap it was only 28% (cancel won). Price has rallied into the limit, so fill is now likely if the order is still working.
2. **P(TP2 before stop | fill): ~31-36%.** Analog on those 14 fills (manage to 14:30, stop-before-target on same bar): TP2 5, stop 8, timeout 1 = **36% (n=14, small)**. Driftless barrier: 8.3/(8.3+18.5) = **31%**. Break-even at 2.23R = 31%. TP3 analog was 0/14 hits before stop/timeout — do not lean on the runner.
3. **EV per fill: about 0R to +0.15R** (driftless ~0R; analog 0.36×2.23−0.64 ≈ +0.15R). Per order placed (× ~78% fill): about 0R to +0.12R. **The tested London sweep+MSS+FVG model (this setup's family) is REJECTED at −0.14R / −0.28R.** Counter-trend Ping-Pong bucket was only +0.06R. No demonstrated edge beyond noise.
4. **COUNTER-TREND:** fights bias.md GBP BULL and timeframes.md 4H/1H bull. Agrees with live dollar bid (earlier) and weak EU/GU high-side SMT (EUR barely took Asia high 1.12114 > 1.12112; GBP London high 1.32728 did not take Asia high 1.32750 — SMT-high CONFIRMED base rate 68% n=63 for ≥0.5×Asia-range drop). DXY has since slipped 102.205 → 102.151 (10:05), so the dollar-bid support is softer than at 10:00.
5. **Correlation / risk:** gold B1 (same USD-bid unit) is closed, so a B2 fill takes a **full 0.5%**. London KZ so far: EUR B3 −1R, gold B ~−0.3R to −0.4R.
6. **Caveats:** TP1 is a partial only, not a 1:2 target. Prefer stop beyond Asia/day high pool (~1.32765) and then require TP3 for 1:2. Cancel at 11:00 or if 1.32538 prints unfilled. Hard flat before 14:30 CPI.
**Score: 3/5 probability. COUNTER-TREND. Passes 1:2 only at TP2 (setups stop) or TP3 (safer stop). Fill likely; expectancy ≈ breakeven on base rates (REJECTED family model). Small analog n=14 — treat +0.15R as noise, not an edge.**

## Disagreements
- confluence.md holds B2 at 3/5 structure; base rates here say no positive expectancy after the REJECTED London M12 family. Score matches on the 3/5 label, not on edge.
- Analog fill 78% assumes the 10:05 geometry holds; a dip back through 1.32590 re-opens the cancel race.

## Data notes
- GBPUSD 5m analog window: 18 weekdays ending 2026-10-07 (older pickle). Live path from tvDatafeed 10:05 bar.

---
Updated: 2026-10-14 10:15 SAST

## Scored: Scalp Bot S18 + S19 (alerted 10:09). Both COUNTER-TREND, one soft-dollar 0.5% unit (opposite of GBP B2)
Data: OANDA 5m via tvDatafeed, to the 10:10 bar. Analog = an entry at the 10:05-10:10 close on 18 recent weekdays (2026-09-18 to 10-13), with the same stop/target distances, run to 14:29. A same-bar touch of both is scored as a loss.

### S18 NAS100 LONG COUNTER-TREND: entry 30627.4-30638.6 (pref ~30633), stop 30623.5, target 30704.7 (~7.5R)
- **Fill: NOT filled as of 10:10.** The 10:10 bar is last 30666.6 (high 30668.0), so it needs a ~30-pt pullback. The zone traded before the alert (low since 09:55 was 30604.4).
- **P(target before stop): ~6-12%.** Analog: target 1, stop 17 = **6% (n=18)**. Barrier model 9.5/81.2 = 12%. Break-even at 7.5R = 12%.
- **EV: about -0.5R (analog) to ~0R (model).** The 9.5-pt stop is about the same size as a 5m bar, so noise takes most fills.
- Gate: Idea A needs a 15m close above 30677, which has not happened yet. S18 is not bias-gated (Scalp rule), but it is still COUNTER-TREND vs 4H bear.

### S19 XAUUSD LONG COUNTER-TREND: entry 4151.36-4151.91, stop 4143.0, target 4173.2 (~2.5R)
- **Fill: NOT filled as of 10:10.** Last 4152.85, about 1 above the zone (range since 09:55: 4147.98-4153.96). A fill is likely on any small dip.
- **P(target before stop by 14:30): ~22-28%.** Analog: target 4, stop 13, flat 1 = **22% (n=18)**. Barrier model 8.6/30.2 = 28%. Break-even at 2.5R = 29%.
- **EV: about -0.2R (analog) to ~0R (model).**
- **Gate conflict:** gold stays bearish until a 1H close above 4156 or a 15m close above 4170.5. Neither has happened, so S19 runs into the bearish gate. The 4173.2 target sits **above** 4170.5, so it needs the gate to flip. **S19 is the direct opposite of the live Idea B / B1 short (4148.17).** They should not both be held: B1's early-exit rule (a 5m close above 4149.06) fires before S19 would make sense. Price at 4152.85 is already above that level, so B1 should be checked now.

### Shared
- **CPI cut: both must be flat by 14:30 SAST**, filled or not. Cancel unfilled orders at 14:15.
- **Unit:** S18 and S19 together = ONE soft-dollar 0.5% unit (split, e.g. 0.25% each), opposite to GBP B2 (long dollar, unfilled). The DXY high of 102.205 (10:00) did not take 102.207, so the soft-dollar read holds while the 1H stays under 102.22.
- **Ping-Pong EUR OTE long: STOPPED, -1R.** It is the same unit as B3. B3 is still open on that unit, so the soft-dollar theme has already lost 1R today. Adding S18/S19 adds to that same exposure.
- **Verdict:** S18 2/5 and S19 1/5. Neither has shown positive expectancy, and both are COUNTER-TREND.

---
Updated: 2026-10-14 10:20 SAST

## Scored: Ping-Pong XAUUSD LONG (UNPROVEN, COUNTER-TREND), scored together with S19 as ONE soft-dollar 0.5% unit
Setup: buy limit 4148.05 (IFVG), stop 4142.755, target 4163.905 (London high) = 3.0R. Context: London swept the Asia low 4144.455 to 4143.26 (09:15); the 10:05 MSS closed at 4153.82. Valid to ~11:00 SAST. Ping-Pong's IFVG backtest: ~+0.03R (OANDA).
- **Fill: NOT filled.** At the 10:10 bar, last was 4152.435, 4.4 above the limit; the low since 10:05 is 4150.46.
- **P(fill by 11:00): 61%.** Analog: a 4.4 dip from the 10:10 close by 11:00 happened on 11 of 18 days.
- **P(target before stop | fill): 0% analog (0/11, n tiny) to 25% (driftless model 5.295/21.15).** Break-even at 3.0R is 25%.
- **EV: about -1.0R (analog) to ~0R (model).** The team's IFVG evidence is also weak: time_patterns.md has IFVG entries at -0.08R (n=14), and Ping-Pong's figure is +0.03R.
- **Gate:** the bearish gate is intact. Its 4163.905 target is BELOW 4170.5 and 4156 is on the path, so it can pay without a full gate flip (S19's 4173.2 can't). It is still COUNTER-TREND against M/W/D bear and directly opposite live short B1.

## Unit view: S19 vs Ping-Pong gold long (one 0.5% soft-dollar unit; opposite GBP B2)
| | S19 | Ping-Pong |
|---|---|---|
| Entry / stop / target | 4151.36-4151.91 / 4143.0 / 4173.2 | 4148.05 / 4142.755 / 4163.905 |
| R:R | 2.5 | 3.0 |
| P(fill) | near price, likely | 61% (n=18) |
| P(target first) analog / model | 22% (n=18) / 28% | 0% (n=11) / 25% |
| Break-even | 29% | 25% |
| EV | -0.2R to 0R | -1.0R to 0R |
**If only one is taken: S19** (its replay result is less bad, and it has a wider stop under the 4143.26 sweep low). The Ping-Pong entry has the better price and the better gate-friendly target, but in the 11 replay fills, every 4.4 dip carried on to the stop. **Do not take both** (it's one unit). Neither shows positive expectancy. Scores: S19 1/5, Ping-Pong 1/5.
- **CPI: flat by 14:30 SAST.** Ping-Pong expires ~11:00 anyway.
- The soft-dollar theme is already -1R today (Ping-Pong EUR OTE stopped).

---
Updated: 2026-10-14 10:19 SAST
Probability Bot | kill-zone scoring run (10:18 fire). **No new setups since the 10:20-stamped section above**; status changes only. Live OANDA/TVC 1m via tvDatafeed (nologin) to the 10:18 bar. Analogs use the 7 weekdays available in the 5m feed (n=7, very small, direction only).

## Status changes (already-scored setups)
- **S18 NAS100 LONG COUNTER-TREND: NOT filled for anyone acting on the 10:09 alert.** Lowest low after 10:09 is 30642.6, above the zone top 30638.6. scalps.md (10:15) marks it FILLED on the 10:07 retest, but that came before the alert. Flagged as a disagreement. Last 30665.7, high 30675.0. A fill now needs a ~27-pt pullback. Analog: a 27-pt dip from the 10:15 close before 11:00 happened 5/7 days, so a late fill stays likely. The prior score holds: 2/5, EV about -0.5R to 0R, and the 9.5-pt stop is within 5m noise. Gate: the 10:15 15m bar high is 30675.0, still under 30677.
- **S19 XAUUSD LONG COUNTER-TREND: FILLED 10:10** (low 4151.625 in the 4151.355-4151.910 FVG). Last 4155.86, high 4157.875, about +0.5R open. From here the target 4173.2 is 17.3 away and the stop 4143.0 is 12.9 away. Driftless barrier model: **43%** target first. Analog to 14:30: target 1, stop 5, flat 1 (n=7). Score stays 1/5, but the gate matters now: **a 1H close above 4156 at 11:00 SAST lifts the team's bearish gold read**, and it is 0.1 under that level right now. If the 1H closes above 4156, re-label S19 from COUNTER-TREND to gate-neutral. If not, it stays COUNTER-TREND. Flat by 14:30 (CPI).
- **Ping-Pong XAU LONG (limit 4148.05): fill odds are falling.** The low since the alert is 4151.625. Price is 7.8 above the limit and 8.05 under the 4163.905 target, and a target print before the fill voids it. Analog by 11:00: fill 3, target first 1, neither 3 (n=7), so **P(fill) is about 40%, down from 61%.** Still 1/5, one unit with S19, and since S19 is filled this order should be cancelled so the unit isn't doubled.
- **GBPUSD B2 SHORT COUNTER-TREND:** still unfilled. High since the alert is 1.32644, last 1.32641, 2.4 pips from the 1.32665 limit. The score is unchanged (3/5, EV about breakeven, 1:2 met only at TP2/TP3). DXY is soft at 102.164 (no 1H close above 102.22), which removes the dollar-bid support. A fill would oppose the open S19 soft-dollar unit. Cancel at 11:00.

---
Updated: 2026-10-14 10:43 SAST
Probability Bot | kill-zone scoring run (10:40 fire, 04:40 NY). Sources: setups.md 10:38, pingpong.md 10:35, scalps.md 10:36, confluence.md 10:31, time_patterns.md, bias.md. Live OANDA/TVC 1m + 5m via tvDatafeed (nologin) to the 10:40 closed 1m bar. Analog = same stop/target distances from the matching 5m close on 17-18 prior weekdays (2026-09-18/21 to 10-13), run to 14:29 (CPI cut); same-bar touch of both = loss. Small n, direction only. Scripts: data/prob/analog_1040.py, score_1040.py.

## Live at 10:40
NAS 30622.8 (low 30620.0 @10:39) | XAU 4144.94 (low 4144.02 @10:37) | EUR 1.11974 (low 1.11972) | GBP 1.32588 | **DXY 102.209, high 102.212 @10:41: the 102.207 Asia high is TAKEN.** A 1H close above 102.22 at 11:00 switches off bias.md's DXY bear read. Dollar is bid against every open soft-dollar long.

## Outcome / status updates
- **B10 NAS100 SHORT COUNTER-TREND: TP1 30624.0 HIT 10:39 (low 30620.0), +2.4R.** Stop 30655.5 never traded (high after fill 30651.8).
- **B7 NAS long / Scalp S18 NAS long COUNTER-TREND: STOPPED 10:39, -1R.** Stop 30623.5 traded (30620.0). Same print paid B10. Net NAS for anyone who held both = +1.4R minus costs.
- **Ping-Pong XAU long COUNTER-TREND (limit 4148.05): FILLED 10:36** (low 4144.545). Now about -0.6R; stop 4142.755 is 2.2 away, target 4163.905 is 18.9 away. Analog to target first 3/18 = 17%, barrier 10%. Score stays 1/5. Directly opposite B9.
- **S19 / B8 XAU long: closed 10:29, about -0.15R** (no change).
- **B5 EURUSD LONG COUNTER-TREND: open, about -0.9R.** Low 1.11972 vs stop 1.11968 (0.4 pip). From here: 0/17 analog reached TP1 1.12114 before a 0.6-pip adverse move; barrier 4%. Effectively a -1R trade unless DXY rejects 102.21 now.

## Scored: setups.md B9 XAUUSD SHORT, trend-aligned (NEW)
Sell limit 4152.65 (5m FVG CE), stop 4158.2 (risk 5.55), TP1 4138.3 = **2.59R** (passes 1:2), TP2 4131.8 = 3.8R. Cancel: stop first, TP1 first, or 11:00.
1. **P(fill by 11:00): ~17%.** Price 4144.94 is 7.7 below the limit and only 6.6 above TP1. Analog from the 10:35 close: up 7.7 first 3, TP1-side first 3, neither 12 (n=18). Most likely outcome is cancel unfilled.
2. **P(TP1 before stop | fill): ~28-44%.** Analog short with these distances: 8 TP / 8 stop / 2 flat from the 10:15 close; 7 / 9 / 2 from 10:45 (n=18). Barrier 5.55/19.9 = 28% = break-even at 2.59R.
3. **EV per fill: ~0R (model) to +0.5R (analog, small n, reflects gold's recent down-drift).** Per order placed (x ~17% fill): about 0 to +0.1R.
4. With bias.md M/W/D bear and the gate (no 1H close >4156); bear-day gold HOD forms in Asia 65% (CONFIRMED; today's Asia high 4170.49). DXY bid agrees. Caveat: daily discount ~25%, London family model (sweep+MSS+FVG) REJECTED -0.14/-0.28R.
**Score: 3/5 quality, trend-aligned; fill unlikely (~17%). If it fills, the open Ping-Pong XAU long must go (opposite sides of one instrument).**

## Scored: setups.md B10 NAS100 SHORT, COUNTER-TREND (NEW, already paid)
Entry 30646.2, stop 30655.5 (9.3), TP1 30624.0 = 2.39R / TP2 30604.4 = 4.5R / TP3 30588 = 6.3R.
- At-entry analog (10:30 close, n=18): TP1 first 8, stop 10 = 44%; barrier 30%; break-even 29.5%. EV +0.5R analog / 0R model. COUNTER-TREND vs London intraday bull, with 4H bear and the shut 30677 gate.
- **Result: TP1 hit 10:39, +2.4R.** Runner to TP2 30604.4 is 4.5R from entry; stop to entry after TP1.
**Score: 3/5 (retro). Small n; one win is not an edge.**

## Scored: setups.md B6 GBPUSD LONG, bias-aligned (NEW to this file; filled ~10:11)
Entry 1.32612, stop 1.32563 (4.9 pips), TP1 1.32728 = 2.37R (passes), TP2 2.9R, TP3 5.0R.
- At-entry analog (n=17): 5 TP / 12 stop = 29%; barrier 30%; break-even 30%. **EV ≈ 0R.**
- Now 1.32588, about -0.5R. From here: TP1 first 3/17 = 18%, barrier 15%.
**Score: 2/5. With GBP daily bull, but DXY just took 102.207.**

## Scored: Ping-Pong GBPUSD LONG IFVG (NEW; alerted 10:28, FILLED 10:36, low 1.32590)
Entry 1.32598, stop 1.32558 (4.0), target 1.32728 = 3.25R (passes). UNPROVEN, with GBP daily bull, against 15m BOS down.
- At-entry analog (10:35 close, n=17): 4 / 13 = 24%; barrier 23.5%; break-even 23.5%. **EV ≈ 0R.** Ping-Pong GU backtest 8-14 Oct: n=4, all -1R (worst instrument).
- Now 1.32588, about -0.25R. TP first 3/17 = 18%.
**Score: 1/5. Same trade as B6 (stops 0.5 pip apart, same target): treat as a duplicate, not a second position.**

## Scored: setups.md B5 EURUSD LONG, COUNTER-TREND (NEW to this file; filled 10:33)
Entry 1.12016, stop 1.11968 (4.8), TP1 1.12114 = 2.04R (passes, barely), TP2 3.25R.
- At-entry analog (n=17): 6 / 11 = 35%; barrier 33%; break-even 33%. EV ≈ 0 to +0.06R.
- Now 0.4 pip from the stop (see above).
**Score: 1/5. COUNTER-TREND vs monthly/4H bear; second EUR long today after B3 -1R.**

## Risk units (team rule, same dollar direction = one 0.5%)
- **Soft-dollar unit OPEN: B5 EUR long + B6 GBP long + Ping-Pong GBP long + Ping-Pong XAU long.** All four are under water as DXY takes 102.207. Today the soft-dollar side is already -1R (B3) -1R (PP EUR) -1R (S18/B7) -0.15R (S19/B8).
- **Dollar-bid unit:** B10 (TP1 banked) + B9 (pending). Holding both clusters is a hedge.

## Disagreements
- confluence.md (10:31) still lists the gold long zone 3/5 and B6 2/5 live; the 5m reclaim it was built on failed at 10:29, and the Ping-Pong limit filled on the way down.
- B9 analog EV (+0.5R) leans on 18 days of gold down-drift; the barrier model says breakeven. Don't read it as an edge.

---
Updated: 2026-10-14 10:48 SAST

## Status: Ping-Pong longs FILLED on the 10:35 bar (per Ping-Pong)
- XAU long 4148.05: about -0.5R at the fill report. GBPUSD long 1.32598: about flat. They are the soft-dollar side, together with B3 (EUR); the EUR OTE was already stopped at -1R. Gold long vs live gold short B1 = offsetting exposure.

## Scored: Ping-Pong NAS100 SHORT (Unicorn): sell limit 30651.8, stop 30677.0, target 30519.6 = 5.25R, window to ~11:35 SAST. Time Pattern: PROMISING
- **Trend: WITH the trend.** 4H bear (timeframes.md), 1H bear (orderflow.md), weekly bear retrace, daily lean bear. It is against bias.md's London lean bull only. The 15m 30677 gate agrees: there has been no 15m close above 30677, so the NAS long is still invalid and the stop sits just above that gate.
- **Fill: NOT filled since the 10:41 alert.** The 10:29/10:35 1m highs printed exactly 30651.8 before the alert/MSS; I don't count those. The 10:30 high was 30654.6 (pre-MSS). Last was 30612.5 at 10:44, 39 pts under the limit.
- **P(fill by 11:35): ~28%.** Analog: a 36-pt rally from the 10:40 close by 11:35 happened on 5 of 18 days.
- **P(target before stop | fill): 0/5 analog (stop 4, flat 1; n tiny) vs 16% driftless model (25.2/157.4).** Break-even at 5.25R = 16%.
- **EV per fill: about -0.8R (analog) to ~0R (model).** Per order ≈ -0.2R to 0R. A 25-pt NAS stop is only about 2-3 5m bars of noise, and 132 pts to the London low before 14:30 is a long way (the day so far has ranged ~155 pts).
- **CPI: flat by 14:30 SAST.** Any open position is closed at market even if it is between stop and target.
- **Unit:** short NAS = risk-off / long-dollar side, the opposite of S18 and the Ping-Pong XAU/GU longs. It partly hedges them; it is not a fresh independent edge.
- **Score: 2/5.** Trend-aligned and gate-consistent, but unlikely to fill and with no measured edge.

---
Updated: 2026-10-14 10:48 SAST
Probability Bot | kill-zone scoring run (10:47 fire, 04:47 NY). New since last run: confluence.md 10:46 Trade idea C. setups.md 10:43, scalps.md 10:44 and pingpong.md 10:40 have nothing new beyond what is scored above. Live OANDA/TVC 1m + 5m via tvDatafeed (nologin) to the 10:47 1m bar. Analog = same distances from the matching 5m close on 18 prior weekdays (2026-09-21 to 10-13), run to 14:29 (CPI cut); same-bar touch of both = loss. Small n, direction only. Script: data/prob/score_1050.py.

## Live at 10:47
NAS 30606.8 (low 30602.6) | XAU 4143.955 (low 4143.015, day low 4143.255 now traded) | EUR 1.11974 | GBP 1.32594 | DXY 102.213 (high 102.219). The 102.22 1H-close gate is decided at 11:00 SAST.

## Scored: confluence.md Trade idea C NAS100 SHORT (NEW; same entry/stop as Ping-Pong NAS short, adds TP1)
Sell limit 30651.8, stop 30677.0 (25.2), **TP1 30585.5 = 2.63R (passes 1:2)**, TP2 30519.6 = 5.25R. Cancel if TP1 prints first, 30677 trades first, or 11:35 SAST. Flat by 14:30 (CPI).
1. **P(fill by 11:35): ~6%.** Price is 45 pts under the limit and only 21.3 pts above TP1. Analog from the 10:40 close: rally 45 first 1, TP1-side first 11, neither 6 (n=18). Most likely outcome is a cancel when 30585.5 prints. Not filled since the 10:41 alert (high since 30623.8).
2. **P(TP1 before stop | fill): ~28% model; analog 56% unconditional (10/18) but 0/5 for the fills that follow a rally (see the 10:48 section).** Break-even at 2.63R = 27.5%.
3. **EV per fill: ~0R (model)**; the +1.0R unconditional analog overstates it, because a fill needs a 45-pt rally against the trade. Per order placed (x ~6% fill): ~0R.
4. Trend: with 4H/1H/15m/5m bear (orderflow.md 10:47 has NAS back to bearish on all of them) and the shut 30677 gate. confluence.md labels it COUNTER-TREND to bias.md's London lean bull; with the higher timeframes it is trend-aligned.
5. **Unit:** it's the same trade as the Ping-Pong NAS short, so one position, not two. It's on the dollar-bid side with the B10 runner and B9.
**Score: 2/5 (same as the Ping-Pong version). TP1 makes the 1:2 check easier, but the fill is very unlikely and no measured edge.**

## Status updates
- **B5 EURUSD long COUNTER-TREND: STOPPED 10:42, -1R** (low 1.11960 vs stop 1.11968).
- **Ping-Pong XAU long COUNTER-TREND: open, about -0.85R.** The 4143.255 day low has traded (4143.015); the stop 4142.755 is 0.26 away.
- **B9 XAU short: unfilled** (high since 10:30 4151.075 vs 4152.65); price is 5.7 above TP1. Cancel at 11:00 is likely.
- **B6 / Ping-Pong GBP long (one position): open, about -0.4R / -0.1R**, low 1.32584, stops untouched.
- **B10 NAS short runner:** last 30606.8, about +4.2R from entry; TP2 30604.4 is 2.4 pts away.
- Soft-dollar side today: B3 -1R, PP EUR -1R, S18/B7 -1R, S19/B8 -0.15R, B5 -1R; PP XAU and B6/PP GU still open.

---
Updated: 2026-10-14 13:05 SAST
Probability Bot | kill-zone scoring run (13:02 fire, 07:02 NY, first NY AM slot). **No new setups since 10:48.** Changed files checked: setups.md 10:58 ("No new setups"), confluence.md 10:58 (no new idea), pingpong.md 11:01 ("No new alertable setups"), scalps.md 12:40 (nothing open), liquidity.md 12:53, intermarket.md 12:59, bias.md 13:01 (gate changes only). Live OANDA/TVC 1m via tvDatafeed (nologin), 09:44-13:03 SAST bars. Script: data/prob/fetch_1305.py. Status only; no new scores. No alert sent.

## Live at 13:03
NAS 30533.6 (low since 11:00 30531.8; 30519.6 not broken) | XAU 4136.365 (low 4136.135) | EUR 1.11886 (low 1.11878) | GBP 1.32612 | DXY 102.264 (high 102.266).

## Outcome updates (already-scored setups)
- **B10 NAS100 SHORT, COUNTER-TREND: TP3 30588 HIT 11:24 (~+6.3R on that portion).** Stop 30655.5 never traded. Note: a trail above the 30612.0/30609.5 highs (management option) would have been taken at 11:04 (high 30622.0 at 11:18) before TP3.
- **Idea C / Ping-Pong NAS100 SHORT 30651.8: CANCELLED unfilled.** TP1 30585.5 printed 11:24 before a fill (high 10:46-11:35 = 30622.0). Matches the ~6% fill score.
- **B9 XAUUSD SHORT 4152.65: CANCELLED unfilled at 11:00** (high since alert 4146.175). TP1 4138.3 printed only at 13:02, after the cancel.
- **Ping-Pong XAUUSD LONG, COUNTER-TREND: STOPPED 10:51, −1R** (low 4142.545 vs stop 4142.755).
- **B6 = Ping-Pong GBPUSD LONG (one position): still OPEN.** Low since 10:35 fill 1.32583, high 1.32694; stops 1.32563 / 1.32558 and TP1 1.32728 untouched. Mark: B6 ≈ 0R (entry 1.32612), Ping-Pong ≈ +0.35R (entry 1.32598).
  - Re-check (geometry unchanged, context worse): driftless barrier for TP1 before stop from 1.32612 = 4.9/(4.9+11.6) ≈ **30%** (B6) and 5.4/17.0 ≈ **32%** (Ping-Pong). Break-even at 2.4R ≈ 29%, so EV ≈ 0R. bias.md 13:01 / intermarket.md 12:59 now read DXY bid (1H closes 102.225 / 102.227 above the 102.22 gate) and EUR long off, so the soft-dollar side has lost its support; GBP's refusal to follow DXY (SMT) is the only thing holding it. **Score stays 3/5 at best, leaning 2/5. Must be flat before US CPI 14:30 SAST.**

## Gate changes (bias.md 13:01, not yet verified on a 1H close)
- DXY bear read suspended; bull toward 102.37 / 102.574 above 102.22, bear back below 102.207.
- EURUSD COUNTER-TREND long off (broke 1.1188); long only back above 1.1198.
- XAUUSD bear confirmed; draws 4131.8, then 4103.4. NAS long on hold; below 30519.6 the draw is 30401.2.

## Base-rate reminders for NY AM (time_patterns.md)
- XAU 07:00 NY (13:00 SAST) 1m range sweep+MSS+FVG: +0.31R / +0.50R (n=38); Wed +0.36R (n=7); longs +0.63R, shorts +0.07R. **CPI at 14:30 SAST cuts the window short today.**
- PDH/PDL sweep 13-16 SAST + close-back to session mid: 65% (n=72), against-bias 90% (n=20), PROMISING.
- London sweep+MSS+FVG and Silver Bullet remain REJECTED.

---
Updated: 2026-10-14 13:14 SAST

## Scored: Idea D = Scalp S20, XAUUSD SHORT, WITH the trend: sell limit 4139.19, stop 4142.60 (risk 3.41), TP1 4131.8 (2.17R), runners 4125 / 4105.5. Cancel unfilled 14:15, flat by 14:25 (CPI 14:30)
- **Live OANDA 1m:** the 13:12 bar (forming) is at 4139.89 (high 4140.36). The 13:11 bar's high of 4139.475 traded through the limit, so it is **FILLED (touched 13:11)** if the order was live by then. Mark: about -0.2R. Range since 12:30: 4136.025-4145.42.
- **P(fill before 14:15): ~100%** (already touched).
- **P(TP1 before stop by 14:25): 33% analog** (a short at the 13:05-13:10 5m close with the same distances: TP1 5, stop 10 out of **n=15** usable days of 18, 0 flat; a same-bar touch of both = loss) **vs 32% driftless model** (3.41/10.80). **Break-even at 2.17R = 31.5%.**
- **EV: gross +0.06R (analog) to ~0R (model).** Spread of $0.20-0.35 on a $3.41 stop costs ~0.06-0.10R, so **net ≈ -0.05R to 0R.** Runners (4125/4105.5) are unlikely before 14:25; don't count on them.
- **Caveats:**
  - **The 3.4-pt stop is about one 5m bar of gold noise.** A wick or spread widening into CPI can stop it out without any change in structure.
  - Gold is in deep daily discount (~25%).
  - The trade fights the open Ping-Pong XAU long (4148.05) and adds to B1 if B1 is still open: same long-dollar unit as B2/NAS short.
  - The bearish gate is intact (no 1H close above 4156, no 15m close above 4170.5): trend-aligned.
- **Score: 2/5.** With the trend, but break-even after costs, and the stop is too tight for pre-CPI gold.

---
Updated: 2026-10-14 13:23 SAST
Probability Bot | kill-zone scoring run (13:21 fire, 07:21 NY). New since last run: scalps.md **S21** XAU long (alerted 13:19); S20/Idea D stopped −1R. setups.md 13:18 no new Entry Model setup; pingpong.md 13:21 no new alertable setups; confluence.md 13:11 Idea D already scored at 13:14. Live OANDA/TVC 1m + XAU 5m via tvDatafeed (nologin) to the 13:22 1m / 13:20 5m. Analog = same distances from the matching 5m close on 18 prior weekdays (2026-09-18 to 10-13), run to 14:25 (pre-CPI); same-bar touch of both = loss. Small n, direction only. Pickles: data/prob/*_1m_1321.pkl, XAUUSD_5m_1321.pkl.

## Live at 13:22
NAS 30566.8 | XAU 4141.65 (day/NY low 4136.025) | EUR 1.11939 | GBP 1.32635 | DXY 102.238 (off day high 102.271).

## Outcome updates (already-scored setups)
- **Idea D / S20 XAUUSD SHORT: STOPPED 13:18, −1R.** Filled 13:11 at 4139.19; stop 4142.60 traded on the 13:18 bar (high 4142.820). TP1 4131.8 never reached (post-fill low stayed the pre-fill day low 4136.025). Prior 2/5 / ~0R score is historical only.
- **B6 / Ping-Pong GBPUSD LONG: still OPEN.** Last 1.32635 ≈ +0.5R (B6 from 1.32612) / ≈ +0.9R (PP from 1.32598). Stop 1.32563 / 1.32558 and TP1 1.32728 untouched. Soft-dollar unit still live into USD-bid / CPI — flat by 14:30.

## Scored: Scalp S21 XAUUSD LONG, COUNTER-TREND (NEW; alerted 13:19)
Buy limit **4139.94** (CE of 1m bull FVG 4138.940–4140.935 after sweep of 4136.025 @13:06 and bullish 1m MSS @13:16 through 4141.53). Stop **4135.70** (risk **4.24**). TP1 **4157.9** = **4.2R**; TP2 4163.9 = 5.7R; TP3 4175 = 8.3R. Cancel unfilled 14:15; if filled, flat by 14:25 (CPI 14:30). Status @13:22: **UNFILLED** (low since alert 4140.05, ~0.11 above the limit).
1. **P(fill by 14:15): ~67-72%.** From the 13:15/13:20 area, a dip of ~1.7 before a run of ~16 to TP1 printed first on **13/18** days (72%); before a ~5.6 fail-reclaim move on **12/18** (67%). n=18, small.
2. **P(TP1 before stop | fill, by 14:25): ~17% analog / ~19% barrier.** Same distances from the 13:15 5m close: TP1 3, stop 8, neither 7 (**17%**, n=18). Resolved-only 3/11 = 27%. Driftless barrier 4.24/(4.24+17.96) = **19%**. Break-even at 4.2R ≈ **19%**. TP2 before stop: 1/18 (6%) — do not count on runners before CPI.
3. **EV per fill: about −0.12R (analog 17%) to ~0R (barrier).** Spread on a $4.24 stop (~$0.2–0.35) costs ~0.05–0.08R, so **net ≈ −0.15R to −0.05R.** Per order placed (× ~70% fill): about −0.10R to −0.04R.
4. **COUNTER-TREND:** fights bias.md / liquidity HTF bear and timeframes M→5m bear alignment. The closest positive base rate is the XAU 07:00 NY 1m range sweep+MSS+FVG model (+0.31R/+0.50R, longs +0.63R, Wed +0.36R) — structurally similar, but that sample is not a 4-pt stop into a CPI cut, and today's bearish gate (no 1H close >4156, no 15m >4170.5) is still intact.
5. **Units:** soft-dollar with open B6/PP GU long — **same 0.5% soft-dollar unit**, not a fresh risk add. Opposite of the just-stopped S20 dollar-bid short.
**Score: 2/5 probability. COUNTER-TREND. Passes 1:2 on geometry (4.2R). Fill likely; expectancy flat-to-slightly-negative after costs. Small n. Must be flat by 14:25 if filled.** Upgrade only if DXY loses 102.207 with a 1H close and the bearish gold gate breaks.

## Disagreements
- scalps.md alerts S21 as valid 1:4.2; base rates here show no positive expectancy into CPI with a tight stop. Flagged, not hidden.
- Gold 2.0 log (13:18) said NO_SETUP (no fresh bull FVG to retrace); Scalp Bot used a different 1m FVG (4138.940–4140.935) — noted.

## Data notes
- tvDatafeed nologin ~18 weekdays of XAU 5m; 5m cannot resolve intrabar order (same-bar = loss).

---
Updated: 2026-10-14 13:35 SAST
Probability Bot | kill-zone scoring run (13:34 fire, 07:34 NY). New since last run (13:21): setups.md **B11** / scalps.md **S22** NAS100 SHORT (alerted 13:29/13:31; one unit). S21 already scored at 13:23 — fill/status only. pingpong.md 13:26–13:31 no new alertable setups; confluence.md 13:31 notes S21 fill. Live OANDA/TVC 1m + NAS 5m via tvDatafeed (nologin) to the 13:34 1m / 13:30 5m. Analog = same distances from the matching 5m close on 18 prior weekdays (2026-09-18 to 10-13), run to 14:25 (pre-CPI); same-bar touch of both = loss. Small n, direction only. Pickles: data/prob/*_1m_1334.pkl, NAS100USD_5m_1334.pkl.

## Live at 13:34
NAS 30569.0 (NY AM high now 30579.6 @13:33; day/London low 30519.6 untouched) | XAU 4140.07 | EUR 1.11920 | GBP 1.32594 | DXY 102.254.

## Outcome updates (already-scored setups)
- **S21 XAUUSD LONG, COUNTER-TREND: FILLED 13:24** at 4139.94 (1m low 4139.51). Stop 4135.70 untouched (post-fill low 4138.585 @13:28). Last 4140.07 ≈ +0.03R. TP1 4157.9 untouched. Prior score 2/5 / EV flat-to-slightly-negative holds. Soft-dollar unit with open B6/PP GU. Flat by 14:25 (CPI).
- **B6 / Ping-Pong GBPUSD LONG: still OPEN.** Last 1.32594 ≈ −0.4R (B6 from 1.32612) / ≈ −0.1R (PP from 1.32598). Stop 1.32563 / 1.32558 and TP1 1.32728 untouched. Flat before 14:30 CPI.

## Scored: setups.md B11 = Scalp S22, NAS100 SHORT, bias-aligned (NEW; already closed)
Sell limit **30562.05** (CE of 1m bear FVG 30560.6–30563.5 after buy-side raid 30576.2 @13:17 and 1m MSS @13:21). Stop **30577.0** (risk **14.95**). TP1 **30529.6** = **2.17R** (passes 1:2); TP2 30519.6 = 2.84R; TP3 30500 = 4.15R. Cancel was 14:15 / CPI flat 14:25. Charter M12 scalp (not M13; indices window opens 14:30).
- **Path (OANDA 1m):** **FILLED 13:26** (high 30562.8). Post-fill low **30545.0 @13:29** (≈ +1.14R heat toward TP1). **STOPPED 13:33, −1R** (high 30579.6; 13:32 high 30576.4 still under the stop). TP1 never reached. Same as S22 — one 0.5% unit, not two.
1. **P(fill by 14:15): ~100% at the alert geometry.** From the 13:20 5m close 30559.4, a +2.65 rally before a −29.8 run to TP1 printed first on **18/18** days. Actual fill came on the next bar.
2. **P(TP1 before stop | fill, by 14:25): ~17–28% analog / 31.5% barrier.** Same distances from the 13:25 5m close: TP1 3, stop 15 (**17%**, n=18). From 13:20: 5 / 12 / 1 = **28%**. Driftless barrier 14.95/(14.95+32.45) = **31.5%** = break-even at 2.17R. TP2 analog 11–22%.
3. **EV per fill: about −0.46R (17% analog) to ~0R (barrier); −0.11R at the 28% analog.** The London sweep+MSS+FVG family is REJECTED (−0.14R/−0.28R). The positive XAU 07:00 NY model does **not** transfer to NAS. NAS day H/L rarely forms in NY AM (H 7% / L 4%).
4. **Bias:** agrees with bias.md (below 30519.6 draw 30401.2) and intermarket NAS-weak SMT — **not COUNTER-TREND.** Caveats from setups.md still apply: raid of a minor 1m/5m high (not ~30590), 1m-only MSS, modest displacement, pre-CPI.
5. **Units:** dollar-bid / risk-off side. Soft-dollar (B6 + S21) was the open opposite cluster. Prior NY AM NAS loss this KZ: this stop itself.
**Score: 2/5 probability (retro). Bias-aligned and 1:2 met at TP1, but expectancy ≈ flat-to-negative on analogs; no measured NAS NY-AM edge. Result: −1R.** Small n=18.

## Disagreements
- setups.md 13:29 still listed B11 as PENDING sell limit; OANDA 1m shows fill 13:26 and stop 13:33 (matches scalps.md 13:34). Verified path used here.
- A 14.95-pt NAS stop is only ~1–2 5m bars of noise into CPI — same tight-stop risk that stopped S20.

## Data notes
- tvDatafeed nologin ~18 weekdays of NAS 5m; 5m cannot resolve intrabar order (same-bar = loss).

---
Updated: 2026-10-14 13:49 SAST
Probability Bot | kill-zone scoring run (13:47 fire, 07:47 NY). **No new alerted setups since 13:35.** Changed files checked: setups.md 13:48 (B12 NAS short candidate NOT ALERTED, FVG failed 13:45), scalps.md 13:47 (S23 = same idea, VOID before alert; Gold 2.0 no new setup), pingpong.md 13:40 pass (no new alertable setups), confluence.md 13:40 (no new idea), liquidity.md 13:45, timeframes.md 13:43, orderflow.md 13:47. Prices below are from peer files' OANDA 1m reads at 13:46-13:47 (no fresh fetch this run). Status only; no new scores. No alert sent.

## Outcome / status updates (already-scored setups)
- **B12 / S23 NAS100 SHORT: VOID, not scored.** Never alerted; the 13:45 1m bar closed 30571.4 above the FVG top 30569.0 on the same bar that would have filled the 30566.2 limit. No position, no R. (setups.md calls it "alerted 13:46" in one line; scalps.md 13:47 says NO_ALERT. scalps.md is the owner, so treated as not alerted.)
- **S21 / G2-1 XAUUSD LONG, COUNTER-TREND: still OPEN** from 4139.94. New post-fill low 4137.970 @13:46 (about −0.46R on the S21 4135.70 stop); last ~4138.4 ≈ −0.36R. Stop and TP1 4157.9 untouched; 4136.025 sell-side still resting ~0.3 above the stop. Prior 2/5, EV flat-to-slightly-negative holds. Flat by 14:25 (CPI 14:30).
- **B6 / Ping-Pong GBPUSD LONG: still OPEN.** Last 1.32640 ≈ +0.57R (B6) / ≈ +1.05R (PP). NY AM low 1.32582 held above stops 1.32563 / 1.32558; TP1 1.32728 untouched. Score 3/5 leaning 2/5 unchanged. DXY 102.212-102.215, just above 102.207; a break under it helps B6 (USD offered). Flat by 14:25.
- No new entries after 14:15 (team CPI rule).

---
Updated: 2026-10-14 14:08 SAST
Probability Bot | kill-zone scoring run (14:05 fire, 08:05 NY). New since last run (13:49): pingpong.md **GU OTE long** (alerted 13:51) and **NAS OTE long** (alerted 14:01). setups.md 13:55 / scalps.md 14:01 no new Entry Model or Scalp alerts (S21/B6 status only; S23 still VOID). confluence.md 14:01 flagged the GU OTE as unscored. Live OANDA/TVC 1m + 5m via tvDatafeed (nologin) to the 14:07 1m / 14:05 5m. Analog = same distances from the matching 5m close on 17–18 prior weekdays (2026-09-18 to 10-13), run to 14:25 (pre-CPI); same-bar touch of both = loss. Small n, direction only. Pickles: data/prob/*_1m_1405.pkl, *_5m_1405.pkl.

## Live at 14:07–14:08
NAS 30592.2 (since 13:55: H 30607.8 / L 30551.0) | XAU 4146.275 (post-fill S21 H 4150.35 / L 4136.995) | GBP 1.32684 (since 13:45: H 1.32702 / L 1.32622) | DXY 102.215 (still above 102.207).

## Outcome updates (already-scored setups)
- **S21 / G2-1 XAUUSD LONG, COUNTER-TREND: still OPEN** from 4139.94. Worst 4136.995 @13:57 (≈ −0.69R); best 4150.35; last ≈ +1.5R. Stop 4135.70 and TP1 4157.9 untouched. Prior 2/5 holds. Flat by 14:25 (CPI). Soft-dollar with B6/PP GU.
- **B6 / Ping-Pong GBPUSD IFVG LONG: still OPEN.** High since fill 1.32702 (≈ +1.8R on B6 from 1.32612; TP1 1.32728 not hit). Low 1.32582 held above stops. Last ≈ +1.5R. Flat by 14:25.
- **B12 / S23:** still VOID (never alerted).

## Scored: Ping-Pong GU OTE LONG (NEW alert 13:51) — VOID before fill
Buy limit **1.32603**, stop **1.32572** (risk **3.1 pips**), target **1.32694** = **2.94R** (engine 2.98R). Bias-aligned (daily GU bull / 15m at sweep); NOT COUNTER-TREND. Soft-dollar unit with open B6/PP IFVG and S21.
- **Path (OANDA 1m):** limit **never touched** (low since MSS 1.32622). Target **1.32694 printed** (high **1.32702** after 13:45) while unfilled → **VOID** (same rule as the 09:30 EU OTE short). No position, no R.
- Retro geometry only (would have applied if filled): driftless barrier 3.1/(3.1+9.1) ≈ **25%** = break-even at 2.94R; 5m analog TP-before-stop from 13:40/13:50 closes **18–29%** (n=17), from 13:45 **0%** (n=17). Tiny Ping-Pong missed-days OTE bucket −0.75R (n=10); GU n=4 avg −1.00R.
- **Score: n/a (VOID).** Would have been ~2/5 / ~0R expectancy into CPI even if filled. No alert re-fire.

## Scored: Ping-Pong NAS OTE LONG, COUNTER-TREND (NEW alert 14:01)
Buy limit **30544.9** (OTE), stop **30527.6** (risk **17.3**), TP **30617.5** = **4.18R** (passes 1:2). Cancel unfilled **14:15**; flat by **14:25** (CPI 14:30). Status @14:07: **UNFILLED** (low since MSS 30551.0, ~6.1 pts above the limit; last 30592.2).
1. **P(fill by 14:15): ~6–28%.** From a 13:55-like close with ~30.7 pts to the limit vs ~41.9 to the target: fill first **5/18 = 28%**. With the live gap (~47 pts down vs ~25 up to TP): fill first **1/18 = 6%**. Most paths cancel or time out before 14:15.
2. **P(TP before stop | fill, by 14:25): ~0–6% analog / ~19% barrier.** Same distances from 13:45/13:50/13:55 5m closes: TP 1/1/0 out of 18 (**6% / 6% / 0%**). Driftless barrier 17.3/(17.3+72.6) = **19.2%** = break-even at 4.18R. A 17-pt NAS stop is ~1–2 5m bars of noise into CPI.
3. **EV per fill: about −0.7R (6% analog) to ~0R (barrier).** Per order placed (× ~6–28% fill): about −0.2R to 0R.
4. **COUNTER-TREND:** fights bias.md / daily lean bear. Gate for a NAS long (15m close >30677) unmet (15m still ~30575). London sweep+MSS+FVG family REJECTED (−0.14/−0.28R). NAS day H/L rarely forms in NY AM (H 7% / L 4%). Prior NY AM NAS shorts this KZ: B11/S22 −1R; B12/S23 VOID.
5. **Units:** soft-dollar / risk-on side — **same 0.5% soft-dollar unit** as open B6/PP GU and S21 if filled, not a fresh add. Opposite of the stopped NAS shorts.
**Score: 1/5 probability. COUNTER-TREND. Passes 1:2 on geometry (4.18R). Fill unlikely before 14:15; expectancy flat-to-negative. Small n=18.** Upgrade only after a 15m close >30677 and a fresh score on the pullback geometry.

## Disagreements
- confluence.md 14:01 held the GU OTE at 3/5 structure while unfilled; path since then voids it (target before fill). Flagged.
- pingpong.md labels the NAS OTE UNPROVEN with Classic eligibility; base rates show no positive expectancy into CPI with a tight stop against the bear gate.

## Data notes
- tvDatafeed nologin ~18 weekdays of 5m; 5m cannot resolve intrabar order (same-bar = loss).
- Team CPI rule: no new entries after 14:15; flat by 14:25.

---
Updated: 2026-10-14 14:22 SAST
Probability Bot | kill-zone scoring run (14:22 fire, 08:22 NY). New since last run (14:08): scalps.md **S24** NAS100 LONG COUNTER-TREND (alerted 14:08; MISSED/VOID by 14:10 — never scored). setups.md 14:16 / scalps.md 14:18 / pingpong.md 14:21: no further new alerts (CPI blackout 14:15-14:45). PP NAS OTE (scored 14:08 as UNFILLED) → VOID 14:10 (status only). Live path from peer OANDA 1m reads (setups/scalps/confluence/pingpong 14:08-14:18); analogs from data/prob/NAS100USD_5m_1405.pkl (18 prior weekdays). Same-bar touch of both = loss. Small n, direction only.

## Live context @14:18–14:22
NAS ~30618-30621 (NY AM H 30626.5 @14:16) | XAU ~4150 (S21 best 4153.32 @14:16 ≈ +3.16R) | GBP ~1.32700 (B6 best 1.32702 ≈ +1.84R) | DXY ~102.207 (wick 102.203 @14:16, no close under 102.207). CPI blackout ON; flat by 14:25.

## Outcome updates (already-scored setups)
- **Ping-Pong NAS OTE LONG (scored 14:08, 1/5): VOID before fill.** Target 30617.5 hit 14:05/14:09 (high 30618.6 then 30625.4) before limit 30544.9 filled (low since MSS 30551.0 / 30571.6). Stop untouched. 0R. Matches pingpong.md correction 14:11.
- **S21 / G2-1 XAUUSD LONG, COUNTER-TREND: still OPEN** from 4139.94. Best **4153.32 @14:16 ≈ +3.16R**; last ~4150 ≈ +2.5R. Stop 4135.70 / TP1 4157.9 untouched. Prior 2/5 holds. Flat by 14:25 (CPI). Soft-dollar with B6.
- **B6 / Ping-Pong GBPUSD IFVG LONG: still OPEN.** Best 1.32702 ≈ +1.84R; last ≈ +1.8R. TP1 1.32728 untouched. Flat by 14:25.
- **PP GU OTE:** still VOID (scored 14:08).

## Scored: Scalp S24 NAS100 LONG, COUNTER-TREND (NEW alert 14:08) — MISSED / VOID before fill
Buy limit **30583.8** (CE of 1m bull FVG 30580.6-30587.0 after 1m bull MSS 14:00 through 30581.6). Stop **30566.6** (risk **17.2**). TP1 **30622** = **2.22R** (passes 1:2); TP2 30675 = 5.30R; TP3 30704.7 = 7.03R. Cancel unfilled 14:15; flat by 14:25 if filled. Charter-style M12 continuation scalp (not M13; index window opens 14:30).
- **Path (OANDA 1m, scalps.md / confluence.md):** limit **never touched** (lowest after alert **30589.0 @14:09**, 5.2 pts above). TP1 **30622** printed **30625.4 @14:10** while unfilled → **MISSED / VOID** (0R). Stop never touched. scalps.md 14:14 final: MISSED; confluence.md 14:12: VOID target-before-fill.
1. **P(fill by 14:15) at alert geometry: ~61% analog / path = 0%.** From a 14:05-like close with ~8.4 pts to the limit vs ~29.8 to TP1: fill first **11/18 = 61%**, cancel 1, timeout 6 (n=18). Live path cancelled/voided (TP1 side won). From 14:00 closes: fill 13/18 = 72%.
2. **P(TP1 before stop | fill, by 14:25): ~18% analog / 31% barrier.** On the 11 analog fills: TP 2, stop 5, timeout 4 = **18%** (n=11, very small). Driftless barrier 17.2/(17.2+38.2) = **31.0%** = break-even at 2.22R. From 14:00 fills: TP 0/13 = **0%** (stop 9, timeout 4).
3. **EV per fill: about −0.41R (18% analog) to ~0R (barrier).** Per order placed (× ~61% fill): about −0.25R to 0R. London sweep+MSS+FVG family REJECTED (−0.14/−0.28R). No measured NAS NY-AM long edge. A 17-pt NAS stop is ~1–2 5m bars of noise into CPI.
4. **COUNTER-TREND:** fights bias.md / 4H bear and intermarket NAS-weak. Gate for NAS CT long (15m close >30677) unmet at alert (15m still ~30575-30604). Prior NY AM NAS this KZ: B11/S22 −1R; B12/S23 VOID; PP NAS OTE VOID.
5. **Units:** separate 0.5% from soft-dollar (B6 + S21) per scalps.md — would have been a fresh NAS unit if filled.
**Score: n/a (MISSED/VOID, 0R).** Would have been **2/5** / flat-to-negative expectancy into CPI even if filled (passes 1:2 on geometry only). Small n=11–18. No re-alert.

## Disagreements
- scalps.md labels S24 MISSED; confluence.md labels VOID (target-before-fill). Same path, same 0R — treated as VOID/MISSED here.
- confluence.md 14:12 nudged probability for S24; this section closes that gap.

## Data notes
- Analogs: NAS100USD 5m pickle to 14:05 (data/prob/NAS100USD_5m_1405.pkl), 18 weekdays Sep 18–Oct 13. 5m cannot resolve intrabar order (same-bar = loss).
- Team CPI rule: no new entries after 14:15; flat by 14:25.

---
Updated: 2026-10-14 14:38 SAST
Probability Bot | kill-zone scoring run (14:36 fire, 08:36 NY). New since last run (14:22): **no new alerted setups.** setups.md 14:25 NO_ALERT; scalps.md 14:26/14:28 NO_ALERT and 14:34 Gold 2.0 watch (third instance SHORT **SKIPPED**, not alerted); pingpong.md 14:26/14:27/14:33 no new alertable setups; confluence.md 14:30 zones only (no zone ≥4/5, no new trade idea); liquidity.md 14:31 map only. CPI blackout 14:15-14:45 SAST. Status changes below come from peer OANDA 1m reads (no new fetch this run). No prices invented.

## Outcome updates (already-scored setups)
- **S21 / G2-1 XAUUSD LONG, COUNTER-TREND (scored 2/5): CLOSED FLAT FOR CPI at 14:25.** ≈ **+2.59R** (S21 stop) / ≈ +2.49R (G2-1 CE) at exit 4150.915. Best 4154.555 @14:23 ≈ +3.3R; TP1 4157.9 never traded; stop never traded. A 2/5 score that paid: one outcome, does not change the base rate (n=1).
- **B6 / Ping-Pong GBPUSD IFVG LONG (bias-aligned): CLOSED FLAT FOR CPI at 14:25.** ≈ **+1.47R** on setups.md's entry/stop (exit 1.32684); ≈ +2.15R on Ping-Pong's own 1.32598/1.32558. Best 1.32710 ≈ +2.0R; TP1 1.32728 missed by ~1.8 pips. Stop never traded.
- **S24, PP NAS OTE, PP GU OTE:** final VOID/MISSED, 0R. PP NAS Classic row (13:00 sweep) expired unfilled at 14:25, never alerted.
- Nothing open. Soft-dollar unit freed.

## Not scored: scalps.md Gold 2.0 third instance XAU SHORT (paper only, SKIPPED)
High-side raid 4155.835 (14:29) → CPI 1m MSS (14:30 close 4128.490) → 1m bear FVG 4129.710-4151.630. Paper edge 4129.710, stop ~4156.8 (risk ~27.1 USD), only TOP1 4066.53 clears 1:2 (~2.33R). **Not an alert:** formed inside the CPI blackout with a news-sized stop. No base rate here covers a post-CPI 1m FVG entry; the closest tested family (sweep+MSS+FVG) is REJECTED (−0.14/−0.28R), and the target needs a further ~63 USD drop from the edge by 15:00 — treat as low-odds (not measured). Trend-aligned (gold bear gate intact: no 1H close >4156; CPI dropped price to ~4117-4130, well under it). Paper tracking only; scalps.md will log 4066.53 vs 4156.8 vs 15:00 expiry.

## KZ running tally (alerted, OANDA chart prices, NY AM so far)
S20 XAU short −1R; B11/S22 NAS short −1R; S21/G2-1 XAU CT long ≈ +2.5R flat; B6 GU long ≈ +1.5R flat; S23/S24/PP OTEs void 0R. Net ≈ +2R on four filled units. Small n; no edge claim.

## Data notes
- No fresh price fetch this run (no new setup to score). New entries allowed again from 14:45 SAST; next scoring run 14:47.

---
Updated: 2026-10-14 14:57 SAST
Probability Bot | kill-zone scoring run (14:53 fire, 08:53 NY). New since last run (14:38): setups.md **B14** XAUUSD SHORT (alerted/filled 14:49, TRIGGER ALERT 14:51); scalps.md **S25** NAS100 LONG COUNTER-TREND and **S26** XAUUSD LONG COUNTER-TREND (both ALERTED 14:53). Live OANDA/TVC 1m + 5m via tvDatafeed (nologin) to the 14:57 1m / 14:55 5m. Analog = same distances from matching 5m closes on 18 prior weekdays (2026-09-18 to 10-13), run to 16:00 SAST; same-bar touch of both = loss. Small n, direction only. Pickles: data/prob/*_1m_1453.pkl, *_5m_1453.pkl (5m merged with prior long history).

## Live at 14:57
NAS **30398.8** (since S25 fill 14:52: H 30451.8 / L 30397.6) | XAU **4096.34** (since B14 fill 14:49: H 4107.69 / L 4095.67) | EUR 1.11322 | GBP 1.32084 | DXY **102.716** (still well above the broken 102.207 / post-CPI bid).

## Outcome notes (path-critical only)
- **S21 / B6:** already closed flat for CPI at 14:25 (prior 14:38 section). Soft-dollar unit was free before these alerts.
- **B14 vs S26:** both now live on OANDA chart prices (see below) — **DIRECT CONFLICT** on one XAU unit.

## Scored: B14 XAUUSD SHORT — FILLED 14:49 (TRIGGER ALERT 14:51), trend-aligned
Sell limit CE **4105.34** of 1m bear FVG 4102.795-4107.88. Stop **4117.60** (risk **12.26**). TP1 **4075.0** = **+2.47R** (passes 1:2). TP2 **4066.53** (PWL) = **+3.17R**. Early exit: 1m close above FVG top **4107.88**. Manage to end of NY AM (**16:00 SAST**). NOT COUNTER-TREND (M13/M12/M7; XAU bear gate intact: no 15m close >4170.5, no 1H close >4156).
**Live path:** filled 14:49 (H 4105.60). Since fill: maxH **4107.69** (FVG top 4107.88 untouched; no 1m close above it), minL **4095.67** (≈ +0.79R), last 4096.34 ≈ **+0.73R**. Stop and TP1 untouched. **OPEN**, open risk −1R at stop.
1. **P(fill): 100%** (already filled).
2. **P(TP1 before stop | fill, by 16:00): ~11–17% analog / ~29% barrier.** From 14:50 5m closes: TP1 2 / stop 7 / timeout 9 = **11% (n=18)**; from 14:45: **17%** (T3/S5/N10). +2R (24.52 pts / 4080.82): **22–28%**. TP2: **6%**. Driftless barrier TP1 12.26/(12.26+30.34) = **28.8%** = break-even at 2.47R. Wed-only n=3: 1/1/1 (noise).
3. **EV per fill: about −0.11R (TP1 analog, timeout=0) to ~0R (barrier); +2R analog ≈ +0.06R.** Treating non-wins as −1R (no timeout credit) is worse (~−0.4R to −0.6R) — use the timeout=0 / barrier band. Closest tested family: XAU NY AM 07:00 NY 1m range sweep+MSS+FVG **+0.31R/+0.50R (n=38)**; **shorts only +0.07R (n=22)**; Wed +0.36R (n=7). London sweep+MSS+FVG REJECTED (−0.14/−0.28R) — not the right bucket, but a caution. Gold bear-day HOD in Asia **65% CONFIRMED** — today's Asia high **4170.49** fits a bear day and supports the short theme.
4. **Trend support:** D/4H/1H/15m bear gate intact; DXY post-CPI bid (~102.72) is USD-long confluence for gold short. Price bounced through the FVG once (fill) and is working lower.
5. **Caveats / conflict:** **Do not stack with S26** (same instrument, opposite direction). A 1m close above 4107.88 is array failure / early exit. NY AM is a weak bucket for gold day extremes (H 6% / L 5%). Runner TP2 needs a further ~29 USD from last — take TP1 seriously.
**Score: 3/5 probability. Trend-aligned. Passes 1:2 (2.47R). Expectancy ≈ flat (analog) to breakeven (barrier); base-rate shorts only mildly positive. Manage: TP1 4075, early exit on 1m close >4107.88, flat by 16:00. Open risk −1R. Do not also take S26.**

## Scored: S25 NAS100 LONG, COUNTER-TREND — ALERTED 14:53, FILLED 14:52 on OANDA path
Buy CE **30425.1** of 1m bull FVG 30421.4-30428.8 after sweep of week low 30401.2 to **30369.8** and MSS through 30427.8. Stop **30361.7** (risk **63.4**). Target **30665.0** = **+3.78R** (passes 1:2). Prudent partial / +2R at **30551.9**. Cancel if below 30369.8, if 30552 prints unfilled, or 16:00 SAST. COUNTER-TREND vs 4H/15m/5m bear. Full 0.5%.
**Live path:** alert said pending; OANDA 14:52 L **30417.7** traded the CE → **FILLED**. Since fill: H 30451.8 (≈ +0.42R), L 30397.6 (≈ −0.43R), last 30398.8 ≈ −0.41R. Stop / void 30369.8 / +2R untouched. **OPEN**.
1. **P(fill): 100% now.** At alert geometry (~20 pts to limit vs ~106 to 30552 cancel): fill-first analog **72–83% (n=18)** — path matched.
2. **P(+2R / TP before stop | fill, by 16:00): ~28% analog (+2R) / ~33% barrier; full TP ~0–6%.** From 14:50: +2R T5/S10/N3 = **28%**; full 239.9-pt TP **0%** (14:50) / **6%** (14:45). Driftless barrier +2R = **33.3%** = break-even at 2R; full TP barrier 63.4/(63.4+239.9) = **20.9%** = break-even at 3.78R.
3. **EV per fill: about 0R at +2R (analog timeout=0 and barrier); full TP analog ≈ −0.35R to −0.7R.** Use +2R / 30552 as the working target; 30665 is a runner only.
4. **COUNTER-TREND:** fights 4H/15m/5m bear and post-CPI USD bid (DXY ~102.72). NAS CT long gate (15m close >30677) **unmet**. NAS day H/L rarely forms in NY AM (H 7% / L 4%). London sweep+MSS+FVG family REJECTED (−0.14/−0.28R). Support: **PDH/PDL sweep 13-16 SAST + close-back → session mid 65% PROMISING (against-bias 90%, n=20)** — this is a turtle-soup CT long off the week-low raid, so that base rate is the right one to cite, not the rejected London family.
5. **Units:** risk-on / soft-dollar side — **same thesis side as S26** if both taken (not a hedge of B14). Separate NAS 0.5% unit from XAU.
**Score: 2/5 probability. COUNTER-TREND. Passes 1:2 (3.78R geometry; work +2R). Fill done; expectancy ≈ flat at +2R, negative if hunting 30665 into 16:00. Small n=18.** Upgrade only after a 15m close >30677 and a fresh score.

## Scored: S26 XAUUSD LONG, COUNTER-TREND — ALERTED 14:53, FILLED 14:52 on OANDA path — CONFLICTS WITH B14
Buy CE **4099.98** of 1m bull FVG 4098.675-4101.285 after sweep to **4085.29** and MSS 14:49. Stop **4083.05** (risk **16.93**). Target **4155.84** = **+3.30R** (passes 1:2). +2R at **4133.84**. Cancel if below 4085.29, if 4133.84 prints unfilled, or 16:00 SAST. COUNTER-TREND vs D/4H/1H/15m bear. Full 0.5%.
**Live path:** OANDA 14:52 L **4096.65** traded the CE → **FILLED**. Since fill: H 4107.535 (≈ +0.45R), L 4095.67 (≈ −0.25R), last 4096.34 ≈ **−0.21R**. Stop / void / +2R untouched. **OPEN** — and **B14 is also OPEN** on the same instrument the other way.
1. **P(fill): 100% now.** At alert (~5.7 pts to limit vs ~28 to 4133.84 cancel): fill-first analog **72–78% (n=18)** — path matched.
2. **P(+2R / TP before stop | fill, by 16:00): ~0% analog / ~23–33% barrier.** From 14:45 and 14:50: +2R and full TP both **T0 / S9 / N9 = 0% TP-first (n=18)**. Half the analogs stop, half time out by 16:00 — a +34–56 USD gold rally in ~1h from a random post-14:50 long is rare on 5m. Driftless barrier +2R = **33.3%**; full TP 16.93/(16.93+55.86) = **23.3%**.
3. **EV per fill: about −0.5R (analog, timeout=0) to ~0R (barrier).** Non-win-as-loss framing ≈ −1R on the analog. The only constructive cite is **PDH/PDL sweep 13-16 SAST + close-back → session mid 65% (against-bias 90%, n=20)** — turtle-soup CT. That is a mid-reclaim rate, not a measured +3.3R-by-16:00 rate.
4. **COUNTER-TREND + DIRECT CONFLICT with B14:** S26 buys the bounce Entry Model is shorting from the 1m bear FVG. Gold bear gate intact; Asia HOD 65% on bear days supports B14's side, not S26. **Do not take both. They share opposing theses on one XAU unit.** If B14 is on, S26 is not a fresh 0.5% — it is the opposite bet. If somehow both filled (chart path says yes), treat as a conflicted XAU book and pick one thesis; do not double risk.
5. **Units:** soft-dollar / risk-on with S25; opposite B14 (USD-long gold short).
**Score: 2/5 probability on geometry/turtle-soup alone; effectively 1/5 if B14 is already on.** COUNTER-TREND. Passes 1:2 (3.30R). Analog expectancy negative into 16:00; barrier ~0R. **Verdict: do not take alongside B14. Prefer B14 (trend-aligned 3/5) over S26 if choosing one XAU idea.**

## Conflict / units summary
| Setup | Side | CT? | Status @14:57 | RR | Score | Unit |
|---|---|---|---|---|---|---|
| B14 XAU short | USD-long | no | OPEN ~+0.7R | 2.47R | **3/5** | XAU A |
| S25 NAS long | risk-on | **yes** | OPEN ~−0.4R | 3.78R | **2/5** | NAS |
| S26 XAU long | soft-dollar | **yes** | OPEN ~−0.2R | 3.30R | **2/5** (1/5 w/ B14) | XAU B — **conflicts with A** |

**Do not take B14 and S26 together.** S25 is a separate NAS unit but the same soft-dollar/risk-on side as S26.

## Disagreements
- setups.md (B14 short) vs scalps.md (S26 long): both alerted; both filled on OANDA. Probability sides with **B14** on trend + Asia-HOD bear-day base rate; S26 only has the PDH/PDL turtle-soup PROMISING rate and fights the open short.
- Scalps labels S25/S26 valid ≥1:2 CT scalps; base rates show flat-to-negative expectancy into 16:00 at the stated targets (work +2R partials if taken).

## Data notes
- tvDatafeed nologin: 1m ~300 bars today; 5m analogs use ~18 weekdays (merged long history + fresh 1453). 5m cannot resolve intrabar order (same-bar = loss).
- NY AM KZ ends **16:00 SAST**. No fabricated prices.

---
Updated: 2026-10-14 15:07 SAST

## Status verification (OANDA 1m via tvDatafeed, through the 15:05 bar)
| Trade | Side / unit | Entry | Stop | OANDA check | Result | vs Confluence Bot |
|---|---|---|---|---|---|---|
| S25 NAS100 LONG (CT) | soft-dollar / risk-on | 30425.1 (14:52, L 30417.7) | 30361.7 | 14:59 L 30356.2 hit stop (14:58 L 30365.8 did not) | **-1R, closed** | matches |
| S26 XAUUSD LONG (CT) | soft-dollar | 4099.98 (14:52 L 4096.65; also 14:56 L 4099.615) | 4083.05 | 15:02 L 4083.66; **15:04 L 4083.005 hit stop (by 0.045)** | **-1R, closed** | **DIFFERS:** Confluence had about -0.81R/open with a 4083.68 low. 15:02 OANDA low is 4083.66, and the 15:04 bar stopped it. Scalp Bot also logs -1R at 15:04. |
| B14 XAUUSD SHORT (trend) | long-dollar | 4105.34 (14:49 H 4105.60) | 4117.60 (risk 12.26) | max H since fill 4107.69, stop untouched; low 4083.005 (15:04) | **OPEN: +1.50R at 4086.91 (15:05)**, best +1.82R | Confluence +1.56R matches price ~4086.2 (it changes tick by tick); TP1 4075 not hit |

## Units now
- **Soft-dollar / risk-on unit:** S25 -1R and S26 -1R are both closed. The earlier EUR OTE -1R is also in this unit. **Today this theme has lost repeatedly.** Earlier-session longs (B3, PP XAU/GU, S18/S19) are not re-verified in this run.
- **Long-dollar / risk-off unit:** B14 XAU short open at +1.50R (TP1 4075, TP2 4066.53; array-failure exit on a 1m close above 4107.88). B15 NAS short (sell limit 30407.25, alerted 15:00) is the same unit. Not filled: the high since 15:00 is 30392.8. If it fills, it is not a fresh 0.5%.
- **Lesson for scoring:** a counter-trend long against a post-CPI USD bid went 0/2 here. That fits the earlier analog stop-rates (6-22% targets first).

---
Updated: 2026-10-14 15:15 SAST
Probability Bot | kill-zone scoring run (15:11 fire, 09:11 NY). New since last run (14:53): setups.md **B15** NAS100 SHORT (alerted 15:00). scalps.md 15:05 NO_ALERT; confluence.md 15:04 no new idea. Live OANDA/TVC 1m + 5m via tvDatafeed (nologin) to 15:12 SAST. Analog = same distances from 15:05/15:10 5m closes on 18 prior weekdays (2026-09-18 to 10-13). A same-bar touch of both counts as a loss. Small n, so read these for direction only. Pickles: data/prob/*_1511.pkl.

## Live @15:12
NAS **30392.7** (since 15:00: H 30402.4 / L 30358.4) | XAU **4083.29** (since B14 fill: H 4107.69 / L 4082.68) | DXY **102.828** (NY AM high ~102.856).

## Outcome updates (already scored)
- **B14 XAUUSD SHORT: OPEN, about +1.80R** (best +1.85R at 4082.68). Stop 4117.60 untouched, no 1m close above 4107.88, TP1 4075 not hit yet. Prior 3/5 holds.
- **S25 NAS100 LONG (COUNTER-TREND): STOPPED, -1R at 14:59** (L 30356.2).
- **S26 XAUUSD LONG (COUNTER-TREND): STOPPED, -1R at 15:04** (L 4083.005).

## Scored: B15 NAS100 SHORT, trend-aligned (NEW; alerted 15:00; Charter M13/M12), PENDING
Sell limit CE **30407.25** (1m bear FVGs 30406.0-30408.5 / 30413.4-30419.2). Stop **30458.5** (risk **51.25**). TP1 **30300** = **+2.09R** (passes 1:2). TP2 **30273.2** = +2.62R. TP3 30110.1 = +5.80R. Cancel unfilled if price goes above 30451.8 first, if 30300 prints first, or at 17:00 SAST. After a fill, exit early on a 1m close above 30419.2. NOT COUNTER-TREND on weekly/daily, but it fights bias.md's 14:51 intraday reversal-long read and sells in deep daily discount (liquidity.md 2.6%).
**Live path:** not filled. The high since 15:00 is 30402.4, 4.85 under the limit. Last is 30392.7, so it needs +14.55 points to fill against -92.7 points to the cancel.
1. **P(fill): ~83% (15/18 analog, by 16:00 and by 17:00).** It's the same from 15:10 closes.
2. **P(TP1 before stop | fill, to 16:00): ~39% analog (T7/S10/N1) / 32.3% barrier.** The break-even rate at 2.09R is 32.4%. From 15:10 it's T8/S10. To 17:00 it's T7/S11.
   P(TP2 first): 17% analog (T3/S10/N5) / 27.7% barrier (BE 27.6%). To 17:00 the analog is 28%.
3. **EV per fill: about 0R (barrier) to +0.26R (analog TP1, with timeout counted as 0).** The TP2 analog is -0.12R. Per order (x 83% fill), that's about 0R to +0.21R. With n=18, treat +0.26R as noise, not an edge.
4. **Base rates:** the family model (London sweep+MSS+FVG 2R) is REJECTED at -0.14R / -0.28R. NAS seldom sets its day high or low in NY AM (H 7% / L 4%), and price has already printed a new day low (30356.2). There's no NAS NY AM M13 backtest with positive EV on file. Earlier NAS NY AM shorts today were B11 -1R and B13 void.
5. **Units:** it's the **same long-dollar / risk-off unit as open B14**. If B14 is still on, a B15 fill is **not a fresh 0.5%**. Split the unit, or let B15 take the full 0.5% only after B14 closes. The soft-dollar counter-trend side (S25/S26) is already -2R combined this kill zone.
**Score: 2/5 probability. Trend-aligned (weekly/daily). Passes 1:2 (TP1 2.09R). Fill is likely (~83%), and expectancy is roughly flat to mildly positive on small n. Take TP1 seriously; TP2 hits less often by 16:00. Shares B14's unit.**

## Units now
| Setup | Side | CT? | Status @15:12 | RR | Score | Unit |
|---|---|---|---|---|---|---|
| B14 XAU short | long-dollar | no | OPEN ~+1.80R | 2.47R | 3/5 | long-dollar |
| B15 NAS short | long-dollar / risk-off | no | PENDING (limit 30407.25) | 2.09R | **2/5** | same as B14 |
| S25 NAS long | risk-on | yes | STOPPED -1R | | | closed |
| S26 XAU long | soft-dollar | yes | STOPPED -1R | | | closed |

## Disagreements
- B15 vs bias.md 14:51: bias.md's NAS reversal long was overrun (new day low 30356.2). Probability sides with B15's direction but scores only 2/5 because the base-rate edge is thin.
- probability.md 14:57 had S25/S26 open. They are now marked stopped (matches confluence.md / scalps.md).
