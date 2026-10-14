# Ping-Pong Bot findings
Updated: 2026-10-14 15:44 SAST (live kill-zone scanner)

## Missed-days backtest 8-14 Oct
Updated: 2026-10-14 09:25 SAST
Data: OANDA via TradingView (tvDatafeed, nologin), 5m LTF + 15m HTF, fetched 09:21 SAST; closed candles only (last 5m bar 09:15-09:20 SAST). Full sessions present Thu 8 - Tue 13 Oct; Wed 14 to 09:20 only. No gaps found. Overlap with the 7 Oct pickles matched exactly.
Method: scripts/pingpong_backtest.py run() unchanged (scripts/missed_bt.py), filled trades only, R:R>=2, fill inside Asian 20-00 / London 02-05 / NY AM 07-10 / SB 10-11 / LC 10-12 NY. COUNTER-TREND = against the script's 15m BOS trend (no daily-bias file used). DXY was not used as a filter.

| SAST | Inst | Setup | Conf | Dir | Entry | Stop | Target | R:R | R | KZ | Labels |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Thu 08 Oct 02:10 | XAU | Ping-Pong | OTE | Short | 4112.13 | 4114.81 | 4103.44 | 3.24 | -1.00 (loss) | Asian | UNPROVEN |
| Thu 08 Oct 02:10 | XAU | Classic | OTE | Short | 4112.13 | 4114.81 | 4100.30 | 4.42 | -1.00 (loss) | Asian | UNPROVEN |
| Thu 08 Oct 03:10 | NAS | Ping-Pong | OB | Long | 31178.20 | 31160.70 | 31248.60 | 4.02 | +4.02 (win) | Asian | UNPROVEN |
| Thu 08 Oct 05:35 | XAU | Ping-Pong | OB | Short | 4137.74 | 4143.93 | 4105.56 | 5.21 | +5.21 (win) | Asian | UNPROVEN, COUNTER-TREND |
| Thu 08 Oct 13:30 | NAS | Ping-Pong | OB | Long | 30950.20 | 30908.20 | 31059.00 | 2.59 | +2.59 (win) | NY AM | UNPROVEN, COUNTER-TREND |
| Thu 08 Oct 15:10 | XAU | Classic | OTE | Short | 4128.25 | 4132.87 | 4109.97 | 3.96 | -1.00 (loss) | NY AM | UNPROVEN |
| Fri 09 Oct 04:10 | EU | Ping-Pong | IFVG | Short | 1.12249 | 1.12298 | 1.12108 | 2.88 | -1.00 (loss) | Asian | UNPROVEN, COUNTER-TREND |
| Fri 09 Oct 04:15 | XAU | Ping-Pong | OB | Short | 4171.67 | 4177.58 | 4139.60 | 5.43 | -1.00 (loss) | Asian | UNPROVEN, COUNTER-TREND |
| Fri 09 Oct 09:05 | GU | Ping-Pong | OB | Long | 1.32359 | 1.32302 | 1.32502 | 2.51 | -1.00 (loss) | London Open | UNPROVEN |
| Mon 12 Oct 02:05 | NAS | Ping-Pong | OB | Short | 31055.40 | 31089.80 | 30891.00 | 4.78 | +4.78 (win) | Asian | UNPROVEN, COUNTER-TREND |
| Mon 12 Oct 03:25 | EU | Ping-Pong | OB | Short | 1.12148 | 1.12182 | 1.11951 | 5.79 | +5.79 (win) | Asian | UNPROVEN, COUNTER-TREND |
| Mon 12 Oct 03:50 | GU | Ping-Pong | OB | Short | 1.32491 | 1.32542 | 1.32298 | 3.78 | -1.00 (loss) | Asian | UNPROVEN, COUNTER-TREND |
| Mon 12 Oct 13:05 | XAU | Ping-Pong | OTE | Long | 4171.95 | 4168.27 | 4188.28 | 4.44 | -1.00 (loss) | NY AM | UNPROVEN, COUNTER-TREND |
| Mon 12 Oct 17:10 | XAU | Ping-Pong | OTE | Short | 4170.65 | 4176.09 | 4154.73 | 2.93 | +0.24 (time) | London Close | UNPROVEN |
| Mon 12 Oct 17:10 | XAU | Classic | OTE | Short | 4170.65 | 4176.09 | 4154.73 | 2.93 | +0.24 (time) | London Close | UNPROVEN |
| Tue 13 Oct 03:20 | XAU | Ping-Pong | OTE | Long | 4157.75 | 4153.18 | 4175.89 | 3.97 | -1.00 (loss) | Asian | UNPROVEN, COUNTER-TREND |
| Tue 13 Oct 10:30 | EU | Ping-Pong | IFVG | Short | 1.11910 | 1.11974 | 1.11720 | 2.97 | -1.00 (loss) | London Open | UNPROVEN, COUNTER-TREND |
| Tue 13 Oct 15:15 | GU | Ping-Pong | OTE | Short | 1.32489 | 1.32525 | 1.32398 | 2.50 | -1.00 (loss) | NY AM | UNPROVEN, COUNTER-TREND |
| Wed 14 Oct 02:05 | GU | Classic | OTE | Short | 1.32565 | 1.32586 | 1.32478 | 4.09 | -1.00 (loss) | Asian | UNPROVEN |
| Wed 14 Oct 02:30 | XAU | Ping-Pong | OTE | Long | 4157.37 | 4154.23 | 4166.62 | 2.94 | -1.00 (loss) | Asian | UNPROVEN |
| Wed 14 Oct 03:25 | NAS | Ping-Pong | OB | Short | 30636.40 | 30664.40 | 30558.60 | 2.78 | -1.00 (loss) | Asian | UNPROVEN |

Totals: all n=21, avg +0.42R (sum +8.87R). Ping-Pong n=17 avg +0.68R; Classic n=4 avg -0.69R. Conf: OB n=9 +2.04R; OTE n=10 -0.75R; IFVG n=2 -1.00R; Unicorn n=0. By inst: NAS n=4 +2.60R; EU n=3 +1.26R; XAU n=10 -0.13R; GU n=4 -1.00R.
Caveats: 1 week, tiny n; OB result is driven by 4 wins (2.6-5.8R); no PROMISING (Unicorn) setups printed; 13/21 entries are in the Asian KZ (02-06 SAST); Classic and Ping-Pong took the same XAU OTE entry on 8 Oct 02:10 and 12 Oct 17:10 (double-counted).

## Wed 14 Oct 2026 (live)
Levels (no pre-London levels run today, so computed by the scanner from OANDA/TVC 5m closed candles via TradingView, refreshed 15:44 SAST; last closed 5m bar 15:35-15:40 SAST):
| Inst | PDH | PDL | Asia H | Asia L | London H (final) | London L (final) | Last close |
|---|---|---|---|---|---|---|---|
| NAS | 30715.4 | 30401.2 | 30704.7 | 30558.6 | 30675.0 | 30519.6 | 30391.6 |
| XAU | 4200.625 | 4147.0 | 4170.49 | 4144.455 | 4163.905 | 4141.435 | 4098.785 |
| EU | 1.12047 | 1.11538 | 1.12112 | 1.11982 | 1.12114 | 1.11949 | 1.11356 |
| GU | 1.32594 | 1.32046 | 1.32750 | 1.32538 | 1.32728 | 1.32568 | 1.31994 |
| DXY | 102.587 | 102.162 | 102.207 | 102.076 | 102.226 | 102.092 | 102.725 |
Daily bias (findings/bias.md 15:05 OVERRUN; 15:15 15m now closed): **NAS CT long DROPPED** (15:15 15m close 30364.8 < 30369.8 → BEAR with daily/weekly; LOD 30350.6), XAU BEAR (LOD 4079.73, draw 4066.535), EU BEAR (LOD 1.11142), GU BEAR (15:00 15m close 1.31934 < week low 1.32017; draw 1.31808; LOD 1.31846), DXY BULL (session high 102.875 on 15:20).

### Check log
- 09:27 SAST (London Open), closed candles to 09:20:
  - NAS: Ping-Pong LONG after London swept Asia low 30558.6 (08:00-08:05, extreme 30519.6), MSS 08:40. Confirmations: Unicorn/OB 30574.6, IFVG 30575.5, OTE 30547.45. Stop 30517.6, target Asia high 30704.7. Unicorn entry R:R 2.28. Not filled yet (low since MSS 30585.5); fill window to the 09:40 SAST bar. **ALERTED** as PROMISING, COUNTER-TREND (against 15m BOS trend and daily lean bear). DXY falling = mild support.
  - GU: Ping-Pong long after 08:05 swing-low sweep, IFVG fill 08:45, stopped 09:05; R:R 0.98, below 1:2, not alertable. OTE 1.32666 R:R 2.67 also filled then stopped (low 1.32573 under stop 1.32634).
  - XAU: Asia low 4144.455 swept by the 09:15 bar (low 4143.57); no MSS yet. Watching.
  - EU: no London-KZ setup at that pass (06:00 short IFVG outside scanned kill zones).
- 09:30 SAST (London Open), closed candles to 09:25 (bar open 09:20):
  - NAS: same Unicorn/OB long 30574.6 still unfilled (low since MSS still 30585.5); 4 bars left in fill window (~09:40). No re-alert.
  - EU: NEW Ping-Pong SHORT after 15m swing-high sweep 08:40 (extreme 1.12114), MSS 09:00. Confirmations: OTE 1.120904 R:R 2.04 (unfilled; high since MSS 1.12086), OB 1.12081 R:R 1.37 filled, IFVG 1.12076 R:R 1.12 filled. Stop 1.12124, target nearest opposing pool 1.12022. **ALERTED** OTE as UNPROVEN, COUNTER-TREND (vs daily lean bull; with 15m BOS short). DXY 102.137 bear = mild headwind for the short. Fill window to ~10:00 SAST.
  - XAU: Asia low still swept (extreme 4143.57); no MSS yet. Watching.
  - GU: no new alertable setup (prior long stopped). Fresh 15m swing-low sweeps 09:00/09:10 watching for MSS.
  - DXY: confluence only, no setup.
- 09:37 SAST (London Open), closed candles to 09:35 (last bar open 09:30), fetched 09:36 via TradingView. Per-sweep detail from scripts/pp_live_detail.py (engine rules, no busy filter).
  - EU: the 09:30 alerted OTE short (1.12090 / stop 1.12124 / target 1.12022) is VOID. Its target 1.12022 traded at 09:10 (bar low 1.12002; London low 1.12000 at 09:15) before the entry filled (high since MSS 1.12082). The previous pass missed this. Opposite pool swept, so per rule 3 the next look is a long; 09:10 sweep of 15m swing low 1.12022 has no MSS yet. Correction sent to Hilda; no new alert.
  - NAS: Unicorn/OB long 30574.6 still unfilled (low since MSS 30585.5; 09:30 bar low 30594.5). Last bar of fill window is 09:35 (window ends ~09:40); the separate 09:41 recheck routine handles it. No re-alert.
  - XAU: Asia low 4144.455 swept again; new extreme 4143.255 (09:30 bar). No MSS yet. Watching.
  - GU: 09:00/09:10 swing-low sweeps (extreme 1.32573), no MSS yet. Earlier long stopped. Nothing alertable.
  - DXY: 102.122, drifting lower from 102.176 (09:15); confluence only.
  - Classic: no with-trend HTF-OTE sweep setups at 1:2+ (EU 08:20 with-trend long OTE filled 09:00 and stopped; GU 08:40 long stopped).

- 09:42 SAST recheck (NAS Unicorn/OB long 30574.6 / stop 30517.6 / target 30704.7), OANDA:NAS100USD 5m closed candles via TradingView, fetched 09:42; last closed bar 09:35 (low 30596.8):
  - **EXPIRED, never filled.** Lowest low after the 08:40 MSS was 30585.5 (09:00 bar), 10.9 pts above the entry; the fill window closed with the 09:35 bar. No trade, 0R.
  - Current price 30609.6 (forming 09:40 bar). Target 30704.7 (Asia high) not reached; London high so far 30642.1.

