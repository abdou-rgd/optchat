# Comparatif : DeepSeek Harness (dsh) vs Pi Durable, pour de l'IA en local

Question posée par Abdou : lequel des deux sera le plus utile et le plus puissant pour faire de l'IA en local (RTX 3060 12 Go, Bonsai 2 27B, mémoire OptChat) ?

Sources : `dsh-integration.md` (recherche + exécutions réelles), `dsh-spike.md` (13 exécutions headless contre Bonsai), `pi-durable.md` (lecture du code source), `pi-durable-spike.md` (installation et test réels).

## Ce que sont les deux

- **dsh** est un *produit* : agent de codage complet (24 outils, sandbox Windows, persona, sessions, compaction, sous-agents, workflows, MCP, app desktop et web), construit comme une composition de ~300 plugins. Version candidate (0.1.7-rc.2 en npx, 0.2.0-rc.2 dans l'app desktop).
- **Pi Durable** est une *bibliothèque* : un harness d'exécution durable (chaque étape est une tâche checkpointée, reprise après crash, plusieurs clients sur une même conversation), sans interface, avec un environnement d'outils Node. Version 1.0.4, annoncée expérimentale, en TypeScript.

## Tableau

| critère | dsh | Pi Durable |
|---|---|---|
| Tourne avec Bonsai local | **Oui, vérifié** : 13 exécutions headless, outils fichiers/shell/lecture parallèle, plugin `zoom` appelé par le modèle | **Oui, vérifié** : installation Windows en 27 s, provider OpenAI-compatible avec clé factice, 7 appels `zoom` en streaming sur 7 bien parsés, tours de 1 à 5 s (10 s quand le digest change) |
| Reprise après crash | Non testée (reprise de session par id seulement) | **Vérifiée** : process tué pendant la génération → requête renvoyée à l'identique au redémarrage, 4 tokens recalculés, pas de doublon ; tué pendant un `zoom` → outil rejoué (`replay: "safe"`), tour terminé |
| Mémoire OptChat en pratique | Outil `zoom` chargé en plugin (45 lignes) ; la vue devrait passer par un backend de compaction | **Hook `beforeRequest` + digest + zoom = 200 lignes de code produit**, réponses justes (2222, PostgreSQL) ; compacteur de fond sur le 8B fonctionnel en bonus |
| Prêt à l'emploi | **Oui** : agent de codage utilisable ce soir, UI desktop | Non : il faut écrire l'agent (prompt, outils, boucle) |
| Coût en tokens du harness | **Lourd** : 5,8k tokens d'enveloppe (24 outils + persona) sur une fenêtre de 12k ; 2,8k avec un preset allégé | Minimal : seulement ce qu'on y met |
| Mémoire OptChat (réécriture du contexte à chaque requête) | **Pas de point d'accroche direct** : seulement un backend de compaction (un message résumé remplace une tranche, doit être plus petit, s'exécute dans le tour). OptChat approximatif, hystérésis à reconstruire | **Point d'accroche exact** : hook `beforeRequest` qui reçoit toute la liste de messages et la remplace ; tâches de fond ; stockage JSONL append-only |
| Compaction native | Fonctionne, mais bloque le tour 10-30 s et évince une partie du cache KV ; seuil par défaut inadapté à 12k | Tâche de fond, posée au tour suivant ; à désactiver si on fournit sa propre vue |
| Durabilité | Sessions reprises par id ; pas de reprise d'une tâche interrompue | **Reprise après crash** : tâche interrompue rejouée depuis son checkpoint, requêtes exactly-once |
| Extensibilité | Plugins puissants mais contraints : versions épinglées à la version exacte de dsh, import `@deepseek-ai/*` seulement depuis l'arbre du profil, pnpm | Extensions = prompt + outils + hooks + tâches, en TypeScript, API instable |
| Multi-utilisateur / bots | Un process par prompt en headless ; UI mono-utilisateur | Plusieurs clients attachés à une conversation ; pensé pour des bots Slack/GitHub |
| Maturité | RC, deux versions coexistent sur la machine | 1.0.4 expérimental, changements d'API annoncés |
| Effort pour héberger OptChat | 2-4 jours (backend de compaction + outils), résultat approximatif | 0,5-1 jour de spike, 2-4 jours pour un port complet, résultat fidèle |

## Verdict

Les deux ne jouent pas dans la même catégorie, et c'est ça la réponse.

- **Pour coder en local dès maintenant** : dsh. Il marche avec Bonsai, les outils sont là, l'UI est là. Une seule condition : un preset allégé (persona + quelques outils), sinon la moitié de la fenêtre de 12k part dans l'enveloppe et il ne reste presque rien pour le code.
- **Pour construire un assistant personnel à mémoire infinie qui tourne en permanence** (ce que vise OptChat) : Pi Durable. Son hook `beforeRequest` est exactement l'emplacement où OptChat remplace l'historique par le digest, son stockage JSONL est le `log.jsonl` du prototype, ses tâches de fond sont le compacteur, et la reprise après crash est ce qu'on veut d'un agent qui tourne la nuit. Prix à payer : tout écrire soi-même en TypeScript, sur une API encore mouvante.
- **Le plus puissant pour de l'IA en local, au sens « ce que je peux en faire »** : Pi Durable + OptChat, parce que sur une carte de 12 Go la ressource rare est la fenêtre de contexte, et Pi laisse décider de chaque token envoyé au modèle, là où dsh en consomme la moitié avant la première question. dsh reste l'outil de codage à côté.

Recommandation concrète : garder le prototype Python comme référence (rappel 8/8), porter la vue + zoom dans une extension Pi Durable (le spike `pi-spike/optchat-pi.mjs` donne le squelette, 2-3 jours pour un port complet), et utiliser dsh avec un preset allégé pour le code. Réévaluer dsh quand une version stable donnera un point d'accroche par requête ou une compaction non bloquante.

Deux pièges découverts pendant les spikes, valables quel que soit l'hôte :
- **Un seul client par serveur llama.cpp** : une requête épinglée sur un slot (`id_slot`) prend la place d'une requête non épinglée en cours, qui se termine tronquée mais marquée « stop ». Donner un port dédié à chaque application.
- **Ancrer la coupure des messages bruts sur le message utilisateur du tour courant**, sinon chaque appel d'outil change le préfixe et recalcule ~2,7k tokens.
