# OptChat local bench (model not labelled, RTX 3060 12GB)

Turns: 48  |  total wall: 2.9 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 4, 'merges': 58, 'verbatim': 84, 'calls': 17, 'errors': 0, 'seconds': 108.48590040206909}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 3.9 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.49 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 0.58 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.93 | Inès Marchetti reprend le module de facturation à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.56 | Dans le fichier `.env.ci`. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 18.71 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.52 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 0.52 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 1.2 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 1.29 | 0.0 | 763 | 42 | 721 | 0 |
| 2 | filler | 0.45 | 0.0 | 833 | 40 | 793 | 0 |
| 3 | fact | 1.46 | 0.0 | 900 | 64 | 836 | 0 |
| 4 | filler | 0.43 | 0.0 | 981 | 47 | 934 | 0 |
| 5 | filler | 0.42 | 0.0 | 1025 | 41 | 984 | 0 |
| 6 | fact | 0.95 | 0.0 | 1073 | 46 | 1027 | 0 |
| 7 | filler | 2.53 | 0.01 | 1347 | 693 | 654 | 0 |
| 8 | filler | 0.44 | 0.0 | 1419 | 42 | 1377 | 0 |
| 9 | fact | 1.02 | 0.0 | 1475 | 53 | 1422 | 0 |
| 10 | filler | 0.41 | 0.0 | 1540 | 44 | 1496 | 0 |
| 11 | filler | 1.16 | 0.0 | 1583 | 41 | 1542 | 0 |
| 12 | fact | 10.97 | 7.92 | 1599 | 945 | 654 | 0 |
| 13 | filler | 0.45 | 0.0 | 1664 | 36 | 1628 | 0 |
| 14 | filler | 0.81 | 0.0 | 1704 | 37 | 1667 | 0 |
| 15 | fact | 0.87 | 0.0 | 1763 | 45 | 1718 | 0 |
| 16 | filler | 0.42 | 0.0 | 1818 | 39 | 1779 | 0 |
| 17 | filler | 9.8 | 6.41 | 1827 | 1173 | 654 | 0 |
| 18 | fact | 1.04 | 0.0 | 1908 | 51 | 1857 | 0 |
| 19 | filler | 0.45 | 0.0 | 1970 | 40 | 1930 | 0 |
| 20 | filler | 1.17 | 0.0 | 2011 | 38 | 1973 | 0 |
| 21 | fact | 1.2 | 0.0 | 2095 | 58 | 2037 | 0 |
| 22 | filler | 19.41 | 16.15 | 2039 | 1385 | 654 | 0 |
| 23 | filler | 0.43 | 0.0 | 2091 | 37 | 2054 | 0 |
| 24 | filler | 1.59 | 0.0 | 2136 | 42 | 2094 | 0 |
| 25 | filler | 0.47 | 0.0 | 2213 | 38 | 2175 | 0 |
| 26 | filler | 1.14 | 0.0 | 2257 | 40 | 2217 | 0 |
| 27 | filler | 14.85 | 11.67 | 2249 | 1595 | 654 | 0 |
| 28 | filler | 2.96 | 0.0 | 2295 | 42 | 2253 | 0 |
| 29 | filler | 4.41 | 0.0 | 2423 | 94 | 2379 | 0 |
| 30 | filler | 1.23 | 0.0 | 2638 | 43 | 2595 | 0 |
| 31 | filler | 18.43 | 14.65 | 2646 | 1992 | 654 | 0 |
| 32 | filler | 0.44 | 0.0 | 2697 | 48 | 2649 | 0 |
| 33 | filler | 0.43 | 0.0 | 2741 | 41 | 2700 | 0 |
| 34 | filler | 1.14 | 0.0 | 2783 | 40 | 2743 | 0 |
| 35 | filler | 22.47 | 18.68 | 2695 | 2041 | 654 | 0 |
| 36 | filler | 0.4 | 0.0 | 2742 | 44 | 2698 | 0 |
| 37 | filler | 1.12 | 0.0 | 2785 | 41 | 2744 | 0 |
| 38 | filler | 0.39 | 0.0 | 2846 | 36 | 2810 | 0 |
| 39 | filler | 0.77 | 0.0 | 2885 | 37 | 2848 | 0 |
| 40 | recall | 3.9 | 0.0 | 2757 | 2103 | 654 | 0 |
| 41 | recall | 0.49 | 0.0 | 2801 | 43 | 2758 | 0 |
| 42 | recall | 0.58 | 0.0 | 2850 | 45 | 2805 | 0 |
| 43 | recall | 0.93 | 0.0 | 2899 | 41 | 2858 | 0 |
| 44 | recall | 0.56 | 0.0 | 2957 | 40 | 2917 | 0 |
| 45 | recall | 18.71 | 14.44 | 2897 | 2243 | 654 | 0 |
| 46 | recall | 0.52 | 0.0 | 2944 | 42 | 2902 | 0 |
| 47 | recall | 0.52 | 0.0 | 2990 | 41 | 2949 | 0 |