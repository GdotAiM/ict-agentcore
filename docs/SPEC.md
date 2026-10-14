# ICT Multi-Agent Pipeline: Build Spec (handover)

Owner: Hilda (timezone SAST, Africa/Johannesburg). Prepared 2026-10-14.
Reference design: https://github.com/GdotAiM/novamart-agentcore-multi-agent (Strands Agents on Amazon Bedrock AgentCore: orchestrator + specialist agents, Knowledge Bases, Guardrails, Memory, DynamoDB shared state, X-Ray tracing). Copy the *patterns*, not the customer-support domain.
Sample data and the current team rules are in `reference/` (sensitive data redacted, see end).

This system produces **analysis and alerts only**. It never places trades. Not financial advice.

---

## 1. Goal

Today 13 bots each post their own alerts into three group chats and write their own markdown files. Result on 14 Oct: dozens of overlapping messages, bots disagreeing about whether a trade filled or stopped, stale files being read as current.

Build **one pipeline** that runs once per kill zone (and re-evaluates on a timer inside it, e.g. every 5 min on closed candles) and sends Hilda **one combined call**: either "no trade" with reasons, or a short list of trades that passed every hard rule, each with entry, stop, TP, R:R, size, confluence score, probability and a trace link.

## 2. Architecture

```mermaid
flowchart TD
    S[Scheduler: kill-zone clock from NY time] --> O[Orchestrator / Lead agent]
    D[(Market data service\nTradingView OANDA -> fallback)] --> O
    O --> MR{{Market read - parallel}}
    MR --> BIAS[Bias]
    MR --> TF[Timeframe]
    MR --> IM[Intermarket]
    MR --> LIQ[Liquidity Scout]
    MR --> OF[Order Flow]
    BIAS & TF & IM & LIQ & OF --> CTX[Market context object]
    CTX --> SF{{Setup finders - parallel}}
    SF --> EM[Entry Model]
    SF --> SC[Scalp]
    SF --> PP[Ping-Pong]
    EM & SC & PP --> CAND[Candidate setups]
    CAND --> CF[Confluence]
    CF --> PR[Probability]
    PR --> MEN[ICT Mentor]
    MEN --> RULES[Hard-rule engine - code, not LLM]
    RULES -->|pass| ALERT[One combined call to Hilda]
    RULES -->|blocked| LOG
    ALERT --> LOG[Journal Coach + Time Pattern logging]
    ST[(Trade-state table)] <--> RULES
    ST <--> LOG
    KB[(Knowledge base: ICT transcripts + rule files)] --> MEN
    KB --> PR
    GR[Guardrails] -.-> O
    TR[Tracing] -.-> O
```

Principles:
- Agents never talk to each other directly. Each receives an input object from the orchestrator and returns **strict JSON** (validate with pydantic / JSON Schema; invalid output = agent result discarded and logged, never guessed).
- Every output carries `as_of` (SAST ISO timestamp of the last **closed** candle used) and `data_source`. The orchestrator rejects outputs older than the current cycle (fixes stale files).
- Rules that decide money are in deterministic code (section 3), not prompts.
- Markdown findings files become optional human-readable *renders* of the JSON, not the source of truth.

### Common envelope (every agent)
```json
{
  "agent": "bias",
  "run_id": "uuid",
  "as_of": "2026-10-14T15:45:00+02:00",
  "data_source": "TV:OANDA" ,
  "fallback_used": false,
  "instruments": { "<SYMBOL>": { ...agent-specific... } },
  "notes": "max 300 chars",
  "errors": []
}
```
`<SYMBOL>` is one of `NAS100, XAUUSD, EURUSD, GBPUSD, DXY`. Prices are numbers, never strings. Times are ISO 8601 with offset.

### 2.1 Orchestrator (lead agent)
- Role: decides when to run (kill-zone clock), fetches data once and shares it, fans out agents, collects JSON, runs rule engine, writes trade-state table, sends the single message, owns the trace.
- Inputs: clock, data service, trade-state table, previous cycle context.
- Output: `CombinedCall`:
```json
{ "run_id":"", "kill_zone":"NY_AM", "as_of":"", "headline":"No trade | 1 setup",
  "market_summary": {"NAS100":"bearish, invalid > 30720", "...": "..."},
  "trades":[{"trade_id":"B15","instrument":"NAS100","direction":"short","order":"limit",
     "entry":30407.25,"stop":30458.5,"tp1":30300,"rr":2.1,"risk_unit":"U3","risk_pct":0.5,
     "early_exit":"1m close > 30419.2","counter_trend":false,"confluence":4,
     "p_win":0.38,"exp_r":0.17,"sources":["entry_model","liquidity"],"trace_url":""}],
  "open_trade_updates":[{"trade_id":"B14","status":"open","note":"close if 1m closes > 4107.88"}],
  "blocked":[{"candidate_id":"","reason":"RR_BELOW_2_AFTER_STOP_PAD"}] }
```

