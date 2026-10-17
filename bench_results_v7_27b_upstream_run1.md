# OptChat local bench (model not labelled, RTX 3060 12GB)

Turns: 48  |  total wall: 5.3 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 38, 'merges': 91, 'verbatim': 86, 'calls': 30, 'errors': 0, 'seconds': 213.2651870250702}

## Recall: 8/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.39 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | OK | 0 | 1 | 0.5 | 2222 |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 16.66 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.67 | Inès Marchetti le 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 0.41 | .env.ci |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.48 | 650 € |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.47 | 9h15 |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 24.77 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 4.51 | 0.0 | 697 | 769 | 0 | 1 |
| 1 | filler | 1.74 | 0.0 | 885 | 42 | 843 | 0 |
| 2 | filler | 0.5 | 0.0 | 966 | 40 | 926 | 0 |
| 3 | fact | 3.88 | 0.0 | 1034 | 157 | 969 | 1 |
| 4 | filler | 8.49 | 6.37 | 1452 | 798 | 654 | 0 |
| 5 | filler | 0.42 | 0.0 | 1496 | 41 | 1455 | 0 |
| 6 | fact | 2.35 | 0.0 | 1544 | 98 | 1498 | 0 |
| 7 | filler | 19.69 | 15.56 | 1711 | 1103 | 654 | 0 |
| 8 | filler | 1.59 | 0.0 | 1848 | 91 | 1806 | 0 |
| 9 | fact | 2.52 | 0.0 | 1979 | 112 | 1926 | 0 |
| 10 | filler | 18.73 | 14.68 | 2049 | 1445 | 654 | 0 |
| 11 | filler | 2.37 | 0.0 | 2169 | 88 | 2128 | 0 |
| 12 | fact | 2.6 | 0.0 | 2326 | 118 | 2270 | 0 |
| 13 | filler | 34.89 | 30.32 | 2330 | 1719 | 654 | 0 |
| 14 | filler | 1.93 | 0.0 | 2438 | 80 | 2401 | 0 |
| 15 | fact | 2.01 | 0.0 | 2567 | 96 | 2522 | 0 |
| 16 | filler | 25.17 | 20.17 | 2489 | 1880 | 654 | 0 |
| 17 | filler | 2.73 | 0.0 | 2606 | 90 | 2564 | 0 |
| 18 | fact | 1.17 | 0.0 | 2770 | 51 | 2719 | 0 |
| 19 | filler | 13.1 | 8.85 | 2823 | 2169 | 654 | 0 |
| 20 | filler | 1.08 | 0.0 | 2865 | 38 | 2827 | 0 |
| 21 | fact | 1.44 | 0.0 | 2946 | 58 | 2888 | 0 |
| 22 | filler | 0.41 | 0.0 | 3022 | 43 | 2979 | 0 |
| 23 | filler | 24.38 | 20.13 | 2838 | 2184 | 654 | 0 |
| 24 | filler | 1.62 | 0.0 | 2883 | 42 | 2841 | 0 |
| 25 | filler | 0.44 | 0.0 | 2961 | 38 | 2923 | 0 |
| 26 | filler | 1.26 | 0.0 | 3004 | 40 | 2964 | 0 |
| 27 | filler | 0.43 | 0.0 | 3069 | 37 | 3032 | 0 |
| 28 | filler | 34.54 | 27.98 | 2783 | 2129 | 654 | 0 |
| 29 | filler | 4.01 | 0.0 | 2905 | 94 | 2861 | 0 |
| 30 | filler | 1.3 | 0.0 | 3103 | 43 | 3060 | 0 |
| 31 | filler | 0.43 | 0.0 | 3174 | 41 | 3133 | 0 |
| 32 | filler | 21.37 | 16.83 | 3025 | 2371 | 654 | 0 |
| 33 | filler | 0.43 | 0.0 | 3070 | 42 | 3028 | 0 |
| 34 | filler | 1.12 | 0.0 | 3113 | 41 | 3072 | 0 |
| 35 | filler | 0.45 | 0.0 | 3180 | 43 | 3137 | 0 |
| 36 | filler | 0.43 | 0.0 | 3228 | 45 | 3183 | 0 |
| 37 | filler | 26.21 | 20.94 | 2984 | 2330 | 654 | 0 |
| 38 | filler | 0.36 | 0.0 | 3045 | 37 | 3008 | 0 |
| 39 | filler | 0.86 | 0.0 | 3084 | 38 | 3046 | 0 |
| 40 | recall | 0.39 | 0.0 | 3138 | 38 | 3100 | 0 |
| 41 | recall | 0.5 | 0.0 | 3183 | 44 | 3139 | 0 |
| 42 | recall | 16.66 | 11.72 | 3209 | 2555 | 654 | 0 |
| 43 | recall | 0.67 | 0.0 | 3259 | 42 | 3217 | 0 |
| 44 | recall | 0.41 | 0.0 | 3310 | 41 | 3269 | 0 |
| 45 | recall | 0.48 | 0.0 | 3352 | 40 | 3312 | 0 |
| 46 | recall | 0.47 | 0.0 | 3399 | 43 | 3356 | 0 |
| 47 | recall | 24.77 | 19.71 | 3310 | 2656 | 654 | 0 |