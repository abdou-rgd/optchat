# OptChat local bench (Bonsai 2 27B PTQ1_0, RTX 3060 12GB)

Turns: 48  |  total wall: 5.5 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 2, 'merges': 60, 'verbatim': 88, 'calls': 16, 'errors': 0, 'seconds': 190.50046133995056}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.53 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 4.92 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 41.03 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.97 | Inès Marchetti, à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.74 | Dans le fichier `.env.ci`. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.71 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.66 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 1 | 2 | 34.99 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 32.49 | 0.0 | 697 | 516 | 181 | 0 |
| 1 | filler | 2.69 | 0.0 | 747 | 42 | 705 | 0 |
| 2 | filler | 0.87 | 0.0 | 819 | 40 | 779 | 0 |
| 3 | fact | 0.9 | 0.0 | 886 | 64 | 822 | 0 |
| 4 | filler | 0.85 | 0.0 | 936 | 47 | 889 | 0 |
| 5 | filler | 0.79 | 0.0 | 980 | 41 | 939 | 0 |
| 6 | fact | 3.12 | 0.0 | 1028 | 46 | 982 | 0 |
| 7 | filler | 4.58 | 0.02 | 1286 | 1105 | 181 | 0 |
| 8 | filler | 0.89 | 0.0 | 1358 | 42 | 1316 | 0 |
| 9 | fact | 0.87 | 0.0 | 1414 | 53 | 1361 | 0 |
| 10 | filler | 0.81 | 0.0 | 1461 | 44 | 1417 | 0 |
| 11 | filler | 2.21 | 0.0 | 1504 | 41 | 1463 | 0 |
| 12 | fact | 30.28 | 26.82 | 1565 | 1384 | 181 | 0 |
| 13 | filler | 0.62 | 0.0 | 1604 | 36 | 1568 | 0 |
| 14 | filler | 0.97 | 0.0 | 1645 | 37 | 1608 | 0 |
| 15 | fact | 0.56 | 0.0 | 1704 | 45 | 1659 | 0 |
| 16 | filler | 0.55 | 0.0 | 1746 | 39 | 1707 | 0 |
| 17 | filler | 12.4 | 7.34 | 1795 | 1614 | 181 | 0 |
| 18 | fact | 0.57 | 0.0 | 1879 | 51 | 1828 | 0 |
| 19 | filler | 0.56 | 0.0 | 1922 | 40 | 1882 | 0 |
| 20 | filler | 1.24 | 0.0 | 1963 | 38 | 1925 | 0 |
| 21 | fact | 0.6 | 0.0 | 2042 | 58 | 1984 | 0 |
| 22 | filler | 34.85 | 30.35 | 1998 | 1817 | 181 | 0 |
| 23 | filler | 0.55 | 0.0 | 2037 | 37 | 2000 | 0 |
| 24 | filler | 4.87 | 0.0 | 2081 | 42 | 2039 | 0 |
| 25 | filler | 0.97 | 0.0 | 2147 | 38 | 2109 | 0 |
| 26 | filler | 1.94 | 0.0 | 2190 | 40 | 2150 | 0 |
| 27 | filler | 28.33 | 21.13 | 2176 | 1995 | 181 | 0 |
| 28 | filler | 3.52 | 0.0 | 2221 | 42 | 2179 | 0 |
| 29 | filler | 3.66 | 0.0 | 2336 | 44 | 2292 | 0 |
| 30 | filler | 1.66 | 0.0 | 2463 | 131 | 2332 | 0 |
| 31 | filler | 0.54 | 0.0 | 2532 | 41 | 2491 | 0 |
| 32 | filler | 27.29 | 22.6 | 2453 | 2272 | 181 | 0 |
| 33 | filler | 0.52 | 0.0 | 2497 | 41 | 2456 | 0 |
| 34 | filler | 7.36 | 0.0 | 2539 | 40 | 2499 | 0 |
| 35 | filler | 1.54 | 0.0 | 2611 | 42 | 2569 | 0 |
| 36 | filler | 0.76 | 0.0 | 2658 | 44 | 2614 | 0 |
| 37 | filler | 24.71 | 18.82 | 2657 | 2476 | 181 | 0 |
| 38 | filler | 0.58 | 0.0 | 2716 | 36 | 2680 | 0 |
| 39 | filler | 1.03 | 0.0 | 2755 | 37 | 2718 | 0 |
| 40 | recall | 0.53 | 0.0 | 2806 | 37 | 2769 | 0 |
| 41 | recall | 4.92 | 0.0 | 2850 | 43 | 2807 | 0 |
| 42 | recall | 41.03 | 35.72 | 2666 | 2485 | 181 | 0 |
| 43 | recall | 0.97 | 0.0 | 2715 | 41 | 2674 | 0 |
| 44 | recall | 0.74 | 0.0 | 2768 | 40 | 2728 | 0 |
| 45 | recall | 0.71 | 0.0 | 2814 | 39 | 2775 | 0 |
| 46 | recall | 0.66 | 0.0 | 2861 | 42 | 2819 | 0 |
| 47 | recall | 34.99 | 27.71 | 2873 | 2841 | 181 | 1 |