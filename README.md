# Protocole HORIZON

**Une date où le sceau doit être ressellé.**

HORIZON nomme l'hypothèse cryptographique d'un acte et le jour de calendrier où elle cesse de suffire. La menace utile 2026, c'est *harvest-now-decrypt-later*, pas un QPU de poche.

Ce dépôt est la version 0. Il tient dans un téléphone. Zéro token. Zéro serveur payant.

**Ouvert (MIT).** Le protocole reste public. Voir [COPYRIGHT.md](COPYRIGHT.md) et [INTERDIT.md](INTERDIT.md).

## Primitive

```
sceau  +  suite  +  hypothèse  +  re-presser-avant  →  fiche .horizon.json
```

Trois suites, tenues séparées :

| Suite | Ce que v0 porte | Hypothèse |
|---|---|---|
| `ed25519` | Ed25519 seul | Shor n'existe pas encore à cette taille |
| `UFHY1` | Ed25519 + ML-DSA-65 (`UFHY1:<ed>:<mldsa65>`) | au moins une des deux signatures survit |
| `mldsa87` | déclarée seulement — non signée en v0 | on ne fait plus confiance à l'elliptique |

`UFHY1` = Ed25519 + **ML-DSA-65**. Un nom de suite, jamais une date de calendrier. mode-protocol refuse déjà UFHY1-comme-date ; ce rail refuse aussi.
UFHY1 signe AND aujourd'hui ; l'hypothèse est OR plus tard.

`re-presser-avant` est exclusif : le jour nommé est déjà trop tard. On resselle avant cette date UTC. Date manquante : refus. Date passée à l'écriture : refus. Aujourd'hui à l'écriture : refus.
La date est un jour de calendrier UTC.

`mldsa87` peut être déclarée. QUANTUM v0 ne la signe pas. QUANTUM signe plus tard. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM. Un merge n'est pas un sceau.

## Verrous physiques (ce rail)

- HORIZON nomme une hypothèse cryptographique et le jour de calendrier où elle cesse de suffire.
- Menace utile 2026 = harvest-now-decrypt-later, pas un QPU de poche.
- Suites : `ed25519` | `UFHY1` | `mldsa87`. `UFHY1` = Ed25519 + ML-DSA-65 — une suite, pas une date.
- `re-presser-avant` est exclusif `YYYY-MM-DD` (UTC). Le jour nommé refuse (`reste <= 0`). On resselle avant cette date UTC. Manquant : refus. Passée ou aujourd'hui à l'écriture : refus.
- `juger` deny = resseller, pas « le fichier est faux ».
- QUANTUM signe plus tard. Clés hors Git. `mldsa87` peut être déclarée ; v0 ne la signe pas. Ne pas frapper `quantique`.
- Ce rail n'est pas UNFORGE, QUELLE, ni TÉMOIN. Pas de token, pas de L1, pas de cloud PQC, pas d'avis juridique.

Jugement = Carl : `python3 horizon.py ecrire|lire|juger`.

## Lancer

```bash
python3 horizon.py ecrire --suite UFHY1 --cible unforge --re-presser-avant 2028-08-31
python3 horizon.py lire examples/hybride.horizon.json
python3 horizon.py juger examples/hybride.horizon.json
```

Un `deny` de `juger` ne dit pas que le fichier est faux. Il dit : resseller.

Verrous physiques (stdlib, sans paquet en plus) :

```bash
python3 -m unittest discover -s tests -v
```

## Vérifié vs présumé

Les tests verrouillent les lignes ci-dessous. Rien dans ce dépôt n'est un théorème. Rien ici n'est un sceau QUANTUM. Un merge n'est pas un sceau.

| Affirmation | Statut |
|---|---|
| `UFHY1` comme date de calendrier est refusé | **vérifié** par les tests de ce rail |
| `re-presser-avant` manquant est refusé | **vérifié** |
| date passée à l'écriture est refusée | **vérifié** |
| écriture d'un `YYYY-MM-DD` futur | **vérifié** |
| `juger` le jour nommé UTC = deny + resseller | **vérifié** |
| `juger` deny = resseller, pas « le fichier est faux » | **vérifié** |
| la fiche JSON n'est pas un sceau QUANTUM | **vérifié** |
| `mldsa87` peut être déclarée ; v0 ne la signe pas | **vérifié** |
| harvest-now-decrypt-later comme menace utile 2026 | **présumé** (modèle de menace, non prouvé ici) |
| hypothèse UFHY1 (au moins une signature survit) | **présumé** |
| signature QUANTUM | **plus tard** — clés hors Git, pas dans ce dépôt |
| EasyCrypt / formal-layer | **pas ici** |
| frapper `quantique` | **refusé** |
| QPU de poche comme menace utile 2026 | **refusé** |

## Ce que v0 n'est pas

Voir [INTERDIT.md](INTERDIT.md). En bref :

- pas UNFORGE (le sceau reste le sceau)
- pas QUELLE (l'origine d'un bit n'est pas une date)
- pas TÉMOIN (la force d'un aléa n'est pas une hypothèse Shor)
- pas un token, pas un L1, pas un cloud PQC, pas un avis juridique
- pas un sceau QUANTUM
- pas `UFHY1` vendu comme une date
- pas `quantique` frappé sur ce rail

Un sceau périmé n'est pas faux. Il est à resseller.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |
| [MODE](https://github.com/carllaliberte/mode-protocol) | le collapse des quatre |

`unforge-check` peut *lire* une fiche HORIZON (`--horizon`). Il ne signe pas.
MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`JUGE.md`](JUGE.md) — date ≠ suite
- [`schema/horizon.v0.json`](schema/horizon.v0.json)
- [`horizon.py`](horizon.py) — `python3 horizon.py ecrire` / `lire` / `juger`
- [`examples/hybride.horizon.json`](examples/hybride.horizon.json)
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
