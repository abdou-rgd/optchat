# OptChat local bench (model not labelled, RTX 3060 12GB)

Turns: 48  |  total wall: 4.5 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 31, 'merges': 89, 'verbatim': 91, 'calls': 27, 'errors': 0, 'seconds': 225.31646585464478}

## Recall: 7/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 1 | 2 | 1.59 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 2 | 3 | 29.98 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 1 | 2 | 2.01 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 1 | 2 | 27.76 | Inès Marchetti, à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 1 | 2 | 2.01 | Dans le fichier `.env.ci` (pas dans `.env`). |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 1 | 2 | 1.75 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | MISS | 7 | 8 | 58.17 | <tool_call> <function=zoom> <parameter=id> n172 </parameter> </function> </tool_call> |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 1 | 2 | 9.27 | La couleur d'embed du bot Discord est **#3FA7D6**. |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 1.32 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 1.37 | 0.0 | 759 | 42 | 717 | 0 |
| 2 | filler | 0.44 | 0.0 | 831 | 40 | 791 | 0 |
| 3 | fact | 1.49 | 0.0 | 898 | 64 | 834 | 0 |
| 4 | filler | 0.43 | 0.0 | 981 | 47 | 934 | 0 |
| 5 | filler | 0.43 | 0.0 | 1025 | 41 | 984 | 0 |
| 6 | fact | 0.89 | 0.0 | 1074 | 46 | 1028 | 0 |
| 7 | filler | 2.47 | 0.02 | 1346 | 692 | 654 | 0 |
| 8 | filler | 0.45 | 0.0 | 1416 | 42 | 1374 | 0 |
| 9 | fact | 1.08 | 0.0 | 1472 | 53 | 1419 | 0 |
| 10 | filler | 0.48 | 0.0 | 1539 | 44 | 1495 | 0 |
| 11 | filler | 1.21 | 0.0 | 1584 | 41 | 1543 | 0 |
| 12 | fact | 10.97 | 7.69 | 1597 | 943 | 654 | 0 |
| 13 | filler | 0.48 | 0.0 | 1666 | 36 | 1630 | 0 |
| 14 | filler | 0.86 | 0.0 | 1707 | 37 | 1670 | 0 |
| 15 | fact | 0.91 | 0.0 | 1768 | 45 | 1723 | 0 |
| 16 | filler | 0.4 | 0.0 | 1825 | 39 | 1786 | 0 |
| 17 | filler | 10.39 | 6.3 | 1832 | 1178 | 654 | 0 |
| 18 | fact | 1.11 | 0.0 | 1934 | 51 | 1883 | 0 |
| 19 | filler | 0.43 | 0.0 | 1998 | 40 | 1958 | 0 |
| 20 | filler | 1.02 | 0.0 | 2039 | 38 | 2001 | 0 |
| 21 | fact | 1.4 | 0.0 | 2118 | 58 | 2060 | 0 |
| 22 | filler | 21.29 | 18.04 | 2050 | 1396 | 654 | 0 |
| 23 | filler | 0.44 | 0.0 | 2102 | 37 | 2065 | 0 |
| 24 | filler | 1.6 | 0.0 | 2147 | 42 | 2105 | 0 |
| 25 | filler | 0.46 | 0.0 | 2224 | 38 | 2186 | 0 |
| 26 | filler | 1.18 | 0.0 | 2268 | 40 | 2228 | 0 |
| 27 | filler | 15.52 | 12.25 | 2273 | 1619 | 654 | 0 |
| 28 | filler | 3.21 | 0.0 | 2319 | 42 | 2277 | 0 |
| 29 | filler | 3.25 | 0.0 | 2452 | 44 | 2408 | 0 |
| 30 | filler | 1.31 | 0.0 | 2586 | 43 | 2543 | 0 |
| 31 | filler | 0.44 | 0.0 | 2657 | 41 | 2616 | 0 |
| 32 | filler | 24.08 | 20.34 | 2541 | 1887 | 654 | 0 |
| 33 | filler | 0.46 | 0.0 | 2585 | 41 | 2544 | 0 |
| 34 | filler | 1.2 | 0.0 | 2628 | 40 | 2588 | 0 |
| 35 | filler | 0.45 | 0.0 | 2696 | 42 | 2654 | 0 |
| 36 | filler | 0.41 | 0.0 | 2743 | 44 | 2699 | 0 |
| 37 | filler | 18.58 | 13.71 | 2723 | 2069 | 654 | 0 |
| 38 | filler | 0.42 | 0.0 | 2788 | 36 | 2752 | 0 |
| 39 | filler | 0.87 | 0.0 | 2827 | 37 | 2790 | 0 |
| 40 | recall | 1.59 | 0.0 | 2880 | 169 | 2843 | 1 |
| 41 | recall | 29.98 | 23.15 | 2832 | 2495 | 654 | 2 |
| 42 | recall | 2.01 | 0.0 | 3251 | 220 | 3206 | 1 |
| 43 | recall | 27.76 | 21.29 | 3184 | 2706 | 654 | 1 |
| 44 | recall | 2.01 | 0.0 | 3440 | 162 | 3400 | 1 |
| 45 | recall | 1.75 | 0.0 | 3641 | 167 | 3601 | 1 |
| 46 | recall | 58.17 | 35.04 | 3363 | 7966 | 654 | 7 |
| 47 | recall | 9.27 | 3.51 | 4769 | 2096 | 2847 | 1 |