- 09:42-09:48 SAST (London Open) scanner pass. First fetch 09:41 (closed to 09:40), re-fetched 09:47 once the 09:40 bar closed, so closed candles to 09:45 (last 5m bar open 09:40). scripts/pp_live_scan.py + pp_live_detail.py via TradingView. Levels table refreshed (XAU London low 4143.255 and last closes changed).
  - EU: NEW Ping-Pong LONG (rule 3 reverse after the short's target pool 1.12022 was swept). Sweep of 15m swing low 1.12022 at 09:10, extreme 1.12000 (09:15), MSS 09:35 (close 1.12072 above 08:10 fractal high 1.12068; thin 0.4-pip break). Confirmations: OTE 1.12024 R:R 2.63, unfilled (09:40 bar low 1.12034, 1.0 pip short of it). Unicorn 1.12042 (R:R 1.38), IFVG 1.12038 (1.58) and OB 1.12050 (1.07) are all below 1:2. Stop 1.11990, target 1.12114 (London high). Void check since the 09:10 sweep: lowest low 1.12000 (stop not hit), highest high 1.12082 (target not hit), so it is valid. Fill window runs to the 10:35 bar (~10:40 SAST). Labels: UNPROVEN. With the daily lean bull (not counter to daily) but against 15m BOS (down) and monthly bear. DXY 102.150 (bear bias) = mild support. **ALERTED** as UNPROVEN (with daily lean bull; vs 15m BOS down).
  - NAS: Unicorn/OB long 30574.6 confirmed **EXPIRED unfilled**. The last engine fill bar was 09:40 (MSS 08:40 + 12 bars; low 30603.6). Lowest low since MSS 30585.5. Stop 30517.6 and target 30704.7 were never touched, so it was not invalid and needs no correction. Agrees with the 09:42 recheck. No re-alert.
  - XAU: Asia low 4144.455 swept (extreme 4143.255 at 09:30); still no MSS (sweep windows 08:50 and 09:15 open). Last close 4148.275. Watching.
  - GU: 09:00/09:10 15m swing-low sweeps (extreme 1.32573), no MSS yet. Nothing alertable.
  - DXY: 102.150, confluence only.
  - Classic: no new with-trend HTF-OTE setups at 1:2+.

- 09:52 SAST (London Open) scanner pass, fetched 09:51 via TradingView, closed candles to 09:50 (last 5m bar open 09:45). scripts/pp_live_scan.py + pp_live_detail.py.
  - EU: the 09:48 alerted OTE long 1.12024 **FILLED** on the 09:45 bar (low 1.12020). Checked every bar since the 09:10 sweep: lowest low 1.12000 (09:15, before fill), stop 1.11990 never touched; highest high 1.12082, target 1.12114 not reached. Valid fill, no correction needed. Open at 1.12028 close (about +0.1R). No re-alert.
  - NAS: no new sweep since the 08:40 MSS setup (expired unfilled). Last close 30616.0. Nothing alertable.
  - XAU: Asia low 4144.455 sweep (extreme 4143.255) still has no MSS; 09:15 sweep window still open. Last close 4148.625. Watching.
  - GU: 09:00/09:10 15m swing-low sweeps (extreme 1.32573), no MSS yet, windows open. Last close 1.32623. Nothing alertable.
  - DXY: 102.160, ticking up off 102.121 (mild headwind for EU long); confluence only.
  - Classic: no new with-trend HTF-OTE sweep setups at 1:2+.

- 09:58 SAST (London Open) scanner pass, fetched 09:58 via TradingView, closed candles to 09:55 (last 5m bar open 09:50). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_0957.txt.
  - EU: the 09:48 alerted OTE long 1.12024 still **OPEN**. Filled 09:45. Through the 09:50 bar: low since fill 1.12002 (stop 1.11990 not hit), high 1.12046 (target 1.12114 not hit). Close 1.12004 ≈ −0.59R mark-to-market. No VOID, no correction. Fill window still open (engine W=12 from MSS 09:35 → ~10:35). No re-alert.
  - NAS: expired Unicorn/OB long unchanged. Last close 30620.4. Nothing new alertable.
  - XAU: Asia low 4144.455 / 09:15 swing-low sweeps still no MSS (window open; 08:50 window expired). Extreme 4143.255. Last close 4148.415. Watching.
  - GU: 09:00/09:10 swing-low sweeps (extreme 1.32573) still no MSS (windows open). Last close 1.32601. Nothing alertable.
  - DXY: 102.179, confluence only (mild tick up; slight headwind for EU long).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No correction.

- 10:06 SAST (London Open) scanner pass, fetched 10:06 via TradingView, closed candles to 10:05 (last 5m bar open 10:00). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1006.txt.
  - EU: the 09:48 alerted OTE long 1.12024 **STOPPED −1.00R**. Filled 09:45. 09:55 bar low 1.11992 (0.2 pip above stop 1.11990); 10:00 bar low 1.11974 took the stop. Target 1.12114 never reached (high since fill 1.12046). Outcome −1R; no VOID (was filled). No re-alert. New Asia-low sweep 10:00 at 1.11982 — no MSS yet. Watching.
  - NAS: expired Unicorn/OB long unchanged. Last close 30625.6. Nothing new alertable (prior London long fill window closed 09:40).
  - XAU: Asia low 4144.455 / 09:15 swing-low sweeps still no MSS (window open; 07:45 and 08:50 expired). Extreme 4143.255. Last close 4151.425. Watching.
  - GU: 09:10 and 10:00 15m swing-low sweeps (extreme 1.32568 / 1.32573) still no MSS (windows open). Prior long stopped. Last close 1.32584. Nothing alertable.
  - DXY: 102.198, London high so far 102.205; confluence only (tick up = mild headwind for EU longs).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction (EU was filled then stopped).

- 10:11 SAST (London Open) scanner pass. First fetch ~10:09 only had closed candles to 10:05 (10:05 bar still forming), so re-fetched 10:10 for closed candles to 10:10 (last 5m bar open 10:05). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1011.txt (scan_1010.txt = the earlier fetch).
  - XAU: NEW Ping-Pong LONG. Asia low 4144.455 (= 15m swing low) swept 09:15, extreme 4143.255 (09:30), MSS 10:05 (bar closed 4153.82, high 4153.96). Stop 4142.755 (extreme - 0.5 buffer), target London high 4163.905. Confirmations: IFVG 4148.05 R:R 3.00, OTE 4146.41 R:R 4.79, OB 4146.02 R:R 5.48. No Unicorn. Void check over every 5m bar 09:15-10:05: lowest low 4143.255 (stop not hit), highest high 4153.96 (target not hit); not filled yet (MSS is the last closed bar). Engine fill window 12 bars to the 11:05 bar; London Open KZ ends 11:00 SAST. Labels: UNPROVEN, COUNTER-TREND (daily bias bear; 15m BOS down; bias.md gate needs 1H close >4156 to lift bearish read). DXY 102.150 falling off 102.205 = supports the long. Note: the same 10:05 bar traded above 4152.6, the hard stop on Confluence Bot's gold short idea B. US CPI 14:30 SAST. **ALERTED** (IFVG primary, OB/OTE deeper alternatives).
  - NAS: 10:05 bar swept 15m swing high 30642.1 (high 30651.4), no MSS yet (window open). Earlier Unicorn/OB long expired unfilled. Last close 30646.2. Watching.
  - EU: alerted OTE long already stopped −1R at 10:00. 10:00 Asia-low sweep 1.11982 (extreme 1.11974), no MSS yet (window open). Last close 1.12054. Nothing alertable.
  - GU: 10:00 15m swing-low sweep 1.32573 (extreme 1.32568), no MSS yet (window open); 09:00/09:10 windows expired. Last close 1.32638. Nothing alertable.
  - DXY: 102.150, confluence only.
  - Classic: no new with-trend HTF-OTE sweep setups at 1:2+.

- 10:26 SAST (London Open) scanner pass (this is the 10:11 NY-schedule slot run late: an attempt to wait for the 10:10 bar was cut off when the box restarted ~10:15, and the 10:16/10:21 slots wrote nothing). Fetched 10:26 via TradingView, closed candles to 10:25 (last 5m bar open 10:20). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1026.txt and detail_1026.txt.
  - GU: NEW Ping-Pong LONG. 15m swing low 1.32573 swept 10:00 (extreme 1.32568), MSS 10:15 (close 1.32650). Stop 1.32558 (extreme - 1 pip buffer), target London high 1.32728. Confirmations: IFVG 1.32598 R:R 3.25, OB 1.32596 R:R 3.47, OTE 1.32593 R:R 3.89. No Unicorn. Void check over every 5m bar 10:00-10:20: lowest low 1.32568 (stop not hit), highest high 1.32658 (target not hit); not filled (low since MSS 1.32637). Fill window 12 bars from MSS (to ~11:15 SAST bar); London Open KZ ends 11:00 SAST. Labels: UNPROVEN (with daily GU bull; against 15m BOS down). DXY 102.153 under London high 102.205, bear bias = supports the long. GU was the worst instrument in the backtests. **ALERTED** (IFVG primary, OB/OTE deeper alternatives).
  - XAU: alerted IFVG long 4148.05 still **UNFILLED and valid**. Every bar since the 09:15 sweep checked: lowest low after MSS 4150.395 (10:20 bar), stop 4142.755 never touched, highest high 4157.875 (10:15), target 4163.905 not reached. Fill window to ~11:05 bar. No re-alert, no correction.
  - NAS: 10:05 sweep of 15m swing high 30642.1, London high now 30675.0, still no MSS (window open). Last close 30642.6. Nothing alertable.
  - EU: 10:00 Asia-low sweep 1.11982 (extreme 1.11974) still no MSS (window open). Earlier alerted long stopped −1R. Last close 1.12056. Nothing alertable.
  - DXY: 102.153, confluence only.
  - Classic: no new with-trend HTF-OTE sweep setups at 1:2+.

- 10:35 SAST (London Open) scanner pass, fetched 10:35 via TradingView, closed candles to 10:35 (last 5m bar open 10:30). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1035.txt and detail_1035.txt.
  - XAU: alerted IFVG long 4148.05 still **UNFILLED and valid**. Every bar since the 09:15 sweep checked: lowest low 4143.255 (stop 4142.755 not hit), highest high 4157.875 (target 4163.905 not hit). Low since MSS 10:05 is 4148.23 (10:30 bar) — 0.18 above entry. Fill window to ~11:05 bar. No re-alert, no correction.
  - GU: alerted IFVG long 1.32598 still **UNFILLED and valid**. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32662 (target 1.32728 not hit). Low since MSS 10:15 is 1.32606 (10:30 bar) — 0.8 pip above entry. Fill window to ~11:15 bar. No re-alert, no correction.
  - NAS: 10:05 sweep of 15m swing high 30642.1 still no MSS (window open; London high 30675.0). Earlier Unicorn/OB long expired unfilled. Last close 30646.8. Nothing alertable.
  - EU: 10:00 Asia-low sweep 1.11982 (extreme 1.11974) still no MSS (window open). Earlier alerted long stopped −1R. Last close 1.12014. Nothing alertable.
  - DXY: 102.182, confluence only (tick up off London high 102.205 = mild headwind for XAU/GU longs).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 10:40 SAST (London Open) scanner pass, fetched 10:41 via TradingView, closed candles to 10:40 (last 5m bar open 10:35). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1040.txt and detail_1040.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1040.md.
  - XAU: alerted IFVG long 4148.05 **FILLED** on the 10:35 bar (low 4144.02; also filled alt OTE 4146.41 / OB 4146.02). Every bar since the 09:15 sweep checked: lowest low 4143.255 (stop 4142.755 not hit), highest high 4157.875 (target 4163.905 not hit). Close 4145.255 ≈ −0.53R mark-to-market. Still OPEN; fill window to ~11:05. No VOID. No re-alert (status only).
  - GU: alerted IFVG long 1.32598 **FILLED** on the 10:35 bar (low 1.32588; also filled alt OB 1.32596 / OTE 1.32593). Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32662 (target 1.32728 not hit). Close 1.32601 ≈ +0.07R mark-to-market. Still OPEN; fill window to ~11:15. No VOID. No re-alert (status only).
  - NAS: NEW Ping-Pong SHORT. 15m swing high 30642.1 swept 10:05 (extreme 30675.0 at 10:15 = London high), MSS 10:35 (close 30621.0). Stop 30677.0 (extreme + 2 pt buffer), target London low 30519.6. Confirmations: Unicorn 30651.8 R:R 5.25, IFVG 30651.4 R:R 5.15, OB 30645.8 R:R 4.04, OTE 30658.8 R:R 7.64. Void check over every 5m bar 10:05-10:35: highest high 30675.0 (stop not hit), lowest low 30620.0 (target not hit); not filled yet (MSS is the last closed bar; engine fill from next bar). Fill window 12 bars from MSS (to ~11:35 SAST bar); London Open KZ ends 11:00 SAST. Labels: PROMISING (Unicorn). With daily lean bear (not COUNTER-TREND); with 15m trend at sweep (counter15m=False; detail also notes Classic eligibility). DXY 102.207 / London high 102.208 = supports the short. **ALERTED** (Unicorn primary; OTE/IFVG/OB alternatives).
  - EU: 10:00 Asia-low sweep 1.11982 still no MSS (window open); London low now 1.11973 (10:35 bar). Earlier alerted long stopped −1R. Last close 1.11974. Nothing alertable.
  - DXY: 102.207, London high 102.208; confluence only (firm = headwind for open XAU/GU longs, support for NAS short).
  - Classic: no separate Classic HTF-OTE print at 1:2+ beyond the NAS with-trend note above (no invented Classic levels).
  - **NEW alert:** NAS Unicorn short. Status: XAU + GU filled and open. No VOID correction.

- 10:51 SAST (London Open) scanner pass, fetched 10:51 via TradingView, closed candles to 10:50 (last 5m bar open 10:45). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1051.txt and detail_1051.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1051.md.
  - XAU: alerted IFVG long 4148.05 still **OPEN**. Filled 10:35. Every bar since the 09:15 sweep checked: lowest low 4142.99 (10:45 bar; stop 4142.755 not hit — 0.235 above), highest high 4157.875 (target 4163.905 not hit). Close 4143.77 ≈ −0.81R mark-to-market. New 10:45 sweep of 15m swing low 4143.255 — no MSS yet (window open). Fill window to ~11:05. No VOID. No re-alert.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32662 (target 1.32728 not hit). Low since fill 1.32583 (10:45). Close 1.32600 ≈ +0.05R. Fill window to ~11:15. No VOID. No re-alert.
  - NAS: alerted Unicorn short 30651.8 still **UNFILLED and valid**. Every bar since the 10:05 sweep checked: highest high 30675.0 (stop 30677.0 not hit), lowest low 30602.6 (target 30519.6 not hit). High since MSS (next-bar fill rule) 30629.8 (10:40); MSS bar itself printed high 30651.8 = entry but engine does not fill on the MSS bar. Fill window to ~11:35; London Open KZ ends 11:00 SAST. Classic eligibility noted on same sweep (same levels) — no separate Classic alert. No re-alert.
  - EU: 10:00 Asia-low sweep 1.11982 still no MSS; also 10:40 sweeps of 15m swing lows 1.11962 / 1.11972 — no MSS (windows open). London low now 1.11959. Earlier alerted long stopped −1R. Last close 1.11964. Nothing alertable.
  - DXY: 102.218, London high now 102.222; confluence only (firm = headwind for open XAU/GU longs, support for NAS short).
  - Classic: no new with-trend HTF-OTE setups at 1:2+ beyond the NAS with-trend note above.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 11:01 SAST (London Open, last slot) scanner pass. First fetch 10:59 (closed to 10:55), re-fetched 11:00 once the 10:55 bar closed, so closed candles to 11:00 (last 5m bar open 10:55). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1100.txt and detail_1100.txt (scan_1059/detail_1059 = earlier fetch). Backup findings/pingpong.md → data/pp_live/pingpong_bak_1059.md and pingpong_bak_1101.md. Levels table refreshed.
  - XAU: alerted IFVG long 4148.05 **STOPPED −1.00R** confirmed on 5m: 10:50 bar low 4142.545 took stop 4142.755 (engine: OTE/OB/IFVG all loss, exit 10:50). Agrees with the 10:57 correction note. It was filled first, so it is a loss, not VOID; no correction needed. 10:55 bar made a new London low 4141.435. 10:45 sweep of 15m swing low 4143.255 still no MSS (window open). Last close 4143.24.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32662 (target 1.32728 not hit). Low since fill 1.32583, high since fill 1.32635. Close 1.32617 ≈ +0.48R. No re-alert.
  - NAS: alerted Unicorn short 30651.8 still **UNFILLED and valid**. Every bar since the 10:05 sweep checked: highest high 30675.0 (stop 30677.0 not hit), lowest low 30588.8 (10:55; target 30519.6 not hit). High since MSS 30629.8 (10:40), 22 pts below entry. Fill window to ~11:35 SAST, past the London Open KZ; no scanner slot until 13:01, so its fill/expiry gets checked then. No re-alert.
  - EU: 10:00 Asia-low sweep 1.11982 expired with no MSS. 10:40 sweeps 1.11962/1.11972 and new 10:55 sweep 1.11951 (London low 1.11949), no MSS (windows open). Last close 1.11950. Nothing alertable.
  - DXY: 102.225, London high 102.226; confluence only (firm dollar = headwind for GU long, support for NAS short).
  - Classic: no new with-trend HTF-OTE setups at 1:2+ beyond the NAS with-trend note.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 13:06 SAST (NY AM) scanner pass. First fetch 13:03 (closed to 12:55), re-fetched 13:05 once the 13:00 bar closed, so closed candles to 13:05 (last 5m bar open 13:00). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1305.txt and detail_1305.txt (scan_1302/detail_1302 = earlier fetch). Backup findings/pingpong.md → data/pp_live/pingpong_bak_1302.md. Levels table refreshed.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit — 3.4 pips short at 12:20). Low since fill 1.32583, high since fill 1.32694. Close 1.32610 ≈ +0.30R. No re-alert.
  - NAS: alerted Unicorn short 30651.8 **EXPIRED, never filled.** Fill window closed with the 11:35 bar. Highest high since MSS 30629.8 (10:40), 22 pts below entry. Every bar since the 10:05 sweep checked: highest high 30675.0 (stop 30677.0 not hit), lowest low 30529.6 on the 13:00 bar (target 30519.6 not hit — 10 pts short). Not VOID; no correction. 13:00 bar also swept 15m swing low 30556.0 — no MSS yet (window open). Last close 30541.0.
  - XAU: alerted IFVG long already STOPPED −1R (10:50). Midday Ping-Pong long after 12:00 sweep / MSS 12:15 (OTE/OB/IFVG) filled 12:20 and stopped 12:25 −1R — between London Open and NY AM, not a KZ alert. 13:00 bar new low 4136.135. Nothing alertable. Last close 4137.47.
  - EU: earlier alerted long already STOPPED −1R. Sweeps of 15m swing lows 1.11902/1.11904 (12:25) and 1.11882 (12:30) — no MSS yet (windows open). Last close 1.11892. Nothing alertable.
  - DXY: 102.262, session high 102.266 on the 13:00 bar (above London high 102.226); confluence only (firm dollar = headwind for open GU long; supports shorts if they appear).
  - GU note (not alerted): Ping-Pong SHORT after 12:20 sweep of 15m swing high 1.32692, MSS 12:50, OTE 1.32676 R:R 3.37 / OB 1.32673 R:R 2.90, stop 1.32704, target 1.32583. Unfilled (best high since MSS 1.32666). Void-check since sweep: high 1.32694 / low 1.32606 — stop/target untouched. Fill window to ~13:50. Skipped: opposite GU long still OPEN; MSS between KZs; UNPROVEN + COUNTER-TREND vs daily bull.
  - Classic: no new with-trend HTF-OTE setups at 1:2+ in NY AM.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 13:11 SAST (NY AM) scanner pass, fetched 13:10 via TradingView, closed candles to 13:10 (last 5m bar open 13:05). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1311.txt and detail_1311.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1311.md. Levels unchanged except last closes (NAS 30544.5, XAU 4137.765, EU 1.11894, GU 1.32616, DXY 102.253).
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit). Low since fill 1.32583, high since fill 1.32694. Close 1.32616 ≈ +0.45R (engine shows it as "eod" at the 13:05 bar, which is the engine's day cut, not a stop or target). No re-alert.
  - GU note (not alerted): 12:50 MSS Ping-Pong short (OTE 1.32676 / OB 1.32673) **EXPIRED unfilled** with the 13:05 bar (high since MSS 1.32666). Stop 1.32704 and target 1.32583 untouched.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open). Alerted Unicorn short already expired unfilled at 11:35; its target 30519.6 still not reached (low 30529.6). Last close 30544.5. Nothing alertable.
  - XAU: new low 4136.025 (13:05 bar), below London low 4141.435 and PDL 4147.0; 12:00 sweep setup already filled and stopped −1R at 12:25 (not a KZ alert). No new sweep/MSS setup. Last close 4137.765. Nothing alertable.
  - EU: 12:25/12:30 sweeps of 15m swing lows 1.11902/1.11904/1.11882 still no MSS (windows open); low 1.11878. Last close 1.11894. Nothing alertable.
  - DXY: 102.253, session high 102.266; confluence only (firm dollar = headwind for open GU long).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 13:16 SAST (NY AM) scanner pass, fetched 13:15 via TradingView, closed candles to 13:15 (last 5m bar open 13:10). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1315.txt and detail_1315.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1315.md. Last closes: NAS 30564.6, XAU 4138.99, EU 1.11922, GU 1.32641, DXY 102.242.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit). Low since fill 1.32583 (13:10 low 1.32597), high since fill 1.32694. Close 1.32641 ≈ +1.08R. Engine marks eod at 13:10 (day cut, not stop/target). No re-alert.
  - GU note (not alerted): 12:50 MSS Ping-Pong short (OTE 1.32676 / OB 1.32673) still **UNFILLED** (high since MSS 1.32666). Detail fill window still open past 13:10 (to ~13:50); prior 13:11 "expired at 13:05" was the engine day-cut clip, not a true expiry. Still skipped: opposite GU long OPEN; MSS between KZs; UNPROVEN + COUNTER-TREND vs daily bull.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open). 13:10 bar bounced to 30564.6. Alerted Unicorn short already expired unfilled. Nothing alertable.
  - XAU: no new sweep/MSS in NY AM; 12:00 setup already stopped −1R. Last close 4138.99 (13:10 high 4141.155). Nothing alertable.
  - EU: 12:25/12:30 sweeps of 15m swing lows 1.11902/1.11904/1.11882 still no MSS (windows open); low since 1.11878. Last close 1.11922. Nothing alertable.
  - DXY: 102.242, session high 102.271 on the 13:10 bar; confluence only (firm dollar = mild headwind for open GU long).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 13:21 SAST (NY AM) scanner pass, fetched 13:20 via TradingView once the 13:15 bar closed, so closed candles to 13:20 (last 5m bar open 13:15). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1320.txt and detail_1320.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1320.md. Levels unchanged; last closes: NAS 30565.0, XAU 4142.52, EU 1.11932, GU 1.32650, DXY 102.236.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (12:20; target 1.32728 not hit). Low since fill 1.32583, high since fill 1.32694 (13:15 bar 1.32625-1.32660). Close 1.32650 ≈ +1.30R. Engine "eod" at 13:15 is the day cut, not stop/target. No re-alert.
  - GU note (not alerted): 12:50 MSS Ping-Pong short (OTE 1.32676 / OB 1.32673) still **UNFILLED** (high since MSS 1.32666); stop 1.32704 and target 1.32583 untouched. Still skipped (opposite GU long OPEN; MSS between KZs; UNPROVEN + COUNTER-TREND vs daily bull).
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open); 13:15 bar 30560.0-30576.2. Alerted Unicorn short already expired unfilled. Nothing alertable.
  - XAU: 13:15 bar bounced to 4143.625 (low of day 4136.025 at 13:05); no new pool sweep/MSS in NY AM (London low / PDL already swept earlier; 12:00 setup stopped −1R). Nothing alertable.
  - EU: 12:25/12:30 sweeps of 15m swing lows 1.11902/1.11904/1.11882 still no MSS (windows open); low since 1.11878, 13:15 bar high 1.11939. Nothing alertable.
  - DXY: 102.236, easing off session high 102.271 (13:10); confluence only (softer dollar = mild support for open GU long).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 13:26 SAST (NY AM) scanner pass. First fetch 13:24/13:25 (closed to 13:25; last 5m bar open 13:20); re-verified 13:27 with scripts/pp_live_scan.py + pp_live_detail.py (same closed set). Raw stdout data/pp_live/scan_1326.txt and detail_1326.txt (also scan_1325/detail_1325). Backup findings/pingpong.md → data/pp_live/pingpong_bak_1325.md and pingpong_bak_1326.md. Levels unchanged; last closes: NAS 30559.4, XAU 4139.775, EU 1.11921, GU 1.32622, DXY 102.248.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (12:20; target 1.32728 not hit). Low since fill 1.32583, high since fill 1.32694 (13:20 bar 1.32618-1.32652). Close 1.32622 ≈ +0.60R. Engine "eod" at 13:20 is the day cut, not stop/target. No re-alert.
  - GU note (not alerted): 12:50 MSS Ping-Pong short (OTE 1.32676 R:R 3.37 / OB 1.32673 R:R 2.90), stop 1.32704, target 1.32583, still **UNFILLED** (high since MSS 1.32666; low 1.32597). Fill window still open (7/12 bars through 13:20; ends ~13:50). An earlier draft of this pass wrongly marked it expired at 13:20 — corrected on re-verify. Still skipped: opposite GU long OPEN; MSS between KZs; UNPROVEN + COUNTER-TREND vs daily bull. Never alerted → no correction.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open); since 13:00 high 30576.2 / low 30529.6. Alerted Unicorn short already expired unfilled at 11:35. Nothing alertable.
  - XAU: 13:20 close 4139.775; low of day 4136.025 (13:05). No new pool sweep/MSS in NY AM; 12:00 setup stopped −1R. Nothing alertable.
  - EU: 12:30 sweep of 15m swing low 1.11882 still no MSS (window open); 12:25 sweeps expired. Since 12:30 low 1.11878 / high 1.11942. Nothing alertable.
  - DXY: 102.248, under session high 102.271 (13:10); confluence only (firm dollar = mild headwind for open GU long).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 13:31 SAST (NY AM) scanner pass, fetched 13:32 via TradingView, closed candles to 13:30 (last 5m bar open 13:25). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1331.txt and detail_1331.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1331.md. Levels unchanged; last closes: NAS 30549.0, XAU 4139.265, EU 1.11928, GU 1.32627, DXY 102.247.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (12:20; target 1.32728 not hit). Low since fill 1.32583, high since fill 1.32694 (13:25 bar 1.32617-1.32636). Close 1.32627 ≈ +0.73R. Engine "eod" at 13:25 is the day cut, not stop/target. No re-alert.
  - GU note (not alerted): 12:50 MSS Ping-Pong short (OTE 1.32676 / OB 1.32673), stop 1.32704, target 1.32583, still **UNFILLED** (high since MSS 1.32666; low 1.32597); fill window last bar 13:25 per engine, so effectively expiring. Stop/target untouched. Never alerted → no correction.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open); 13:25 bar 30545.0-30562.8. Alerted Unicorn short already expired unfilled. Nothing alertable.
  - XAU: 13:25 close 4139.265; low of day 4136.025 (13:05), high since 13:00 4143.625. No new pool sweep/MSS in NY AM; 12:00 setup stopped −1R. Nothing alertable.
  - EU: 12:30 sweep of 15m swing low 1.11882 now **expired** with no MSS. Since 13:00 low 1.11881 / high 1.11942. Nothing alertable.
  - DXY: 102.247, under session high 102.271 (13:10); confluence only.
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 13:40 SAST (NY AM) scanner pass. Waited for 13:35 bar close; fetched 13:40 via TradingView, closed candles to 13:40 (last 5m bar open 13:35). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1340.txt and detail_1340.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1340.md. Levels last closes refreshed; last closes: NAS 30562.8, XAU 4139.545, EU 1.1194, GU 1.32616, DXY 102.234.
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit). Low since fill 1.32582 (13:30), high since fill 1.32694. Close 1.32616 ≈ +0.45R. Engine "eod" at 13:35 is the day cut, not stop/target. No re-alert.
  - GU note (not alerted): 12:50 MSS Ping-Pong short (OTE 1.32676 R:R 3.37 / OB 1.32673 R:R 2.90), stop 1.32704, target 1.32583 — **VOID**: target 1.32583 hit on the 13:30 bar (low 1.32582) before fill (high since MSS 1.32666). Never alerted → no correction. Fill window moot.
  - GU: NEW 13:30 sweep of 15m swing low 1.32583 (extreme 1.32582) — no MSS yet (window open). Watching.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open; ~4 bars left → ~14:00). Need close above fractal ~30576.2; best closes 30569.4 (13:30), 30565.0 (13:15). Alerted Unicorn short already expired unfilled. Nothing alertable.
  - XAU: no new NY AM sweep/MSS with open fill window; 10:50 and 12:25 setups already −1R. LOD 4136.025 (13:05). Last close 4139.545. Nothing alertable.
  - EU: 12:30 sweep of 1.11882 confirmed expired no MSS; earlier alerted long already −1R. NY AM H/L 1.11943 / 1.11881. Last close 1.1194. Nothing alertable.
  - DXY: 102.234, under session high 102.271 (13:10); confluence only (mild headwind for open GU long).
  - Classic: no new with-trend HTF-OTE setups at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.

