# HORIZON Protocol

**Une date où le sceau doit être ressellé.**

HORIZON names the cryptographic hypothesis of an act and the calendar day it stops being enough. The useful 2026 threat is *harvest-now-decrypt-later*, not a pocket QPU.

This repository is version 0. It fits on a phone. Zero token. Zero paid server.

**Open source (MIT).** The protocol stays public. See [COPYRIGHT.md](COPYRIGHT.md) and [INTERDIT.md](INTERDIT.md).

## Primitive

```
sceau  +  suite  +  hypothèse  +  re-presser-avant  →  fiche .horizon.json
```

Three suites, kept separate:

| Suite | What v0 carries | Hypothesis |
|---|---|---|
| `ed25519` | Ed25519 alone | Shor is not yet at this size |
| `UFHY1` | Ed25519 + ML-DSA-65 (`UFHY1:<ed>:<mldsa65>`) | at least one of the two signatures survives |
| `mldsa87` | declared only — not signed in v0 | we no longer trust the elliptic curve |

`UFHY1` = Ed25519 + **ML-DSA-65**. A suite name, never a calendar date. mode-protocol already refuses UFHY1-as-date; this rail refuses it too.

`re-presser-avant` must be `YYYY-MM-DD` still ahead at write. Missing date: refuse. Past date at write: refuse.

`mldsa87` may be declared. QUANTUM v0 does not sign it. QUANTUM signs later. Keys stay off Git. This repo is not a QUANTUM seal. A merge is not a seal.

## Physics locks (this rail)

- HORIZON names a cryptographic hypothesis and the calendar day it stops being enough.
- 2026 useful threat = harvest-now-decrypt-later, not a pocket QPU.
- Suites: `ed25519` | `UFHY1` | `mldsa87`. `UFHY1` is Ed25519 + ML-DSA-65 — a suite, not a date.
- `re-presser-avant` = `YYYY-MM-DD` still ahead at write. Missing: refuse. Past: refuse.
- `juger` deny means resell, not « the file is fake ».
- QUANTUM signs later. Keys off Git. `mldsa87` may be declared; v0 does not sign it. Do not mint `quantique`.
- This rail is not UNFORGE, QUELLE, or TÉMOIN. No token, L1, PQC cloud, or legal opinion.

Judgment = Carl: `python3 horizon.py ecrire|lire|juger`.

## How to run

```bash
python3 horizon.py ecrire --suite UFHY1 --cible unforge --re-presser-avant 2028-08-31
python3 horizon.py lire examples/hybride.horizon.json
python3 horizon.py juger examples/hybride.horizon.json
```

A judge `deny` does not say the file is fake. It says: resell.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

Tests lock the rows below. Nothing in this repository is a theorem. Nothing here is a QUANTUM seal. A merge is not a seal.

| Claim | Status |
|---|---|
| `UFHY1` as a calendar date is refused | **verified** by tests on this rail |
| missing `re-presser-avant` is refused | **verified** |
| past date at write is refused | **verified** |
| future `YYYY-MM-DD` writes | **verified** |
| `juger` deny = resell, not « the file is fake » | **verified** |
| JSON card is not a QUANTUM seal | **verified** |
| `mldsa87` may be declared; v0 does not sign it | **verified** |
| harvest-now-decrypt-later as the 2026 useful threat | **assumed** (threat model, not proven here) |
| UFHY1 hypothesis (at least one signature survives) | **assumed** |
| QUANTUM signature | **later** — keys off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| mint `quantique` | **refused** |
| pocket QPU as the 2026 useful threat | **refused** |

## What v0 is not

See [INTERDIT.md](INTERDIT.md). In short:

- pas UNFORGE (le sceau reste le sceau)
- pas QUELLE (l'origine d'un bit n'est pas une date)
- pas TÉMOIN (la force d'un aléa n'est pas une hypothèse Shor)
- pas un token, pas un L1, pas un cloud PQC, pas un avis juridique
- pas un sceau QUANTUM
- pas `UFHY1` vendu comme une date
- pas `quantique` frappé sur cette rail

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
