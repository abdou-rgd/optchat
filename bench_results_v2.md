# OptChat local bench (Bonsai 2 27B PTQ1_0, RTX 3060 12GB)

Turns: 46  |  total wall: 4.9 min  |  compaction: {'summaries': 90, 'merges': 60, 'seconds': 206.2947108745575, 'calls': 41}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | pixel | ✅ | 1 | 2 | 6.74 | Pixel. |
| Quel est le port SSH du serveur de prod d'Atlas ? | 2222 | ✅ | 0 | 1 | 0.61 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | postgres | ✅ | 0 | 1 | 0.76 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | marchetti | ✅ | 0 | 1 | 1.01 | Inès Marchetti, à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | .env.ci | ✅ | 0 | 1 | 5.5 | Dans le fichier `.env.ci`. |
| Quel est mon budget max pour le GPU ? | 650 | ✅ | 0 | 1 | 0.63 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | 9h15 | ✅ | 0 | 1 | 0.64 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | 3fa7d6 | ✅ | 0 | 1 | 0.68 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|
| 0 | fact | 6.54 | 697 | 516 | 181 | 1 |
| 1 | filler | 1.67 | 922 | 42 | 880 | 0 |
| 2 | filler | 0.55 | 995 | 40 | 955 | 0 |
| 3 | fact | 3.32 | 1063 | 65 | 998 | 0 |
| 4 | filler | 2.76 | 1396 | 1215 | 181 | 0 |
| 5 | filler | 0.54 | 1440 | 41 | 1399 | 0 |
| 6 | fact | 2.8 | 1488 | 46 | 1442 | 0 |
| 7 | filler | 1.76 | 1632 | 40 | 1592 | 0 |
| 8 | filler | 3.69 | 1673 | 1492 | 181 | 0 |
| 9 | fact | 1.44 | 1740 | 53 | 1687 | 0 |
| 10 | filler | 0.59 | 1810 | 44 | 1766 | 0 |
| 11 | filler | 1.38 | 1855 | 41 | 1814 | 0 |
| 12 | fact | 1.76 | 1935 | 56 | 1879 | 0 |
| 13 | filler | 3.75 | 1962 | 1781 | 181 | 0 |
| 14 | filler | 1.12 | 2002 | 37 | 1965 | 0 |
| 15 | fact | 1.06 | 2064 | 45 | 2019 | 0 |
| 16 | filler | 0.53 | 2119 | 39 | 2080 | 0 |
| 17 | filler | 1.55 | 2163 | 42 | 2121 | 0 |
| 18 | fact | 4.81 | 2140 | 1959 | 181 | 0 |
| 19 | filler | 0.57 | 2202 | 40 | 2162 | 0 |
| 20 | filler | 1.23 | 2243 | 38 | 2205 | 0 |
| 21 | fact | 1.67 | 2322 | 58 | 2264 | 0 |
| 22 | filler | 0.53 | 2395 | 43 | 2352 | 0 |
| 23 | filler | 4.36 | 2331 | 2150 | 181 | 0 |
| 24 | filler | 1.53 | 2375 | 42 | 2333 | 0 |
| 25 | filler | 0.53 | 2441 | 38 | 2403 | 0 |
| 26 | filler | 1.49 | 2484 | 40 | 2444 | 0 |
| 27 | filler | 0.52 | 2548 | 37 | 2511 | 0 |
| 28 | filler | 5.57 | 2437 | 2256 | 181 | 0 |
| 29 | filler | 0.52 | 2506 | 41 | 2465 | 0 |
| 30 | filler | 0.57 | 2556 | 48 | 2508 | 0 |
| 31 | filler | 0.52 | 2600 | 41 | 2559 | 0 |
| 32 | filler | 1.59 | 2642 | 40 | 2602 | 0 |
| 33 | filler | 5.06 | 2682 | 2501 | 181 | 0 |
| 34 | filler | 0.52 | 2729 | 44 | 2685 | 0 |
| 35 | filler | 1.39 | 2772 | 41 | 2731 | 0 |
| 36 | filler | 0.56 | 2832 | 36 | 2796 | 0 |
| 37 | filler | 1.09 | 2872 | 37 | 2835 | 0 |
| 38 | recall | 6.74 | 2589 | 2408 | 181 | 1 |
| 39 | recall | 0.61 | 2901 | 43 | 2858 | 0 |
| 40 | recall | 0.76 | 2950 | 45 | 2905 | 0 |
| 41 | recall | 1.01 | 2999 | 41 | 2958 | 0 |
| 42 | recall | 5.5 | 2873 | 2692 | 181 | 0 |
| 43 | recall | 0.63 | 2919 | 39 | 2880 | 0 |
| 44 | recall | 0.64 | 2966 | 42 | 2924 | 0 |
| 45 | recall | 0.68 | 3013 | 42 | 2971 | 0 |