- 13:51 SAST (NY AM) scanner pass, fetched 13:51 via TradingView, closed candles to 13:50 (last 5m bar open 13:45). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1351.txt and detail_1351.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1351.md. Levels unchanged; last closes: NAS 30561.0, XAU 4138.42, EU 1.11971, GU 1.32652, DXY 102.211.
  - GU: NEW Ping-Pong LONG. 15m swing low 1.32583 swept 13:30 (extreme 1.32582), MSS 13:45 (close 1.32652). Stop 1.32572 (extreme - 1 pip), target 15m swing high 1.32694. Confirmations: OTE 1.32603 R:R 2.98 (engine); Unicorn 1.32630 (R:R 1.10) and OB 1.32637 (0.88) below 1:2. Void check over every 5m bar 13:30-13:45: lowest low 1.32582 (stop not hit), highest high 1.32652 (target not hit); not filled (MSS is the last closed bar). Fill window 12 bars from MSS (to ~14:45 SAST bar); US CPI 14:30 SAST falls inside it. Labels: UNPROVEN (OTE, not Unicorn); with daily GU bull and with 15m at the sweep (engine flags Classic eligibility on the same levels; no separate Classic alert). DXY 102.211 easing off session high 102.271 = supports the long. Note: the 10:28 GU long is still open in the same direction. Lot sizing uses the [REDACTED: account balance].md (0.5% = [REDACTED]): stop 3.1 pips x $10/pip/lot = $31 per lot → 7.98 lots; [REDACTED: third-party account sizing]
  - GU: alerted IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit). Low since fill 1.32582 (13:30). Close 1.32652 ≈ +1.35R. No re-alert.
  - GU note: 12:50 MSS short stays VOID (target hit 13:30 before fill); never alerted.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open to ~14:00; fractal ~30576.2, best close 30569.4). Nothing alertable.
  - XAU: no new NY AM sweep/MSS; 10:50 and 12:25 setups already −1R. Last close 4138.42 (LOD 4136.025). Nothing alertable.
  - EU: all NY-morning sweeps expired with no MSS. Last close 1.11971. Nothing alertable.
  - DXY: 102.211, falling off session high 102.271 (13:10); confluence only (supports GU long).
  - Classic: no separate Classic print beyond the GU with-trend note.
  - **NEW alert:** GU OTE long. No VOID correction.

