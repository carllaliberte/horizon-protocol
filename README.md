# HORIZON Protocol

**Une date où le sceau doit être ressellé.**

HORIZON nomme l'hypothèse cryptographique d'un acte et le jour où elle cesse de suffire. La menace utile en 2026 n'est pas un QPU de poche. C'est *harvest-now-decrypt-later*.

Ce dépôt est la version 0. Elle tient dans un téléphone. Zéro token. Zéro serveur payant.

**Open source (MIT).** Le protocole reste public. Voir [COPYRIGHT.md](COPYRIGHT.md) et [INTERDIT.md](INTERDIT.md).

## Primitive

```
sceau  +  suite  +  hypothèse  +  re-presser-avant  →  fiche .horizon.json
```

Trois suites, séparées :

| Suite | Ce que QUANTUM signe aujourd'hui | Hypothèse |
|---|---|---|
| `ed25519` | Ed25519 seul | Shor n'existe pas encore à cette taille |
| `UFHY1` | `UFHY1:<ed>:<mldsa65>` | au moins une des deux signatures survit |
| `mldsa87` | pas encore | on ne fait plus confiance à l'elliptique |

`UFHY1` = Ed25519 + **ML-DSA-65**. Un seul nom, une seule courbe.  
`mldsa87` se déclare ; QUANTUM v0 ne le signe pas. Sans date : refus. Date déjà passée à l'écriture : refus.

## v0 au cellulaire

```bash
python3 horizon.py ecrire --suite UFHY1 --cible unforge --re-presser-avant 2028-08-31
python3 horizon.py lire examples/hybride.horizon.json
python3 horizon.py juger examples/hybride.horizon.json
```

Un juge `deny` ne dit pas que le fichier est faux. Il dit : resseller.

## Ce que v0 n'est pas

- pas UNFORGE (le sceau reste le sceau)
- pas QUELLE (l'origine d'un bit n'est pas une date)
- pas TÉMOIN (la force d'un aléa n'est pas une hypothèse Shor)
- pas un token, pas un cloud PQC, pas un avis juridique

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |

`unforge-check` peut *lire* une fiche HORIZON (`--horizon`). Il ne signe pas.  
MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe. Les clés restent hors Git.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`schema/horizon.v0.json`](schema/horizon.v0.json)
- [`horizon.py`](horizon.py) — écrire + lire + juger
- [`examples/hybride.horizon.json`](examples/hybride.horizon.json)
