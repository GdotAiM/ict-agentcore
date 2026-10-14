# 14 Oct 2026 1m OANDA / TVC fixtures

Fetched 2026-10-14 via `tvDatafeed` (nologin) from TradingView:
`OANDA:NAS100USD`, `OANDA:XAUUSD`, `OANDA:EURUSD`, `OANDA:GBPUSD`, `TVC:DXY`.

Timestamps are SAST (Africa/Johannesburg). These are the **real** 1m bars used by the
bots that day. Acceptance test 10 (S25 stopped −1R at 14:59 SAST) **reproduces** on
this data: fill on the 14:52 bar (L 30417.7 through CE 30425.1), stop on the 14:59
bar (L 30356.2 through stop 30361.7).

yfinance `NQ=F` / `^NDX` 1m for the same day was also available but is a different
product (futures / cash index) and is not used for the S25 assertion.
