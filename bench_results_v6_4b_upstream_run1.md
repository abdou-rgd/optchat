# OptChat local bench (Ternary Bonsai 2 4B Q2_0 on upstream llama.cpp b11700 (run1), RTX 3060 12GB)

Turns: 48  |  total wall: 0.9 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 4, 'merges': 60, 'verbatim': 86, 'calls': 18, 'errors': 0, 'seconds': 23.186205625534058}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.16 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.19 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 6.18 | PostgreSQL. L'utilisateur a choisi cette base de données plutôt que MongoDB à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.26 | Inès Marchetti. À partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.18 | .env.ci |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.19 | 650 euros |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.2 | 9h15 |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 3.0 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 0.69 | 0.0 | 697 | 697 | 0 | 0 |
| 1 | filler | 0.34 | 0.0 | 741 | 48 | 693 | 0 |
| 2 | filler | 10.35 | 0.0 | 800 | 63 | 737 | 0 |
| 3 | fact | 0.95 | 0.0 | 2060 | 1264 | 796 | 0 |
| 4 | filler | 0.19 | 0.0 | 2136 | 80 | 2056 | 0 |
| 5 | filler | 0.18 | 0.0 | 2176 | 44 | 2132 | 0 |
| 6 | fact | 0.17 | 0.0 | 2221 | 49 | 2172 | 0 |
| 7 | filler | 1.8 | 1.11 | 1302 | 648 | 654 | 0 |
| 8 | filler | 0.18 | 0.0 | 1374 | 76 | 1298 | 0 |
| 9 | fact | 0.19 | 0.0 | 1426 | 56 | 1370 | 0 |
| 10 | filler | 0.18 | 0.0 | 1470 | 48 | 1422 | 0 |
| 11 | filler | 0.36 | 0.0 | 1509 | 43 | 1466 | 0 |
| 12 | fact | 2.42 | 1.9 | 1480 | 826 | 654 | 0 |
| 13 | filler | 0.17 | 0.0 | 1516 | 40 | 1476 | 0 |
| 14 | filler | 0.22 | 0.0 | 1551 | 39 | 1512 | 0 |
| 15 | fact | 0.2 | 0.0 | 1599 | 52 | 1547 | 0 |
| 16 | filler | 0.19 | 0.0 | 1638 | 43 | 1595 | 0 |
| 17 | filler | 1.84 | 1.22 | 1666 | 1012 | 654 | 0 |
| 18 | fact | 0.27 | 0.0 | 1722 | 60 | 1662 | 0 |
| 19 | filler | 0.18 | 0.0 | 1771 | 53 | 1718 | 0 |
| 20 | filler | 0.31 | 0.0 | 1807 | 40 | 1767 | 0 |
| 21 | fact | 0.25 | 0.0 | 1879 | 76 | 1803 | 0 |
| 22 | filler | 3.91 | 3.26 | 1851 | 1197 | 654 | 0 |
| 23 | filler | 0.17 | 0.0 | 1886 | 39 | 1847 | 0 |
| 24 | filler | 0.4 | 0.0 | 1926 | 44 | 1882 | 0 |
| 25 | filler | 0.16 | 0.0 | 1990 | 68 | 1922 | 0 |
| 26 | filler | 0.27 | 0.0 | 2027 | 41 | 1986 | 0 |
| 27 | filler | 2.61 | 1.94 | 1973 | 1319 | 654 | 0 |
| 28 | filler | 0.64 | 0.0 | 2013 | 44 | 1969 | 0 |
| 29 | filler | 1.03 | 0.0 | 2109 | 100 | 2009 | 0 |
| 30 | filler | 0.37 | 0.0 | 2247 | 142 | 2105 | 0 |
| 31 | filler | 0.18 | 0.0 | 2305 | 62 | 2243 | 0 |
| 32 | filler | 4.32 | 3.57 | 2167 | 1513 | 654 | 0 |
| 33 | filler | 0.18 | 0.0 | 2207 | 44 | 2163 | 0 |
| 34 | filler | 0.36 | 0.0 | 2246 | 43 | 2203 | 0 |
| 35 | filler | 0.19 | 0.0 | 2307 | 65 | 2242 | 0 |
| 36 | filler | 0.18 | 0.0 | 2350 | 47 | 2303 | 0 |
| 37 | filler | 3.88 | 2.92 | 2368 | 1714 | 654 | 0 |
| 38 | filler | 0.18 | 0.0 | 2415 | 51 | 2364 | 0 |
| 39 | filler | 0.21 | 0.0 | 2450 | 39 | 2411 | 0 |
| 40 | recall | 0.16 | 0.0 | 2490 | 44 | 2446 | 0 |
| 41 | recall | 0.19 | 0.0 | 2530 | 44 | 2486 | 0 |
| 42 | recall | 6.18 | 5.2 | 2450 | 1796 | 654 | 0 |
| 43 | recall | 0.26 | 0.0 | 2506 | 60 | 2446 | 0 |
| 44 | recall | 0.18 | 0.0 | 2555 | 53 | 2502 | 0 |
| 45 | recall | 0.19 | 0.0 | 2592 | 41 | 2551 | 0 |
| 46 | recall | 0.2 | 0.0 | 2634 | 46 | 2588 | 0 |
| 47 | recall | 3.0 | 2.07 | 2556 | 1902 | 654 | 0 |