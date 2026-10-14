# S25 NAS100 long: fill / stop on real 14 Oct 1m data

| Event | Spec / reference | Fixture bar | Result |
|---|---|---|---|
| Alert | 14:53 SAST, buy limit CE 30425.1, stop 30361.7 | — | pending |
| Fill | 14:52 L 30417.7 traded through CE | `NAS100_1m_2026-10-14.csv` 14:52 H 30451.8 L 30417.7 | filled @ 30425.1 |
| Stop | 14:59 L 30356.2 | 14:59 H 30376.6 L 30356.2 | closed result_r=−1.0 |

**Verdict:** S25 reproduces on real OANDA 1m data fetched via tvDatafeed. No synthetic
fixture was needed. Source files live under `tests/fixtures/replay_1m/`.
