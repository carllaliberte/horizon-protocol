#!/usr/bin/env python3
"""HORIZON v0 — écrire / lire / juger / sceller une date de ressellage.

Pas de QPU inventé. UFHY1 signe en local-v0 (Ed25519 AND ML-DSA-65).
QUANTUM n'est pas ce processus.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

FORMAT = "horizon.v0"
SUITES = ("ed25519", "UFHY1", "mldsa87")
CIBLES = ("unforge", "situs", "figure", "quelle", "temoin", "mesure")
HYPOTHESES = {
    "ed25519": "Shor n'existe pas encore à cette taille",
    "UFHY1": "au moins une des deux signatures survit",
    "mldsa87": "on ne fait plus confiance à l'elliptique",
}


def _aujourd_hui() -> date:
    return datetime.now(timezone.utc).date()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_jour(s: str) -> date:
    return date.fromisoformat(s)


def _exiger_jour(
    s: str | None,
    *,
    manquant: str = "refus : re-presser-avant manquant",
) -> date:
    if s is None or not str(s).strip():
        raise SystemExit(manquant)
    raw = str(s).strip()
    if raw in SUITES:
        raise SystemExit("refus : suite, pas une date. UFHY1 = Ed25519 + ML-DSA-65")
    try:
        return _parse_jour(raw)
    except ValueError:
        raise SystemExit("re-presser-avant : YYYY-MM-DD") from None


def ecrire(
    suite: str,
    re_presser_avant: str,
    cible: str = "unforge",
    cible_id: str | None = None,
    juridiction: str = "QC",
    langue: str = "fr-CA",
) -> dict:
    suite = (suite or "").strip()
    if suite not in SUITES:
        raise SystemExit("suite : ed25519 | UFHY1 | mldsa87")
    cible = (cible or "unforge").strip().lower()
    if cible not in CIBLES:
        raise SystemExit("cible : unforge | situs | figure | quelle | temoin | mesure")
    jour = _exiger_jour(re_presser_avant)
    if jour <= _aujourd_hui():
        raise SystemExit("refus : date déjà passée. un horizon se pose devant soi")
    carte = {
        "format": FORMAT,
        "horizon_id": "HZ-" + uuid.uuid4().hex[:12],
        "cible": cible,
        "cible_id": cible_id or None,
        "suite": suite,
        "hypothese": HYPOTHESES[suite],
        "re_presser_avant": jour.isoformat(),
        "juridiction": juridiction,
        "langue": langue,
        "pose_at": _now(),
        "revocable": True,
        "sceau": None,
        "note": "v0. sceau=null. Périmé ≠ faux. Reseller.",
    }
    return carte


def lire(chemin: str) -> dict:
    p = Path(chemin).expanduser()
    carte = json.loads(p.read_text(encoding="utf-8"))
    if carte.get("format") != FORMAT:
        raise SystemExit("pas une fiche horizon.v0")
    if carte.get("suite") not in SUITES:
        raise SystemExit("suite inconnue")
    _exiger_jour(
        carte.get("re_presser_avant"),
        manquant="fiche refusée : pas de date",
    )
    return carte


def juger(carte: dict, aujourd: date | None = None) -> dict:
    jour = _exiger_jour(
        carte.get("re_presser_avant"),
        manquant="fiche refusée : pas de date",
    )
    here = aujourd or _aujourd_hui()
    reste = (jour - here).days
    if reste <= 0:
        return {
            "decision": "deny",
            "flag": "horizon",
            "suite": carte.get("suite"),
            "re_presser_avant": carte["re_presser_avant"],
            "jours_restants": reste,
            "note": "périmé. le sceau n'est pas faux. resseller.",
        }
    sceau = carte.get("sceau")
    sceau_ok = None
    if sceau and carte.get("suite") == "UFHY1":
        from ufhy1 import verify as ufhy1_verify

        payload = _payload(carte)
        sceau_ok = ufhy1_verify(sceau, payload.encode("utf-8")).get("ok")
        if not sceau_ok:
            return {
                "decision": "deny",
                "flag": "horizon",
                "suite": carte.get("suite"),
                "re_presser_avant": carte["re_presser_avant"],
                "jours_restants": reste,
                "sceau_ok": False,
                "note": "sceau UFHY1 refusé. AND today.",
            }
    return {
        "decision": "allow",
        "flag": "horizon",
        "suite": carte.get("suite"),
        "re_presser_avant": carte["re_presser_avant"],
        "jours_restants": reste,
        "sceau_ok": sceau_ok,
        "note": "dans l'hypothèse déclarée. encore " + str(reste) + " j.",
    }


def _payload(carte: dict) -> str:
    corps = {k: v for k, v in carte.items() if k != "sceau"}
    return json.dumps(corps, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sceller(carte: dict, keys: str = "keys") -> dict:
    if carte.get("suite") != "UFHY1":
        raise SystemExit("sceller v0 : seulement suite UFHY1")
    from ufhy1 import sign as ufhy1_sign

    carte["note"] = "scellé UFHY1 local-v0. AND today."
    payload = _payload(carte)
    carte["sceau"] = ufhy1_sign(payload.encode("utf-8"), keys)
    return carte


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="horizon")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("ecrire")
    pe.add_argument("--suite", required=True)
    pe.add_argument("--re-presser-avant", required=True)
    pe.add_argument("--cible", default="unforge")
    pe.add_argument("--cible-id", default=None)
    pe.add_argument("--juridiction", default="QC")
    pe.add_argument("--langue", default="fr-CA")
    pe.add_argument("--vers", default="carte.horizon.json")
    pl = sub.add_parser("lire")
    pl.add_argument("fichier")
    pj = sub.add_parser("juger")
    pj.add_argument("fichier")
    ps = sub.add_parser("sceller")
    ps.add_argument("fichier")
    ps.add_argument("--keys", default="keys")
    args = p.parse_args(argv)
    if args.cmd == "ecrire":
        carte = ecrire(
            suite=args.suite,
            re_presser_avant=args.re_presser_avant,
            cible=args.cible,
            cible_id=args.cible_id,
            juridiction=args.juridiction,
            langue=args.langue,
        )
        Path(args.vers).write_text(
            json.dumps(carte, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        out = dict(carte)
        out["fichier"] = args.vers
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.cmd == "lire":
        print(json.dumps(lire(args.fichier), ensure_ascii=False, indent=2))
    elif args.cmd == "sceller":
        carte = sceller(lire(args.fichier), args.keys)
        Path(args.fichier).write_text(
            json.dumps(carte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(carte, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(juger(lire(args.fichier)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
