"""
Download all SmartMine datasets from Roboflow Universe.

Usage:
    python scripts/download_datasets.py

Requires:
    ROBOFLOW_API_KEY set in .env or as an environment variable.
    pip install roboflow python-dotenv

Each source is downloaded only once; subsequent runs skip existing directories.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Path resolution ───────────────────────────────────────────────────────────
_here = Path(__file__).resolve().parent
PROJECT_ROOT = _here.parent

# ── Source catalogue ──────────────────────────────────────────────────────────
# 'dest' is relative to PROJECT_ROOT.
# 'version' is the Roboflow dataset version number to download.
SOURCES = {
    # ── PPE ──────────────────────────────────────────────────────────────────
    "css-data": {
        "workspace": "roboflow-100",
        "project":   "construction-site-safety",
        "version":   1,
        "url":       "https://universe.roboflow.com/roboflow-100/construction-site-safety",
        "dest":      "datasets/raw/ppe/css-data",
    },
    # ── Vehicles ─────────────────────────────────────────────────────────────
    "construction_vehicles": {
        "workspace": "0925",
        "project":   "construction-vehicle-inspection",
        "version":   1,
        "url":       "https://universe.roboflow.com/0925/construction-vehicle-inspection",
        "dest":      "datasets/raw/vehicles/construction_vehicles",
    },
    "mining_area_detection": {
        "workspace": "septiana-s-workspace",
        "project":   "mining-area-vehicle-detection",
        "version":   1,
        "url":       "https://universe.roboflow.com/septiana-s-workspace/mining-area-vehicle-detection",
        "dest":      "datasets/raw/vehicles/mining_area_detection",
    },
    "riskalert": {
        "workspace": "personal-q02wc",
        "project":   "riskalert-mining",
        "version":   1,
        "url":       "https://universe.roboflow.com/personal-q02wc/riskalert-mining",
        "dest":      "datasets/raw/vehicles/riskalert",
    },
    "riskalertai": {
        "workspace": "personal-q02wc",
        "project":   "riskalertai-mining",
        "version":   10,
        "url":       "https://universe.roboflow.com/personal-q02wc/riskalertai-mining",
        "dest":      "datasets/raw/vehicles/riskalertai",
    },
    "deteccion_escenarios": {
        "workspace": "personal-q02wc",
        "project":   "deteccion-de-escenarios-de-riesg-a8hb1",
        "version":   8,
        "url":       "https://universe.roboflow.com/personal-q02wc/deteccion-de-escenarios-de-riesg-a8hb1",
        "dest":      "datasets/raw/vehicles/deteccion_escenarios",
    },
    # ── PPE — descarga directa (no Roboflow) ─────────────────────────────────
    # SPEC-008: Construction-PPE de Ultralytics (AGPL-3.0, riesgo documentado
    # en specs/008). Se baja como zip directo.
    "construction_ppe": {
        "type": "http_zip",
        "url":  "https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip",
        "dest": "datasets/raw/ppe/construction_ppe",
    },
    # ── mining_area: NO descargar — excluido del merge por SPEC-007 AC-3 ─────
    # (clases de evento de zona + 185 labels corruptos; ver docs/research/)
}

DOWNLOAD_FORMAT = "yolov8"


def _check_api_key() -> str:
    api_key = os.environ.get("ROBOFLOW_API_KEY", "").strip()
    if not api_key or api_key == "your_roboflow_api_key_here":
        print(
            "\n[ERROR] ROBOFLOW_API_KEY is not set.\n"
            "\nTo get a free API key:\n"
            "  1. Sign up at https://app.roboflow.com/\n"
            "  2. Go to Settings → API Keys\n"
            "  3. Copy the key into .env:\n"
            "       ROBOFLOW_API_KEY=your_actual_key\n"
        )
        sys.exit(1)
    return api_key


def _is_downloaded(dest: Path) -> bool:
    """Return True if the destination has at least one image file."""
    return any(dest.rglob("*.jpg")) or any(dest.rglob("*.png"))


def download_http_zip(alias: str, meta: dict) -> bool:
    """Download and extract a plain zip dataset (non-Roboflow sources)."""
    import io
    import zipfile
    from urllib.request import urlopen

    dest = PROJECT_ROOT / meta["dest"]
    if _is_downloaded(dest):
        print(f"  [SKIP] {alias} — already present at {dest}")
        return True

    dest.mkdir(parents=True, exist_ok=True)
    print(f"  [DOWNLOAD] {alias}")
    print(f"    Source : {meta['url']}")
    try:
        with urlopen(meta["url"]) as resp:
            data = resp.read()
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = zf.namelist()
            # Si el zip envuelve todo en un directorio raíz único, aplanarlo.
            roots = {n.split("/", 1)[0] for n in names if n.strip("/")}
            strip_root = len(roots) == 1 and all("/" in n for n in names if not n.endswith("/"))
            for n in names:
                target_rel = n.split("/", 1)[1] if strip_root else n
                if not target_rel or n.endswith("/"):
                    continue
                target = dest / target_rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(n) as src, open(target, "wb") as out:
                    out.write(src.read())
        print(f"    Saved  → {dest}")
        return True
    except Exception as exc:
        print(f"    [WARN] Failed to download {alias}: {exc}")
        return False


def download_source(alias: str, meta: dict, api_key: str) -> bool:
    """Download a single dataset. Returns True on success, False on error."""
    try:
        from roboflow import Roboflow
    except ImportError:
        print("[ERROR] roboflow package not found. Run: pip install roboflow")
        sys.exit(1)

    dest = PROJECT_ROOT / meta["dest"]

    if _is_downloaded(dest):
        print(f"  [SKIP] {alias} — already present at {dest}")
        return True

    dest.mkdir(parents=True, exist_ok=True)
    print(f"  [DOWNLOAD] {alias}")
    print(f"    Source : {meta['url']}")
    print(f"    Format : {DOWNLOAD_FORMAT} v{meta['version']}")

    try:
        rf = Roboflow(api_key=api_key)
        project = rf.workspace(meta["workspace"]).project(meta["project"])
        version = project.version(meta["version"])
        version.download(DOWNLOAD_FORMAT, location=str(dest), overwrite=False)
        print(f"    Saved  → {dest}")
        return True
    except Exception as exc:
        print(f"    [WARN] Failed to download {alias}: {exc}")
        print(f"    Check version number or visit {meta['url']} for the correct version.")
        return False


def main() -> None:
    print("SmartMine — Dataset Download")
    print("=" * 50)

    api_key = _check_api_key()

    results = {}
    for alias, meta in SOURCES.items():
        if meta.get("type") == "http_zip":
            results[alias] = download_http_zip(alias, meta)
        else:
            results[alias] = download_source(alias, meta, api_key)

    print()
    print("Summary")
    print("-" * 50)
    ok_count = 0
    for alias, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  {alias:<30} {status}")
        if success:
            ok_count += 1

    print(f"\n{ok_count}/{len(SOURCES)} datasets available.")

    if ok_count < len(SOURCES):
        print("\nSome downloads failed. Check version numbers in SOURCES or visit")
        print("the Roboflow Universe URLs above to find the correct version.")
        sys.exit(1)


if __name__ == "__main__":
    main()
