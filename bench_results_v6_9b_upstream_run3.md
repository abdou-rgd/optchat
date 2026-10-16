# OptChat local bench (Ternary Bonsai 2 9B Q2_0 on upstream llama.cpp b11700 (run2), RTX 3060 12GB)

Turns: 48  |  total wall: 1.1 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 4, 'merges': 60, 'verbatim': 86, 'calls': 18, 'errors': 0, 'seconds': 36.83436870574951}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.18 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.24 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 8.04 | Vous avez choisi **PostgreSQL** pour Atlas. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.39 | Inès Marchetti reprend le module de facturation à partir du **15 novembre**. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.33 | ATLAS_BUILD_KEY se trouve dans le fichier **.env.ci**. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.34 | Votre budget max pour le GPU est de **650 euros**. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.37 | Votre rendez-vous chez le dentiste est prévu à **9h15**. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 5.49 | La couleur d'embed du bot Discord est **#3FA7D6**. |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 0.44 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 0.65 | 0.0 | 754 | 61 | 693 | 0 |
| 2 | filler | 0.34 | 0.0 | 828 | 78 | 750 | 0 |
| 3 | fact | 0.62 | 0.0 | 901 | 77 | 824 | 0 |
| 4 | filler | 0.24 | 0.0 | 979 | 82 | 897 | 0 |
| 5 | filler | 0.19 | 0.0 | 1019 | 44 | 975 | 0 |
| 6 | fact | 0.44 | 0.0 | 1062 | 47 | 1015 | 0 |
| 7 | filler | 1.13 | 0.01 | 1350 | 696 | 654 | 0 |
| 8 | filler | 0.22 | 0.0 | 1434 | 88 | 1346 | 0 |
| 9 | fact | 0.44 | 0.0 | 1486 | 56 | 1430 | 0 |
| 10 | filler | 0.22 | 0.0 | 1547 | 65 | 1482 | 0 |
| 11 | filler | 0.5 | 0.0 | 1587 | 44 | 1543 | 0 |
| 12 | fact | 4.6 | 3.52 | 1574 | 920 | 654 | 0 |
| 13 | filler | 0.29 | 0.0 | 1631 | 61 | 1570 | 0 |
| 14 | filler | 0.34 | 0.0 | 1673 | 46 | 1627 | 0 |
| 15 | fact | 0.4 | 0.0 | 1725 | 56 | 1669 | 0 |
| 16 | filler | 0.23 | 0.0 | 1778 | 57 | 1721 | 0 |
| 17 | filler | 3.4 | 2.38 | 1794 | 1140 | 654 | 0 |
| 18 | fact | 0.47 | 0.0 | 1855 | 65 | 1790 | 0 |
| 19 | filler | 0.24 | 0.0 | 1914 | 63 | 1851 | 0 |
| 20 | filler | 0.37 | 0.0 | 1952 | 42 | 1910 | 0 |
| 21 | fact | 0.57 | 0.0 | 2022 | 74 | 1948 | 0 |
| 22 | filler | 5.99 | 4.88 | 1923 | 1269 | 654 | 0 |
| 23 | filler | 0.26 | 0.0 | 1971 | 52 | 1919 | 0 |
| 24 | filler | 0.76 | 0.0 | 2016 | 49 | 1967 | 0 |
| 25 | filler | 0.23 | 0.0 | 2097 | 85 | 2012 | 0 |
| 26 | filler | 0.45 | 0.0 | 2135 | 42 | 2093 | 0 |
| 27 | filler | 5.58 | 4.52 | 2123 | 1469 | 654 | 0 |
| 28 | filler | 1.06 | 0.0 | 2165 | 46 | 2119 | 0 |
| 29 | filler | 1.47 | 0.0 | 2277 | 116 | 2161 | 0 |
| 30 | filler | 0.48 | 0.0 | 2419 | 146 | 2273 | 0 |
| 31 | filler | 0.22 | 0.0 | 2477 | 62 | 2415 | 0 |
| 32 | filler | 5.8 | 4.71 | 2194 | 1540 | 654 | 0 |
| 33 | filler | 0.18 | 0.0 | 2234 | 44 | 2190 | 0 |
| 34 | filler | 0.3 | 0.0 | 2271 | 41 | 2230 | 0 |
| 35 | filler | 0.23 | 0.0 | 2319 | 52 | 2267 | 0 |
| 36 | filler | 0.21 | 0.0 | 2363 | 48 | 2315 | 0 |
| 37 | filler | 7.73 | 6.19 | 2493 | 1839 | 654 | 0 |
| 38 | filler | 0.2 | 0.0 | 2549 | 60 | 2489 | 0 |
| 39 | filler | 0.3 | 0.0 | 2584 | 39 | 2545 | 0 |
| 40 | recall | 0.18 | 0.0 | 2628 | 48 | 2580 | 0 |
| 41 | recall | 0.24 | 0.0 | 2668 | 44 | 2624 | 0 |
| 42 | recall | 8.04 | 6.67 | 2538 | 1884 | 654 | 0 |
| 43 | recall | 0.39 | 0.0 | 2585 | 51 | 2534 | 0 |
| 44 | recall | 0.33 | 0.0 | 2639 | 58 | 2581 | 0 |
| 45 | recall | 0.34 | 0.0 | 2687 | 52 | 2635 | 0 |
| 46 | recall | 0.37 | 0.0 | 2739 | 56 | 2683 | 0 |
| 47 | recall | 5.49 | 3.95 | 2765 | 2111 | 654 | 0 |