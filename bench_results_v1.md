# OptChat local bench (Bonsai 2 27B PTQ1_0, RTX 3060 12GB)

Turns: 46  |  total wall: 4.9 min  |  compaction: {'summaries': 90, 'merges': 59, 'seconds': 211.64696431159973}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | pixel | ✅ | 0 | 1 | 4.8 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | 2222 | ✅ | 0 | 1 | 0.58 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | postgres | ✅ | 0 | 1 | 0.78 | PostgreSQL, pour son support des transactions. |
| Qui reprend le module de facturation, et quand ? | marchetti | ✅ | 0 | 1 | 5.72 | Inès Marchetti reprend le module de facturation à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | .env.ci | ✅ | 0 | 1 | 0.62 | Dans `.env.ci`. |
| Quel est mon budget max pour le GPU ? | 650 | ✅ | 0 | 1 | 0.62 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | 9h15 | ✅ | 0 | 1 | 5.08 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | 3fa7d6 | ✅ | 1 | 2 | 2.38 | `#3FA7D6`. |

## Per-turn cost

| # | tag | wall s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|
| 0 | fact | 1.15 | 697 | 4 | 693 | 0 |
| 1 | filler | 1.77 | 757 | 42 | 715 | 0 |
| 2 | filler | 0.58 | 828 | 40 | 788 | 0 |
| 3 | fact | 1.71 | 895 | 64 | 831 | 0 |
| 4 | filler | 0.57 | 974 | 47 | 927 | 0 |
| 5 | filler | 2.35 | 1115 | 934 | 181 | 0 |
| 6 | fact | 1.14 | 1163 | 46 | 1117 | 0 |
| 7 | filler | 1.74 | 1219 | 40 | 1179 | 0 |
| 8 | filler | 3.3 | 1365 | 1184 | 181 | 0 |
| 9 | fact | 1.41 | 1432 | 53 | 1379 | 0 |
| 10 | filler | 0.62 | 1498 | 44 | 1454 | 0 |
| 11 | filler | 4.11 | 1488 | 1307 | 181 | 0 |
| 12 | fact | 1.58 | 1569 | 56 | 1513 | 0 |
| 13 | filler | 0.61 | 1630 | 36 | 1594 | 0 |
| 14 | filler | 3.82 | 1658 | 1477 | 181 | 0 |
| 15 | fact | 1.11 | 1719 | 45 | 1674 | 0 |
| 16 | filler | 0.52 | 1775 | 39 | 1736 | 0 |
| 17 | filler | 4.62 | 1806 | 1625 | 181 | 0 |
| 18 | fact | 1.28 | 1889 | 51 | 1838 | 0 |
| 19 | filler | 0.57 | 1950 | 40 | 1910 | 0 |
| 20 | filler | 4.65 | 1851 | 1670 | 181 | 0 |
| 21 | fact | 1.63 | 1936 | 58 | 1878 | 0 |
| 22 | filler | 0.53 | 2008 | 43 | 1965 | 0 |
| 23 | filler | 3.96 | 2052 | 1871 | 181 | 0 |
| 24 | filler | 1.54 | 2096 | 42 | 2054 | 0 |
| 25 | filler | 0.55 | 2162 | 38 | 2124 | 0 |
| 26 | filler | 5.21 | 2097 | 1916 | 181 | 0 |
| 27 | filler | 0.53 | 2167 | 37 | 2130 | 0 |
| 28 | filler | 1.67 | 2213 | 43 | 2170 | 0 |
| 29 | filler | 4.43 | 2288 | 2107 | 181 | 0 |
| 30 | filler | 0.6 | 2338 | 48 | 2290 | 0 |
| 31 | filler | 0.57 | 2382 | 41 | 2341 | 0 |
| 32 | filler | 5.06 | 2308 | 2127 | 181 | 0 |
| 33 | filler | 0.54 | 2374 | 42 | 2332 | 0 |
| 34 | filler | 0.51 | 2421 | 44 | 2377 | 0 |
| 35 | filler | 5.47 | 2516 | 2335 | 181 | 0 |
| 36 | filler | 0.5 | 2576 | 36 | 2540 | 0 |
| 37 | filler | 1.02 | 2615 | 37 | 2578 | 0 |
| 38 | recall | 4.8 | 2590 | 2409 | 181 | 0 |
| 39 | recall | 0.58 | 2634 | 43 | 2591 | 0 |
| 40 | recall | 0.78 | 2683 | 45 | 2638 | 0 |
| 41 | recall | 5.72 | 2779 | 2598 | 181 | 0 |
| 42 | recall | 0.62 | 2837 | 40 | 2797 | 0 |
| 43 | recall | 0.62 | 2881 | 39 | 2842 | 0 |
| 44 | recall | 5.08 | 2621 | 2440 | 181 | 0 |
| 45 | recall | 2.38 | 2667 | 41 | 2626 | 1 |