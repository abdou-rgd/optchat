# OptChat local bench (Ternary Bonsai 2 9B Q2_0 on upstream llama.cpp b11700, RTX 3060 12GB)

Turns: 48  |  total wall: 1.1 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 3, 'merges': 60, 'verbatim': 87, 'calls': 17, 'errors': 0, 'seconds': 38.96559953689575}

## Recall: 7/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.17 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.21 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 7.88 | PostgreSQL. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | MISS | 0 | 1 | 0.29 | Inès Marchetti reprend le module de facturation. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.25 | Dans le fichier .env.ci. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.22 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.23 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 5.58 | #3FA7D6. |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 1.13 | 0.0 | 697 | 697 | 0 | 0 |
| 1 | filler | 0.61 | 0.0 | 758 | 65 | 693 | 0 |
| 2 | filler | 0.32 | 0.0 | 832 | 78 | 754 | 0 |
| 3 | fact | 0.59 | 0.0 | 905 | 77 | 828 | 0 |
| 4 | filler | 0.22 | 0.0 | 983 | 82 | 901 | 0 |
| 5 | filler | 0.19 | 0.0 | 1023 | 44 | 979 | 0 |
| 6 | fact | 0.41 | 0.0 | 1066 | 47 | 1019 | 0 |
| 7 | filler | 0.95 | 0.01 | 1354 | 700 | 654 | 0 |
| 8 | filler | 0.22 | 0.0 | 1424 | 74 | 1350 | 0 |
| 9 | fact | 0.44 | 0.0 | 1476 | 56 | 1420 | 0 |
| 10 | filler | 0.23 | 0.0 | 1538 | 66 | 1472 | 0 |
| 11 | filler | 0.41 | 0.0 | 1578 | 44 | 1534 | 0 |
| 12 | fact | 3.32 | 2.34 | 1545 | 891 | 654 | 0 |
| 13 | filler | 0.28 | 0.0 | 1600 | 59 | 1541 | 0 |
| 14 | filler | 0.31 | 0.0 | 1642 | 46 | 1596 | 0 |
| 15 | fact | 0.38 | 0.0 | 1695 | 57 | 1638 | 0 |
| 16 | filler | 0.22 | 0.0 | 1748 | 57 | 1691 | 0 |
| 17 | filler | 3.47 | 2.47 | 1788 | 1134 | 654 | 0 |
| 18 | fact | 0.41 | 0.0 | 1850 | 66 | 1784 | 0 |
| 19 | filler | 0.22 | 0.0 | 1907 | 61 | 1846 | 0 |
| 20 | filler | 0.35 | 0.0 | 1945 | 42 | 1903 | 0 |
| 21 | fact | 0.5 | 0.0 | 2015 | 74 | 1941 | 0 |
| 22 | filler | 5.27 | 4.2 | 1880 | 1226 | 654 | 0 |
| 23 | filler | 0.24 | 0.0 | 1928 | 52 | 1876 | 0 |
| 24 | filler | 0.69 | 0.0 | 1973 | 49 | 1924 | 0 |
| 25 | filler | 0.2 | 0.0 | 2051 | 82 | 1969 | 0 |
| 26 | filler | 0.43 | 0.0 | 2089 | 42 | 2047 | 0 |
| 27 | filler | 5.44 | 4.39 | 2089 | 1435 | 654 | 0 |
| 28 | filler | 1.42 | 0.0 | 2131 | 46 | 2085 | 0 |
| 29 | filler | 1.04 | 0.0 | 2278 | 151 | 2127 | 0 |
| 30 | filler | 0.46 | 0.0 | 2388 | 114 | 2274 | 0 |
| 31 | filler | 0.21 | 0.0 | 2448 | 64 | 2384 | 0 |
| 32 | filler | 10.16 | 8.95 | 2446 | 1792 | 654 | 0 |
| 33 | filler | 0.16 | 0.0 | 2486 | 44 | 2442 | 0 |
| 34 | filler | 0.49 | 0.0 | 2523 | 41 | 2482 | 0 |
| 35 | filler | 0.21 | 0.0 | 2590 | 71 | 2519 | 0 |
| 36 | filler | 0.19 | 0.0 | 2633 | 47 | 2586 | 0 |
| 37 | filler | 7.56 | 5.99 | 2758 | 2104 | 654 | 0 |
| 38 | filler | 0.19 | 0.0 | 2812 | 58 | 2754 | 0 |
| 39 | filler | 0.3 | 0.0 | 2847 | 39 | 2808 | 0 |
| 40 | recall | 0.17 | 0.0 | 2892 | 49 | 2843 | 0 |
| 41 | recall | 0.21 | 0.0 | 2932 | 44 | 2888 | 0 |
| 42 | recall | 7.88 | 6.51 | 2732 | 2078 | 654 | 0 |
| 43 | recall | 0.29 | 0.0 | 2772 | 44 | 2728 | 0 |
| 44 | recall | 0.25 | 0.0 | 2819 | 51 | 2768 | 0 |
| 45 | recall | 0.22 | 0.0 | 2861 | 46 | 2815 | 0 |
| 46 | recall | 0.23 | 0.0 | 2904 | 47 | 2857 | 0 |
| 47 | recall | 5.58 | 4.08 | 2917 | 2263 | 654 | 0 |