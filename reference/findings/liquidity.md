Updated: 2026-10-14 15:43 SAST
Data source: TradingView OANDA:NAS100USD [15m, 1d, 1h, 1m, 4h, 5m]; TradingView OANDA:XAUUSD [15m, 1d, 1h, 1m, 4h, 5m]; TradingView OANDA:EURUSD [15m, 1d, 1h, 1m, 4h, 5m]; TradingView OANDA:GBPUSD [15m, 1d, 1h, 1m, 4h, 5m]; TradingView TVC:DXY [15m, 1d, 1h, 1m, 4h, 5m] (map built 2026-10-14 15:42 SAST). OANDA CFD/TVC index prices; never invented.

## Peer files
- bias.md: fresh (Updated 2026-10-14 15:33 SAST)
- intermarket.md: fresh (Updated 2026-10-14 12:59 SAST)
- Bias used for ranking (freshest of bias.md / intermarket.md per instrument; morning bias only as fallback; bearish or neutral -> sell-side ranked first):
  - NAS100: intraday bullish (source: bias.md (15:27) intraday); daily neutral (context)
  - XAUUSD: intraday bearish (source: bias.md (15:27) intraday); daily bearish (context)
  - EURUSD: intraday bearish (source: bias.md (15:27) intraday); daily bullish (context)
  - GBPUSD: intraday bearish (source: bias.md (15:27) intraday); daily bullish (context)
  - DXY: intraday bullish (source: bias.md (15:27) intraday); daily bearish (context)
- DISAGREE NAS100: bias.md (15:27) intraday bullish vs intermarket.md (12:59) bearish -> using bullish from bias.md (15:27) intraday
- DISAGREE GBPUSD: bias.md (15:27) intraday bearish vs intermarket.md (12:59) bullish -> using bearish from bias.md (15:27) intraday
- CONTEXT NAS100: intraday bullish runs against daily neutral
- CONTEXT EURUSD: intraday bearish runs against daily bullish
- CONTEXT GBPUSD: intraday bearish runs against daily bullish
- CONTEXT DXY: intraday bullish runs against daily bearish

Ranking = weighted heuristic (bias alignment, TF weight, liquidity-type count, PD/PW/PM, 4H-15m order flow, minus distance/ADR). Tag = kill-zone reach estimate vs 14d ADR. Kill zones (NY time -> SAST today): Asian KZ 02:00-06:00; London Open KZ 08:00-11:00; NY AM KZ 13:00-16:00; Silver Bullet 16:00-17:00; London Close KZ 16:00-18:00; NY PM KZ 19:30-22:00. 'now:' only inside an active kill zone.

## NAS100 (OANDA:NAS100USD) - intraday bias bullish (source: bias.md (15:27) intraday), daily neutral
Price at map build: 30429.2

Structure:
- D: DR 30312-31401, EQ 30856, discount 11.3%, flow bull (BOS bull @10-05 00:00), ERL->IRL
- 4H: DR 30312-30705, EQ 30508, discount 31.3%, flow bear (BOS bear @10-14 11:00), ERL->IRL
- 1H: DR 30312-30705, EQ 30508, discount 31.3%, flow bear (MSS bear @10-14 14:00), ERL->IRL
- 15m: DR 30312-30665, EQ 30488, discount 34.8%, flow bear (MSS bear @10-14 14:30), ERL->IRL
- 5m: DR 30312-30452, EQ 30382, premium 87.6%, flow bear (MSS bear @10-14 14:30), ERL->IRL
- 1m: DR 30312-30436, EQ 30374, premium 98.9%, flow bull (MSS bull @10-14 15:40), IRL->ERL

Ranked above:
- TOP1 30704.7 [level = 4H Old high BSL 30704.7; cluster 30689.8-30704.7] (+275.5pts, +0.905%) [London Close KZ] untouched :: 5m Old high BSL + 1m REQH + 5m REQH + 5m EQH + 1m EQH + 4H Old high BSL + 1H Old high BSL + 15m Old high BSL + sess today's day high + sess today Asian KZ high
- TOP2 30720.8 [level = 15m REQH 30720.8; cluster 30707.8-30720.8] (+291.6pts, +0.958%) [London Close KZ] untouched :: 1m EQH + 1m REQH + D PDH + 15m REQH + 5m REQH
- TOP3 30665 [level = 15m Old high BSL 30665; cluster 30655-30665] (+235.8pts, +0.775%) [Silver Bullet] untouched :: 5m 08:30 NY open + 15m Old high BSL + 5m Old high BSL + 1m Old high BSL + sess today NY AM KZ high + sess today NY high

