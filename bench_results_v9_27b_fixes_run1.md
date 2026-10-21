# OptChat local bench (Bonsai 2 27B Q2_0, upstream b11700, guard+join+cut, RTX 3060 12GB)

Turns: 48  |  total wall: 1.9 min  |  compactor: same server, slot 1  |  compaction stats: {'summaries': 7, 'merges': 60, 'verbatim': 83, 'calls': 5, 'errors': 0, 'seconds': 33.561967611312866, 'guard_merges': 0, 'joined': 56}

## Recall: 7/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 4.64 | Pixel. |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | MISS | 1 | 2 | 2.38 | Je n'ai pas d'information sur le port SSH du serveur de prod d'Atlas dans notre historique. |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | OK | 0 | 1 | 0.59 | PostgreSQL, à cause des transactions. |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | OK | 0 | 1 | 0.89 | Inès Marchetti reprend le module de facturation à partir du 15 novembre. |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 0 | 1 | 9.03 | Dans le fichier `.env.ci`. |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | OK | 0 | 1 | 0.45 | 650 €. |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | OK | 0 | 1 | 0.49 | 9h15. |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | OK | 0 | 1 | 0.52 | #3FA7D6 |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 2.36 | 0.0 | 697 | 697 | 0 | 0 |
| 1 | filler | 1.26 | 0.0 | 755 | 42 | 713 | 0 |
| 2 | filler | 0.42 | 0.0 | 825 | 40 | 785 | 0 |
| 3 | fact | 1.31 | 0.0 | 892 | 64 | 828 | 0 |
| 4 | filler | 0.5 | 0.0 | 970 | 47 | 923 | 0 |
| 5 | filler | 0.46 | 0.0 | 1014 | 41 | 973 | 0 |
| 6 | fact | 1.9 | 0.0 | 1062 | 67 | 1016 | 1 |
| 7 | filler | 2.81 | 0.01 | 1413 | 759 | 654 | 0 |
| 8 | filler | 0.54 | 0.0 | 1490 | 81 | 1409 | 0 |
| 9 | fact | 1.0 | 0.0 | 1547 | 53 | 1494 | 0 |
| 10 | filler | 0.47 | 0.0 | 1612 | 44 | 1568 | 0 |
| 11 | filler | 1.27 | 0.0 | 1657 | 41 | 1616 | 0 |
| 12 | fact | 6.48 | 3.2 | 1762 | 1108 | 654 | 0 |
| 13 | filler | 0.45 | 0.0 | 1829 | 36 | 1793 | 0 |
| 14 | filler | 0.82 | 0.0 | 1870 | 37 | 1833 | 0 |
| 15 | fact | 0.8 | 0.0 | 1931 | 45 | 1886 | 0 |
| 16 | filler | 0.48 | 0.0 | 1985 | 39 | 1946 | 0 |
| 17 | filler | 4.15 | 0.01 | 2073 | 1419 | 654 | 0 |
| 18 | fact | 1.02 | 0.0 | 2172 | 51 | 2121 | 0 |
| 19 | filler | 0.43 | 0.0 | 2234 | 40 | 2194 | 0 |
| 20 | filler | 1.39 | 0.0 | 2275 | 38 | 2237 | 0 |
| 21 | fact | 1.28 | 0.0 | 2367 | 58 | 2309 | 0 |
| 22 | filler | 4.21 | 0.02 | 2383 | 1729 | 654 | 0 |
| 23 | filler | 0.39 | 0.0 | 2422 | 37 | 2385 | 0 |
| 24 | filler | 1.82 | 0.0 | 2466 | 42 | 2424 | 0 |
| 25 | filler | 0.43 | 0.0 | 2552 | 38 | 2514 | 0 |
| 26 | filler | 1.19 | 0.0 | 2595 | 40 | 2555 | 0 |
| 27 | filler | 4.55 | 0.02 | 2626 | 1972 | 654 | 0 |
| 28 | filler | 3.09 | 0.0 | 2671 | 42 | 2629 | 0 |
| 29 | filler | 4.64 | 0.0 | 2805 | 94 | 2761 | 0 |
| 30 | filler | 1.27 | 0.0 | 3028 | 43 | 2985 | 0 |
| 31 | filler | 4.43 | 0.01 | 3133 | 2479 | 654 | 0 |
| 32 | filler | 0.43 | 0.0 | 3184 | 48 | 3136 | 0 |
| 33 | filler | 0.41 | 0.0 | 3228 | 41 | 3187 | 0 |
| 34 | filler | 1.42 | 0.0 | 3270 | 40 | 3230 | 0 |
| 35 | filler | 12.54 | 7.92 | 3166 | 2512 | 654 | 0 |
| 36 | filler | 0.46 | 0.0 | 3214 | 44 | 3170 | 0 |
| 37 | filler | 1.23 | 0.0 | 3259 | 41 | 3218 | 0 |
| 38 | filler | 0.47 | 0.0 | 3324 | 36 | 3288 | 0 |
| 39 | filler | 0.87 | 0.0 | 3365 | 37 | 3328 | 0 |
| 40 | recall | 4.64 | 0.0 | 3190 | 2536 | 654 | 0 |
| 41 | recall | 2.38 | 0.0 | 3235 | 252 | 3192 | 1 |
| 42 | recall | 0.59 | 0.0 | 3538 | 45 | 3493 | 0 |
| 43 | recall | 0.89 | 0.0 | 3587 | 41 | 3546 | 0 |
| 44 | recall | 9.03 | 3.8 | 3479 | 2825 | 654 | 0 |
| 45 | recall | 0.45 | 0.0 | 3525 | 39 | 3486 | 0 |
| 46 | recall | 0.49 | 0.0 | 3571 | 42 | 3529 | 0 |
| 47 | recall | 0.52 | 0.0 | 3618 | 42 | 3576 | 0 |