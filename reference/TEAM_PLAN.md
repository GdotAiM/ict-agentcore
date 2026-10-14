# Hilda's ICT trading team: how we work together

Markets: NAS100, XAUUSD, EURUSD, GBPUSD, with DXY for confluence.
Data: TradingView, OANDA symbols (OANDA:NAS100USD, OANDA:XAUUSD, OANDA:EURUSD, OANDA:GBPUSD, TVC:DXY).
Times: SAST (Africa/Johannesburg). Hilda's kill zones are always in NY time and convert to SAST as NY+6 until 1 Nov 2026, then NY+7: Asian 20:00-00:00 (SAST 02:00-06:00), London Open 02:00-05:00 (08:00-11:00), NY AM 07:00-10:00 (13:00-16:00), Silver Bullet 10:00-11:00 (16:00-17:00), London Close 10:00-12:00 (16:00-18:00), NY PM 13:30-16:00 (19:30-22:00). Asia builds the range, London sweeps it (the Judas swing) and NY delivers.
Analysis only. No bot places trades. Never invent prices.

## Shared files (all in /workspace/ict-team/findings/)
Each bot WRITES only its own file and READS the others before working.
Start every update with a timestamp line: `Updated: YYYY-MM-DD HH:MM SAST`.

| Bot | Writes | Reads | When (weekdays, SAST) |
|---|---|---|---|
| Bias Bot | bias.md: per-instrument bias, dealing range, premium/discount, invalidation level, weekly profile | intermarket.md | 07:20, plus a Sunday weekly outlook |
| Intermarket Bot | intermarket.md: DXY, yields, risk-on or risk-off, SMT (EU vs GU, NQ vs ES, gold vs DXY) | bias.md | 07:25 and 12:50 |
| Order Flow Bot | orderflow.md: order flow per instrument and timeframe (FVGs and order blocks respected or failing, displacement), the level that would flip it, agreement with bias | bias.md, liquidity.md, intermarket.md | 07:30, plus kill-zone updates when flow shifts |
| Liquidity Scout | liquidity.md: ranked draws above and below per instrument and timeframe, untouched or swept, and live sweep alerts | bias.md, intermarket.md | 07:35, plus ~15-minute sweep checks |
| Entry Model Bot | setups.md: active and recent full setups (sweep, MSS, FVG/OTE) with entry, stop and target | bias.md, liquidity.md, intermarket.md | during kill zones |
| Scalp Bot | scalps.md: scalp ideas with entry, stop, target, R:R, reason and outcome | liquidity.md (primary driver), setups.md, intermarket.md; bias.md as context only | every ~5 minutes in kill zones |
| Journal Coach | journal file + review.md: stats, best setups and sessions, mistakes | setups.md, scalps.md, Hilda's logged trades | 21:30 log prompt, Saturday 10:00 review |
| Time Pattern Bot | time_patterns.md: recurring time-of-day and day-of-week patterns with sample size and hit rate, plus upcoming pattern windows | liquidity.md, setups.md | weekly research, plus alerts before pattern windows |
| Confluence Bot | confluence.md: price zones where several bots agree, scored 1-5, with conflicts and a trade idea if it meets 1:2 R:R | all findings files | every ~15 minutes in kill zones, plus before the briefing |
| Timeframe Bot | timeframes.md: order flow per timeframe (M to 1m), alignment or conflict, the timeframe in control, recommended timeframe pairing, warnings on setups that fight a higher-timeframe array | bias.md, liquidity.md, setups.md, scalps.md | 07:30, then every ~30 minutes in kill zones |
| Grok Bot (coordinator) | briefing.md: combined picture and disagreements | everything | 07:40 briefing, 12:50 NY update |

## Order of the morning
07:20 Bias, then 07:25 Intermarket, then 07:35 Liquidity, then 07:40 combined briefing, then 07:45 London heads-up. Kill-zone bots start working at the open.

## Rules
- If your file depends on one that's stale (older than today) or missing, say so in your output and work from fresh data.
- Flag disagreements with other bots explicitly. Don't hide them.
- When a level gets swept or a setup triggers, update your file straight away so the others see it.

| ICT Mentor Bot | findings/ict_mentor.md | all findings files | Weekdays 07:35 SAST and at the start of each kill zone. Checks every setup against ICT YouTube teachings and cites the source |

## Team rules from Hilda (7 Oct 2026)
- There is no cap on alerts per kill zone. Alert every valid setup that meets 1:2 or better.
- Counter-trend setups are allowed, but every one must be clearly labelled COUNTER-TREND.
| Ping-Pong Bot | findings/pingpong.md | liquidity.md, timeframes.md, orderflow.md, time_patterns.md | every ~5 minutes in kill zones. Phase Classic and Ping-Pong models (PING_PONG_RULES.md) |
| Probability Bot | findings/probability.md | all findings + time_patterns backtests + review.md | 07:36 SAST and every 15 min in kill zones. Scores win rate and expected R for every setup |

Team rooms (7 Oct+): ICT Market Read c9903ab4 (Bias, Timeframe, Intermarket, Liquidity), ICT Setups cb490cee (Confluence, Entry Model, Scalp, Ping-Pong), ICT Research 12d9f2b7 (Order Flow, Time Pattern, Mentor, Journal). Grok Bot + Probability Bot in all.

- 14 Oct 2026 (Hilda): NO rule against trading again after a loss in the same kill zone. Correlated setups (same dollar direction) share one 0.5% unit while both open; once one closes, the next gets the full 0.5%. If the prior trade lost, the alert says so.