Ranked below:
- TOP1 30311.5 [level = 1m Old low SSL 30311.5] (-117.7pts, -0.387%) [Silver Bullet] untouched :: 1m Old low SSL + sess today NY AM KZ low + sess today NY low + sess today's day low
- TOP2 30110.1 [level = D Old low SSL 30110.1] (-319.1pts, -1.049%) [London Close KZ] untouched :: D Old low SSL + 4H Old low SSL + 4H EQL + 1H EQL
- TOP3 30273.2 [level = 1H EQL 30273.2; cluster 30273.2-30279.7] (-156.0pts, -0.513%) [Silver Bullet] untouched :: 4H Old low SSL + 4H REQL + 1H EQL

Swept today / removed from ranking: 30320 (below, logged sweep 15:38, pending reclaim (1/3 closes inside)); 30346 (below, logged sweep 15:31, pending reclaim (2/3 closes inside)); 30356 (below, logged sweep 15:19, reclaimed/reversal); 30370 (below, logged sweep 14:58, contested/chop); 30400 (below, logged sweep 14:36, continuation); 30520 (below, logged sweep 14:30, continuation); 30500 (below, logged sweep 14:30, continuation); 30580 (above, logged sweep 13:58, reclaimed/reversal COUNTER-TREND (bearish reclaim vs intraday bullish bias)); 30576 (above, logged sweep 13:32, reclaimed/reversal COUNTER-TREND (bearish reclaim vs intraday bullish bias)); 30439 sess prior London Open KZ low (swept 10-13 15:28); 30417 sess prior Asian KZ low (swept 10-13 15:32); 30445 sess prior London Close KZ low (swept 10-14 14:31); 30401 D PDL (swept 10-14 14:36); 30401 sess prior NY AM KZ low (swept 10-14 14:36); 30401 sess prior NY low (swept 10-14 14:36); 30400 - Round number (swept 10-14 14:36); 30475 1H Bear breaker (swept 10-13 14:01); 30478 4H Bear FVG (swept 10-14 11:01); 30479 M Monthly open (swept 10-14 00:01)

Secondary (nearest 8): 30452 (above, +22.6pts) 5m Old high BSL; 30526 (above, +96.3pts) 15m Bear FVG; 30300 (below, -129.2pts) 4H Old low SSL; 30200 (below, -229.2pts) 4H Bull FVG; 30675 (above, +245.8pts) 15m Old high BSL; 30139 (below, -290.6pts) 4H Old low SSL; 30750 (above, +321.1pts) 1m EQH; 30078 (below, -351.0pts) D Bull FVG

## XAUUSD (OANDA:XAUUSD) - intraday bias bearish (source: bias.md (15:27) intraday), daily bearish
Price at map build: 4098.305

Structure:
- D: DR 4066.5-4217.4, EQ 4142, discount 22.3%, flow bear (BOS bear @09-28 00:00), ERL->IRL
- 4H: DR 4079.7-4200.6, EQ 4140.2, discount 16.9%, flow bear (MSS bear @10-14 07:00), ERL->IRL
- 1H: DR 4079.7-4170.5, EQ 4125.1, discount 22.5%, flow bear (MSS bear @10-14 10:00), ERL->IRL
- 15m: DR 4079.7-4155.8, EQ 4117.8, discount 26.8%, flow bear (MSS bear @10-14 14:30), ERL->IRL
- 5m: DR 4079.7-4155.8, EQ 4117.8, discount 26.8%, flow bear (BOS bear @10-14 15:15), ERL->IRL
- 1m: DR 4079.7-4107.4, EQ 4093.6, premium 73.8%, flow bull (MSS bull @10-14 15:29), ERL->IRL