- 13:56 SAST (NY AM) scanner pass. Waited for the 13:50 bar to close; fetched 13:55 via TradingView, closed candles to 13:55 (last 5m bar open 13:50). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1356.txt and detail_1356.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1356.md. Levels unchanged; last closes: NAS 30565.4, XAU 4139.9, EU 1.11961, GU 1.32660, DXY 102.215.
  - GU: alerted 13:51 OTE long 1.32603 / stop 1.32572 / target 1.32694 still **UNFILLED and valid**. Every bar since the 13:30 sweep checked: lowest low 1.32582 (13:30; stop not hit), highest high 1.32663 (13:50; target not hit). Low since MSS 1.32640 (13:50 bar), 3.7 pips above entry. Fill window to ~14:45; CPI 14:30. No re-alert, no correction.
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit). Close 1.32660 ≈ +1.55R. Engine "eod" at 13:50 is the day cut, not stop/target. No re-alert.
  - GU note: 12:50 MSS short stays VOID (target hit 13:30 before fill); never alerted.
  - NAS: 13:00 sweep of 15m swing low 30556.0 (extreme 30529.6) still no MSS (window open to ~14:00; fractal ~30576.2, 13:50 bar high 30570.8 / close 30565.4). Nothing alertable.
  - XAU: no new NY AM sweep/MSS; 10:50 and 12:25 setups already −1R. Last close 4139.9 (LOD 4136.025). Nothing alertable.
  - EU: all NY-morning sweeps expired with no MSS; no new sweep. Last close 1.11961. Nothing alertable.
  - DXY: 102.215, flat under session high 102.271; confluence only.
  - Classic: no separate Classic print beyond the GU with-trend note.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 14:01 SAST (NY AM) scanner pass, fetched 14:00 via TradingView, closed candles to 14:00 (last 5m bar open 13:55). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1401.txt and detail_1401.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1401.md. Levels last closes refreshed; last closes: NAS 30575.6, XAU 4139.465, EU 1.11926, GU 1.32658, DXY 102.234.
  - NAS: NEW Ping-Pong LONG. 15m swing low 30556.0 swept 13:00 (extreme 30529.6), MSS 13:55 (close 30575.6 above fractal). Stop 30527.6 (extreme - 2 pt buffer), target 15m swing high 30617.5. Confirmations: OTE 30544.9 R:R 4.18 (engine); Unicorn 30560 (R:R 1.77), IFVG 30563.6 (1.50), OB 30570.4 (1.10) all below 1:2. Void check over every 5m bar 13:00-13:55: lowest low 30529.6 (stop not hit), highest high 30581.6 (target not hit); not filled (MSS is the last closed bar; engine fills from next bar). Fill window 12 bars from MSS (to ~14:55 SAST bar); US CPI 14:30 SAST falls inside it. Labels: UNPROVEN (OTE, not Unicorn); COUNTER-TREND vs daily lean bear / bias COUNTER-TREND long on hold (needs close above 30677). Engine with 15m at the sweep (counter15m=False; Classic eligibility noted — no separate Classic alert). DXY 102.234 under session high 102.271 = mild headwind for the long. Lot sizing ([REDACTED balance], 0.5%): stop 17.3 pts × $1/pt/lot → 14.31 lots; [REDACTED: third-party account sizing]
  - GU: alerted 13:51 OTE long 1.32603 / stop 1.32572 / target 1.32694 still **UNFILLED and valid**. Every bar since the 13:30 sweep checked: lowest low 1.32582 (stop not hit), highest high 1.32666 (13:55; target not hit). Low since MSS 1.32622 (13:55), 1.9 pips above entry. OB 1.32637 / Unicorn 1.32630 filled on 13:55 but both below 1:2 (engine eod clip). Fill window to ~14:45; CPI 14:30. No re-alert, no correction.
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32694 (target 1.32728 not hit). Close 1.32658 ≈ +1.50R. Engine "eod" at 13:55 is the day cut, not stop/target. No re-alert.
  - GU note: 12:50 MSS short stays VOID (target hit 13:30 before fill); never alerted.
  - XAU: no new NY AM sweep/MSS with open fill window; 10:50 and 12:25 setups already −1R. Last close 4139.465 (LOD 4136.025). Nothing alertable.
  - EU: all NY-morning sweeps expired with no MSS; no new sweep. Last close 1.11926. Nothing alertable.
  - DXY: 102.234, under session high 102.271; confluence only (mild headwind for NAS/GU longs).
  - Classic: no separate Classic print beyond the NAS with-trend note.
  - **NEW alert:** NAS OTE long. No VOID correction.

- 14:06 SAST (NY AM) scanner pass, fetched 14:06 via TradingView once the 14:00 bar closed, so closed candles to 14:05 (last 5m bar open 14:00). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1405.txt and detail_1405.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1405.md. Levels last closes refreshed; last closes: NAS 30604.8, XAU 4145.53, EU 1.11956, GU 1.32694, DXY 102.207.
  - GU: alerted 13:51 OTE long 1.32603 / stop 1.32572 / target 1.32694 is **VOID**. Its target 1.32694 traded on the 14:00 bar (high 1.32702) before the entry filled (lowest low since MSS 13:45 was 1.32622 on the 13:55 bar, 1.9 pips above entry; 14:00 bar low 1.32658). Stop 1.32572 never touched (lowest low since the 13:30 sweep 1.32582). **Correction needed** (alerted setup now invalid).
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32702 (14:00 bar; target 1.32728 not hit, 2.6 pips short). Close 1.32694 ≈ +2.40R. Engine "eod" at 14:00 is the day cut, not stop/target. No re-alert.
  - GU: 14:00 bar swept 15m swing high 1.32694 (high 1.32702) — no MSS yet (window open). Watching for a short; opposite GU long still open, daily GU bull.
  - NAS: alerted 14:01 OTE long 30544.9 / stop 30527.6 / target 30617.5 still **UNFILLED and valid**. Every bar since the 13:00 sweep checked: lowest low 30529.6 (stop not hit), highest high 30607.8 (14:00 bar; target not hit, 9.7 pts short). Low since MSS 30571.6 (14:00 bar), 26.7 pts above entry. Fill window to ~14:55; CPI 14:30. At risk of VOID if 30617.5 trades before a fill. No re-alert, no correction.
  - XAU: 14:00 bar swept 15m swing high 4145.735 (high 4146.10) — no MSS yet (window open). 10:50 and 12:25 setups already −1R. Last close 4145.53. Nothing alertable.
  - EU: all NY-morning sweeps expired with no MSS; no new sweep. Last close 1.11956. Nothing alertable.
  - DXY: 102.207, falling off 13:55 high 102.255 and under session high 102.271; confluence only (softer dollar = support for open GU long and the NAS long idea).
  - Classic: no separate Classic print beyond the NAS with-trend note (engine Classic row on the 13:00 NAS sweep is the same unfilled OTE level; no separate alert).
  - **No new alertable setups** (R:R≥2 not already alerted). **Correction:** GU 13:51 OTE long VOID.

- 14:10 SAST (NY AM) scanner pass. Waited for the 14:05 bar to close; fetched 14:10 via TradingView, closed candles to 14:10 (last 5m bar open 14:05). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1410.txt and detail_1410.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1410.md. Levels unchanged; last closes: NAS 30618.6, XAU 4146.475, EU 1.11948, GU 1.32668, DXY 102.225.
  - NAS: alerted 14:01 OTE long 30544.9 / stop 30527.6 / target 30617.5 is **VOID**. Target 30617.5 traded on the 14:05 bar (high 30618.6) before the entry filled (lowest low since MSS 13:55 was 30571.6 on the 14:00 bar, 26.7 pts above entry; 14:05 bar low 30589.0). Stop 30527.6 never touched (lowest low since the 13:00 sweep 30529.6). Engine still shows "unfilled" (it does not apply the void rule). **Correction needed.**
  - NAS: 14:05 bar swept 15m swing high 30617.5 — no MSS yet (window open). Per rule 3 watch for the reverse short (with daily lean bear).
  - NAS note: engine Classic row on the 13:00 sweep (same entry 30544.9 / stop 30527.6, target London high 30675.0, R:R 7.50) unfilled, stop/target untouched. Not alerted: same level as the just-voided PP alert, ~74 pts from price, and Classic is with-trend while daily is lean bear and engine NAS trend now −1.
  - GU: alerted 13:51 OTE long 1.32603 / stop 1.32572 / target 1.32694 stays **VOID** (target hit 14:00, high 1.32702, before fill; low since MSS 1.32622; 14:05 bar low 1.32647). Stop never touched. Correction combined with NAS and sent 14:11.
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.32702 (14:00; target 1.32728 not hit). 14:05 bar 1.32647-1.32696. Close 1.32668 ≈ +1.75R (engine eod mark 1.84R is the day cut, not stop/target). No re-alert.
  - GU: 14:00 sweep of 15m swing high 1.32694 — no MSS yet (window open).
  - GU note: 12:50 MSS short stays VOID (target hit 13:30 before fill); never alerted.
  - XAU: 14:00 sweep of 15m swing high 4145.735 — no MSS yet (14:05 high 4150.35). 10:50 and 12:25 setups already −1R. Last close 4146.475. Nothing alertable.
  - EU: no new sweep; all NY-morning sweeps expired with no MSS. Last close 1.11948. Nothing alertable.
  - DXY: 102.225, under session high 102.271; confluence only.
  - Classic: only the NAS row above; not alerted.
  - **No new alertable setups** (R:R≥2 not already alerted). **Corrections:** NAS 14:01 OTE long VOID; GU 13:51 OTE long VOID (sent 14:11).


