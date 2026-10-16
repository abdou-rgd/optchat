# OptChat local bench (Bonsai 2 27B PTQ1_0, RTX 3060 12GB)

Turns: 48  |  total wall: 6.0 min  |  compactor: http://127.0.0.1:18436  |  compaction stats: {'summaries': 85, 'merges': 137, 'verbatim': 92, 'calls': 33, 'errors': 0, 'seconds': 100.64135813713074}

## Recall: 2/8

| question | expected | ok | zooms | rounds | s | answer |
|---|---|---|---|---|---|---|
| Comment s'appelle mon chat ? | `\bpixel\b` | OK | 0 | 1 | 0.68 | Pixel |
| Quel est le port SSH du serveur de prod d'Atlas ? | `\b2222\b` | MISS | 1 | 2 | 4.8 | Je n'ai pas d'information sur le port SSH du serveur de prod d'Atlas dans ma mémoire. |
| Quelle base de données ai-je choisie pour Atlas, et pourquoi ? | `postgre` | MISS | 1 | 6 | 46.98 | (stopped: too many tool rounds) |
| Qui reprend le module de facturation, et quand ? | `marchetti.*15|15.*marchetti` | MISS | 0 | 6 | 31.71 | (stopped: too many tool rounds) |
| Dans quel fichier se trouve ATLAS_BUILD_KEY ? | `\.env\.ci` | OK | 2 | 4 | 59.67 | Le token de build `ATLAS_BUILD_KEY` se trouve dans le fichier `.env.ci` (pas dans `.env`). |
| Quel est mon budget max pour le GPU ? | `(?<!\d)650(?!\d)` | MISS | 4 | 6 | 37.29 | (stopped: too many tool rounds) |
| À quelle heure est mon rendez-vous chez le dentiste ? | `(?<!\d)0?9\s*[h:]\s*15(?!\d)` | MISS | 1 | 6 | 17.27 | (stopped: too many tool rounds) |
| Quelle est la couleur d'embed du bot Discord ? | `3fa7d6` | MISS | 0 | 6 | 26.56 | (stopped: too many tool rounds) |

## Per-turn cost

| # | tag | wall s | wait compaction s | prompt tok | uncached tok | cached tok | zooms |
|---|---|---|---|---|---|---|---|
| 0 | fact | 1.63 | 0.0 | 697 | 43 | 654 | 0 |
| 1 | filler | 1.49 | 0.0 | 751 | 42 | 709 | 0 |
| 2 | filler | 0.54 | 0.0 | 819 | 40 | 779 | 0 |
| 3 | fact | 1.53 | 0.0 | 886 | 64 | 822 | 0 |
| 4 | filler | 0.55 | 0.0 | 962 | 47 | 915 | 0 |
| 5 | filler | 0.5 | 0.0 | 1006 | 41 | 965 | 0 |
| 6 | fact | 0.95 | 0.0 | 1054 | 46 | 1008 | 0 |
| 7 | filler | 3.12 | 0.01 | 1323 | 1142 | 181 | 0 |
| 8 | filler | 0.54 | 0.0 | 1387 | 42 | 1345 | 0 |
| 9 | fact | 1.23 | 0.0 | 1443 | 53 | 1390 | 0 |
| 10 | filler | 0.58 | 0.0 | 1508 | 44 | 1464 | 0 |
| 11 | filler | 1.44 | 0.0 | 1553 | 41 | 1512 | 0 |
| 12 | fact | 5.93 | 1.67 | 1535 | 1354 | 181 | 0 |
| 13 | filler | 0.55 | 0.0 | 1601 | 36 | 1565 | 0 |
| 14 | filler | 1.03 | 0.0 | 1641 | 37 | 1604 | 0 |
| 15 | fact | 1.01 | 0.0 | 1702 | 45 | 1657 | 0 |
| 16 | filler | 0.51 | 0.0 | 1756 | 39 | 1717 | 0 |
| 17 | filler | 5.53 | 1.41 | 1748 | 1567 | 181 | 0 |
| 18 | fact | 1.21 | 0.0 | 1828 | 51 | 1777 | 0 |
| 19 | filler | 0.54 | 0.0 | 1888 | 40 | 1848 | 0 |
| 20 | filler | 1.41 | 0.0 | 1929 | 38 | 1891 | 0 |
| 21 | fact | 1.6 | 0.0 | 2013 | 58 | 1955 | 0 |
| 22 | filler | 8.83 | 3.31 | 1881 | 1700 | 181 | 0 |
| 23 | filler | 24.73 | 0.0 | 1933 | 1752 | 181 | 0 |
| 24 | filler | 3.2 | 0.0 | 1978 | 42 | 1936 | 0 |
| 25 | filler | 0.86 | 0.0 | 2056 | 38 | 2018 | 0 |
| 26 | filler | 2.26 | 0.0 | 2099 | 40 | 2059 | 0 |
| 27 | filler | 10.71 | 6.45 | 2155 | 1974 | 181 | 0 |
| 28 | filler | 5.94 | 0.0 | 2201 | 42 | 2159 | 0 |
| 29 | filler | 5.86 | 0.0 | 2327 | 44 | 2283 | 0 |
| 30 | filler | 2.39 | 0.0 | 2452 | 43 | 2409 | 0 |
| 31 | filler | 0.84 | 0.0 | 2521 | 41 | 2480 | 0 |
| 32 | filler | 12.32 | 8.03 | 2198 | 2017 | 181 | 0 |
| 33 | filler | 0.78 | 0.0 | 2242 | 41 | 2201 | 0 |
| 34 | filler | 2.22 | 0.0 | 2284 | 40 | 2244 | 0 |
| 35 | filler | 0.84 | 0.0 | 2348 | 42 | 2306 | 0 |
| 36 | filler | 0.77 | 0.0 | 2395 | 44 | 2351 | 0 |
| 37 | filler | 14.23 | 8.14 | 2362 | 2181 | 181 | 0 |
| 38 | filler | 0.91 | 0.0 | 2425 | 36 | 2389 | 0 |
| 39 | filler | 1.72 | 0.0 | 2466 | 37 | 2429 | 0 |
| 40 | recall | 0.68 | 0.0 | 2520 | 37 | 2483 | 0 |
| 41 | recall | 4.8 | 0.0 | 2564 | 170 | 2521 | 1 |
| 42 | recall | 46.98 | 12.77 | 2654 | 3126 | 181 | 1 |
| 43 | recall | 31.71 | 0.77 | 4013 | 4640 | 181 | 0 |
| 44 | recall | 59.67 | 14.5 | 4074 | 8124 | 181 | 2 |
| 45 | recall | 37.29 | 22.86 | 3367 | 3619 | 181 | 4 |
| 46 | recall | 17.27 | 2.57 | 3873 | 4041 | 181 | 1 |
| 47 | recall | 26.56 | 11.64 | 3702 | 3894 | 181 | 0 |