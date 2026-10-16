# Résumé de la session du 7 octobre 2026 (soir)

Contexte : Abdou a demandé un avis sur le gist OptChat de VictorTaelin (chat infini dont l'historique est la mémoire, compressé en arbre binaire de résumés avec zoom) pour une IA locale avec Ternary Bonsai 27B et DeepSeek Harness (dsh), puis a dit « occupe-toi en », a autorisé toute action, et a demandé en fin de nuit : un test de Pi Durable en plus, un comparatif dsh vs Pi Durable (lequel est le plus utile et le plus puissant pour faire de l'IA en local), un rapport HTML détaillé et illustré écrit par Opus, puis l'extinction du PC.

## Chronologie

1. **Avis initial** : OptChat colle bien au local parce qu'il garde un préfixe de prompt stable (cache KV), n'a pas besoin de base vectorielle, et décrit les sorties d'outils au lieu de les copier. Réserves : le cache KV d'un 27B ternaire a la taille d'un 27B normal ; le « modèle pas cher » de compaction suppose un second modèle ; un 27B zoome peu de lui-même.
2. **Inventaire de la machine** : RTX 3060 12 Go ; Hermes (Nous Research) installé avec un llama.cpp standard b10964 et le GGUF Bonsai 2 27B PTQ1_0 ; dsh 0.1.7-rc.2 (desktop + cache npx) ; un fork PrismML de llama.cpp (prism b10743 CUDA) dans `~/mitsuba/llama`, seul capable de charger les formats PTQ1_0/PQ2_0 (types ggml 142/143). Hermes avait échoué sur Bonsai les 2 et 3 octobre pour cette raison.
3. **Prototype Python** `optchat.py` (log append-only, arbre, vue avec hystérésis, outils zoom/read_message, client llama.cpp avec slot dédié à la compaction, thread de fond) + `bench.py` (8 faits plantés, remplissage, 8 questions de rappel).
4. **Banc v1** : rappel 8/8 mais résumés en anglais, rôles utilisateur/assistant confondus, balises recopiées. **Banc v2** après correction des prompts : 8/8, résumés propres.
5. **Enquête cache KV** : avec ce modèle hybride (SSM + attention), une divergence à l'intérieur du prompt force un recalcul depuis bien avant (512 tokens en arrière si la divergence est en fin de prompt, jusqu'au préfixe système si elle est au milieu). Vérifié proprement en fin de soirée sur serveur neuf dans trois configurations (base, sans cache-reuse, checkpoints rapprochés : identiques, `run/flag_experiment.log`). Les essais f16 et `-ub 128` du milieu de soirée sont invalides : les `taskkill` sous Git Bash ne tuaient rien, l'ancien serveur gardait le port (neuf processus llama-server trouvés à la fin). Conséquence pour OptChat : les modifications du digest doivent être rares (hystérésis), et le préfixe système + outils (654 tokens) a été isolé pour rester en cache.
6. **Revue de code par un sous-agent Opus** : 15 constats (compaction sans gestion d'erreurs, pas de réparation après crash, `os.replace` sous Windows, le banc qui effaçait les données du vrai chat, coupure de la zone brute entre un appel d'outil et son résultat, parsing fragile des sorties par lots, verrou périmé…). Tous corrigés, dont sortie du compacteur contrainte par schéma JSON.
7. **Second modèle de compaction** : téléchargement de Ternary Bonsai 8B (la variante Q2_0 ne se charge pas sur ce build, la PQ2_0 oui). **Banc v3** : rappel 2/8, le 8B recopie et perd des faits à chaque fusion. Abandonné ; le 27B reste compacteur.
8. **Banc v4** (27B compacteur, lignes verbatim pour les messages courts, réponse forcée sans outils au dernier tour) : rappel 8/8, 88 lignes L0 sur 90 sans appel modèle, 16 appels de compaction pour 48 tours. Le coût de la compaction est la génération des fusions (~5 000 tokens à 24 tok/s ≈ 190 s de GPU par 48 tours), cachée derrière le temps de réflexion de l'utilisateur en usage réel.
9. **Recherche Pi Durable** (sous-agent Sonnet, lecture du code source) puis **spike pratique** (sous-agent Opus, installation réelle et test contre Bonsai) : voir `pi-durable.md` et `pi-durable-spike.md`.
10. **Recherche et spike dsh** (sous-agents) : voir `dsh-integration.md` (si présent) et `dsh-spike.md`.

## Chiffres clés

- VRAM : 27B + 2 slots de 12k + KV q8 = 7,3 Go (mesure propre, serveur seul). Les valeurs 8,6 / 11,9 / 12,0 Go notées plus tôt incluaient des serveurs fantômes et ne sont pas fiables.
- 27B : prefill ~300 tok/s (court) à ~600 tok/s (long), génération ~24 tok/s. 8B : génération ~106 tok/s.
- Tour en cache : ~1 s. Tour avec promotion (digest modifié) : 4,5 à 5 s. Prompt total à 80 messages : ~2,9k tokens dont digest ~1,5k.
- Appel d'outil (zoom) fonctionne via `--jinja` ; `enable_thinking=false` respecté.

## Fichiers

- `optchat.py`, `bench.py`, `start_servers.sh`, `README.md`
- `bench_results_v1.md`, `_v2.md`, `_v3_8b.md`, `_v4.md` ; `run/bench*.log`, `run/data_v2/` (données brutes du banc v2), `data_bench/` (banc v4)
- `run/probe_cache.py` (sonde du cache KV), `run/compare_compactor.py`
- `models/Ternary-Bonsai-8B-PQ2_0.gguf`
- `notes/` : recherches et spikes ; `pi-spike/`, `dsh-spike/` : code des spikes
