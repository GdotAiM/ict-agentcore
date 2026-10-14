Updated: 2026-10-14 15:39 SAST

Timeframe Bot | NY AM KZ (07:00-10:00 NY = 13:00-16:00 SAST), run 15:36-15:39 SAST. Full rewrite; previous 15:14 file backed up at /workspace/tf/timeframes_prev_20261014_1514.md.
Source: TradingView via tvDatafeed (nologin) OANDA:NAS100USD, OANDA:XAUUSD, OANDA:EURUSD, OANDA:GBPUSD, TVC:DXY, 1M/1W/1D/4H/1H/15m/5m fetched 15:37 SAST, clean (all 35 symbol/timeframe pairs returned). Structure on CLOSED bars only: 5m to the 15:30 bar, 15m to the 15:15 bar (15:30 15m FORMING until 15:45), 1H to the 14:00 bar (15:00 1H FORMING until 16:00), 4H to the 11:00 bar (DXY 4H to 09:00; DXY 13:00 4H forming until 17:00), D to Tue 13 Oct. Forming-bar prices are marked "intrabar". Raw: /workspace/tf/an_20261014_1536.txt, /workspace/tf/bars_20261014_1536.pkl. No prices invented. Analysis only.

## Peer files
- FRESH: scalps.md (15:37), bias.md (15:33), liquidity.md (15:33), setups.md (15:32), confluence.md (15:31), pingpong.md (15:29). None stale (all today).
- LAGGING: orderflow.md (15:14) is older than the closed 15:00/15:15 15m. intermarket.md (12:59) is pre-CPI. liquidity.md 15:33 still ranks NAS "intraday bullish" from bias.md 15:27, but bias.md 15:33 has NAS BEAR after the 15:15 close (Confluence Bot flagged the same).
- DISAGREEMENT: setups.md (15:32) lists B15 NAS short as PENDING, but the OANDA 15:33 1m/15m high 30410.2 traded through the 30407.25 sell limit before TP1 30300 printed (scalps.md 15:37 flags the same). On OANDA bars B15 is FILLED at 15:33. Entry Model Bot should confirm.

