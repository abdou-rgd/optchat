# OptChat local bench (Underdog-Saluki-27B-1.0 IQ2-mix, RTX 3060 12GB)

Turns: 48  |  total wall: 3.9 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 5, 'merges': 60, 'verbatim': 85, 'calls': 19, 'errors': 0, 'seconds': 137.07393074035645}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.48 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.63 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 31.87 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 1.05 | Inès Marchetti, à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.78 | Dans le fichier .env.ci. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.67 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 1.05 | Jeudi 23 octobre à 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 20.1 | #3FA7D6. |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 3.03 | 0.0 | 697 | 697 | 0 | 0 |
| 1 | filler | 1.82 | 0.0 | 759 | 42 | 717 | 0 |
| 2 | filler | 1.0 | 0.0 | 829 | 40 | 789 | 0 |
| 3 | fact | 2.03 | 0.0 | 905 | 64 | 841 | 0 |
| 4 | filler | 0.59 | 0.0 | 986 | 47 | 939 | 0 |
| 5 | filler | 0.55 | 0.0 | 1030 | 41 | 989 | 0 |
| 6 | fact | 1.38 | 0.0 | 1078 | 46 | 1032 | 0 |
| 7 | filler | 4.34 | 0.01 | 1354 | 1173 | 181 | 0 |
| 8 | filler | 0.56 | 0.0 | 1431 | 42 | 1389 | 0 |
| 9 | fact | 1.39 | 0.0 | 1487 | 53 | 1434 | 0 |
| 10 | filler | 0.63 | 0.0 | 1552 | 44 | 1508 | 0 |
| 11 | filler | 1.82 | 0.0 | 1597 | 41 | 1556 | 0 |
| 12 | fact | 16.98 | 12.12 | 1595 | 1414 | 181 | 0 |
| 13 | filler | 0.55 | 0.0 | 1661 | 36 | 1625 | 0 |
| 14 | filler | 0.96 | 0.0 | 1701 | 37 | 1664 | 0 |
| 15 | fact | 1.12 | 0.0 | 1758 | 45 | 1713 | 0 |
| 16 | filler | 0.54 | 0.0 | 1812 | 39 | 1773 | 0 |
| 17 | filler | 14.11 | 8.27 | 1825 | 1644 | 181 | 0 |
| 18 | fact | 1.37 | 0.0 | 1920 | 51 | 1869 | 0 |
| 19 | filler | 0.57 | 0.0 | 1980 | 40 | 1940 | 0 |
| 20 | filler | 1.72 | 0.0 | 2021 | 38 | 1983 | 0 |
| 21 | fact | 1.88 | 0.0 | 2107 | 58 | 2049 | 0 |
| 22 | filler | 26.61 | 21.73 | 2017 | 1836 | 181 | 0 |
| 23 | filler | 0.56 | 0.0 | 2069 | 37 | 2032 | 0 |
| 24 | filler | 2.25 | 0.0 | 2114 | 42 | 2072 | 0 |
| 25 | filler | 0.52 | 0.0 | 2191 | 38 | 2153 | 0 |
| 26 | filler | 1.82 | 0.0 | 2233 | 40 | 2193 | 0 |
| 27 | filler | 18.88 | 14.1 | 2210 | 2029 | 181 | 0 |
| 28 | filler | 3.74 | 0.0 | 2256 | 42 | 2214 | 0 |
| 29 | filler | 5.54 | 0.0 | 2371 | 44 | 2327 | 0 |
| 30 | filler | 2.06 | 0.0 | 2524 | 43 | 2481 | 0 |
| 31 | filler | 0.58 | 0.0 | 2600 | 41 | 2559 | 0 |
| 32 | filler | 27.03 | 21.81 | 2408 | 2227 | 181 | 0 |
| 33 | filler | 0.52 | 0.0 | 2452 | 41 | 2411 | 0 |
| 34 | filler | 1.87 | 0.0 | 2494 | 40 | 2454 | 0 |
| 35 | filler | 0.62 | 0.0 | 2567 | 42 | 2525 | 0 |
| 36 | filler | 0.53 | 0.0 | 2615 | 44 | 2571 | 0 |
| 37 | filler | 24.96 | 18.81 | 2583 | 2402 | 181 | 0 |
| 38 | filler | 0.47 | 0.0 | 2635 | 36 | 2599 | 0 |
| 39 | filler | 0.99 | 0.0 | 2673 | 37 | 2636 | 0 |
| 40 | recall | 0.48 | 0.0 | 2722 | 37 | 2685 | 0 |
| 41 | recall | 0.63 | 0.0 | 2766 | 43 | 2723 | 0 |
| 42 | recall | 31.87 | 26.14 | 2574 | 2393 | 181 | 0 |
| 43 | recall | 1.05 | 0.0 | 2623 | 41 | 2582 | 0 |
| 44 | recall | 0.78 | 0.0 | 2676 | 40 | 2636 | 0 |
| 45 | recall | 0.67 | 0.0 | 2722 | 39 | 2683 | 0 |
| 46 | recall | 1.05 | 0.0 | 2769 | 42 | 2727 | 0 |
| 47 | recall | 20.1 | 14.08 | 2751 | 2570 | 181 | 0 |