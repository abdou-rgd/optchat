# OptChat local bench (Ternary Bonsai 2 9B Q2_0 on upstream llama.cpp b11700 (run2), RTX 3060 12GB)

Turns: 48  |  total wall: 1.0 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 3, 'merges': 60, 'verbatim': 87, 'calls': 17, 'errors': 0, 'seconds': 35.16124510765076}

## Recall: 7/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.19 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.26 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 7.38 | PostgreSQL, car vous l'aviez choisi pour Atlas (versus MongoDB). |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | MISS | 0 | 1 | 0.49 | Je ne trouve pas d'information dans ma mémoire concernant le module de facturation ni la date de sa prise en charge. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.27 | Dans le fichier `.env.ci`. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.24 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.24 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 5.35 | #3FA7D6. |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 0.6 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 0.43 | 0.0 | 741 | 48 | 693 | 0 |
| 2 | filler | 0.2 | 0.0 | 800 | 63 | 737 | 0 |
| 3 | fact | 0.53 | 0.0 | 863 | 67 | 796 | 0 |
| 4 | filler | 0.21 | 0.0 | 937 | 78 | 859 | 0 |
| 5 | filler | 0.18 | 0.0 | 977 | 44 | 933 | 0 |
| 6 | fact | 0.23 | 0.0 | 1020 | 47 | 973 | 0 |
| 7 | filler | 0.76 | 0.01 | 1291 | 637 | 654 | 0 |
| 8 | filler | 0.2 | 0.0 | 1350 | 63 | 1287 | 0 |
| 9 | fact | 0.19 | 0.0 | 1402 | 56 | 1346 | 0 |
| 10 | filler | 0.19 | 0.0 | 1445 | 47 | 1398 | 0 |
| 11 | filler | 0.41 | 0.0 | 1485 | 44 | 1441 | 0 |
| 12 | fact | 3.31 | 2.34 | 1510 | 856 | 654 | 0 |
| 13 | filler | 0.27 | 0.0 | 1568 | 62 | 1506 | 0 |
| 14 | filler | 0.31 | 0.0 | 1610 | 46 | 1564 | 0 |
| 15 | fact | 0.38 | 0.0 | 1663 | 57 | 1606 | 0 |
| 16 | filler | 0.22 | 0.0 | 1716 | 57 | 1659 | 0 |
| 17 | filler | 3.31 | 2.35 | 1768 | 1114 | 654 | 0 |
| 18 | fact | 0.42 | 0.0 | 1830 | 66 | 1764 | 0 |
| 19 | filler | 0.21 | 0.0 | 1887 | 61 | 1826 | 0 |
| 20 | filler | 0.33 | 0.0 | 1925 | 42 | 1883 | 0 |
| 21 | fact | 0.5 | 0.0 | 1994 | 73 | 1921 | 0 |
| 22 | filler | 5.76 | 4.69 | 1929 | 1275 | 654 | 0 |
| 23 | filler | 0.26 | 0.0 | 1977 | 52 | 1925 | 0 |
| 24 | filler | 0.72 | 0.0 | 2022 | 49 | 1973 | 0 |
| 25 | filler | 0.2 | 0.0 | 2100 | 82 | 2018 | 0 |
| 26 | filler | 0.36 | 0.0 | 2138 | 42 | 2096 | 0 |
| 27 | filler | 5.86 | 4.73 | 2124 | 1470 | 654 | 0 |
| 28 | filler | 1.05 | 0.0 | 2166 | 46 | 2120 | 0 |
| 29 | filler | 1.06 | 0.0 | 2279 | 117 | 2162 | 0 |
| 30 | filler | 0.48 | 0.0 | 2387 | 112 | 2275 | 0 |
| 31 | filler | 0.23 | 0.0 | 2447 | 64 | 2383 | 0 |
| 32 | filler | 6.82 | 5.55 | 2250 | 1596 | 654 | 0 |
| 33 | filler | 0.19 | 0.0 | 2290 | 44 | 2246 | 0 |
| 34 | filler | 0.47 | 0.0 | 2327 | 41 | 2286 | 0 |
| 35 | filler | 0.25 | 0.0 | 2387 | 64 | 2323 | 0 |
| 36 | filler | 0.25 | 0.0 | 2431 | 48 | 2383 | 0 |
| 37 | filler | 7.06 | 5.58 | 2516 | 1862 | 654 | 0 |
| 38 | filler | 0.21 | 0.0 | 2563 | 51 | 2512 | 0 |
| 39 | filler | 0.32 | 0.0 | 2598 | 39 | 2559 | 0 |
| 40 | recall | 0.19 | 0.0 | 2643 | 49 | 2594 | 0 |
| 41 | recall | 0.26 | 0.0 | 2683 | 44 | 2639 | 0 |
| 42 | recall | 7.38 | 5.96 | 2422 | 1768 | 654 | 0 |
| 43 | recall | 0.49 | 0.0 | 2475 | 57 | 2418 | 0 |
| 44 | recall | 0.27 | 0.0 | 2536 | 65 | 2471 | 0 |
| 45 | recall | 0.24 | 0.0 | 2578 | 46 | 2532 | 0 |
| 46 | recall | 0.24 | 0.0 | 2621 | 47 | 2574 | 0 |
| 47 | recall | 5.35 | 3.94 | 2645 | 1991 | 654 | 0 |