- 14:21 SAST (NY AM) scanner pass. Waited for the 14:15 bar to close; fetched 14:20–14:21 via TradingView, closed candles to 14:20 (last 5m bar open 14:15). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1419.txt and detail_1419.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1419.md. Levels last closes refreshed; last closes: NAS 30618.0, XAU 4146.265, EU 1.1191, GU 1.3266, DXY 102.248.
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.3271 (14:15 bar; target 1.32728 not hit — 1.8 pips short). Low since fill 1.32582 (13:30), high since fill 1.3271. Close 1.3266 ≈ +1.55R (peak ≈ +2.80R at 1.3271). Engine eod mark at 14:15 is the day cut, not stop/target. No re-alert.
  - GU: alerted 13:51 OTE long 1.32603 stays **VOID** (target hit 14:00 before fill; correction already sent 14:11). 14:15 high 1.3271 does not change VOID status.
  - GU: 14:00 sweep of 15m swing high 1.32694 — no MSS yet (window open; 14:15 high 1.3271 / low 1.32647). Watching for reverse short (opposite GU long still open; daily GU bull).
  - GU note: 12:50 MSS short stays VOID (target 1.32583 hit 13:30 before fill); never alerted. Engine best high since MSS now 1.3271 (above stop 1.32704) — moot.
  - NAS: alerted 14:01 OTE long 30544.9 stays **VOID** (target 30617.5 hit 14:05 before fill; correction already sent 14:11). Low since MSS fill bars still 30571.6; high since 13:00 now 30630.4.
  - NAS: 14:05 sweep of 15m swing high 30617.5 and new 14:10 sweep of 15m swing high 30622.0 — no MSS yet (windows open; 14:15 high 30630.4 / close 30618.0). Watching for reverse short (with daily lean bear).
  - NAS note: Classic row on the 13:00 sweep (entry 30544.9 / stop 30527.6 / target London high 30675.0 R:R 7.50) still unfilled; stop/target untouched. Not alerted (same voided PP entry level; COUNTER vs daily lean bear).
  - XAU: 14:00 sweep of 15m swing high 4145.735 — no MSS yet (14:15 high 4153.32 / close 4146.265). 10:50 and 12:25 setups already −1R. Nothing alertable.
  - EU: no new sweep; all NY-morning sweeps expired with no MSS. Last close 1.1191. Nothing alertable.
  - DXY: 102.248, under session high 102.271 (13:10); confluence only (firmer on 14:15 = mild headwind for open GU long).
  - Classic: only the NAS row above; not alerted.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 14:26 SAST (NY AM) scanner pass. Waited for the 14:20 bar to close; fetched 14:25 via TradingView, closed candles to 14:25 (last 5m bar open 14:20). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1425.txt and detail_1425.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1425.md. Levels unchanged; last closes: NAS 30616.4, XAU 4150.945, EU 1.11936, GU 1.32684, DXY 102.231.
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.3271 (14:15; target 1.32728 not hit). 14:20 bar 1.32662-1.32692. Close 1.32684 ≈ +2.15R. Engine eod mark at 14:20 is the day cut, not stop/target. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). 14:00 sweep of 15m swing high 1.32694 — no MSS yet (window open). 12:50 short stays VOID; never alerted.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:05/14:10 sweeps of 15m swing highs 30617.5 / 30622.0 — no MSS yet (windows open; 14:20 bar 30596.4-30624.6, close 30616.4). Watching for reverse short (with daily lean bear). Classic row on the 13:00 sweep (entry 30544.9 / stop 30527.6 / target 30675.0) still unfilled, untouched; not alerted (same reasons as before).
  - XAU: 14:00 sweep of 15m swing high 4145.735 — no MSS yet (high since 4154.555 on 14:20, close 4150.945). 10:50 and 12:25 setups already −1R. Nothing alertable.
  - EU: no new sweep; all NY-morning sweeps expired with no MSS. Last close 1.11936. Nothing alertable.
  - DXY: 102.231, under session high 102.271; confluence only. US CPI 14:30 SAST next.
  - Classic: only the NAS row above; not alerted.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 14:27 SAST (NY AM) scanner pass. Fetched 14:27 via TradingView; last closed 5m still open 14:20 (14:25 bar still forming; closes at 14:30 — did not wait). Same closed set as the prior 14:26 pass. scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1427.txt and detail_1427.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1426.md. Levels last closes unchanged: NAS 30616.4, XAU 4150.945, EU 1.11936, GU 1.32684, DXY 102.231.
  - GU: alerted 10:28 IFVG long 1.32598 still **OPEN**. Filled 10:35. Every bar since the 10:00 sweep checked: lowest low 1.32568 (stop 1.32558 not hit), highest high 1.3271 (14:15; target 1.32728 not hit). 14:20 bar 1.32662-1.32692. Close 1.32684 ≈ +2.15R. Engine eod mark at 14:20 is the day cut, not stop/target. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). 14:00 sweep of 15m swing high 1.32694 — no MSS yet (window open; high since 1.3271 / low 1.32647). 12:50 short stays VOID; never alerted.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:05/14:10 sweeps of 15m swing highs 30617.5 / 30622.0 — no MSS yet (windows open; high since 30630.4 / low 30596.4 on 14:20, close 30616.4). Watching for reverse short (with daily lean bear). Classic row on the 13:00 sweep (entry 30544.9 / stop 30527.6 / target 30675.0) still unfilled, untouched; not alerted (same voided PP entry level; COUNTER vs daily lean bear). Fill window on the voided PP OTE ends at 14:20 bar — moot (VOID).
  - XAU: 14:00 sweep of 15m swing high 4145.735 — no MSS yet (high since 4154.555 on 14:20, close 4150.945). 10:50 and 12:25 setups already −1R. Nothing alertable.
  - EU: no new sweep; all NY-morning sweeps expired with no MSS. Last close 1.11936. Nothing alertable.
  - DXY: 102.231, under session high 102.271; confluence only. US CPI 14:30 SAST next.
  - Classic: only the NAS row above; not alerted.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction.


- 14:33 SAST (NY AM) scanner pass. Fetched 14:33 via TradingView; closed candles to 14:30 (last 5m bar open 14:25 — CPI bar). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1432.txt and detail_1432.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1432.md. Levels last closes refreshed; last closes: NAS 30654.8, XAU 4153.27, EU 1.1199, GU 1.32684, DXY 102.195.
  - GU: alerted 10:28 IFVG long 1.32598 **CLOSED flat for CPI** at the 14:25 open 1.32684, **+2.15R** (see Close 14:29 note). Engine marks eod exit 14:25 R 2.43 on close 1.32684; Close note uses open = +2.15R. TP 1.32728 never traded (session high 1.32716 on 14:25; prior peak 1.32710 at 14:15/14:17). Stop never touched. Do not reopen; no open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Fill window ended with the 14:25 bar — moot. 14:00 sweep of 15m swing high 1.32694 — no MSS yet (window open; high since 1.32716 on 14:25 / low 1.32647). 12:50 short stays VOID; never alerted.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Fill window ended with the 14:25 bar — moot. 14:05/14:10 sweeps of 15m swing highs 30617.5 / 30622.0 — no MSS yet (windows open; 14:25 bar high 30665.0 / low 30614.8 / close 30654.8). Watching for reverse short (with daily lean bear). Classic row on the 13:00 sweep (entry 30544.9 / stop 30527.6 / target 30675.0 R:R 7.50) still unfilled; high since 30665.0 (target not hit); fill window ended 14:25 — expired unfilled; not alerted (same voided PP entry level; COUNTER vs daily lean bear).
  - XAU: 14:00 sweep of 15m swing high 4145.735 — no MSS yet (high since 4155.835 on 14:25, close 4153.27). 10:50 and 12:25 setups already −1R. Nothing alertable.
  - EU: no new sweep; all NY-morning sweeps expired with no MSS. Last close 1.1199. Nothing alertable.
  - DXY: 102.195, soft under session high 102.271 (13:10); confluence only (softer dollar on CPI bar). US CPI 14:30 SAST just printed; team blackout 14:15-14:45 noted — scanned and logged; no brand-new qualifying setup.
  - Classic: only the NAS row above (expired unfilled); not alerted.
  - **No new alertable setups** (R:R≥2 not already alerted). No VOID correction. GU 10:28 already CLOSED (Close 14:29).


- 14:36 SAST (NY AM) scanner pass. Fetched 14:36 via TradingView; closed candles to 14:35 (last 5m bar open 14:30 — CPI reaction bar). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1436.txt and detail_1436.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1436.md. Levels last closes refreshed; last closes: NAS 30426.0, XAU 4114.52, EU 1.11511, GU 1.32248, DXY 102.579.
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R at 14:25 open 1.32684). Engine marks a 14:30 −1R exit on the same levels — ignore (manual flat already taken; do not reopen). No open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Engine "FILLED 14:30 loss" is moot (VOID before fill). 12:50 short stays VOID; never alerted.
  - GU: NEW Ping-Pong SHORT. 15m swing high 1.32694 swept 14:00 (extreme 1.32716 on 14:25/14:30), MSS 14:30 (close 1.32248 below fractal). Stop 1.32726 (extreme + 1 pip), target 1.32176. Confirmations: OB 1.32662 R:R 7.59, IFVG 1.32636 R:R 5.11, OTE 1.32568 R:R 2.47 (all unfilled; best since MSS None — MSS is the last closed bar; engine fills from next bar). Void check over every 5m bar 14:00-14:30: highest high 1.32716 (stop not hit), lowest low 1.32213 (target 1.32176 not hit — 3.7 pips short). Fill window 12 bars from MSS (to ~15:30 SAST). Labels: UNPROVEN; **COUNTER-TREND** vs daily GU bull above 1.3248 (price now under 1.3248 on the CPI bar — bias gate may be in question, but daily tag still bull until Bias updates). DXY 102.579 spike = supports the short. **Held — CPI entry blackout 14:15-14:45 (confluence.md/setups.md/scalps.md); next new entries from 14:45.** Not alerted this pass.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Engine "FILLED 14:30 loss" is moot (VOID before fill). Classic row on the 13:00 sweep (30544.9 / 30527.6 / 30675.0) also engine-filled 14:30 loss — same voided entry level; never alerted.
  - NAS: NEW Ping-Pong SHORT. 15m swing high 30617.5 swept 14:05 (extreme 30665.0 on 14:25), MSS 14:30 (close 30426.0 below fractal). Stop 30667.0 (extreme + 2 pt), target 30417.3. Confirmations: OB 30614.8 R:R 3.78, OTE 30594.1 R:R 2.42 (IFVG 30581.6 R:R 1.92 below 1:2); all unfilled (best since MSS None). Void check over every 5m bar 14:05-14:30: highest high 30665.0 (stop not hit), lowest low 30424.6 (target 30417.3 not hit — 7.3 pts short). 14:10 sweep of 30622.0 rides the same displacement into the 14:30 MSS. Fill window to ~15:30. Labels: UNPROVEN; with daily lean bear (not COUNTER-TREND). Engine with 15m at the sweep (Classic eligibility noted). DXY spike supports. Lot sizing if alerted after blackout ([REDACTED balance], 0.5%): OB stop 52.2 pts × $1/pt → 4.74 lots / [REDACTED: third-party account sizing]; OTE stop 72.9 pts → 3.40 / 0.96 lots. **Held — CPI entry blackout 14:15-14:45; next new entries from 14:45.** Not alerted this pass.
  - NAS: 14:30 also swept many 15m swing lows / London low 30519.6 (low 30424.6) — no MSS yet on those (window open). Watching for reverse long after the short idea.
  - XAU: 14:00 sweep of 15m swing high 4145.735 got MSS 14:30 (ext 4155.835, stop 4156.335) but **target None** (engine — opposing pool already overrun; 14:30 low 4113.46 blew through Asia/London lows / PDL). Not alertable. Fresh 14:30 swing-low sweeps (4136.025 etc.) — no MSS yet. 10:50 and 12:25 setups already −1R. Nothing alertable.
  - EU: no MSS on pre-CPI sweeps; 14:30 raided PDL 1.11538 (low 1.11501, close 1.11511) — many 15m swing-low / PDL sweeps, no MSS yet (windows open). Last close 1.11511. Nothing alertable.
  - DXY: 102.579 (14:30 high 102.587 = PDH), sharp USD bid on CPI; confluence only (supports GU/NAS shorts; headwind for any residual longs).
  - Classic: NAS Classic row on 13:00 long is the voided/engine-loss level — not alerted. No separate new Classic print at 1:2+ beyond the NAS short's with-trend note.
  - **No alert this pass** (CPI entry blackout 14:15-14:45 still in force until 14:45). Two NEW R:R≥2 shorts logged for post-blackout: NAS OB/OTE short; GU OB/IFVG/OTE short (COUNTER-TREND). No VOID correction (prior VOIDs already sent; no open alerted unfilled setup).