### 2.2 Market-read agents (parallel)
| Agent | Role (from current bot) | Inputs | Instrument-level JSON output |
|---|---|---|---|
| Bias | HTF narrative: M/W/D order flow, dealing range, premium/discount, draw on liquidity, weekly profile | D/W/M bars | `{"bias":"bullish|bearish|neutral","confidence":0-1,"dealing_range":{"high":n,"low":n},"zone":"premium|discount|eq","draw_on_liquidity":n,"invalidation":n,"weekly_profile":"str","reason":"str"}` |
| Timeframe | Order flow on M,W,D,4H,1H,15m,5m,1m; alignment; which TF in control; recommended pairing | all TF bars, Bias output | `{"per_tf":{"D":{"dir":"bull|bear|range","pd_array":{"type":"FVG|OB|breaker","low":n,"high":n},"zone":"premium|discount"}, "...":{}},"aligned":bool,"in_control":"1H","pairing":"D-15m-1m","conflicts":["str"]}` |
| Intermarket | DXY, US10Y/US02Y, NAS vs ES, EU vs GU SMT, gold vs DXY/yields, risk-on/off | DXY, yields, ES, pairs | `{"dxy_dir":"up|down|flat","yields_dir":"up|down|flat","risk":"on|off|mixed","smt":[{"pair":"EURUSD/GBPUSD","side":"high|low","leader":"EURUSD","time":""}],"supports":"long|short|none","reason":"str"}` |
| Liquidity Scout | EQH/EQL and relative equal highs/lows, PDH/PDL, session highs/lows, swept or resting | bars all TFs | `{"pools":[{"id":"","type":"EQH|EQL|PDH|PDL|ASIA_H|ASIA_L|LON_H|LON_L|SWING","tf":"15m","price":n,"touches":[""],"tolerance":n,"status":"resting|swept","swept_at":null,"distance":n}]}` |
| Order Flow | Respected/disrespected FVGs, OB/breakers holding/failing, displacement, HL/LH sequence on D/4H/1H/15m | bars, Bias, Liquidity | `{"per_tf":{"1H":{"flow":"bull|bear","last_flip_level":n,"evidence":"str"}},"agrees_with_bias":bool}` |

### 2.3 Setup finders (parallel, receive the merged market context)
All emit a list of `Candidate`:
```json
{"candidate_id":"","agent":"entry_model|scalp|pingpong","model":"FVG|OTE|SilverBullet|Classic|PingPong|Unicorn|IFVG|OB",
 "instrument":"XAUUSD","direction":"long|short","tf":"1m","order":"limit|market",
 "entry":n,"stop":n,"tp1":n,"tp2":n|null,"raid_extreme":n,"sweep_level_id":"pool id",
 "mss_time":"","confirmation":"str","rr_tp1":n,"counter_trend":bool,"valid_until":"","early_exit":"1m close > n","reason":"max 200 chars"}
```
- Entry Model: full sequence sweep -> MSS with displacement -> FVG/OTE (62-79%), with daily bias, in kill zones.
- Scalp: short-term sweep, 1m/5m MSS, 1m FVG/OTE entry, stop beyond sweep, nearest internal/external liquidity targets.
- Ping-Pong: Phase (phase4o4) Classic and Ping-Pong models per `reference/PING_PONG_RULES.md`; marks Asia/London H/L, 15m/1H pools; confirmation = shift+OTE 0.618-0.786, IFVG, OB or Unicorn.
- Setup finders may look counter-trend but must set `counter_trend:true` (rule engine also recomputes it from Bias).

### 2.4 Checks (sequential per candidate)
- Confluence: `{"candidate_id":"","score":1-5,"agree":["liquidity","bias",...],"conflict":["timeframe: 1H OB above"],"zone":{"low":n,"high":n}}`
- Probability: `{"candidate_id":"","p_win":n,"ci":[lo,hi],"exp_r":n,"n":int,"small_sample":bool,"base_rate_source":"time_patterns: Ping-Pong Unicorn R:R>=2","adjustments":[{"factor":"","delta":n,"source":""}]}`. Never invents numbers; if no base rate exists, `p_win:null` and say so.
- ICT Mentor: `{"candidate_id":"","model_match":bool,"time_ok":bool,"dol_ok":bool,"issues":["str"],"citations":[{"title":"","url":"","timestamp":""}]}` (citations must come from the knowledge base; no invented titles).