## NAS100 (intrabar 30345.2; day/week L 30320.0 @15:32, 15:30 15m H 30410.2)
- M bull, W bull (retracing, week low 30320.0), D bull structure. Price is inside the tested D bull FVG 29740-30417 and the tested 4H bull FVG 30019-30410.
- 4H BEAR: 11:00 4H closed 30369.8 (break of 30417). 15:00 4H forming 30345.2 (L 30320.0).
- 1H BEAR: 14:00 1H closed 30369.8 (break of 30559). 15:00 1H forming.
- 15m BEAR: 15:00 C 30401.4, 15:15 C 30364.8 (below 30369.8, killing bias.md's CT long). Untested 15m bear FVG 30452-30596 overhead.
- 5m BEAR: 15:15 closed below 30370 (fresh 5m bear break); 15:30 C 30364.6 after a raid to 30410.2.
- Alignment: CONFLICT on HTF only (M/W/D bull vs 4H/1H/15m/5m bear), aligned from 4H down.
- In control: 4H bear, SAME. Reaffirmed by the 15:15 15m close 30364.8.
- Hand-back: a 15m close above 30677 hands control to the bulls (team gate). Earlier warning: a 15m close above 30451.8.
- Pairing: 4H bias + 15m arrays, 5m/1m triggers. Draws 30300 / 30273.2, then 30110.1 / 30100.

## XAUUSD (intrabar 4104.70; day L 4079.73 @15:20, bounce H 4107.37 @15:35)
- M bear, W bear, D bear. D bull FVG 4146.1-4154.7 well above.
- 4H BEAR: 11:00 4H closed 4097.91. 15:00 4H forming 4104.92.
- 1H BEAR: 14:00 1H closed 4097.91. 15:00 1H forming 4104.70.
- 15m BEAR: 15:00 C 4089.19, 15:15 C 4090.40. 15:30 15m forming 4104.70 (H 4107.37), pressing the bottom of the untested 15m bear FVG 4107.7-4144.7.
- 5m BEAR on structure (15:15 closed below 4085.3), but 15:30 5m closed 4102.07 on a displaced bounce, and liquidity.md/scalps.md have a 1m bull MSS (15:29). LTF bounce, not a shift.
- Alignment: ALIGNED bear M→15m; 5m/1m bouncing.
- In control: D/4H bear, SAME.
- Hand-back (team gate): a 15m close above 4170.5 or a 1H close above 4156. Earlier warning: a 15m close above 4107.69. The 15:30 15m (closes 15:45) is 0.3 under it intrabar, so that's the close to watch.
- Pairing: 4H + 15m, 5m/1m triggers. Draws 4075, then 4066.535 (PWL).

## EURUSD (intrabar 1.11356; day L 1.11142 @15:20)
- M bear, W bear, D bear.
- 4H BEAR (11:00 C 1.11290), 1H BEAR (14:00 C 1.11290), 15m BEAR (15:00 C 1.11234, 15:15 C 1.11299), 5m BEAR on structure (15:30 C 1.11329, bouncing).
- Alignment: ALIGNED bear M→15m; 5m bouncing.
- In control: D bear, SAME.
- Hand-back: a 1H close above 1.11982 (confirm above 1.12114). Earlier warning: a 15m close above 1.11452.
- Pairing: D bias + 1H/15m arrays. Draws 1.1100, then 1.1065.

## GBPUSD (intrabar 1.32018; day L 1.31846 @15:20, 0.1 pip above PWL 1.31845)
- M ranging, W bear, D bear.
- 4H BEAR (11:00 C 1.32042), 1H BEAR (14:00 C 1.32042), 15m BEAR (15:00 C 1.31934, 15:15 C 1.31985), 5m BEAR on structure (15:30 C 1.32022, back over the 1.32017 week low intrabar).
- Alignment: ALIGNED bear W→15m; 5m bouncing.
- In control: D bear, SAME (since the 15:14 shift).
- Hand-back: a 1H close above 1.32594 returns control to the 4H/1H bulls. Earlier warning: a 15m close above 1.32192.
- Pairing: D bias + 1H/15m arrays, 5m triggers. Draws 1.31845 (PWL), then 1.31808.

## DXY (intrabar 102.718; day/month H 102.875 @15:20)
- M bull inside the untested monthly bear FVG 101.98-103.20. W bull, D bull.
- 4H BULL (09:00 C 102.25; 13:00 4H forming 102.72). 1H BULL (14:00 C 102.748). 15m BULL (15:00 C 102.804, 15:15 C 102.759). 5m BULL on structure (15:30 C 102.742), 1m rolling over (scalps.md: low 102.711).
- Alignment: ALIGNED bull W→15m; 5m/1m fading.
- In control: D/4H bull, SAME.
- Hand-back: a 1H close below 102.207 (confirm below 102.143). Earlier warning: a 15m close below 102.617. bias.md uses 102.748; the forming 15:30 15m is under it intrabar.
- Intermarket: the dollar fade is what's feeding the XAU/EUR/GBP bounces. It's still an LTF pullback inside a D/4H bull.

## Active and pending ideas vs HTF (every findings file checked)
- setups.md B14 XAUUSD SHORT, OPEN (fill 4105.34, stop 4117.60, TP1 4075 / TP2 4066.53). TREND-ALIGNED with XAU M/W/D/4H/1H/15m bear and DXY D/4H bull. About +0.05R at 4104.70 (best ~+2.09R at 4079.73). Bounce high 4107.37 is just under the 4107.88 early-exit level. The 1m/5m bounce fights it, but no HTF array does.
- setups.md B15 NAS100 SHORT, FILLED 15:33 on OANDA bars (setups.md still says PENDING). Sell 30407.25, stop 30458.5, TP1 30300 / TP2 30273.2. About +1.21R at 30345.2. TREND-ALIGNED with the 4H bear in control and 1H/15m/5m. HTF-array caution (already flagged, not COUNTER-TREND): it sells inside the D bull FVG 29740-30417 under M/W/D bull, so bank TP1/TP2.
- B14 + B15 share one long-dollar 0.5% unit while both are open (team rule).
- scalps.md: no open ideas (S25/S26 −1R final, S20/S22 −1R, S21/G2-1 flat, S23 VOID, S24 MISSED). Next id S27.
- pingpong.md: nothing open or pending. EU Ping-Pong long (15:25 MSS) VOID, never alerted. GU/NAS 14:36 shorts VOID. GU 10:28 IFVG long CLOSED +2.15R. GU 13:51 / NAS 14:01 OTE longs VOID.
- confluence.md: no new idea. Zones NAS sell-side 5/5, XAU sell-side 5/5, EUR sell-side 4/5, DXY bid 4/5, GBP sell-side 3/5. All TREND-ALIGNED.
- Watches (not ideas): setups.md GBP CT long (turtle soup of 1.31845/1.31808) is COUNTER-TREND vs the GBP W/D/4H/1H/15m bear. EUR/GBP continuation shorts off the bounce would be TREND-ALIGNED. Any XAU long off 4079.73 would be COUNTER-TREND vs D/4H/1H/15m bear (scalps.md declined it on R:R).

## Control vs prior (15:14)
- NAS100: SAME, 4H bear. 15:15 15m close 30364.8 reaffirms it; new low 30320.0.
- XAUUSD: SAME, D/4H bear. No 15m close above 4170.5, no 1H close above 4156. The 15:30 15m bounce is the first LTF test (watch 4107.69 at 15:45).
- EURUSD: SAME, D bear.
- GBPUSD: SAME, D bear (held since the 15:14 shift). 15m closes 1.31934 / 1.31985, far under 1.32192.
- DXY: SAME, D/4H bull. Fading off 102.875 on the 1m/5m only.
- Watch next: the 15:30 15m closes at 15:45 (XAU vs 4107.69, DXY vs 102.748/102.617), then the 15:00 1H closes at 16:00, then the DXY 13:00 4H close at 17:00. Silver Bullet 16:00-17:00 bounce risk is high with everything extended.

## New conflict warnings since 15:14
- None. No new COUNTER-TREND idea is live or pending. B14 and B15 are both TREND-ALIGNED with the timeframe in control.
- Status change only: B15 filled at 15:33 on OANDA (setups.md not yet updated). Its HTF-array caution was already flagged at 15:14.
- No control shift. No alert.