- 14:46 SAST (NY AM) scanner pass. Waited for CPI blackout end (14:45) and the 14:40 bar close; fetched 14:46 via TradingView, closed candles to 14:45 (last 5m bar open 14:40). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1446.txt and detail_1446.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1446.md. Levels last closes refreshed; last closes: NAS 30394.6, XAU 4093.465, EU 1.1139, GU 1.32127, DXY 102.682 (session high 102.721 on 14:40).
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). Engine 14:30 −1R mark still ignored. No open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot.
  - GU: held 14:36 Ping-Pong SHORT (OB 1.32662 R:R 7.59 / IFVG 1.32636 R:R 5.11 / OTE 1.32568 R:R 2.47; stop 1.32726; target 1.32176; MSS 14:30) is **VOID**. Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); lowest low 1.32054 (14:40). Target 1.32176 traded on the 14:35 bar (low 1.32077) before any fill (post-MSS highs 1.32265 / 1.32182 — never reached OB/IFVG/OTE). Never alerted (CPI blackout) → no correction. Fill window still open to ~15:30 but VOID.
  - GU: 14:30/14:35/14:40 sweeps of many 15m swing lows / Asia/London lows / new lows 1.32124–1.32054 — no MSS yet (windows open). Watching for reverse long (daily GU bull broken under 1.3248; bias provisional until refresh).
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot. Classic row on 13:00 sweep same voided entry — never alerted; fill window ended.
  - NAS: held 14:36 Ping-Pong SHORT (OB 30614.8 R:R 3.78 / OTE 30594.1 R:R 2.42; stop 30667.0; target 30417.3; MSS 14:30) is **VOID**. Every bar since the 14:05 sweep checked: highest high 30665.0 (stop not hit); lowest low 30369.8 (14:40). Target 30417.3 traded on the 14:35 bar (low 30390.6) before any fill (post-MSS highs 30436.2 / 30427.8 — never reached OB/OTE). Never alerted (CPI blackout) → no correction. Fill window still open to ~15:30 but VOID. With daily lean bear / DXY spike; engine Classic eligibility noted — moot.
  - NAS: 14:30/14:35 sweeps of many 15m swing lows / London low 30519.6 / PDL 30401.2 (low 30369.8) — no MSS yet (windows open). Watching for reverse long (COUNTER-TREND vs daily lean bear / 4H bear).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun; LOD 4085.29). Fresh 14:30 swing-low sweeps — no MSS yet. Prior setups already −1R. Nothing alertable. Last close 4093.465.
  - EU: 14:30 sweeps of PDL / many swing lows (low 1.11326) — no MSS yet (windows open). Earlier alerted long already −1R. Nothing alertable. Last close 1.1139.
  - DXY: 102.682, session high 102.721 (14:40) above PDH 102.587; confluence only (firm USD = supports shorts if a fresh pullback+MSS appears; headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+ beyond the voided NAS short’s with-trend note.
  - CPI entry blackout 14:15-14:45 has ended. **No new alertable setups** (R:R≥2 not already alerted; held post-CPI shorts both VOID target-before-fill). No VOID correction (never alerted). No open Ping-Pong risk.


- 14:51 SAST (NY AM) scanner pass, fetched 14:50 via TradingView, closed candles to 14:50 (last 5m bar open 14:45). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1450.txt and detail_1450.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1450.md. Levels last closes refreshed; last closes: NAS 30433.8, XAU 4105.335, EU 1.11418, GU 1.32179, DXY 102.645 (session high still 102.721 on 14:40).
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). Engine 14:30 −1R mark still ignored. No open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot.
  - GU: held 14:36 Ping-Pong SHORT (OB 1.32662 R:R 7.59 / IFVG 1.32636 R:R 5.11 / OTE 1.32568 R:R 2.47; stop 1.32726; target 1.32176; MSS 14:30) stays **VOID**. Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); lowest low 1.32054 (14:40). Target 1.32176 traded on the 14:35 bar (low 1.32077) before any fill (post-MSS highs 1.32265 / 1.32182 — never reached OB/IFVG/OTE). Never alerted (CPI blackout) → no correction. Fill window ended with the 14:45 bar — moot (VOID).
  - GU: 14:30/14:35/14:40 sweeps of many 15m swing lows / Asia/London lows / lows 1.32124–1.32054 — still no MSS (windows open; 14:45 bar high 1.3219 / close 1.32179). Watching for reverse long (daily GU bull broken under 1.3248; bias provisional until refresh).
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot. Classic row on 13:00 sweep same voided entry — never alerted; fill window ended.
  - NAS: held 14:36 Ping-Pong SHORT (OB 30614.8 R:R 3.78 / OTE 30594.1 R:R 2.42; stop 30667.0; target 30417.3; MSS 14:30) stays **VOID**. Every bar since the 14:05 sweep checked: highest high 30665.0 (stop not hit); lowest low 30369.8 (14:40). Target 30417.3 traded on the 14:35 bar (low 30390.6) before any fill (post-MSS highs 30436.2 / 30427.8 — never reached OB/OTE). Never alerted (CPI blackout) → no correction. Fill window ended with the 14:45 bar — moot (VOID). With daily lean bear / DXY firm; engine Classic eligibility noted — moot.
  - NAS: 14:30/14:35 sweeps of many 15m swing lows / London low 30519.6 / PDL 30401.2 (low 30369.8) — still no MSS (windows open; 14:45 bar high 30436.8 / close 30433.8). Watching for reverse long (COUNTER-TREND vs daily lean bear / 4H bear).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun; LOD 4085.29). Fresh 14:30 swing-low sweeps — still no MSS (14:45 bounce high 4105.6 / close 4105.335). Prior setups already −1R. Nothing alertable.
  - EU: 14:30 sweeps of PDL / many swing lows (low 1.11326) — still no MSS (windows open; 14:45 high 1.1142 / close 1.11418). Earlier alerted long already −1R. Nothing alertable.
  - DXY: 102.645, under session high 102.721 (14:40) and above PDH 102.587; confluence only (firm USD = supports shorts if a fresh pullback+MSS appears; headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+ beyond the voided NAS short’s with-trend note.
  - **No new alertable setups** (R:R≥2 not already alerted; held post-CPI shorts both VOID target-before-fill). No VOID correction (never alerted). No open Ping-Pong risk.

- 14:56 SAST (NY AM) scanner pass. Waited past 14:55 so the 14:50–14:55 bar was closed; fetched 14:56 via TradingView, closed candles to 14:55 (last 5m bar open 14:50). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1456.txt and detail_1456.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1456.md. Levels last closes refreshed; last closes: NAS 30426.0, XAU 4107.25, EU 1.11414, GU 1.32154, DXY 102.645 (session high still 102.721 on 14:40).
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). Engine 14:30 −1R mark still ignored. No open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot.
  - GU: held 14:36 Ping-Pong SHORT (OB 1.32662 R:R 7.59 / IFVG 1.32636 R:R 5.11 / OTE 1.32568 R:R 2.47; stop 1.32726; target 1.32176; MSS 14:30) stays **VOID**. Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); lowest low 1.32054 (14:40). Target 1.32176 traded on the 14:35 bar (low 1.32077) before any fill (post-MSS highs 1.32265 / 1.32182 / 1.32188 / 1.32192 — never reached OB/IFVG/OTE). Never alerted (CPI blackout) → no correction. Fill window ended with the 14:50 bar — moot (VOID).
  - GU: 14:30/14:35/14:40 sweeps of many 15m swing lows / Asia/London lows / lows 1.32124–1.32054 — still no MSS (windows open; 14:50 bar high 1.32192 / low 1.32089 / close 1.32154). PDL 1.32046 not swept (LOD 1.32054). Watching for reverse long (daily GU bull broken under 1.3248; bias provisional until refresh).
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot. Classic row on 13:00 sweep same voided entry — never alerted; fill window ended.
  - NAS: held 14:36 Ping-Pong SHORT (OB 30614.8 R:R 3.78 / OTE 30594.1 R:R 2.42; stop 30667.0; target 30417.3; MSS 14:30) stays **VOID**. Every bar since the 14:05 sweep checked: highest high 30665.0 (stop not hit); lowest low 30369.8 (14:40). Target 30417.3 traded on the 14:35 bar (low 30390.6) before any fill (post-MSS highs 30436.2 / 30427.8 / 30436.8 / 30451.8 — never reached OB/OTE). Never alerted (CPI blackout) → no correction. Fill window ended with the 14:50 bar — moot (VOID). With daily lean bear / DXY firm; engine Classic eligibility noted — moot.
  - NAS: 14:30/14:35 sweeps of many 15m swing lows / London low 30519.6 / PDL 30401.2 (low 30369.8) — still no MSS (windows open; 14:50 bar high 30451.8 / low 30406.2 / close 30426.0). Watching for reverse long (COUNTER-TREND vs daily lean bear / 4H bear).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun; LOD 4085.29). Fresh 14:30 swing-low sweeps — still no MSS (14:50 bounce high 4107.69 / close 4107.25). Prior setups already −1R. Nothing alertable.
  - EU: 14:30 sweeps of PDL / many swing lows (low 1.11326) — still no MSS (windows open; 14:50 high 1.11452 / low 1.11364 / close 1.11414). Earlier alerted long already −1R. Nothing alertable.
  - DXY: 102.645, under session high 102.721 (14:40) and above PDH 102.587; confluence only (firm USD = supports shorts if a fresh pullback+MSS appears; headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+ beyond the voided NAS short’s with-trend note.
  - **No new alertable setups** (R:R≥2 not already alerted; held post-CPI shorts both VOID target-before-fill; fill windows now closed). No VOID correction (never alerted). No open Ping-Pong risk.


- 15:01 SAST (NY AM) scanner pass. Waited for the 14:55 bar to close; fetched 15:01 via TradingView, closed candles to 15:00 (last 5m bar open 14:55). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1501.txt and detail_1501.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1501.md. Levels last closes refreshed; last closes: NAS 30369.8, XAU 4097.91, EU 1.1129, GU 1.32042, DXY 102.748 (session high 102.76 on 14:55).
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). Engine 14:30 −1R mark still ignored. No open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot.
  - GU: held 14:36 Ping-Pong SHORT (OB 1.32662 R:R 7.59 / IFVG 1.32636 R:R 5.11 / OTE 1.32568 R:R 2.47; stop 1.32726; target 1.32176; MSS 14:30) stays **VOID**. Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); lowest low 1.3203 (14:55). Target 1.32176 traded on the 14:35 bar (low 1.3208) before any fill (post-MSS highs 1.32265 / 1.32182 / 1.32192 / 1.3215 — never reached OB/IFVG/OTE). Never alerted (CPI blackout) → no correction. Engine fill window still open to ~15:30 — moot (VOID).
  - GU: 14:30/14:35/14:40 sweeps of many 15m swing lows / Asia/London lows, plus NEW 14:55 sweeps of PDL 1.32046 and swing lows 1.32038–1.32046 (14:55 low 1.3203) — still no MSS (windows open; 14:55 close 1.32042). Watching for reverse long (bias.md 14:51 lean BULL / STRUCTURE HELD above week low 1.32017; PDL now swept).
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot. Classic row on 13:00 sweep same voided entry — never alerted; fill window ended.
  - NAS: held 14:36 Ping-Pong SHORT (OB 30614.8 R:R 3.78 / OTE 30594.1 R:R 2.42; stop 30667.0; target 30417.3; MSS 14:30) stays **VOID**. Every bar since the 14:05 sweep checked: highest high 30665.0 (stop not hit); lowest low 30356.2 (14:55). Target 30417.3 traded on the 14:35 bar (low 30391) before any fill (post-MSS highs 30436.2 / 30451.8 / 30429 — never reached OB/OTE). Never alerted (CPI blackout) → no correction. Engine fill window still open to ~15:30 — moot (VOID).
  - NAS: 14:30/14:35 sweeps of many 15m swing lows / London low 30519.6 / PDL 30401.2 (prior low 30369.8; new 14:55 low 30356.2) — still no MSS (windows open; 14:55 high 30429 / close 30369.8). Watching for reverse long (bias.md COUNTER-TREND long if sweep holds; invalidation 15m close below 30369.8 — 14:55 5m closed at that level after piercing it).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun; LOD 4085.29; 14:55 low 4092.9 / close 4097.91). Fresh 14:30 swing-low sweeps — still no MSS. Prior setups already −1R. Nothing alertable.
  - EU: 14:30 sweeps of PDL / many swing lows (prior low 1.11326; 14:55 low 1.1127 / close 1.1129) — still no MSS (windows open). Earlier alerted long already −1R. Nothing alertable.
  - DXY: 102.748, new session high 102.76 on 14:55 (above PDH 102.587); confluence only (firm USD = headwind for turtle-soup longs; supports shorts if a fresh pullback+MSS appears).
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted; held post-CPI shorts both VOID target-before-fill; no MSS yet on post-CPI low sweeps). No VOID correction (never alerted). No open Ping-Pong risk.