Ranked below:
- TOP1 4066.53 [level = W PWL 4066.53] (-31.8USD, -0.775%) [Silver Bullet] untouched :: W PWL + D Old low SSL + 4H Old low SSL + 1H Old low SSL
- TOP2 4079.73 [level = 5m Old low SSL 4079.73] (-18.6USD, -0.453%) [Silver Bullet] untouched :: 5m Old low SSL + 1m Old low SSL + sess today NY AM KZ low + sess today NY low + sess today's day low
- TOP3 4019.24 [level = D Old low SSL 4019.24] (-79.1USD, -1.929%) [beyond today (multi-day)] untouched :: D Old low SSL

Ranked above:
- TOP1 4170.49 [level = 1H Old high BSL 4170.49] (+72.2USD, +1.761%) [London Close KZ] untouched :: 1H Old high BSL + 15m Old high BSL + 5m Old high BSL + sess today's day high + sess today Asian KZ high
- TOP2 4155.84 [level = 15m Old high BSL 4155.84; cluster 4153.38-4155.84] (+57.5USD, +1.404%) [London Close KZ] untouched :: 5m 08:30 NY open + 15m Old high BSL + 5m Old high BSL + 1m Old high BSL + sess today NY AM KZ high + sess today NY high
- TOP3 4173.19 [level = 15m Old high BSL 4173.19] (+74.9USD, +1.827%) [London Close KZ] untouched :: 15m Old high BSL + sess prior Silver Bullet high + sess prior London Close KZ high + 1m REQH + 1m EQH

Swept today / removed from ranking: 4083 (below, logged sweep 15:12, reclaimed/reversal COUNTER-TREND (bullish reclaim vs intraday bearish bias)); 4085.3 (below, logged sweep 15:01, reclaimed/reversal COUNTER-TREND (bullish reclaim vs intraday bearish bias)); 4098.8 (below, logged sweep 14:41, contested/chop); 4116.9 (below, logged sweep 14:34, continuation); 4136 (below, logged sweep 14:30, continuation); 4141.1 (below, logged sweep 12:01, continuation); 4142.2 (below, logged sweep 10:58, continuation); 4143.8 (below, logged sweep 09:21, continuation); 4100 - Round number (swept 10-14 14:41); 4096.2 D Bull breaker (swept 10-07 14:25); 4106.7 5m Bear FVG (swept 10-14 14:51); 4089.1 5m Bull FVG (swept 10-14 15:26); 4087.9 5m Volume imbalance (swept 10-14 15:26); 4110.9 M PML (swept 10-06 04:35); 4121.2 4H Bear breaker (swept 10-08 11:05); 4121.7 1H Bear FVG (swept 10-14 14:01); 4124.4 4H Bear FVG (swept 10-14 11:01); 4125 - Round number (swept 10-14 00:04)

