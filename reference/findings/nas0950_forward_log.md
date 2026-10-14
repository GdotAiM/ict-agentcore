# NAS100 09:50–10:10 NY macro: forward-test log

Rules: LONG if price above weekly open (Sun 18:00 NY) AND nearest unswept prior-day level is PDH; SHORT if below weekly open AND nearest unswept is PDL; else no setup. Entry 09:50 NY open, 40pt stop, 120pt target (1:3). Backtest: PROMISING, not confirmed (~62% direction hit 2025 and 2026; +0.35R 2025, +0.19R 2026). Analysis only. Data: TradingView OANDA:NAS100USD 1m. Times NY unless marked SAST.

| Date (NY) | Call | Weekly open | PDH | PDL | Swept before 09:50 | Price at check | 09:30–09:50 range | 09:50 open | 09:50–10:10 outcome | 09:50–11:10 outcome |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-13 (retro, live run failed) | none: below WO but nearest unswept was PDH | 30926.6 | 31087.8 | 30654.2 | PDL (low 30401.2) | 30601.6 (09:49) | 30401.2–30610.6 | 30601.7 | H 30624.3 / L 30558.0, closed 30608.6 (+6.9) | H 30624.3 / L 30500.8, closed 30512.7 (−89.0); 1:3 long would have stopped 09:52, short neither hit |
| 2026-10-14 | none: below WO but PDL already swept, only PDH unswept | 30926.6 | 30715.4 | 30401.2 | PDL (low 30311.5); PDH not swept (high 30704.7) | 30418.2 (09:43) | forming: 30311.5–30438.1 at 09:43 | pending | pending | pending |