- 15:06 SAST (NY AM) scanner pass, fetched 15:05 via TradingView, closed candles to 15:05 (last 5m bar open 15:00). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1505.txt and detail_1505.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1505.md. Levels last closes refreshed; last closes: NAS 30375.8, XAU 4086.815, EU 1.1119, GU 1.31905, DXY 102.829 (session high 102.841 on 15:00).
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). Engine 14:30 −1R mark still ignored. No open Ping-Pong risk. No re-alert.
  - GU: 13:51 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot.
  - GU: held 14:36 Ping-Pong SHORT (OB 1.32662 R:R 7.59 / IFVG 1.32636 R:R 5.11 / OTE 1.32568 R:R 2.47; stop 1.32726; target 1.32176; MSS 14:30) stays **VOID**. Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); lowest low 1.31885 (15:00). Target 1.32176 traded on the 14:35 bar (low 1.32077) before any fill (post-MSS highs 1.32265 / 1.32192 — never reached OB/IFVG/OTE). Never alerted (CPI blackout) → no correction. Engine fill window still open to ~15:30 — moot (VOID).
  - GU: 14:30/14:35/14:40/14:55 sweeps of many 15m swing lows / Asia/London lows / PDL 1.32046, plus NEW 15:00 sweeps of week low 1.32017 / 1.32022 (15:00 low 1.31885 / close 1.31905) — still no MSS (windows open). Watching for reverse long (bias.md 15:05 CONDITIONAL: 15:15 close below 1.32017 drops lean bull → BEAR).
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). Engine FILLED 14:30 loss is moot. Classic row on 13:00 sweep same voided entry — never alerted; fill window ended.
  - NAS: held 14:36 Ping-Pong SHORT (OB 30614.8 R:R 3.78 / OTE 30594.1 R:R 2.42; stop 30667.0; target 30417.3; MSS 14:30) stays **VOID**. Every bar since the 14:05 sweep checked: highest high 30665.0 (stop not hit); lowest low 30356.2 (14:55). Target 30417.3 traded on the 14:35 bar (low 30390.6) before any fill (post-MSS highs 30451.8 / 30436.8 / 30429.4 / 30392.8 — never reached OB/OTE). Never alerted (CPI blackout) → no correction. Engine fill window still open to ~15:30 — moot (VOID).
  - NAS: 14:30/14:35 sweeps of many 15m swing lows / London low 30519.6 / PDL 30401.2 (LOD 30356.2) — still no MSS (windows open; 15:00 bar high 30392.8 / low 30358.4 / close 30375.8). Watching for reverse long (bias.md CONDITIONAL CT long; 15:15 close below 30369.8 kills it).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun; new LOD 4083.005 on 15:00; close 4086.815). Fresh 14:30 swing-low sweeps — still no MSS. Prior setups already −1R. Nothing alertable.
  - EU: 14:30 sweeps of PDL / many swing lows (new LOD 1.11160 on 15:00; close 1.1119) — still no MSS (windows open). Earlier alerted long already −1R. Nothing alertable.
  - DXY: 102.829, new session high 102.841 on 15:00 (above PDH 102.587); confluence only (firm USD = headwind for turtle-soup longs; supports shorts if a fresh pullback+MSS appears).
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups** (R:R≥2 not already alerted; held post-CPI shorts both VOID target-before-fill; no MSS yet on post-CPI low sweeps). No VOID correction (never alerted). No open Ping-Pong risk.


- 15:10 SAST (NY AM) scanner pass. Waited for the 15:05 bar to close; fetched 15:10 via TradingView, closed candles to 15:10 (last 5m bar open 15:05). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1510.txt and detail_1510.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1510.md. Last closes: NAS 30386.8, XAU 4094.65, EU 1.11237, GU 1.31956, DXY 102.795 (new session high 102.856 on 15:05). Detail output identical to 15:05 pass apart from fill-window bar labels — no new sweeps of marked pools, no new MSS.
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). 13:51 OTE long stays **VOID** (correction sent 14:11). No open Ping-Pong risk.
  - GU: 14:36 Ping-Pong SHORT (OB 1.32662 / IFVG 1.32636 / OTE 1.32568; stop 1.32726; target 1.32176) stays **VOID** (target traded 14:35 before fill). Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); post-MSS highs never reached any entry. Never alerted → no correction.
  - GU: post-CPI low sweeps (14:30–15:00, incl. PDL 1.32046 and week low 1.32017) — still no MSS (windows open). New LOD 1.3186 on 15:05 (close 1.31956). Watching for reverse long (bias CONDITIONAL; 15:15 close below 1.32017 → BEAR).
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:36 Ping-Pong SHORT (OB 30614.8 / OTE 30594.1; stop 30667.0; target 30417.3) stays **VOID** (target traded 14:35 before fill; highest high since sweep 30665.0, stop not hit; post-MSS high 30451.8 never reached entries). Never alerted → no correction.
  - NAS: post-CPI low sweeps (London low 30519.6, PDL 30401.2; LOD 30356.2 on 14:55) — still no MSS (windows open; 15:05 bar H 30394.0 / L 30363.1 / C 30386.8). Watching for COUNTER-TREND reverse long (bias: 15:15 close below 30369.8 kills it).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun). Post-CPI swing-low sweeps — still no MSS; LOD 4083.005 (15:00), 15:05 close 4094.65. Nothing alertable.
  - EU: post-CPI PDL / swing-low sweeps — still no MSS (windows open); new LOD 1.11152 on 15:05, close 1.11237. Nothing alertable.
  - DXY: 102.795, new session high 102.856 on 15:05 (above PDH 102.587); confluence only (firm USD = headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups.** No VOID correction needed (nothing alerted is pending). No open Ping-Pong risk.


- 15:15 SAST (NY AM) scanner pass. Waited for the 15:10 bar to close; fetched 15:15 via TradingView, closed candles to 15:15 (last 5m bar open 15:10; last 15m bar open 15:00, closed 15:15). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1515.txt and detail_1515.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1515.md. Levels last closes refreshed; last closes: NAS 30401.4, XAU 4089.185, EU 1.11234, GU 1.31934, DXY 102.804 (session high still 102.856 on 15:05). PDH/PDL/Asia/London unchanged. Detail output identical to 15:10 pass apart from fill-window bar labels — no new sweeps of marked pools, no new MSS.
  - Bias gates (15:00 15m bar, closed 15:15; bias.md not refreshed since 15:05): **NAS 15m close 30401.4 ≥ 30369.8** (H 30403.6 / L 30358.4) → COUNTER-TREND long NOT killed; stays alive but weak toward 30519.6 per bias.md. **GU 15m close 1.31934 < 1.32017** week low (H 1.32042 / L 1.3186) → lean bull DROPPED → BEAR per bias.md (draw 1.31808).
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). 13:51 OTE long stays **VOID** (correction sent 14:11). No open Ping-Pong risk.
  - GU: 14:36 Ping-Pong SHORT (OB 1.32662 / IFVG 1.32636 / OTE 1.32568; stop 1.32726; target 1.32176) stays **VOID** (target traded 14:35 before fill). Every bar since the 14:00 sweep checked: highest high 1.32716 (stop not hit); post-MSS highs never reached any entry (15:10 high 1.3197). Never alerted → no correction.
  - GU: post-CPI low sweeps (14:30–15:00, incl. PDL 1.32046 and week low 1.32017) — still no MSS (windows open to ~15:30). LOD 1.3186 (15:05); 15:10 bar H 1.3197 / L 1.31866 / C 1.31934. 15m now closed below week low → reverse long now COUNTER-TREND vs BEAR bias.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:36 Ping-Pong SHORT (OB 30614.8 / OTE 30594.1; stop 30667.0; target 30417.3) stays **VOID** (target traded 14:35 before fill; highest high since sweep 30665.0, stop not hit; post-MSS high 30451.8 never reached entries). Never alerted → no correction.
  - NAS: post-CPI low sweeps (London low 30519.6, PDL 30401.2; LOD 30356.2 on 14:55) — still no MSS (windows open to ~15:30; 15:10 bar H 30403.6 / L 30383.4 / C 30401.4, back at PDL). Watching for COUNTER-TREND reverse long (gate held at 15:15).
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun). Post-CPI swing-low sweeps — still no MSS; new LOD 4081.25 on 15:10 (close 4089.185; not a marked pool). Nothing alertable.
  - EU: post-CPI PDL / swing-low sweeps — still no MSS (windows open); LOD 1.11152 (15:05), 15:10 close 1.11234. Nothing alertable.
  - DXY: 102.804, session high 102.856 (15:05) holding; confluence only (firm USD = headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups.** No VOID correction needed (nothing alerted is pending). No open Ping-Pong risk.

- 15:23 SAST (NY AM) scanner pass. Fetched 15:24 via TradingView; closed candles to 15:20 (last 5m bar open 15:15; 15:00 15m still the last closed HTF bar — next closes 15:30). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1523.txt and detail_1523.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1523.md. Levels last closes refreshed; last closes: NAS 30361.0, XAU 4080.88, EU 1.11159, GU 1.31866, DXY 102.854 (session high still 102.856; 15:15 high tied). PDH/PDL/Asia/London unchanged. Detail vs 15:15: only last-bar / fill-window / best-since-MSS labels moved — no new sweeps of marked pools, no new MSS.
  - Bias gates (last closed 15m = 15:00 bar): **NAS CT long still alive** on 15:00 close 30401.4 ≥ 30369.8; 15:15 5m H 30405.0 / L 30352.3 / C 30361.0 (new LOD 30352.3) — watching 15:30 15m close vs 30369.8. **GU BEAR** (15:00 close 1.31934 < 1.32017). bias.md not refreshed since 15:05.
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). 13:51 OTE long stays **VOID** (correction sent 14:11). No open Ping-Pong risk.
  - GU: 14:36 Ping-Pong SHORT (OB 1.32662 / IFVG 1.32636 / OTE 1.32568; stop 1.32726; target 1.32176) stays **VOID** (target traded 14:35 before fill). Fill window ends on the 15:15 bar. Highest high since sweep 1.32716 (stop not hit); best since MSS 1.32265 — never reached any entry. Never alerted → no correction.
  - GU: post-CPI low sweeps (14:30–15:00, incl. PDL 1.32046 and week low 1.32017) — still no MSS (14:30 windows open to ~15:30; 15:00 windows later). LOD 1.3186 (15:05); 15:15 bar H 1.31962 / L 1.31866 / C 1.31866. Reverse long would be COUNTER-TREND vs BEAR bias.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:36 Ping-Pong SHORT (OB 30614.8 / OTE 30594.1; stop 30667.0; target 30417.3) stays **VOID** (target traded 14:35 before fill; fill window ends 15:15; highest high since sweep 30665.0, stop not hit; best since MSS 30451.8). Never alerted → no correction.
  - NAS: post-CPI low sweeps (London low 30519.6, PDL 30401.2) — still no MSS (windows open to ~15:30). New LOD 30352.3 on 15:15 (close 30361.0). Watching for COUNTER-TREND reverse long if 15:30 15m holds ≥ 30369.8.
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun); fill window ends 15:15. Post-CPI swing-low sweeps — still no MSS; new LOD 4080.78 on 15:15 (close 4080.88; not a marked pool). Nothing alertable.
  - EU: post-CPI PDL / swing-low sweeps — still no MSS (windows open); LOD 1.11152 (15:05), 15:15 H 1.11253 / L 1.11159 / C 1.11159. Nothing alertable.
  - DXY: 102.854, session high 102.856 holding (15:05 and 15:15 high); confluence only (firm USD = headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups.** No VOID correction needed (nothing alerted is pending). No open Ping-Pong risk.



- 15:29 SAST (NY AM) scanner pass. First fetch ~15:29 only had closed candles to 15:20; re-fetched 15:30 once the 15:25 bar closed, so closed candles to 15:25 (last 5m bar open 15:25; last 15m bar open 15:15, closed 15:30). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1529.txt and detail_1529.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1529.md. Levels last closes refreshed; last closes: NAS 30364.8, XAU 4090.395, EU 1.11299, GU 1.31985, DXY 102.759 (session high 102.875 on 15:20). PDH/PDL/Asia/London unchanged. New LOD: NAS 30350.6 (15:20), XAU 4079.73 (15:20), EU 1.11142 (15:20), GU 1.31846 (15:20).
  - Bias gates (15:15 15m bar, closed 15:30): **NAS CT long DROPPED** — 15:15 close 30364.8 < 30369.8 (H 30405.0 / L 30350.6) → BEAR with daily/weekly per bias.md. **GU BEAR** unchanged (15:00 close 1.31934 < 1.32017). bias.md not refreshed since 15:05.
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). 13:51 OTE long stays **VOID** (correction sent 14:11). No open Ping-Pong risk.
  - GU: 14:36 Ping-Pong SHORT (OB 1.32662 / IFVG 1.32636 / OTE 1.32568; stop 1.32726; target 1.32176) stays **VOID** (target traded 14:35 before fill). Fill window ends on the 15:25 bar. Highest high since sweep 1.32716 (stop not hit); best since MSS 1.32265 — never reached any entry. Never alerted → no correction.
  - GU: post-CPI low sweeps — 14:30 windows **expired** no MSS; 14:35–15:00 (incl. PDL 1.32046 / week low 1.32017) still no MSS (windows open). LOD 1.31846 (15:20); 15:25 bar H 1.3199 / L 1.3190 / C 1.31985. Reverse long would be COUNTER-TREND vs BEAR bias.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:36 Ping-Pong SHORT (OB 30614.8 / OTE 30594.1; stop 30667.0; target 30417.3) stays **VOID** (target traded 14:35 before fill; fill window ends 15:25; highest high since sweep 30665.0, stop not hit; best since MSS 30451.8). Never alerted → no correction.
  - NAS: post-CPI low sweeps — 14:30 windows **expired** no MSS; 14:35 PDL 30401.2 / 30417.3 still no MSS (windows open). LOD 30350.6 (15:20); 15:25 H 30384.4 / L 30355.8 / C 30364.8. Turtle-soup reverse long now also COUNTER-TREND vs BEAR gate (dropped).
  - EU: NEW Ping-Pong LONG on detail. 15m swing low 1.11526 swept 14:30 (extreme 1.11142 on 15:20), MSS 15:25 (close 1.11299). Stop 1.11132, target 1.11992. Confirmations: OTE 1.11189 R:R 13.96, OB 1.11253 R:R 6.11, IFVG 1.11270 R:R 5.23 (all unfilled; best since MSS None — MSS is last closed bar). **VOID** — target 1.11992 traded on the 14:30 sweep bar itself (open/high 1.11992) before any entry fill; stop 1.11132 never hit (LOD 1.11142). counter15m=True; would have been UNPROVEN, COUNTER-TREND vs daily BEAR. Never alerted → no correction. Fill window still open (engine W=12 from next bar) but VOID stands.
  - XAU: 14:00 sweep / MSS 14:30 still **target None** (opposing pool overrun); fill window ends 15:25. Post-CPI 14:30 swing-low sweeps **expired** no MSS; new LOD 4079.73 on 15:20 (close 4090.395; not a marked pool). Nothing alertable.
  - DXY: 102.759, new session high 102.875 (15:20); confluence only (USD still firm = headwind for turtle-soup longs).
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups.** No VOID correction needed (nothing alerted is pending). No open Ping-Pong risk.

