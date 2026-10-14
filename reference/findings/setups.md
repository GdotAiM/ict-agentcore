Updated: 2026-10-14 15:47 SAST
Entry Model Bot | NY AM kill zone (07:00-10:00 NY = 13:00-16:00 SAST), run 15:47 SAST (~09:47 NY), Wed 14 Oct. NEW this run: B16 EURUSD SHORT (Charter M13/M12) — sell limit CE 1.113365 pending, R:R ~3.38 to day low. B14 XAUUSD short still OPEN (~+0.23R). B15 status unchanged (INVALIDATED, already alerted). ALERT needed for B16.
Data: TradingView OANDA:NAS100USD, OANDA:XAUUSD, OANDA:EURUSD, OANDA:GBPUSD, TVC:DXY via tvDatafeed (nologin), 1m/5m/15m, fetched 15:45-15:47 SAST (last 1m bar 15:47 forming). All symbols returned. No yfinance fallback used. Analysis only, not trades. No prices invented; fills judged on OANDA chart prices.

## Peer files
- bias.md: fresh (15:33). NAS BEAR (fail on 15m close >30451.8). XAU BEAR to 4066.535. EUR BEAR (inv 15m close >1.11452). GBP BEAR (inv 15m close >1.32192). DXY BULL (inv 15m close <102.748).
- liquidity.md: fresh (15:43). NOTE: ranking header still uses NAS intraday BULLISH from bias.md 15:27; bias.md 15:33 flipped NAS to BEAR. Also still cites bias 15:27 for EUR/GBP/DXY while structure notes 1m bull MSS reclaim — flag for Liquidity Bot.
- intermarket.md: STALE for direction (12:59, pre-CPI). Needs refresh. DXY now 102.78 after 15:30 15m closed 102.777 (ABOVE 102.748 inv — DXY bull intact).
- Also read: TEAM_PLAN.md, charter_models.md, kz_alerts.csv. No files missing.

## Market at 15:47 SAST
- DXY 102.780: day high 102.875 @15:20, low since 102.710 @15:40. 15:30 15m CLOSED 102.777 — ABOVE bias.md 102.748 invalidation (bull intact). Forming 15:45 ~102.77. Dollar bid resumed off the fade.
- NAS 30432.0: day low 30311.5 @15:38, bounce high 30438.1 @15:43. Still below 30451.8 bear-fail line. 15:30 15m closed 30399.2 (H 30438.1 L 30311.5).
- XAU 4102.49: day low 4079.73 @15:20. Bounce high 4107.37 @15:35, still under FVG top 4107.88; max 1m close since fill still under. Stop 4117.60 untouched.
- EUR 1.11286: bounce high 1.11374 @15:40 (raid of 1.11364 area), then MSS + displacement 15:42; 1m bear FVG 1.11328-1.11345 unfilled (pending retrace). Below 1.11452 inv.
- GBP 1.31921: bounce high 1.32056 @15:35, then lower; 1m bear FVGs 1.31969-1.31980 / 1.31940-1.31955 print but R:R under 1:2 to 1.31808 with stop beyond raid. EUR/GBP: both rejected; EUR had clearer MSS+FVG.

## Active setups

### B16 EURUSD SHORT - NY AM - Charter M13 (2022 model) / M12 - ALERT 15:47 - LIMIT PENDING
- Stage: Trade Execution (limit pending). Bias-aligned (bias.md EUR BEAR).
- Sweep: buy-side raid 15:40 to 1.11374 of 15:35-39 bounce highs 1.11364/1.11362 (into/above prior 5m bear FVG top).
- MSS: 15:30 low 1.11285 broken on 15:42 displacement (L 1.11277 C 1.11278).
- Entry: sell limit CE 1.113365 of 1m bear FVG 1.11328-1.11345 (above EQ of bounce 1.11142-1.11374). Not tagged since formation (max H after 15:42 = 1.11302).
- Stop 1.11394 (raid 1.11374 + ~1.2 pip spread + ~0.8 pip normal 1m wick; risk 5.75 pips). Early-exit / array fail: 1m close above FVG top 1.11345.
- TP1 1.11142 day low (~+3.38R). TP2 1.11100 (~+4.11R).
- Size: equity x 0.5% / (0.000575 x pip value). NOTE: B14 XAU short still OPEN — same dollar direction; share one 0.5% unit while both open (TEAM_PLAN 14 Oct). Prior same-KZ loss: B15 ~-0.46R (already closed).
- Confluence: DXY 15:30 close held above 102.748 (bull intact); bias EUR BEAR; liquidity draw below toward 1.11142.
- Chart: /workspace/charts/EURUSD_short_B16_NYAM_2026-10-14_1547.png

