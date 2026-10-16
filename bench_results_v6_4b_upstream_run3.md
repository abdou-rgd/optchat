# OptChat local bench (Ternary Bonsai 2 4B Q2_0 on upstream llama.cpp b11700 (run3), RTX 3060 12GB)

Turns: 48  |  total wall: 0.6 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 2, 'merges': 60, 'verbatim': 88, 'calls': 16, 'errors': 0, 'seconds': 21.142332315444946}

## Recall: 7/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.15 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | MISS | 0 | 1 | 0.24 | Je n'ai pas cette information dans ma mémoire. |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 5.44 | PostgreSQL |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.31 | Inès Marchetti reprend le module de facturation à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.21 | Le fichier .env.ci |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.19 | 650 euros |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.19 | 9h15 |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 3.67 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 0.32 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 0.32 | 0.0 | 741 | 48 | 693 | 0 |
| 2 | filler | 0.17 | 0.0 | 799 | 62 | 737 | 0 |
| 3 | fact | 0.24 | 0.0 | 861 | 66 | 795 | 0 |
| 4 | filler | 0.18 | 0.0 | 913 | 56 | 857 | 0 |
| 5 | filler | 0.18 | 0.0 | 953 | 44 | 909 | 0 |
| 6 | fact | 0.17 | 0.0 | 998 | 49 | 949 | 0 |
| 7 | filler | 0.54 | 0.01 | 1269 | 615 | 654 | 0 |
| 8 | filler | 0.18 | 0.0 | 1324 | 59 | 1265 | 0 |
| 9 | fact | 0.18 | 0.0 | 1376 | 56 | 1320 | 0 |
| 10 | filler | 0.17 | 0.0 | 1420 | 48 | 1372 | 0 |
| 11 | filler | 0.34 | 0.0 | 1459 | 43 | 1416 | 0 |
| 12 | fact | 2.12 | 1.59 | 1470 | 816 | 654 | 0 |
| 13 | filler | 0.17 | 0.0 | 1506 | 40 | 1466 | 0 |
| 14 | filler | 0.22 | 0.0 | 1541 | 39 | 1502 | 0 |
| 15 | fact | 0.19 | 0.0 | 1589 | 52 | 1537 | 0 |
| 16 | filler | 0.17 | 0.0 | 1628 | 43 | 1585 | 0 |
| 17 | filler | 1.86 | 1.23 | 1655 | 1001 | 654 | 0 |
| 18 | fact | 0.24 | 0.0 | 1711 | 60 | 1651 | 0 |
| 19 | filler | 0.17 | 0.0 | 1757 | 50 | 1707 | 0 |
| 20 | filler | 0.29 | 0.0 | 1793 | 40 | 1753 | 0 |
| 21 | fact | 0.24 | 0.0 | 1862 | 73 | 1789 | 0 |
| 22 | filler | 3.13 | 2.51 | 1748 | 1094 | 654 | 0 |
| 23 | filler | 0.17 | 0.0 | 1783 | 39 | 1744 | 0 |
| 24 | filler | 0.39 | 0.0 | 1823 | 44 | 1779 | 0 |
| 25 | filler | 0.17 | 0.0 | 1886 | 67 | 1819 | 0 |
| 26 | filler | 0.31 | 0.0 | 1923 | 41 | 1882 | 0 |
| 27 | filler | 2.46 | 1.82 | 1862 | 1208 | 654 | 0 |
| 28 | filler | 0.65 | 0.0 | 1902 | 44 | 1858 | 0 |
| 29 | filler | 1.1 | 0.0 | 2002 | 104 | 1898 | 0 |
| 30 | filler | 0.38 | 0.0 | 2145 | 147 | 1998 | 0 |
| 31 | filler | 0.18 | 0.0 | 2204 | 63 | 2141 | 0 |
| 32 | filler | 4.24 | 3.53 | 2074 | 1420 | 654 | 0 |
| 33 | filler | 0.19 | 0.0 | 2114 | 44 | 2070 | 0 |
| 34 | filler | 0.31 | 0.0 | 2153 | 43 | 2110 | 0 |
| 35 | filler | 0.19 | 0.0 | 2209 | 60 | 2149 | 0 |
| 36 | filler | 0.18 | 0.0 | 2252 | 47 | 2205 | 0 |
| 37 | filler | 4.04 | 3.06 | 2275 | 1621 | 654 | 0 |
| 38 | filler | 0.17 | 0.0 | 2330 | 59 | 2271 | 0 |
| 39 | filler | 0.2 | 0.0 | 2365 | 39 | 2326 | 0 |
| 40 | recall | 0.15 | 0.0 | 2404 | 43 | 2361 | 0 |
| 41 | recall | 0.24 | 0.0 | 2444 | 44 | 2400 | 0 |
| 42 | recall | 5.44 | 4.61 | 2362 | 1708 | 654 | 0 |
| 43 | recall | 0.31 | 0.0 | 2401 | 43 | 2358 | 0 |
| 44 | recall | 0.21 | 0.0 | 2455 | 58 | 2397 | 0 |
| 45 | recall | 0.19 | 0.0 | 2495 | 44 | 2451 | 0 |
| 46 | recall | 0.19 | 0.0 | 2537 | 46 | 2491 | 0 |
| 47 | recall | 3.67 | 2.77 | 2501 | 1847 | 654 | 0 |