- 15:37 SAST (NY AM) scanner pass. Fetched 15:37 via TradingView; closed candles to 15:35 (last 5m bar open 15:30; last closed 15m still the 15:15 bar, next closes 15:45). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1537.txt and detail_1537.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1537.md. Levels last closes refreshed; last closes: NAS 30364.6, XAU 4102.065, EU 1.11329, GU 1.32022, DXY 102.742 (session high 102.875 on 15:20 holding). PDH/PDL/Asia/London unchanged. New LOD: NAS 30320.0 (15:30 bar H 30410.2 / L 30320.0; not a marked pool, no new sweep in engine). Detail vs 15:29: no new sweeps of marked pools, no new MSS; 14:00/14:05 sweep fill windows (NAS/XAU/GU) ended on the 15:30 bar.
  - Bias gates: unchanged (no new 15m close since 15:30). NAS BEAR (CT long dropped), GU BEAR, XAU BEAR, EU BEAR, DXY BULL.
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). 13:51 OTE long stays **VOID** (correction sent 14:11). 14:36 Ping-Pong SHORT stays **VOID** (target traded 14:35 before fill); fill window now ended (15:30 bar), never filled (best since MSS 1.32265), stop 1.32726 never hit. Never alerted → no correction.
  - GU: 14:40–15:00 low sweeps (incl. PDL 1.32046 / week low 1.32017) still no MSS (windows open). LOD 1.31846 (15:20); 15:30 bar H 1.32042 / L 1.31973 / C 1.32022 (back above week low, not a 15m close). Reverse long would be COUNTER-TREND vs BEAR.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:36 SHORT stays **VOID**; fill window ended 15:30, never filled (best since MSS 30451.8), stop 30667.0 never hit. All post-CPI low-sweep windows **expired** without MSS. Nothing alertable.
  - EU: 14:30 sweep / MSS 15:25 Ping-Pong LONG (stop 1.11132 / target 1.11992; OTE 1.11189, OB 1.11253, IFVG 1.11270) stays **VOID** — target traded on the 14:30 sweep bar before any fill. 15:30 bar L 1.11285 still above all entries (unfilled); stop not hit (LOD 1.11142). Never alerted → no correction.
  - XAU: 14:00 sweep / MSS 14:30 still **target None**; fill window ended 15:30. No open sweep windows. 15:30 bar ripped H 4106.31 / C 4102.065 off LOD 4079.73 (15:20) — no marked-pool sweep + MSS, nothing alertable.
  - DXY: 102.742, easing off session high 102.875 (15:20); confluence only.
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups.** No VOID correction needed (nothing alerted is pending). No open Ping-Pong risk.


- 15:44 SAST (NY AM) scanner pass, fetched 15:44 via TradingView; closed candles to 15:40 (last 5m bar open 15:35; last closed 15m still the 15:15 bar, next closes 15:45). scripts/pp_live_scan.py + pp_live_detail.py; raw stdout in data/pp_live/scan_1543.txt and detail_1543.txt. Backup findings/pingpong.md → data/pp_live/pingpong_bak_1543.md. Levels last closes refreshed; last closes: NAS 30391.6, XAU 4098.785, EU 1.11356, GU 1.31994, DXY 102.725 (session high 102.875 on 15:20 holding). PDH/PDL/Asia/London unchanged. Detail vs 15:37: no new sweeps of marked pools, no new MSS; fill-window labels on expired 14:00/14:05 setups unchanged (ended 15:30).
  - Bias gates: unchanged (no new 15m close since 15:30). NAS BEAR (CT long dropped), GU BEAR, XAU BEAR, EU BEAR, DXY BULL.
  - GU: 10:28 IFVG long stays **CLOSED** flat for CPI (+2.15R). 13:51 OTE long stays **VOID** (correction sent 14:11). 14:36 Ping-Pong SHORT stays **VOID** (target traded 14:35 before fill); fill window ended 15:30, never filled (best since MSS 1.32265), stop 1.32726 never hit. Never alerted → no correction.
  - GU: 14:55–15:00 low sweeps (incl. PDL 1.32046 / week low 1.32017) still no MSS (windows open). LOD 1.31846 (15:20); 15:35 bar H 1.32022 / L 1.31973 / C 1.31994. Reverse long would be COUNTER-TREND vs BEAR.
  - NAS: 14:01 OTE long stays **VOID** (correction sent 14:11). 14:36 SHORT stays **VOID**; fill window ended 15:30, never filled (best since MSS 30451.8), stop 30667.0 never hit. All post-CPI low-sweep windows **expired** without MSS. Nothing alertable. 15:35 close 30391.6 (earlier LOD 30320.0 on 15:30).
  - EU: 14:30 sweep / MSS 15:25 Ping-Pong LONG (stop 1.11132 / target 1.11992; OTE 1.11189 R:R 13.96, OB 1.11253 R:R 6.11, IFVG 1.11270 R:R 5.23) stays **VOID** — target traded on the 14:30 sweep bar before any fill. Best since MSS still 1.11285 (15:30); 15:35 close 1.11356 still above all entries (unfilled); stop not hit (LOD 1.11142). Engine fill window still open past 15:35 — moot (VOID). Never alerted → no correction.
  - XAU: 14:00 sweep / MSS 14:30 still **target None**; fill window ended 15:30. No open sweep windows. 15:35 close 4098.785 off LOD 4079.73 — no marked-pool sweep + MSS, nothing alertable.
  - DXY: 102.725, easing off session high 102.875 (15:20); confluence only.
  - Classic: no new with-trend HTF-OTE print at 1:2+.
  - **No new alertable setups.** No VOID correction needed (nothing alerted is pending). No open Ping-Pong risk.

### Alerts sent
| SAST | Inst | Setup | Conf | Dir | Entry | Stop | Target | R:R | Labels |
|---|---|---|---|---|---|---|---|---|---|
| 09:27 | NAS | Ping-Pong | Unicorn | Long (limit) | 30574.6 | 30517.6 | 30704.7 | 2.28 | PROMISING, COUNTER-TREND (EXPIRED 09:42: never filled, low since MSS 30585.5) |
| 09:30 | EU | Ping-Pong | OTE | Short (limit) | 1.12090 | 1.12124 | 1.12022 | 2.04 | UNPROVEN, COUNTER-TREND (VOID 09:37: target hit 09:10 before fill; correction sent) |
| 09:48 | EU | Ping-Pong | OTE | Long (limit) | 1.12024 | 1.11990 | 1.12114 | 2.63 | UNPROVEN (with daily lean bull; vs 15m BOS down) (FILLED 09:45; STOPPED −1.00R at 10:00, low 1.11974) |
| 10:12 | XAU | Ping-Pong | IFVG (alt OTE 4146.41 R:R 4.79 / OB 4146.02 R:R 5.48) | Long (limit) | 4148.05 | 4142.755 | 4163.905 | 3.00 | UNPROVEN, COUNTER-TREND (vs daily bear + 15m BOS down); FILLED 10:35 (low 4144.02); **STOPPED −1.00R** on the 10:50 bar (low 4142.545); target 4163.905 never reached |
| 10:28 | GU | Ping-Pong | IFVG (alt OB 1.32596 R:R 3.47 / OTE 1.32593 R:R 3.89) | Long (limit) | 1.32598 | 1.32558 | 1.32728 | 3.25 | UNPROVEN (with daily bull; vs 15m BOS down); FILLED 10:35 (low 1.32588); **CLOSED flat for CPI 14:29** at 14:25 open 1.32684, **+2.15R** (TP 1.32728 never traded; session high 1.32716; peak 1.32710 at 14:15/14:17; low since fill 1.32582); no open Ping-Pong risk |
| 10:41 | NAS | Ping-Pong | Unicorn (alt OTE 30658.8 R:R 7.64 / IFVG 30651.4 R:R 5.15 / OB 30645.8 R:R 4.04) | Short (limit) | 30651.8 | 30677.0 | 30519.6 | 5.25 | PROMISING (with daily lean bear; with 15m at sweep); **EXPIRED 11:35 never filled** (high since MSS 30629.8; low since sweep 30529.6 on 13:00 — target 30519.6 not hit; stop 30677.0 not hit); not VOID |
| 13:51 | GU | Ping-Pong | OTE | Long (limit) | 1.32603 | 1.32572 | 1.32694 | 2.98 | UNPROVEN (with daily bull; with 15m at sweep); lots 7.98 (0.5% of [REDACTED balance]) / [REDACTED: third-party account sizing]; **VOID 14:06: target 1.32694 hit on 14:00 bar (high 1.32702) before fill (low since MSS 1.32622); correction sent 14:11** |
| 14:01 | NAS | Ping-Pong | OTE | Long (limit) | 30544.9 | 30527.6 | 30617.5 | 4.18 | UNPROVEN, COUNTER-TREND (vs daily lean bear / bias long on hold); lots 14.31 (0.5% of [REDACTED balance] at $1/pt) / [REDACTED: third-party account sizing]; **VOID 14:10: target 30617.5 hit on 14:05 bar (high 30618.6) before fill (low since MSS 30571.6); correction sent 14:11** |

### Correction 10:57 SAST
- XAU Ping-Pong IFVG long 4148.05 (filled 10:35): STOPPED at 4142.755 at 10:51 SAST (1m low 4142.545), -1R. Supersedes OPEN status in the 10:51 pass. (Source: Confluence Bot, OANDA 1m.)

### Correction 14:11 SAST
- GU Ping-Pong OTE long 1.32603 (alerted 13:51): VOID — target 1.32694 hit on 14:00 bar (high 1.32702) before fill (low since MSS 1.32622). Stop never touched.
- NAS Ping-Pong OTE long 30544.9 (alerted 14:01): VOID — target 30617.5 hit on 14:05 bar (high 30618.6) before fill (low since MSS 30571.6). Stop never touched.
- Both pending limits cancelled. GU 10:28 IFVG long 1.32598 still OPEN ≈ +1.55R at 14:15 close 1.3266 (peak high 1.3271); stop 1.32558 / target 1.32728 untouched.

### Close 14:29 SAST — GU Ping-Pong IFVG long 1.32598 (filled 10:35): CLOSED flat for CPI at the 14:25 open 1.32684, +2.15R. TP 1.32728 never traded (high 1.32710 at 14:17). Same position as B6; count once. No open Ping-Pong risk.