### B14 XAUUSD SHORT - NY AM - Charter M13 (2022 model) / M12 / M7 sell-side - ALERT 14:49 - TRIGGERED 14:49 (filled CE 4105.34) - OPEN
- Stage: Trade Management. Last 4102.49 (~+0.23R). Best low 4079.73 at 15:20 (~+2.09R). Highs after fill max 4107.69 (14:51); bounce high 4107.37 (15:35). Still under FVG top 4107.88 and stop 4117.60. No 1m close above 4107.88. Stop / TP1 / TP2 untouched.
- Sweep 4115.66 raid of 14:37 high 4114.49 (14:38). MSS: 14:37 low 4108.53 broken 14:39. Entry 1m bear FVG 4102.795-4107.88, filled CE 4105.34.
- Stop 4117.60 (risk 12.26). TP1 4075.0 (+2.47R). TP2 4066.53 PWL (+3.17R). Bias-aligned (bias.md XAU BEAR).
- Size: equity x 0.5% / (12.26 x contract value per 1.00 move). Shares 0.5% unit with B16 while both open.
- Management: exit early on a 1m close above 4107.88. Array held on the 15:35 retest. DXY 15:30 close above 102.748 supports.
- Charts: /workspace/charts/XAUUSD_B14_TRIGGERED_2026-10-14_1450.png and /workspace/charts/XAUUSD_short_B14_NYAM_2026-10-14_1448.png
- Status change this run: none (still OPEN).

## Recent setups (outcomes)
### B15 NAS100 SHORT - NY AM - Charter M13 (2022 model) / M12 - ALERT 15:00 - FILLED 15:33 - INVALIDATED 15:40 (array fail, about -0.46R) - ALERTED 15:42
- Stage: Trade Management -> closed.
- Sweep: buy-side raid 14:49-14:52 to 30451.8. MSS: 14:48/14:53 lows broken on 14:58 displacement. Entry: sell limit CE 30407.25 filled 15:33 (1m high 30410.2).
- After fill: best low 30311.5 @15:38 (about +1.87R; TP1 30300 missed by 11.5 pts). Then 15:40 1m closed 30430.8 above 30419.2 = array fail. About -0.46R. Hard stop 30458.5 untouched.
- Chart: /workspace/charts/NAS100_B15_INVALIDATED_2026-10-14_1542.png (setup chart /workspace/charts/NAS100_short_B15_NYAM_2026-10-14_1459.png)
### B13 NAS100 SHORT candidate - NY AM - Charter M13/M12 - NOT ALERTED / VOID (array fail 14:46)
- Reference chart: /workspace/charts/NAS100_B13_candidate_VOID_NOT_ALERTED_2026-10-14_1447.png

### B6 GBPUSD LONG STOPPED OUT −1R (London Open → NY AM manage, Charter M12) — ALERT 14:37
- Chart: /workspace/charts/GBPUSD_B6_STOPPED_2026-10-14_1430.png

### B12 NAS100 SHORT candidate (= Scalp S23), NY AM, Charter M12 — NOT ALERTED / VOID (FVG failed 13:45)
- Chart: /workspace/charts/NAS100_B12_candidate_NOT_ALERTED_2026-10-14_1347.png

### B11 NAS100 SHORT STOPPED OUT −1R (NY AM, Charter M12) — ALERT 13:34
- Chart: /workspace/charts/NAS100_B11_STOPPED_2026-10-14_1334.png

