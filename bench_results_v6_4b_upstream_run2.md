# OptChat local bench (Ternary Bonsai 2 4B Q2_0 on upstream llama.cpp b11700 (run2), RTX 3060 12GB)

Turns: 48  |  total wall: 0.6 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 2, 'merges': 57, 'verbatim': 86, 'calls': 15, 'errors': 0, 'seconds': 21.6265766620636}

## Recall: 5/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.16 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.2 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | MISS | 0 | 1 | 5.19 | Je ne dispose pas de cette information dans ma mémoire. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | MISS | 0 | 1 | 0.26 | Je ne dispose pas de cette information dans ma mémoire. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 1 | 2 | 0.57 | Le fichier .env.ci |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.24 | 650 euros |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | MISS | 0 | 1 | 1.96 | Je ne dispose pas de cette information dans ma mémoire. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 0.21 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 0.25 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 0.33 | 0.0 | 741 | 48 | 693 | 0 |
| 2 | filler | 0.16 | 0.0 | 798 | 61 | 737 | 0 |
| 3 | fact | 0.22 | 0.0 | 860 | 66 | 794 | 0 |
| 4 | filler | 0.18 | 0.0 | 912 | 56 | 856 | 0 |
| 5 | filler | 0.17 | 0.0 | 952 | 44 | 908 | 0 |
| 6 | fact | 0.17 | 0.0 | 997 | 49 | 948 | 0 |
| 7 | filler | 0.58 | 0.01 | 1268 | 614 | 654 | 0 |
| 8 | filler | 0.18 | 0.0 | 1327 | 63 | 1264 | 0 |
| 9 | fact | 0.19 | 0.0 | 1379 | 56 | 1323 | 0 |
| 10 | filler | 0.17 | 0.0 | 1423 | 48 | 1375 | 0 |
| 11 | filler | 0.34 | 0.0 | 1462 | 43 | 1419 | 0 |
| 12 | fact | 3.12 | 2.57 | 1590 | 936 | 654 | 0 |
| 13 | filler | 0.17 | 0.0 | 1626 | 40 | 1586 | 0 |
| 14 | filler | 0.21 | 0.0 | 1661 | 39 | 1622 | 0 |
| 15 | fact | 0.18 | 0.0 | 1708 | 51 | 1657 | 0 |
| 16 | filler | 0.17 | 0.0 | 1746 | 42 | 1704 | 0 |
| 17 | filler | 2.17 | 1.37 | 1749 | 1095 | 654 | 0 |
| 18 | fact | 0.29 | 0.0 | 1821 | 76 | 1745 | 0 |
| 19 | filler | 0.18 | 0.0 | 1872 | 55 | 1817 | 0 |
| 20 | filler | 0.37 | 0.0 | 1908 | 40 | 1868 | 0 |
| 21 | fact | 0.23 | 0.0 | 1987 | 83 | 1904 | 0 |
| 22 | filler | 3.99 | 3.29 | 1835 | 1181 | 654 | 0 |
| 23 | filler | 0.17 | 0.0 | 1870 | 39 | 1831 | 0 |
| 24 | filler | 0.4 | 0.0 | 1910 | 44 | 1866 | 0 |
| 25 | filler | 0.16 | 0.0 | 1973 | 67 | 1906 | 0 |
| 26 | filler | 0.35 | 0.0 | 2010 | 41 | 1969 | 0 |
| 27 | filler | 3.0 | 2.31 | 1994 | 1340 | 654 | 0 |
| 28 | filler | 0.7 | 0.0 | 2034 | 44 | 1990 | 0 |
| 29 | filler | 1.0 | 0.0 | 2136 | 106 | 2030 | 0 |
| 30 | filler | 0.37 | 0.0 | 2274 | 142 | 2132 | 0 |
| 31 | filler | 0.18 | 0.0 | 2332 | 62 | 2270 | 0 |
| 32 | filler | 3.88 | 3.1 | 2145 | 1491 | 654 | 0 |
| 33 | filler | 0.18 | 0.0 | 2185 | 44 | 2141 | 0 |
| 34 | filler | 0.28 | 0.0 | 2224 | 43 | 2181 | 0 |
| 35 | filler | 0.18 | 0.0 | 2277 | 57 | 2220 | 0 |
| 36 | filler | 0.17 | 0.0 | 2320 | 47 | 2273 | 0 |
| 37 | filler | 4.28 | 3.34 | 2336 | 1682 | 654 | 0 |
| 38 | filler | 0.17 | 0.0 | 2383 | 51 | 2332 | 0 |
| 39 | filler | 0.34 | 0.0 | 2418 | 39 | 2379 | 0 |
| 40 | recall | 0.16 | 0.0 | 2472 | 58 | 2414 | 0 |
| 41 | recall | 0.2 | 0.0 | 2512 | 44 | 2468 | 0 |
| 42 | recall | 5.19 | 4.25 | 2339 | 1685 | 654 | 0 |
| 43 | recall | 0.26 | 0.0 | 2387 | 52 | 2335 | 0 |
| 44 | recall | 0.57 | 0.0 | 2434 | 153 | 2383 | 1 |
| 45 | recall | 0.24 | 0.0 | 2598 | 168 | 2430 | 0 |
| 46 | recall | 1.96 | 1.37 | 2669 | 846 | 1823 | 0 |
| 47 | recall | 0.21 | 0.0 | 2717 | 52 | 2665 | 0 |