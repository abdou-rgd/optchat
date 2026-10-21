# OptChat local bench (Bonsai 2 27B Q2_0, upstream b11700, guard+join+cut, RTX 3060 12GB)

Turns: 48  |  total wall: 1.4 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 3, 'merges': 58, 'verbatim': 85, 'calls': 3, 'errors': 0, 'seconds': 17.276387453079224, 'guard_merges': 0, 'joined': 54}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 4.22 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.46 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 0.55 | PostgreSQL, pour les transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.89 | Inès Marchetti reprend le module de facturation à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.74 | Dans le fichier `.env.ci` (pas dans `.env`). |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 11.34 | 650 euros. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.7 | 9h15 (jeudi 23 octobre). |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 1 | 2 | 1.85 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 1.25 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 1.24 | 0.0 | 749 | 42 | 707 | 0 |
| 2 | filler | 0.41 | 0.0 | 819 | 40 | 779 | 0 |
| 3 | fact | 0.51 | 0.0 | 886 | 64 | 822 | 0 |
| 4 | filler | 0.42 | 0.0 | 938 | 47 | 891 | 0 |
| 5 | filler | 0.39 | 0.0 | 982 | 41 | 941 | 0 |
| 6 | fact | 0.48 | 0.0 | 1030 | 46 | 984 | 0 |
| 7 | filler | 2.27 | 0.01 | 1290 | 636 | 654 | 0 |
| 8 | filler | 0.42 | 0.0 | 1361 | 42 | 1319 | 0 |
| 9 | fact | 0.49 | 0.0 | 1417 | 53 | 1364 | 0 |
| 10 | filler | 0.39 | 0.0 | 1466 | 44 | 1422 | 0 |
| 11 | filler | 1.14 | 0.0 | 1509 | 41 | 1468 | 0 |
| 12 | fact | 2.77 | 0.02 | 1630 | 976 | 654 | 0 |
| 13 | filler | 0.48 | 0.0 | 1671 | 36 | 1635 | 0 |
| 14 | filler | 0.86 | 0.0 | 1712 | 45 | 1667 | 0 |
| 15 | fact | 0.48 | 0.0 | 1773 | 45 | 1728 | 0 |
| 16 | filler | 0.39 | 0.0 | 1817 | 39 | 1778 | 0 |
| 17 | filler | 3.26 | 0.02 | 1906 | 1252 | 654 | 0 |
| 18 | fact | 0.49 | 0.0 | 1987 | 51 | 1936 | 0 |
| 19 | filler | 0.42 | 0.0 | 2032 | 40 | 1992 | 0 |
| 20 | filler | 1.52 | 0.0 | 2073 | 38 | 2035 | 0 |
| 21 | fact | 0.52 | 0.0 | 2170 | 58 | 2112 | 0 |
| 22 | filler | 3.71 | 0.02 | 2162 | 1508 | 654 | 0 |
| 23 | filler | 0.39 | 0.0 | 2201 | 37 | 2164 | 0 |
| 24 | filler | 1.55 | 0.0 | 2245 | 42 | 2203 | 0 |
| 25 | filler | 0.42 | 0.0 | 2323 | 38 | 2285 | 0 |
| 26 | filler | 1.28 | 0.0 | 2366 | 40 | 2326 | 0 |
| 27 | filler | 3.87 | 0.02 | 2427 | 1773 | 654 | 0 |
| 28 | filler | 2.56 | 0.0 | 2472 | 42 | 2430 | 0 |
| 29 | filler | 4.56 | 0.0 | 2589 | 94 | 2545 | 0 |
| 30 | filler | 1.27 | 0.0 | 2811 | 43 | 2768 | 0 |
| 31 | filler | 4.62 | 0.01 | 2864 | 2210 | 654 | 0 |
| 32 | filler | 0.43 | 0.0 | 2915 | 48 | 2867 | 0 |
| 33 | filler | 0.4 | 0.0 | 2959 | 41 | 2918 | 0 |
| 34 | filler | 1.22 | 0.0 | 3001 | 40 | 2961 | 0 |
| 35 | filler | 8.72 | 4.31 | 2966 | 2312 | 654 | 0 |
| 36 | filler | 0.4 | 0.0 | 3013 | 44 | 2969 | 0 |
| 37 | filler | 1.18 | 0.0 | 3056 | 41 | 3015 | 0 |
| 38 | filler | 0.45 | 0.0 | 3119 | 36 | 3083 | 0 |
| 39 | filler | 0.82 | 0.0 | 3160 | 37 | 3123 | 0 |
| 40 | recall | 4.22 | 0.0 | 2986 | 2332 | 654 | 0 |
| 41 | recall | 0.46 | 0.0 | 3030 | 43 | 2987 | 0 |
| 42 | recall | 0.55 | 0.0 | 3079 | 45 | 3034 | 0 |
| 43 | recall | 0.89 | 0.0 | 3127 | 41 | 3086 | 0 |
| 44 | recall | 0.74 | 0.0 | 3185 | 40 | 3145 | 0 |
| 45 | recall | 11.34 | 6.75 | 3106 | 2452 | 654 | 0 |
| 46 | recall | 0.7 | 0.0 | 3153 | 42 | 3111 | 0 |
| 47 | recall | 1.85 | 0.0 | 3206 | 216 | 3165 | 1 |