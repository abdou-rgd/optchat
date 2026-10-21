# OptChat local bench (Bonsai 2 27B Q2_0, upstream b11700, guard+join+cut, RTX 3060 12GB)

Turns: 48  |  total wall: 2.4 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 20, 'merges': 80, 'verbatim': 94, 'calls': 9, 'errors': 0, 'seconds': 58.819183588027954, 'guard_merges': 0, 'joined': 72}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 1 | 2 | 1.95 | Ton chat s'appelle Pixel. |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 1 | 2 | 2.28 | Le port SSH du serveur de prod d'Atlas est 2222. |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 1 | 2 | 16.85 | Vous avez choisi PostgreSQL pour Atlas, pas MongoDB, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 1 | 2 | 2.32 | Inès Marchetti reprend le module de facturation à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 1 | 2 | 2.35 | Le token `ATLAS_BUILD_KEY` se trouve dans le fichier `.env.ci`, pas dans `.env`. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 1 | 2 | 26.48 | Ton budget max pour le nouveau GPU est de 650 €. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 1 | 2 | 2.36 | Ton rendez-vous chez le dentiste est à 9h15 (jeudi 23 octobre). |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 1 | 2 | 2.22 | La couleur d'embed du bot Discord est `#3FA7D6`. |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 2.5 | 0.0 | 697 | 64 | 654 | 1 |
| 1 | filler | 1.22 | 0.0 | 805 | 42 | 763 | 0 |
| 2 | filler | 0.42 | 0.0 | 875 | 40 | 835 | 0 |
| 3 | fact | 1.38 | 0.0 | 942 | 64 | 878 | 0 |
| 4 | filler | 0.43 | 0.0 | 1024 | 48 | 976 | 0 |
| 5 | filler | 0.39 | 0.0 | 1068 | 41 | 1027 | 0 |
| 6 | fact | 4.71 | 2.66 | 1337 | 683 | 654 | 0 |
| 7 | filler | 1.08 | 0.0 | 1392 | 40 | 1352 | 0 |
| 8 | filler | 0.42 | 0.0 | 1459 | 42 | 1417 | 0 |
| 9 | fact | 0.98 | 0.0 | 1515 | 53 | 1462 | 0 |
| 10 | filler | 0.39 | 0.0 | 1580 | 44 | 1536 | 0 |
| 11 | filler | 3.36 | 0.01 | 1660 | 1006 | 654 | 0 |
| 12 | fact | 1.3 | 0.0 | 1743 | 56 | 1687 | 0 |
| 13 | filler | 0.45 | 0.0 | 1810 | 36 | 1774 | 0 |
| 14 | filler | 0.75 | 0.0 | 1851 | 37 | 1814 | 0 |
| 15 | fact | 0.82 | 0.0 | 1910 | 45 | 1865 | 0 |
| 16 | filler | 2.6 | 0.01 | 2010 | 1356 | 654 | 0 |
| 17 | filler | 1.06 | 0.0 | 2054 | 42 | 2012 | 0 |
| 18 | fact | 0.95 | 0.0 | 2129 | 51 | 2078 | 0 |
| 19 | filler | 0.42 | 0.0 | 2189 | 40 | 2149 | 0 |
| 20 | filler | 1.33 | 0.0 | 2230 | 38 | 2192 | 0 |
| 21 | fact | 4.61 | 0.02 | 2266 | 1612 | 654 | 0 |
| 22 | filler | 0.39 | 0.0 | 2341 | 43 | 2298 | 0 |
| 23 | filler | 0.38 | 0.0 | 2380 | 37 | 2343 | 0 |
| 24 | filler | 1.18 | 0.0 | 2424 | 42 | 2382 | 0 |
| 25 | filler | 0.39 | 0.0 | 2490 | 38 | 2452 | 0 |
| 26 | filler | 4.86 | 0.02 | 2523 | 1869 | 654 | 0 |
| 27 | filler | 0.42 | 0.0 | 2586 | 37 | 2549 | 0 |
| 28 | filler | 3.03 | 0.0 | 2631 | 42 | 2589 | 0 |
| 29 | filler | 4.4 | 0.0 | 2763 | 94 | 2719 | 0 |
| 30 | filler | 6.59 | 0.02 | 2944 | 2339 | 654 | 0 |
| 31 | filler | 0.43 | 0.0 | 3089 | 41 | 3048 | 0 |
| 32 | filler | 0.43 | 0.0 | 3140 | 48 | 3092 | 0 |
| 33 | filler | 0.4 | 0.0 | 3184 | 41 | 3143 | 0 |
| 34 | filler | 9.71 | 4.41 | 3200 | 2546 | 654 | 0 |
| 35 | filler | 0.43 | 0.0 | 3267 | 42 | 3225 | 0 |
| 36 | filler | 0.4 | 0.0 | 3314 | 44 | 3270 | 0 |
| 37 | filler | 1.17 | 0.0 | 3357 | 41 | 3316 | 0 |
| 38 | filler | 0.39 | 0.0 | 3420 | 36 | 3384 | 0 |
| 39 | filler | 18.19 | 13.41 | 3049 | 2395 | 654 | 0 |
| 40 | recall | 1.95 | 0.0 | 3100 | 270 | 3063 | 1 |
| 41 | recall | 2.28 | 0.0 | 3410 | 297 | 3367 | 1 |
| 42 | recall | 16.85 | 10.01 | 3455 | 3055 | 654 | 1 |
| 43 | recall | 2.32 | 0.0 | 3792 | 270 | 3751 | 1 |
| 44 | recall | 2.35 | 0.0 | 4107 | 231 | 4066 | 1 |
| 45 | recall | 26.48 | 19.27 | 3680 | 3267 | 654 | 1 |
| 46 | recall | 2.36 | 0.0 | 4005 | 215 | 3962 | 1 |
| 47 | recall | 2.22 | 0.0 | 4268 | 213 | 4226 | 1 |