Secondary (nearest 8): 4094.6 (below, -3.7USD) 5m Bull FVG; 4090.4 (below, -7.9USD) 5m Volume imbalance [internal to today NY AM KZ low 4079.73]; 4109.9 (above, +11.6USD) 1m Old high BSL; 4075 (below, -23.3USD) - Round number; 4050 (below, -48.3USD) - Round number; 4157.9 (above, +59.6USD) 15m Old high BSL [internal to today London Open KZ high 4163.9]; 4163.9 (above, +65.6USD) 15m Old high BSL; 4167.2 (above, +68.9USD) 15m Old high BSL [internal to today's day high 4170.49]

## EURUSD (OANDA:EURUSD) - intraday bias bearish (source: bias.md (15:27) intraday), daily bullish
Price at map build: 1.11278

Structure:
- D: DR 1.1114-1.1654, EQ 1.1384, discount 2.6%, flow bear (BOS bear @10-12 00:00), IRL->ERL
- 4H: DR 1.1114-1.1217, EQ 1.1166, discount 13.8%, flow bear (BOS bear @10-14 11:00), ERL->IRL
- 1H: DR 1.1114-1.1211, EQ 1.1163, discount 14.6%, flow bear (MSS bear @10-14 10:00), ERL->IRL
- 15m: DR 1.1114-1.1199, EQ 1.1157, discount 16.7%, flow bear (BOS bear @10-14 14:30), ERL->IRL
- 5m: DR 1.1114-1.1199, EQ 1.1157, discount 16.7%, flow bear (MSS bear @10-14 14:30), ERL->IRL
- 1m: DR 1.1114-1.1137, EQ 1.1126, premium 61.2%, flow bull (MSS bull @10-14 15:29), ERL->IRL

Ranked below:
- TOP1 1.11142 [level = 5m Old low SSL 1.11142] (-13.6pips, -0.122%) [Silver Bullet] untouched :: 5m Old low SSL + 1m Old low SSL + sess today NY AM KZ low + sess today NY low + sess today's day low + 1m REQL

Ranked above:
- TOP1 1.11464 [level = 5m Bear FVG 1.11464; cluster 1.11452-1.11464] (+18.5pips, +0.167%) [Silver Bullet] untouched :: 1m Old high BSL + 5m Bear FVG
- TOP2 1.12768 [level = W PWH 1.12768] (+149.0pips, +1.339%) [beyond today (multi-day)] untouched :: W PWH + 4H Old high BSL + 1H Old high BSL + 5m EQH
- TOP3 1.12114 [level = 1H Old high BSL 1.12114] (+83.6pips, +0.751%) [beyond today (multi-day)] untouched :: 1H Old high BSL + 15m Old high BSL + 5m Old high BSL + sess today's day high + sess today London Open KZ high + 15m EQH + 5m EQH + 5m REQH + 1m EQH

Swept today / removed from ranking: 1.1115 (below, logged sweep 15:20, reclaimed/reversal COUNTER-TREND (bullish reclaim vs intraday bearish bias)); 1.1132 (below, logged sweep 14:58, contested/chop); 1.1153 (below, logged sweep 14:33, continuation); 1.1188 (below, logged sweep 14:30, continuation); 1.1185 (below, logged sweep 14:30, continuation); 1.1197 (above, logged sweep 14:12, reclaimed/reversal); 1.1194 (above, logged sweep 13:39, reclaimed/reversal); 1.1192 (above, logged sweep 13:14, reclaimed/reversal); 1.1193 (below, logged sweep 11:27, continuation); 1.1125 5m Bull FVG (swept 10-14 15:26); 1.115 - Round number (swept 10-14 00:01); 1.1154 D PDL (swept 10-14 14:31); 1.1154 sess prior Asian KZ low (swept 10-14 14:31); 1.1161 W PWL (swept 10-12 17:42); 1.1163 1H Bear FVG (swept 10-14 14:01); 1.1166 4H Bear FVG (swept 10-14 11:01); 1.1172 sess prior London Open KZ low (swept 10-14 14:30); 1.1178 sess prior Asian KZ high (swept 10-13 07:53); 1.1185 sess prior London Close KZ low (swept 10-14 14:30)

Secondary (nearest 8): 1.1141 (above, +13.5pips) 5m Volume imbalance; 1.11 (below, -27.8pips) - Round number; 1.1168 (above, +40.3pips) 15m Bear FVG; 1.1173 (above, +44.8pips) 5m Bear FVG; 1.1199 (above, +71.4pips) 5m 08:30 NY open; 1.105 (below, -77.8pips) - Round number; 1.1208 (above, +80.4pips) 5m Old high BSL [internal to today's day high 1.12114]; 1.1217 (above, +89.4pips) 5m REQH

## GBPUSD (OANDA:GBPUSD) - intraday bias bearish (source: bias.md (15:27) intraday), daily bullish
Price at map build: 1.31926

Structure:
- D: DR 1.3184-1.3286, EQ 1.3235, discount 8.8%, flow bear (BOS bear @10-01 00:00), IRL->ERL
- 4H: DR 1.3185-1.3275, EQ 1.323, discount 9.7%, flow bull (BOS bull @10-14 03:00), IRL->ERL
- 1H: DR 1.3185-1.3275, EQ 1.323, discount 9.7%, flow bear (MSS bear @10-14 14:00), IRL->ERL
- 15m: DR 1.3185-1.3272, EQ 1.3228, discount 10.1%, flow bear (BOS bear @10-14 14:30), ERL->IRL
- 5m: DR 1.3185-1.3272, EQ 1.3228, discount 10.1%, flow bear (MSS bear @10-14 14:30), ERL->IRL
- 1m: DR 1.3185-1.3206, EQ 1.3195, discount 41.9%, flow bull (MSS bull @10-14 15:29), ERL->IRL

Ranked below:
- TOP1 1.31845 [level = W PWL 1.31845] (-8.1pips, -0.061%) [now: NY AM KZ] untouched :: W PWL + D Old low SSL + 4H Old low SSL + 1H Old low SSL + 15m EQL + 5m EQL
- TOP2 1.31808 [level = D Old low SSL 1.31808] (-11.8pips, -0.089%) [Silver Bullet] untouched :: D Old low SSL + 4H Old low SSL + D REQL + 4H REQL + 1H EQL + 15m REQL + 15m EQL
- TOP3 1.31846 [level = 5m Old low SSL 1.31846] (-8.0pips, -0.061%) [now: NY AM KZ] untouched :: 5m Old low SSL + 1m Old low SSL + sess today NY AM KZ low + sess today NY low + sess today's day low + 1m REQL

Ranked above:
- TOP1 1.32198 [level = 5m Bear FVG 1.32198; cluster 1.32192-1.32197] (+27.2pips, +0.206%) [Silver Bullet] untouched :: 1m Old high BSL + 1m REQH + 5m Bear FVG
- TOP2 1.32857 [level = W PWH 1.32857] (+93.1pips, +0.706%) [beyond today (multi-day)] untouched :: W PWH + D Old high BSL + 4H Old high BSL + 15m REQH
- TOP3 1.32056 [level = 1m Old high BSL 1.32056] (+13.0pips, +0.099%) [Silver Bullet] untouched :: 1m Old high BSL

Swept today / removed from ranking: 1.3186 (below, logged sweep 15:20, reclaimed/reversal COUNTER-TREND (bullish reclaim vs intraday bearish bias)); 1.3202 (below, logged sweep 15:00, continuation); 1.32 (below, logged sweep 15:00, contested/chop); 1.3257 (below, logged sweep 14:30, continuation); 1.3195 5m Bull FVG (swept 10-14 15:28); 1.32 - Round number (swept 10-14 00:01); 1.3202 M PML (swept 10-14 15:00); 1.3205 D PDL (swept 10-14 14:59); 1.3205 sess prior Asian KZ low (swept 10-14 14:59); 1.3207 5m Bear FVG (swept 10-14 14:56); 1.3208 1H Bear breaker (swept 10-13 00:54); 1.3213 15m Volume imbalance (swept 10-14 14:46); 1.3217 sess prior London Open KZ low (swept 10-14 14:35); 1.3221 4H Bull breaker (swept 10-05 17:00)

Secondary (nearest 8): 1.3215 (above, +22.7pips) 5m Volume imbalance; 1.315 (below, -42.6pips) - Round number; 1.3243 (above, +50.0pips) 15m Bear FVG; 1.314 (below, -52.4pips) D Old low SSL; 1.3247 (above, +54.4pips) 5m Bear FVG; 1.3268 (above, +75.7pips) 5m 08:30 NY open [internal to today NY AM KZ high 1.32716]; 1.3272 (above, +79.0pips) 15m Old high BSL; 1.3273 (above, +80.2pips) 15m Old high BSL

## DXY (TVC:DXY) - intraday bias bullish (source: bias.md (15:27) intraday), daily bearish
Price at map build: 102.784

Structure:
- D: DR 98.599-102.88, EQ 100.74, premium 97.6%, flow bull (BOS bull @10-12 00:00), IRL->ERL
- 4H: DR 102.08-102.88, EQ 102.47, premium 87.0%, flow bull (BOS bull @10-12 11:00), ERL->IRL
- 1H: DR 102.08-102.88, EQ 102.47, premium 87.0%, flow bull (MSS bull @10-14 14:00), ERL->IRL
- 15m: DR 102.19-102.88, EQ 102.53, premium 84.8%, flow bull (BOS bull @10-14 14:30), ERL->IRL
- 5m: DR 102.19-102.88, EQ 102.53, premium 84.8%, flow bull (MSS bull @10-14 14:30), ERL->IRL
- 1m: DR 102.71-102.88, EQ 102.79, discount 37.0%, flow bear (MSS bear @10-14 15:29), ERL->IRL

Ranked above:
- TOP1 102.875 [level = 5m Old high BSL 102.875] (+0.1pts, +0.089%) [Silver Bullet] untouched :: 5m Old high BSL + 1m Old high BSL + sess today NY AM KZ high + sess today NY high + sess today's day high + 1m REQH

Ranked below:
- TOP1 102.614 [level = 5m Bull FVG 102.614; cluster 102.614-102.617] (-0.2pts, -0.165%) [Silver Bullet] untouched :: 1m Old low SSL + 1m EQL + 5m Bull FVG
- TOP2 102.193 [level = 15m Old low SSL 102.193; cluster 102.193-102.207] (-0.6pts, -0.575%) [beyond today (multi-day)] untouched :: 15m Rising TL SSL + 5m 08:30 NY open + 15m Old low SSL + 5m Old low SSL + 5m Bull FVG + 1m Old low SSL + sess today NY AM KZ low + sess today NY low + 5m EQL + 5m REQL + 1m REQL
- TOP3 101.754 [level = W PWL 101.754; cluster 101.754-101.772] (-1.0pts, -1.002%) [beyond today (multi-day)] untouched :: 15m REQL + 5m REQL + W PWL + 4H Old low SSL + 15m EQL

Swept today / removed from ranking: 102.86 (above, logged sweep 15:20, reclaimed/reversal COUNTER-TREND (bearish reclaim vs intraday bullish bias)); 102.72 (above, logged sweep 14:58, continuation); 102.59 (above, logged sweep 14:35, continuation); 102.61 (above, logged sweep 14:35, continuation); 102.54 (above, logged sweep 14:31, continuation); 102.27 (above, logged sweep 14:30, continuation); 102.31 (above, logged sweep 14:30, continuation); 102.2 (below, logged sweep 14:16, reclaimed/reversal); 102.79 5m Bear FVG (swept 10-14 15:26); 102.72 5m Bull FVG (swept 10-14 14:56); 102.68 15m Volume imbalance (swept 10-14 14:46); 102.57 D PDH (swept 10-14 14:33); 102.57 sess prior Asian KZ high (swept 10-14 14:33); 102.53 W PWH (swept 10-13 01:55); 102.5 - Round number (swept 10-14 00:01); 102.49 1H Bull FVG (swept 10-14 14:01); 102.44 sess prior London Open KZ high (swept 10-14 14:30); 102.39 sess prior Asian KZ low (swept 10-13 07:54)

Secondary (nearest 8): 103 (above, +0.2pts) - Round number; 102.58 (below, -0.2pts) 5m Volume imbalance; 102.43 (below, -0.4pts) 15m Bull FVG; 102.41 (below, -0.4pts) 5m Bull FVG; 102.14 (below, -0.6pts) 5m Old low SSL [internal to today London Open KZ low 102.092]; 103.5 (above, +0.7pts) - Round number; 102.11 (below, -0.7pts) 5m Old low SSL [internal to today London Open KZ low 102.092]; 102.09 (below, -0.7pts) 15m Old low SSL

## Live sweeps (newest first)
- 2026-10-14 15:38 SAST NAS100 below 30320 swept, extreme 30312, pending reclaim (1/3 closes inside) (1 inside / 0 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 15:31 SAST NAS100 below 30346 swept, extreme 30320, pending reclaim (2/3 closes inside) (2 inside / 0 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 15:20 SAST EURUSD below 1.1115 swept, extreme 1.1114, reclaimed/reversal (4 inside / 0 beyond of 5m closes, checked 15:41) COUNTER-TREND (bullish reclaim vs intraday bearish bias) [in NY AM KZ]
- 2026-10-14 15:20 SAST GBPUSD below 1.3186 swept, extreme 1.3185, reclaimed/reversal (4 inside / 0 beyond of 5m closes, checked 15:41) COUNTER-TREND (bullish reclaim vs intraday bearish bias) [in NY AM KZ]
- 2026-10-14 15:20 SAST DXY above 102.86 swept, extreme 102.88, reclaimed/reversal (4 inside / 0 beyond of 5m closes, checked 15:41) COUNTER-TREND (bearish reclaim vs intraday bullish bias) [in NY AM KZ]
- 2026-10-14 15:19 SAST NAS100 below 30356 swept, extreme 30351, reclaimed/reversal (5 inside / 0 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 15:12 SAST XAUUSD below 4083 swept, extreme 4079.7, reclaimed/reversal (5 inside / 1 beyond of 5m closes, checked 15:41) COUNTER-TREND (bullish reclaim vs intraday bearish bias) [in NY AM KZ]
- 2026-10-14 15:01 SAST XAUUSD below 4085.3 swept, extreme 4083, reclaimed/reversal (7 inside / 1 beyond of 5m closes, checked 15:41) COUNTER-TREND (bullish reclaim vs intraday bearish bias) [in NY AM KZ]
- 2026-10-14 15:00 SAST GBPUSD below 1.3202 swept, extreme 1.3186, continuation (0 inside / 8 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 15:00 SAST GBPUSD below 1.32 swept, extreme 1.3186, contested/chop (1 inside / 7 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:58 SAST NAS100 below 30370 swept, extreme 30356, contested/chop (5 inside / 4 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:58 SAST EURUSD below 1.1132 swept, extreme 1.1115, contested/chop (2 inside / 7 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:58 SAST DXY above 102.72 swept, extreme 102.86, continuation (0 inside / 9 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:41 SAST XAUUSD below 4098.8 swept, extreme 4085.3, contested/chop (3 inside / 9 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:36 SAST NAS100 below 30400 swept, extreme 30370, continuation (4 inside / 9 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:35 SAST DXY above 102.59 swept, extreme 102.72, continuation (0 inside / 13 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:35 SAST DXY above 102.61 swept, extreme 102.72, continuation (0 inside / 13 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:34 SAST XAUUSD below 4116.9 swept, extreme 4085.3, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:33 SAST EURUSD below 1.1153 swept, extreme 1.1133, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:31 SAST DXY above 102.54 swept, extreme 102.72, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST XAUUSD below 4136 swept, extreme 4124.6, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST EURUSD below 1.1188 swept, extreme 1.1171, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST EURUSD below 1.1185 swept, extreme 1.1171, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST GBPUSD below 1.3257 swept, extreme 1.3241, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST DXY above 102.27 swept, extreme 102.35, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST DXY above 102.31 swept, extreme 102.35, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST NAS100 below 30520 swept, extreme 30483, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:30 SAST NAS100 below 30500 swept, extreme 30483, continuation (0 inside / 14 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:16 SAST DXY below 102.2 swept, extreme 102.19, reclaimed/reversal (16 inside / 1 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 14:12 SAST EURUSD above 1.1197 swept, extreme 1.1199, reclaimed/reversal (17 inside / 1 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 13:58 SAST NAS100 above 30580 swept, extreme 30583, reclaimed/reversal (15 inside / 6 beyond of 5m closes, checked 15:41) COUNTER-TREND (bearish reclaim vs intraday bullish bias) [in NY AM KZ]
- 2026-10-14 13:39 SAST EURUSD above 1.1194 swept, extreme 1.1195, reclaimed/reversal (18 inside / 7 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 13:32 SAST NAS100 above 30576 swept, extreme 30580, reclaimed/reversal (20 inside / 6 beyond of 5m closes, checked 15:41) COUNTER-TREND (bearish reclaim vs intraday bullish bias) [in NY AM KZ]
- 2026-10-14 13:14 SAST EURUSD above 1.1192 swept, extreme 1.1194, reclaimed/reversal (15 inside / 15 beyond of 5m closes, checked 15:41) [in NY AM KZ]
- 2026-10-14 12:01 SAST XAUUSD below 4141.1 swept, extreme 4140.5, continuation (16 inside / 28 beyond of 5m closes, checked 15:41) [outside KZ]
- 2026-10-14 11:27 SAST EURUSD below 1.1193 swept, extreme 1.119, continuation (11 inside / 40 beyond of 5m closes, checked 15:41) [outside KZ]
- 2026-10-14 10:58 SAST XAUUSD below 4142.2 swept, extreme 4141.2, continuation (26 inside / 31 beyond of 5m closes, checked 15:41) [in London Open KZ]
- 2026-10-14 09:21 SAST XAUUSD below 4143.8 swept, extreme 4143.7, continuation (29 inside / 47 beyond of 5m closes, checked 15:41) [in London Open KZ]
