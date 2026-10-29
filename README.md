# OptChat local

An endless chat whose history is its memory: every message is kept on disk, and the model sees a view where recent messages are verbatim and older ones are progressively merged into summary lines arranged as a binary tree, with a `zoom` tool to open any node. Nothing is ever deleted, the view always covers the whole conversation, and the prompt cost stays bounded. This is an independent implementation of the idea for a local `llama.cpp` model on one 12 GB card, written in October 2026 as the memory of [Apothicaire](https://github.com/abdou-rgd/apothicaire), the local DMPK assistant of the Officina project (an open, deterministic and verified pharmacokinetic engine, [Caladrius](https://github.com/abdou-rgd/caladrius), with a local assistant that never computes a number itself).

**Attribution.** The design follows the OptChat idea published by Victor Taelin as a gist (an infinite chat compressed into a binary tree of summary lines with zoom). The code here is a new implementation, adapted to `llama.cpp` (KV-cache-aware lazy compaction, a second server slot for the compactor, grammar-constrained summaries); it shares no code with the gist.

**Status.** A prototype with measurements: recall benchmark (8 planted facts, 32 turns of filler, 8 questions) on Ternary Bonsai 2 27B Q2_0 on upstream llama.cpp b11700: 8/8, 7/8, 8/8 over three runs (bench v7), 7/8, 8/8, 8/8 over three runs with the memory fixes of 2026-10-20 (bench v9) (`bench.py`, results in `bench_results*.md`), a failed attempt with an 8B compactor (2/8), and notes on hosting the memory in two agent harnesses (`notes/`, `rapport.html`). One file, `optchat.py`, plus `httpx`. The working notes below are in French.

**License.** MIT OR Apache-2.0, at your option (`LICENSE-MIT`, `LICENSE-APACHE`). Model weights are not included and carry their own licences.

## Run

OptChat needs Python 3.12 with `httpx`, and a `llama-server` from upstream [llama.cpp](https://github.com/ggml-org/llama.cpp) (build b11700, no fork) serving Ternary Bonsai 2 27B in the Q2_0 packing. The file is `Ternary-Bonsai-2-27B-Q2_0-prism-fork-required.gguf`: despite its name, upstream llama.cpp has read it since b11555.

```bash
pip install httpx
bash start_servers_upstream.sh   # llama-server on http://127.0.0.1:18435, 2 slots of 12k tokens (wait ~15 s)
curl http://127.0.0.1:18435/health
python optchat.py chat           # interactive chat, memory in data/
```

The two paths at the top of `start_servers_upstream.sh` (`LLAMA`, `M27`) point to the author's machine: edit them first. Other commands: `say "message"` (one turn), `view` (digest and raw messages of the view), `stats`, `reset` (erases `data/`, refuses while a chat is running). Environment: `OPTCHAT_URL`, `OPTCHAT_DATA`, `OPTCHAT_COMPACT_URL` (a second server for compaction). On Windows, stop the server with `Stop-Process -Name llama-server -Force` in PowerShell (`taskkill /IM` does nothing under Git Bash).

`start_servers.sh` starts the earlier PrismML fork of llama.cpp with the `PTQ1_0` file. It is kept only to reproduce the measurements made on the fork (benches v1 to v4 below, and the fork runs of the Apothicaire benchmark); do not use it for new work.

Recall benchmark (plants 8 facts, 32 turns of filler, 8 questions; uses `data_bench/`, never `data/`):

```bash
python bench.py 2 16
```

Tests need no model server (a fake model stands in for `llama-server`) and run in CI on every pull request:

```bash
python -m unittest discover -s tests
```

---

## Prototype et résultats (notes de travail, 7–8 octobre 2026)

Prototype de l'idée d'OptChat (gist de VictorTaelin : un chat infini dont l'historique est la mémoire, compressé en arbre binaire de résumés) en local sur :

- **Modèle** : Ternary Bonsai 2 27B (PrismML, base Qwen3.8 27B), fichier `Ternary-Bonsai-2-27B-PTQ1_0.gguf` déjà présent dans le dossier modèles de Hermes.
- **Serveur** : le fork PrismML de llama.cpp (`~/mitsuba/llama/llama-server.exe`, build prism b10743, CUDA 13.3). Le llama.cpp standard livré avec Hermes refuse ce format (type ggml 143). Hermes n'avait jamais réussi à faire tourner Bonsai pour cette raison.
- **GPU** : RTX 3060 12 Go. Serveur à 2 slots de 12k tokens, cache KV q8 : 7,3 Go de VRAM (mesuré sur serveur seul).

Tout le travail a été fait le 7 octobre 2026 au soir. Notes détaillées dans `notes/` (Pi Durable, dsh, spikes) et résultats des bancs dans `bench_results_v*.md`.

## Fonctionnement

- `log.jsonl` : chaque message (user, assistant, appels d'outils, résultats) en clair, append-only, fsync. Rien n'est jamais perdu.
- `tree.jsonl` : nœuds de résumé, immuables. L0 = un message → une ligne (≤ 512 octets). L(k+1) = fusion de deux lignes L(k) adjacentes.
- `view.json` : la vue, liste ordonnée couvrant tout le chat. À gauche les nœuds les plus grossiers, à droite les messages bruts. Les niveaux décroissent de gauche à droite.
- Chaque tour = un appel modèle neuf : `[system]` + `[digest <memory> en tour utilisateur]` + messages bruts récents + nouveau message.
- Outils : `zoom(id)` ouvre un nœud sur ses deux enfants (ou sur le message original pour un L0) ; `read_message(n)` lit un message complet.
- Compaction après chaque tour, dans un thread de fond (cachée derrière le temps de réflexion de l'utilisateur), sur le **slot 1** du serveur pour ne jamais évincer le cache KV du chat.

### Choix imposés par le local, et ce qu'on a appris

1. **Compaction paresseuse et par lots** (hystérésis : zone brute 12 → 4 messages, zones de résumé 12 → 8). Chaque modification de la vue invalide le cache KV à partir de ce point ; le faire par lots divise la fréquence.
2. **Le préfixe statique reste en cache** : le digest est un tour utilisateur séparé, pas une partie du prompt système. Système + définitions d'outils (654 tokens) ne sont jamais recalculés.
3. **Contrainte du modèle hybride** (vérifié sur serveur neuf dans trois configurations : flags de base, sans `--cache-reuse`, avec checkpoints rapprochés `--ctx-checkpoints 64 --checkpoint-min-step 256` ; résultats identiques, voir `run/flag_experiment.log`) : Qwen3.8 a des couches récurrentes (SSM). Quand un prompt diverge *à l'intérieur* de la séquence en cache, le serveur recule bien avant le point de divergence : 512 tokens en arrière si la divergence est en fin de prompt, jusqu'au préfixe système si elle est au milieu. Un simple ajout en fin de prompt coûte ~40 tokens ; une modification du digest coûte 1 500 à 2 500 tokens de recalcul (4 à 5 s). D'où l'hystérésis. Les essais avec KV f16 et `-ub 128` faits plus tôt dans la soirée ne sont pas valables (l'ancien serveur avait gardé le port, voir leçon 10) et n'ont pas été refaits.
4. **Messages courts gardés verbatim** (≤ 160 caractères) : ligne L0 exacte sans appel modèle. Sur le banc v4, 88 lignes L0 sur 90 n'ont rien coûté.
5. **Sortie du compacteur contrainte par schéma JSON** (grammaire llama.cpp) : nombre de lignes exact garanti, plus de parsing fragile.
6. **Le Bonsai 8B comme compacteur est un échec** (banc v3 : rappel 2/8). Il recopie au lieu de résumer et perd des faits entiers à chaque fusion. Le 27B reste nécessaire pour la compaction. Le fichier 8B reste dans `models/` (variante PQ2_0 ; la variante Q2_0 du dépôt ne se charge pas sur ce build).
7. **Le coût de la compaction, c'est la génération** : ~5 000 tokens de résumés par 48 tours à 24 tok/s ≈ 190 s de GPU. Regrouper les appels n'y change rien. Pistes : lignes plus courtes, ou un petit modèle *instruct* non ternaire (Qwen3-4B Q4) à tester.
8. **Un 27B zoome peu** : quand les résumés gardent les valeurs exactes, il répond sans zoomer (7 fois sur 8). Quand ils sont mauvais (v3), il lit les messages un par un et épuise les tours d'outils. D'où la règle : le dernier tour d'outils autorisé se fait sans outils, le modèle doit répondre.
9. **Robustesse** (revue de code par un sous-agent, 15 constats corrigés) : réparation au démarrage (ligne tronquée, messages non couverts par la vue), verrou avec détection de PID mort, `os.replace` avec reprise sous Windows, coupure de la zone brute sur une frontière de tour utilisateur, gestion des erreurs HTTP du compacteur, budget en caractères par lot.
10. **Piège Windows / Git Bash** : `taskkill /IM llama-server.exe` ne fait rien sous Git Bash (le `/IM` est converti en chemin). Pendant une bonne partie de la soirée, chaque « redémarrage » du serveur en a ajouté un (neuf processus trouvés à la fin), et l'ancien gardait le port. Les mesures de VRAM prises entre 22h30 et 23h30 sont donc gonflées, et les temps du banc v4 sont bruités. Utiliser `Stop-Process -Name llama-server -Force` en PowerShell.

## Résultats des bancs (Bonsai 2 27B, RTX 3060)

| banc | compacteur | rappel | tour en cache | tour avec promotion | remarques |
|---|---|---|---|---|---|
| v1 | 27B slot 1 | 8/8 | ~1,0 s | ~4,5 s | résumés en anglais, rôles confondus |
| v2 | 27B slot 1, prompt corrigé | 8/8 | ~1,1 s | ~4,9 s | résumés français, bonne attribution |
| v3 | Bonsai 8B (2e serveur) | **2/8** | ~1 s | — | fusions qui perdent des faits, boucles d'outils |
| v4 | 27B slot 1 + verbatim + corrections | 8/8 | ~1,5 s* | ~8 s* | 88/90 lignes L0 gratuites ; *GPU partagé avec le spike Pi Durable pendant le banc |

Un seul run par banc (v1 à v4).

Vue à ~80 messages : 4 à 10 messages bruts + ~28 lignes de résumé ≈ 5,5 Ko ≈ 1,5k tokens ; prompt total ≈ 2,9k tokens.

## Intégration dans un harness

Voir `notes/pi-durable.md` et `notes/pi-durable-spike.md` (Pi Durable, Earendil), `notes/dsh-integration.md` et `notes/dsh-spike.md` (DeepSeek Harness), et le rapport `rapport.html` pour le comparatif et la recommandation.

## Banc v5 : Underdog-Saluki-27B (8 octobre 2026)

Même base Qwen3.8-27B que Bonsai 2, compression IQ2-mix de 7,9 Go lisible par le llama.cpp standard. Résultat (`bench_results_v5_saluki.md`) : rappel 8/8 (un run), 48 tours en 3,9 min, tour en cache ~1,2 s, tour avec promotion ~5 s, génération ~21 tok/s (Bonsai : ~24), 10,0 Go de VRAM occupés (Bonsai : 7,3). Verdict : remplacement valable, surtout si l'on veut se passer du fork PrismML ; Bonsai reste le défaut pour la marge de VRAM. Fichier : `models/Underdog-Saluki-27B-1.0-IQ2-mix.gguf`.

## Banc v6 : Bonsai 2 9B et 4B (Q2_0) sur llama.cpp upstream b11700 (17 octobre 2026)

Même banc de rappel, trois exécutions par modèle, serveur upstream (`llama-server` build 11700, CUDA 12.4, aucun fork), `-c 24576 -np 2 -ngl 99 --jinja -fa on -ctk q8_0 -ctv q8_0`. Fichiers `bench_results_v6_*.md`.

| modèle | fichier | VRAM serveur | génération | rappel (3 runs) | durée d'un run | 27B (v4, fork) |
|---|---|---|---|---|---|---|
| 9B | `Ternary-Bonsai-2-9B-Q2_0.gguf` (2,56 Go) | ≈ 2,95 Go | 77–80 tok/s | 7/8, 7/8, 8/8 | ≈ 1 min | 8/8, ≈ 4–5 min, 7,3 Go |
| 4B | `Ternary-Bonsai-2-4B-Q2_0.gguf` (1,21 Go) | ≈ 1,9 Go | 104–108 tok/s | 8/8, 5/8, 7/8 | < 1 min | |

Les échecs sont des « je ne trouve pas » sur des faits plantés (nom + date, port SSH), donc des pertes à la compaction, comme pour l'ancien 8B mais bien moins fréquentes. Le 27B reste la référence pour la mémoire ; le 9B est un compromis plausible, le 4B un compacteur candidat à tester seul sur le slot 1.

## Banc v7 : Bonsai 2 27B (Q2_0) sur llama.cpp upstream b11700 (17 octobre 2026)

Même banc, même serveur upstream que v6, fichier `Ternary-Bonsai-2-27B-Q2_0-prism-fork-required.gguf` (7,63 Go ; malgré son nom et le README du dépôt HF, il tourne sur le llama.cpp standard depuis b11555). Fichiers `bench_results_v7_*.md`.

| modèle | VRAM serveur | génération | rappel (3 runs) | 27B PTQ1_0 (v4, fork) |
|---|---|---|---|---|
| 27B Q2_0, upstream | ≈ 8,4 Go | ≈ 31 tok/s | 8/8, 7/8, 8/8 | 8/8, ≈ 24 tok/s, 7,3 Go |

Le 7/8 du run 2 est une boucle d'appels d'outils sur une question, pas une perte à la compaction. Conclusion : le fork PrismML n'est plus nécessaire pour le 27B ; il garde 1 Go de VRAM d'avance (7,3 contre ≈ 8,4 Go), mais le choix est fait au banc v8 ci-dessous : llama.cpp standard.

## Banc v8 : 27B Q2_0 upstream, banc complet d'Apothicaire (17 octobre 2026)

Le banc de 25 exercices d'Apothicaire (porte v1 ; 25 exercices × 8 tours = 200 tours) sur le serveur upstream b11700 : 193/200 tours corrects, 0/897 nombres non retrouvés dans un résultat d'outil ou un message de l'utilisateur (nombres vérifiés par la porte, brouillons comme réponses montrées), 141/141 appels d'outils valides, 8,0 s par tour en moyenne (fork PTQ1_0, run du 2026-10-09b : 195/200, 0/926, 160/160, 10,4 s). Un run chacun, un échantillonnage ; chiffres de développement, in-sample (exercices, formulations et règles de score écrits en même temps que la porte qu'ils mesurent) : des comptes, pas des taux avec intervalle. Décision : la démo du 17 novembre tourne sur llama.cpp standard (upstream b11700, Q2_0), script `start_servers_upstream.sh` ; le jeu gelé d'Apothicaire est prévu sur ce même serveur (`bench/FROZEN_SET.md` du dépôt Apothicaire). Le fork (`start_servers.sh`, fichier `PTQ1_0`) ne sert plus qu'à reproduire les anciennes mesures (bancs v1 à v4 et runs d'Apothicaire sur le fork, du 8 au 18 octobre).

## Banc v9 : 27B Q2_0 upstream, garde en octets, jointures sans modèle, coupes propres (21 octobre 2026)

Les trois correctifs de mémoire du 20 octobre (cartes T-094 à T-096, PR #1 fusionnée le 21 octobre) : garde en octets sur le digest et la zone brute avec fusions de niveaux forcées (`view_max_bytes` 18 000, `digest_max_bytes` 12 000) ; fusion sans modèle de deux lignes courtes, messages gardés verbatim jusqu'à 512 octets (au lieu de 160 caractères) ; coupe des lignes de résumé à une limite de mot, jamais dans un caractère UTF-8, et tête + queue des longs messages pour le compacteur. Même banc de rappel, même serveur upstream b11700 et même fichier Q2_0 que v7, trois exécutions (`bench_results_v9_27b_fixes_run1..3.md`, commit `6776a61`).

| | rappel (3 runs) | durée d'un run | appels au compacteur | jointures sans modèle | fusions forcées par la garde |
|---|---|---|---|---|---|
| v9, avec les correctifs | 7/8, 8/8, 8/8 | 1,9 / 1,4 / 2,4 min | 5 / 3 / 9 | 56 / 54 / 72 | 0 / 0 / 0 |
| v7, avant | 8/8, 7/8, 8/8 | 5,3 / 4,5 / 2,9 min | 30 / 27 / 17 | | |

Le 7/8 du run 1 est une perte : à la question du port SSH, après un zoom, le modèle répond ne pas avoir l'information (le 7/8 de v7 est une boucle d'appels d'outils). 23 réponses justes sur 24 des deux côtés (trois runs de 8 questions, un seul jeu de runs de chaque version) : pas de régression mesurée, pas d'amélioration du rappel ; le coût de la compaction (appels au compacteur, durée du run) baisse. La garde en octets ne s'est pas déclenchée dans ces runs de 48 tours (0 fusion forcée) : elle est testée sans modèle (`tests/test_memory.py`), pas par ce banc.