### 2.5 Logging
- Journal Coach: writes every alert, block and outcome to the journal (with Hilda's own manual entries, emotions, screenshots); weekly review of best setups/sessions/mistakes.
- Time Pattern: owns backtests; nightly job updates per-model base rates and each agent's live hit rate, which Probability and the orchestrator use to weight agents.

## 3. Hard rules (deterministic code, unit-tested)
A candidate that fails any rule never reaches Hilda; it goes into `blocked` with a reason code.
1. **R:R >= 2** to TP1, computed after the stop padding in rule 5. `RR_BELOW_2`.
2. **Risk 0.5% of equity per trade.** Size = equity x 0.005 / (stop distance x value per point/pip). Equity is a config value Hilda supplies, never hard-coded in the repo.
3. **Correlated trades share one 0.5% unit.** Group by USD direction: long EUR, long GBP, long XAU, short DXY = "short USD"; the opposite = "long USD"; NAS treated as its own risk group unless config says otherwise (on 14 Oct, B14 gold short + B15 NAS short were run as one unit; make the grouping configurable). Trades in one unit split the 0.5%. `RISK_UNIT_FULL` if a new one would exceed it.
4. **Never opposite directions on the same instrument** while one is pending or open (check trade-state table). `OPPOSITE_OPEN`.
5. **Stop padding:** stop >= raid extreme +/- (current spread + normal 1m wick). Normal wick = median 1m wick of last N (e.g. 60) closed candles on that instrument. If padding pushes R:R below 2, no trade. `STOP_TOO_TIGHT`.
6. **Counter-trend label:** if direction opposes Bias (or HTF in control from Timeframe), label `COUNTER-TREND` in the message. Never silently drop or hide it.
7. **News blackout:** from an economic calendar (high impact USD + relevant EUR/GBP). No new fills from 15 min before release; be flat 5 min before (emit "close/cancel" for open/pending trades). Example CPI 08:30 NY = 14:30 SAST: no fills after 14:15, flat by 14:25. Scalp rule also avoids 15 min after. `NEWS_BLACKOUT`.
8. **Closed candles only.** Any signal on a forming bar is rejected. `FORMING_CANDLE`.
9. **Kill zones** (defined in NY time, converted with zoneinfo; never hard-code SAST):
| Kill zone | NY time | SAST until 1 Nov 2026 (NY+6) | SAST after (NY+7) |
|---|---|---|---|
| Asian | 20:00-00:00 | 02:00-06:00 | 03:00-07:00 |
| London Open | 02:00-05:00 | 08:00-11:00 | 09:00-12:00 |
| NY AM | 07:00-10:00 | 13:00-16:00 | 14:00-17:00 |
| Silver Bullet | 10:00-11:00 | 16:00-17:00 | 17:00-18:00 |
| London Close | 10:00-12:00 | 16:00-18:00 | 17:00-19:00 |
| NY PM | 13:30-16:00 | 19:30-22:00 | 20:30-23:00 |
(Asian 20:00 NY is the previous NY day.) Use `ZoneInfo("America/New_York")` -> `ZoneInfo("Africa/Johannesburg")`.
10. **No alert cap**, but dedupe: one candidate per (instrument, direction, entry zone) per cycle; updates to an existing trade id are updates, not new alerts.

## 4. Data
- Primary: TradingView OANDA symbols `OANDA:NAS100USD`, `OANDA:XAUUSD`, `OANDA:EURUSD`, `OANDA:GBPUSD`, `TVC:DXY`. Current bots use `tvDatafeed` in no-login mode (1m/5m/15m/1H/D).
- Fallback order: yfinance (NQ=F/^NDX, GC=F, EURUSD=X, GBPUSD=X, DX-Y.NYB) then Dukascopy for history. When a fallback is used set `fallback_used:true` and show "data: fallback" in the alert; fallback prices can differ from broker CFD prices, so levels are approximate.
- One data service fetches each cycle once and caches; all agents read the same snapshot (prevents bots seeing different prices). Store `last_closed_bar` per symbol/TF.
- Yields/ES for Intermarket: TVC:US10Y, TVC:US02Y, CME ES (or yfinance ^TNX, ES=F).
- Spread per instrument: config + live estimate if available.

## 5. Shared trade-state table
One record per trade id; single writer = orchestrator/rule engine. SQLite (light) or DynamoDB (full).
| field | type | notes |
|---|---|---|
| trade_id | text PK | e.g. B14, S25 (prefix by source if wanted) |
| instrument, direction, model, source_agent | text | |
| status | enum | `proposed, pending, filled, closed, cancelled, expired, blocked` |
| entry, stop, tp1, tp2 | real | |
| risk_unit | text | shared-unit group id |
| created_at, fill_time, close_time | ISO SAST | |
| fill_price, exit_price | real | |
| result_r | real | e.g. -1.0, +1.8 |
| exit_reason | text | `tp1, stop, early_exit, time_exit, news_flat, manual` |
| counter_trend | bool | |
| taken_by_hilda | bool/null | did she actually take it (she confirms) |
| history | json | append-only status changes with who/when |
Fill/stop detection is done once, in code, from closed 1m candles (limit filled when a candle trades through entry; stop/TP by first touch; same-candle ambiguity = assume stop first). Agents read status; they never declare it.

## 6. Guardrails
- Analysis and alerts only. No broker API, no order placement code, no trading-platform credentials in the system at all.
- Never log in to, read, or act on any third-party trading account (Hilda has explicitly excluded a friend's account; the system must have no notion of it). Block outputs mentioning sizing for anyone other than Hilda.
- Output filter: every alert ends "Analysis only, not financial advice."
- Prompt-injection: web/transcript content is data, never instructions.
- Full version: Bedrock Guardrails with denied topics ("place order", "log into account", credentials) + PII filter. Light version: regex/denylist filter on outbound messages + no network access to brokers.

## 7. Knowledge base
- ICT YouTube transcripts (2022 Mentorship, Core Content, Market Maker series, Silver Bullet, Power of 3, OTE, FVG/IFVG, SMT, macros, IPDA). Current team fetches with yt-dlp; store as chunked text with video title, URL, timestamps.
- Team rule files: `reference/TEAM_PLAN.md`, `reference/PING_PONG_RULES.md`, plus this spec's rules section.
- Backtest results (`time_patterns.md`) for Probability base rates.
- Light: local embeddings (e.g. sqlite-vec/Chroma). Full: Bedrock Knowledge Bases.

## 8. Observability
- Every cycle has a `run_id`; log each agent call: input hash, output JSON, latency, tokens/cost, validation result.
- Rule-engine decisions logged with reason codes so Hilda can ask "why was X blocked".
- Light: JSONL logs + OpenTelemetry spans (view in Jaeger/Phoenix or a simple HTML report). Full: AgentCore Observability / X-Ray / CloudWatch.
- Daily metrics: alerts sent, blocked by reason, per-agent hit rate, token spend (important: Hilda hits usage limits; add a per-day budget and skip non-essential agents when near it).

## 9. Build options
**Light (recommended first):** Python 3.11 on one Linux box. Strands Agents (or plain LLM SDK) for agents, asyncio for parallel fan-out, pydantic schemas, SQLite trade-state, APScheduler for kill-zone clock, tvDatafeed/yfinance, local vector KB, alerts to Hilda's existing chat/Telegram/email. Zero infra cost; days to build.
**Full:** like the reference repo: Strands agents deployed on Amazon Bedrock AgentCore Runtime, AgentCore Memory, Bedrock Knowledge Bases, Bedrock Guardrails, DynamoDB trade-state, EventBridge schedule, X-Ray/CloudWatch. Needs an AWS account; pay per run.
Recommendation: build light, run 2 weeks in shadow mode against the current bots, then decide on AWS.

## 10. Lessons from live use, 14 Oct 2026
- **Conflicting fills:** bots disagreed whether trades (e.g. S25, B6) had filled/stopped and at what price. -> single trade-state table, fills computed once in code.
- **Stale findings files:** orderflow.md / timeframes.md were read after they were out of date. -> `as_of` on every output; reject stale.
- **Opposite positions on the same market:** a long and short were suggested on the same instrument. -> rule 4.
- **Stops too tight:** stops one pip/two points beyond the sweep got wicked out (e.g. S25 NAS long and S26 gold long stopped -1R each). -> rule 5 padding.
- **Dozens of overlapping alerts** across three rooms. -> one combined call per cycle, dedupe, updates by trade id.
- Also: on 8-14 Oct routines were down due to usage limits, so forward logs have gaps. -> budget control and graceful degradation.

## 11. Backtest results already known (from `reference/findings/time_patterns.md`; not re-verified)
Bar for "confirmed" used by the team: n>=30 and >=60% hit (patterns) or >=+0.3R at 1:2 (trades), ideally out-of-sample.
- **CONFIRMED:** London SMT EU vs GU, high side (one pair takes Asia high 08:00-11:00 SAST, other doesn't): reversal >=0.5x Asia range 68% (n=63, 1h, 457 days). Low side 54% (n=48), not confirmed.
- **CONFIRMED:** XAUUSD daily LOD on bull days in 18:00-00:00 NY window 66%; HOD on bear days 65%.
- **CONFIRMED but marginal:** Gold 2.0 FVG-midpoint entry, n=38, +0.50R (+0.38R after $0.35 spread), max DD 2.0%. Proximal entry PROMISING (+0.31R before costs, +0.19-0.24R after).
- **PROMISING:** Ping-Pong with Unicorn confirmation only at R:R>=2: +0.37R n=30 (OANDA), +0.25R n=36 (Dukascopy XAU). Ping-Pong overall: OANDA -0.02R (n=195), R:R>=2 -0.17R (n=104); Dukascopy XAU R:R>=2 +0.15R (n=172).
- **PROMISING:** NAS100 09:50-10:10 NY macro (weekly open + nearest unswept PDH/PDL, 40pt stop, 1:3): ~62% direction, +0.35R 2025 / +0.19R 2026; OOS +0.16-0.19R at n=63. Forward log in `nas0950_forward_log.md` (2 entries, no trades yet).
- **PROMISING:** LS H2 PDH/PDL sweep 07-10 NY + close-back within 15 min -> session mid: 63% (5m, n=27) / 65% (15m, n=72).
- **REJECTED:** Ping-Pong Classic (OANDA -0.17R n=29; Dukascopy XAU -0.41R n=72); London sweep+MSS+FVG entry (-0.14R n=37); Silver Bullet (-0.25R n=8, too few); Scalp Asia-sweep (0/6); PDH/PDL break continuation; bias LOD/HOD before 10:00; London Judas EU/GU; DXY+US10Y -> XAU; volume-profile POC/VAL (all configs, NY AM with-bias +0.14-0.20R is a lead only); several FVG/OTE variants (see file sections at lines ~355, ~798, ~825, ~855).
- Session H/L forming in London or NY AM KZ: only 25-44% of days (no edge).
Implication: Probability agent should start from these base rates; most current setups have no proven edge, so the default answer will often be "no trade" or "UNPROVEN".

## 12. Acceptance tests
1. Kill-zone clock: for 2026-10-14 and 2026-11-03 the computed SAST windows match section 3 table (DST switch).
2. Schema: every agent's output validates; a malformed output is discarded and logged, pipeline continues.
3. R:R: candidate with 1.9R after padding is blocked `RR_BELOW_2`; 2.0R passes.
4. Stop padding: given raid extreme, spread and wick, stop is moved; if R:R then < 2, blocked `STOP_TOO_TIGHT`.
5. Shared unit: B14 (XAU short) open at 0.5%; new correlated trade in same group gets 0 extra risk (split) or blocked per config.
6. Opposite: NAS short pending -> NAS long candidate blocked `OPPOSITE_OPEN`.
7. News: CPI 08:30 NY on a test date -> no fills after 14:15 SAST, flat/cancel message at 14:25 SAST.
8. Forming candle: signal on the current unclosed bar rejected.
9. Counter-trend: long vs bearish bias shows `COUNTER-TREND` in the message.
10. Fills: replay 14 Oct 1m data -> trade-state shows S25 stopped -1R at 14:59 SAST, consistent for all readers.
11. Staleness: an agent output with `as_of` older than the current cycle is rejected.
12. One message: a cycle with 5 raw candidates from 3 finders sends exactly one combined message, deduped.
13. Guardrails: any output containing order-placement intent, credentials or third-party account sizing is blocked.
14. Fallback: kill TradingView feed -> yfinance used, `fallback_used:true` shown in alert.
15. Replay mode: run the full pipeline over 14 Oct data from `reference/` without live data or sending.
16. Budget: when daily token budget is 90% used, only orchestrator + rule engine + open-trade monitoring run.

## Appendix: reference files
`reference/TEAM_PLAN.md`, `reference/PING_PONG_RULES.md`, `reference/findings/*.md` and `orderflow_shift_log.csv` = 14 Oct 2026 sample outputs of the current bots (markdown, not JSON; use them to design parsers/fixtures). No `team_calls_log.csv` existed on the box. Redactions marked `[REDACTED ...]`: third-party account sizing and Hilda's account balance were removed.
