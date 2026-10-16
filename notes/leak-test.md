# Test de « fuite » entre conversations via le cache KV (7 oct. 2026, ~23h20)

Contexte : l'agent de recherche dsh a signalé que, dans 2 de ses 3 exécutions agentiques, le raisonnement de Bonsai citait des phrases du chat OptChat (« [#22] … cache KV ») absentes de sa requête, et a supposé une réutilisation de cache entre slots du llama-server partagé.

Deux tests directs faits depuis la session principale, sur le serveur partagé (27B, 2 slots), juste après le banc v4 et pendant les spikes :

1. **Sans aucun contexte** : système « Tu es un assistant utile. Réponds brièvement. », puis 4 questions dont les réponses existaient dans les conversations du banc (port SSH 2222, chat Pixel, couleur #3FA7D6, budget 650), chaque question sur le slot 0 puis sur le slot 1 (8 requêtes), plus une avec le thinking activé. **Résultat : 8 fois « inconnu »**, raisonnement « We don't know ».
2. **Avec le même préfixe que le banc** (prompt système OptChat + définitions des outils, préfixe de 654 tokens identique aux conversations du banc), mêmes 3 questions sur les deux slots, sans digest. **Résultat : le modèle tente `zoom("n1")` à chaque fois** (comportement attendu avec ce prompt), aucun fait restitué ; avec thinking, il dit chercher dans le digest et ne trouve rien.

Conclusion : non reproduit. Aucune fuite observée. L'observation de l'agent dsh reste inexpliquée (hypothèses : contenu présent dans sa propre requête, ou lecture erronée) et est consignée comme non confirmée.
