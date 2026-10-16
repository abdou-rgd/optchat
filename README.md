# OptChat local

An endless chat whose history is its memory: every message is kept on disk, and the model sees a view where recent messages are verbatim and older ones are progressively merged into summary lines arranged as a binary tree, with a `zoom` tool to open any node. Nothing is ever deleted, the view always covers the whole conversation, and the prompt cost stays bounded. This is an independent implementation of the idea for a local `llama.cpp` model on one 12 GB card, written in October 2026 as the memory of [Apothicaire](https://github.com/abdou-rgd/apothicaire), the local DMPK assistant of the Officina project (an open, deterministic and verified pharmacokinetic engine, [Caladrius](https://github.com/abdou-rgd/caladrius), with a local assistant that never computes a number itself).

**Attribution.** The design follows the OptChat idea published by Victor Taelin as a gist (an infinite chat compressed into a binary tree of summary lines with zoom). The code here is a new implementation, adapted to `llama.cpp` (KV-cache-aware lazy compaction, a second server slot for the compactor, grammar-constrained summaries); it shares no code with the gist.

**Status.** A prototype with measurements: recall benchmark 8/8 planted facts after 32 turns of filler on Ternary Bonsai 2 27B (`bench.py`, results in `bench_results*.md`), a failed attempt with an 8B compactor (2/8), and notes on hosting the memory in two agent harnesses (`notes/`, `rapport.html`). One file, `optchat.py`, plus `httpx`. The working notes below are in French.

**License.** MIT OR Apache-2.0, at your option (`LICENSE-MIT`, `LICENSE-APACHE`). Model weights are not included and carry their own licences.

---

## Prototype et résultats (notes de travail, 7–8 octobre 2026)

Prototype de l'idée d'OptChat (gist de VictorTaelin : un chat infini dont l'historique est la mémoire, compressé en arbre binaire de résumés) en local sur :

- **Modèle** : Ternary Bonsai 2 27B (PrismML, base Qwen3.8 27B), fichier `Ternary-Bonsai-2-27B-PTQ1_0.gguf` déjà présent dans le dossier modèles de Hermes.
- **Serveur** : le fork PrismML de llama.cpp (`~/mitsuba/llama/llama-server.exe`, build prism b10743, CUDA 13.3). Le llama.cpp standard livré avec Hermes refuse ce format (type ggml 143). Hermes n'avait jamais réussi à faire tourner Bonsai pour cette raison.
- **GPU** : RTX 3060 12 Go. Serveur à 2 slots de 12k tokens, cache KV q8 : 7,3 Go de VRAM (mesuré sur serveur seul).

Tout le travail a été fait le 7 octobre 2026 au soir. Notes détaillées dans `notes/` (Pi Durable, dsh, spikes) et résultats des bancs dans `bench_results_v*.md`.

## Lancer

```bash
bash start_servers.sh          # démarre llama-server sur http://127.0.0.1:18435 (attendre ~15 s)
python optchat.py chat         # chat interactif, mémoire dans data/
```

Autres commandes : `say "message"` (un tour), `view` (digest + messages bruts de la vue), `stats`, `reset` (efface `data/`, refuse si un chat tourne). Variables : `OPTCHAT_URL`, `OPTCHAT_DATA`, `OPTCHAT_COMPACT_URL` (second serveur pour la compaction).

Banc d'essai de rappel (plante 8 faits, 32 tours de remplissage, 8 questions ; utilise `data_bench/`, jamais `data/`) :

```bash
python bench.py 2 16
```

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

Vue à ~80 messages : 4 à 10 messages bruts + ~28 lignes de résumé ≈ 5,5 Ko ≈ 1,5k tokens ; prompt total ≈ 2,9k tokens.

## Intégration dans un harness

Voir `notes/pi-durable.md` et `notes/pi-durable-spike.md` (Pi Durable, Earendil), `notes/dsh-integration.md` et `notes/dsh-spike.md` (DeepSeek Harness), et le rapport `rapport.html` pour le comparatif et la recommandation.

## Banc v5 : Underdog-Saluki-27B (8 octobre 2026)

Même base Qwen3.8-27B que Bonsai 2, compression IQ2-mix de 7,9 Go lisible par le llama.cpp standard. Résultat (`bench_results_v5_saluki.md`) : rappel 8/8, 48 tours en 3,9 min, tour en cache ~1,2 s, tour avec promotion ~5 s, génération ~21 tok/s (Bonsai : ~24), 10,0 Go de VRAM occupés (Bonsai : 7,3). Verdict : remplacement valable, surtout si l'on veut se passer du fork PrismML ; Bonsai reste le défaut pour la marge de VRAM. Fichier : `models/Underdog-Saluki-27B-1.0-IQ2-mix.gguf`.

## Banc v6 : Bonsai 2 9B et 4B (Q2_0) sur llama.cpp upstream b11700 (17 octobre 2026)

Même banc de rappel, trois exécutions par modèle, serveur upstream (`llama-server` build 11700, CUDA 12.4, aucun fork), `-c 24576 -np 2 -ngl 99 --jinja -fa on -ctk q8_0 -ctv q8_0`. Fichiers `bench_results_v6_*.md`.

| modèle | fichier | VRAM serveur | génération | rappel (3 runs) | durée d'un run | 27B (v4, fork) |
|---|---|---|---|---|---|---|
| 9B | `Ternary-Bonsai-2-9B-Q2_0.gguf` (2,56 Go) | ≈ 2,95 Go | 77–80 tok/s | 7/8, 7/8, 8/8 | ≈ 1 min | 8/8, ≈ 4–5 min, 7,3 Go |
| 4B | `Ternary-Bonsai-2-4B-Q2_0.gguf` (1,21 Go) | ≈ 1,9 Go | 104–108 tok/s | 8/8, 5/8, 7/8 | < 1 min | |

Les échecs sont des « je ne trouve pas » sur des faits plantés (nom + date, port SSH), donc des pertes à la compaction, comme pour l'ancien 8B mais bien moins fréquentes. Le 27B reste la référence pour la mémoire ; le 9B est un compromis plausible, le 4B un compacteur candidat à tester seul sur le slot 1.
