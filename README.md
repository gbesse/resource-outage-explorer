# Resource Outage Explorer

[English](README.en.md) · [Español](README.es.md)

**Acheter plus de capacité ne répare pas toujours le point de panne commun. Ce laboratoire montre pourquoi.**

Il alloue des ressources partagées, explore toutes les combinaisons de pannes autorisées par un petit catalogue, puis compare les renforts fournis. Chaque allocation est accompagnée d’un certificat flux/coupe contrôlé indépendamment. Le scénario est un exercice synthétique ; aucune ressource réelle n’est envoyée.

## Essayer

Python 3.11 ou supérieur ; bibliothèque standard, sans clé.

```sh
python3 -m outage_explorer serve --lang fr
```

Ouvrir `http://127.0.0.1:8770/?lang=fr`. Huit unités sont couvertes au départ. La perte du dépôt partagé laisse deux unités disponibles et **six non couvertes**. Ajouter quatre unités au moyen principal ou placer un secours dans le même dépôt ne change pas ce pire cas. Un secours indépendant de trois unités réduit le manque maximal à **trois** dans ce catalogue.

```sh
python3 -m outage_explorer demo > analyse.json
python3 -m outage_explorer analyze outage_explorer/examples/shared-depot.json
python3 -m outage_explorer verify scenario.json certificat.json
```

`pip install .` fournit aussi `outage-explorer`. Interface et messages CLI FR/EN/ES.

## Ce qui est démontré

Le modèle est biparti : une ressource dispose d’une capacité entière et d’une liste explicite de besoins qu’elle sait servir. Chaque besoin demande un nombre entier d’unités interchangeables. Les ressources incompatibles ne sont jamais substituées simplement parce qu’une capacité totale existe.

Un calcul de flot maximal produit l’allocation ; un second vérificateur contrôle directement capacités, compatibilités et besoins, puis recalcule la capacité d’une coupe. **Allocation faisable = capacité de coupe** démontre que le débit est maximal dans ce modèle. Il ne peut donc pas masquer une meilleure répartition possible sous les mêmes hypothèses. Les empreintes relient chaque certificat à son scénario.

Les pannes peuvent supprimer plusieurs ressources à la fois. La recherche énumère tous les sous-ensembles dont le coût déclaré respecte le budget, jusqu’à trois points. Le résultat distingue le pire cas, toutes les combinaisons et les ensembles minimaux d’événements causant un manque. **Le nombre de scénarios n’est pas une probabilité de panne.**

Les renforts peuvent augmenter une capacité ou ajouter un moyen avec ses expositions explicites aux pannes existantes. Le choix est le meilleur **renfort unique du catalogue fourni**, dans le budget, et non une optimisation universelle de toutes les configurations d’infrastructure.

## Existant, utilité et limites

[NetworkX fournit déjà les algorithmes de flot/coupe](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.minimum_cut.html). Ce dépôt n’invente pas le théorème : il réunit **panne commune → manque prouvé → renfort trompeur → alternative comparée** dans une démo autonome et vérifiable. L’axe d’exercice partagé prolonge notre PICS Stress Lab ; le [CNIG travaille sur les données PCS/PICS](https://cnig.gouv.fr/gt-plans-communaux-et-intercommunaux-de-sauvegarde-a30138.html), sans que ce prototype soit un outil officiel.

Les unités sont des créneaux d’exercice comparables, pas des personnes, kW ou véhicules convertis implicitement. Pas de déplacement, durée, compétence cachée, priorité, probabilité ou disponibilité réelle modélisée. Aucun secours n’est piloté, contacté, réservé ou dispatché. Les résultats ne garantissent pas la continuité d’un service réel.

Limites : quatorze ressources, douze besoins, douze événements, dix renforts et budget de panne jusqu’à trois points. L’exhaustivité concerne uniquement ce catalogue borné. Une panne omise ou une exposition mal déclarée reste absente du modèle. Aucune supériorité SOTA ou efficacité opérationnelle terrain n’est revendiquée.

## Vérifier

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Douze tests couvrent pannes communes, renforts, budgets, coupes, certificats falsifiés, contraintes d’éligibilité et comparaison à une énumération exhaustive des allocations sur vingt petits réseaux. Navigateur FR/EN/ES, exports et mobile ; CI Python 3.11/3.12 et roue hors sources. Licence MIT ; alpha d’exercice et de recherche.