- B10 NAS100 short COUNTER-TREND (London Open, M12): COMPLETE. TP1/TP2/TP3 hit (+2.4R/+4.5R/+6.3R). Chart: /workspace/charts/NAS100_B10_TP3_HIT_2026-10-14_1305.png
- B9 XAUUSD short (London Open, M12/M7): CANCELLED unfilled at 11:00 SAST.
- B5 EURUSD long COUNTER-TREND: STOPPED OUT 10:42, −1R.
- B7 NAS100 long COUNTER-TREND: STOPPED OUT 10:39, −1R.
- B8 XAUUSD long COUNTER-TREND: INVALIDATED 10:29, ≈ −0.15R.
- B2 GBPUSD short COUNTER-TREND: CANCELLED unfilled 10:19.
- B3 EURUSD long COUNTER-TREND: STOPPED OUT 09:55, −1R.
- B1 XAUUSD short: INVALIDATED 09:49, ≈ −0.3R.
- B4 NAS100 long (09:25-09:41), NOT ALERTED: failed.

## Watching (not setups, no alert)
- NAS100 COUNTER-TREND long (vs bias.md BEAR): sell-side raid 30311.5 @15:38, MSS above 15:33 high 30410.2 @15:40, 1m bull FVG 30398.8-30417.0 already filled; price ~30432. Stop beyond raid ~30304 -> risk ~100+ pts; nearest draws 30451.8 (~0.2-0.5R), 30519.6 (~1.1R), 30576.2 (~1.6-1.8R). Below 1:2 to first meaningful draw, NOT valid. Would need tighter structure or clear path to ≥1:2.
- NAS100 fresh short: only if price raids above 30451.8 and then prints a 1m MSS + bear FVG. A 15m close above 30451.8 would fail bias.md's bear view instead. Bounce high so far 30438.1.
- GBPUSD continuation short: raid 1.32056 @15:35, MSS-ish break of 1.31973, 1m bear FVGs at 1.31969-1.31980 and 1.31940-1.31955. With stop 1.32081 beyond raid, R:R to 1.31808 is ~1.56 from higher FVG CE — under 1:2, NOT valid. Valid only if a retrace builds a 1m bear FVG near 1.32010-1.32040 giving at least 1:2 to 1.31808.
- XAUUSD: no separate re-entry; B14 covers it. Unfilled bull FVGs below (15:30-32) are counter to bias / against open short — ignore.
- DXY: 15:30 close held bull; watch for loss of 102.748 on a later 15m close (would weaken B14/B16 dollar confluence).

## Charter models check (15:47 SAST, Wed)
- M13 (2022 model): B16 EUR new (raid+MSS+1m FVG, limit pending). B14 XAU live. Inside 08:30-11:00 NY index window and 07:00-10:00 NY FX window (FX window ends 16:00 SAST). GBP FVG R:R fail. NAS no new M13 ≥1:2.
- M12 (intraday raids 15m and below): B16 qualifies. NAS CT long under 1:2. GBP under 1:2.
- M7 (universal sell-side): XAU still toward 4066.53 while B14 array holds; EUR toward 1.11142 via B16.
- M6 (universal buy-side): NAS stop run below 30320 then reclaim could become M6, but counter to bias and below 1:2. Not valid.
- M1 (NY KZ scalp, Wed allowed): no clean 5m OTE 62% entry against London momentum with ≥1:2 this run. Not valid.
- M5/M8/M10/M11: no separate 15m PD-array entry beyond B14/B16.
- Swing/position (M2, M3, M4, M9): nothing new lined up.

## Position size
Size = equity x 0.5% / (stop distance x value per pip/point). Only entries of at least 1:2. Stop at least 1 spread + a normal 1m wick beyond the raid extreme.
- B14: equity x 0.5% / 12.26 XAU.
- B16: equity x 0.5% / 0.000575 EUR — shares the unit with B14 while both open.
- KZ tally London Open + NY AM (alerted, OANDA chart prices): B3 -1R, B1 about -0.3R, B8 about -0.15R, B7 -1R, B5 -1R, B10 +2.4R/+4.5R/+6.3R on its portions, B9 0R, B11 -1R, B6 -1R, B15 about -0.46R. Open: B14 (~+0.23R open / best ~+2.1R). Pending: B16.

## Disagreements / stale notes
- liquidity.md (15:43) ranks NAS with intraday BULLISH bias from bias.md 15:27, but bias.md (15:33) says NAS BEAR. Flag for Liquidity Bot.
- intermarket.md (12:59) is pre-CPI and stale; needs a refresh. DXY 15:30 close held above 102.748 (supports USD-bid shorts).
- B14/B16 vs peers: aligned with bias BEAR on XAU/EUR and DXY bull. Correlated dollar-direction — share 0.5% risk unit.
