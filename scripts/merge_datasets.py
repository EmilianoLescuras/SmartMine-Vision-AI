"""
Merge multiple YOLOv8 datasets into one unified dataset.

Usage:
    python scripts/merge_datasets.py

Add new datasets to SOURCES list before running.
Each source needs: path, split dirs, and a class_map that remaps
original class IDs to the unified schema IDs defined in UNIFIED_CLASSES.

SPEC-007 additions:
  - Every label line is validated (5 fields, int class id, 4 floats in [0,1]).
    Invalid lines never enter the corpus; they are recorded in
    `_quarantine/manifest.json` with file, line number, content and reason.
  - Images whose annotations are 100% skipped get an explicit EMPTY label
    file (intentional background) instead of silently missing one.
  - A single pass produces two corpora:
      * smartmine_v1   — full archive schema (33 classes)
      * smartmine_core — training schema (18 classes, all >=100 instances)
  - Everything dropped/remapped is accounted for in `merge_manifest.json`.
"""
from __future__ import annotations

import json
import shutil
import yaml
from pathlib import Path

# ── Unified class schema ──────────────────────────────────────────────────────
UNIFIED_CLASSES = [
    # People & PPE
    "person",                        # 0
    "person_con_casco",              # 1
    "person_sin_casco",              # 2
    "person_con_chaleco",            # 3
    "person_sin_chaleco",            # 4
    "person_con_guantes",            # 5
    "person_sin_guantes",            # 6
    "person_con_lentes",             # 7
    "person_sin_lentes",             # 8
    "person_con_respirador",         # 9
    "person_sin_respirador",         # 10
    "person_ropa_reflectiva",        # 11
    "person_sin_ropa_reflectiva",    # 12
    "mask",                          # 13
    # Vehicles
    "camioneta",                     # 14
    "minibus",                       # 15
    "volquete",                      # 16
    "camion",                        # 17  (reserved: real trucks only — see SPEC-007 AC-4)
    "excavadora",                    # 18
    "retro_excavadora",              # 19
    "cargador_frontal",              # 20
    "motoniveladora",                # 21
    "tractor",                       # 22
    "rodillo",                       # 23
    "cisterna_agua",                 # 24
    # Safety & Environment
    "safety_cone",                   # 25
    "senalizacion",                  # 26
    "hardhat",                       # 27  (alias: generic hardhat from CSS)
    "safety_vest",                   # 28  (alias: generic vest from CSS)
    "animal",                        # 29
    "polvo",                         # 30
    "machinery",                     # 31  (generic, from CSS dataset)
    "vehiculo_generico",             # 32  (generic vehicle from CSS — kept apart
                                     #      so `camion` stays semantically honest)
]

# ── Core training schema (SPEC-007 AC-5) ─────────────────────────────────────
# Only classes with >=100 measured instances and clean object semantics.
# Excluded pairs (guantes/lentes/respirador) have a violation side <100 inst.,
# which makes the compliance pair undetectable; ambient classes (animal/polvo)
# and generic vehicle classes are excluded from training on purpose.
CORE_CLASSES = [
    "person",                        # 0
    "person_con_casco",              # 1
    "person_sin_casco",              # 2
    "person_sin_chaleco",            # 3
    "person_ropa_reflectiva",        # 4
    "person_sin_ropa_reflectiva",    # 5
    "mask",                          # 6
    "hardhat",                       # 7
    "safety_vest",                   # 8
    "safety_cone",                   # 9
    "camioneta",                     # 10
    "volquete",                      # 11
    "excavadora",                    # 12
    "retro_excavadora",              # 13
    "motoniveladora",                # 14
    "rodillo",                       # 15
    "cisterna_agua",                 # 16
    "machinery",                     # 17
]

# unified id → core id (everything else is dropped from core, with accounting)
UNIFIED_TO_CORE: dict[int, int] = {
    0: 0, 1: 1, 2: 2, 4: 3, 11: 4, 12: 5, 13: 6,
    27: 7, 28: 8, 25: 9,
    14: 10, 16: 11, 18: 12, 19: 13, 21: 14, 23: 15, 24: 16,
    31: 17,
}

PROJECT_ROOT = Path(__file__).parent.parent
MERGED_DIR   = PROJECT_ROOT / "datasets" / "merged" / "smartmine_v1"
CORE_DIR     = PROJECT_ROOT / "datasets" / "merged" / "smartmine_core"

# ── Dataset sources ───────────────────────────────────────────────────────────
# class_map: {original_class_id: unified_class_id}
# Set to None to skip a class.
SOURCES = [
    {
        "name": "css_ppe",
        "path": PROJECT_ROOT / "datasets/raw/ppe/css-data",
        "splits": ["train", "valid", "test"],
        "class_map": {
            0: 27,   # Hardhat       → hardhat
            1: 13,   # Mask          → mask
            2: 2,    # NO-Hardhat    → person_sin_casco
            3: None, # NO-Mask       → skip (low priority)
            4: 4,    # NO-Safety Vest→ person_sin_chaleco
            5: 0,    # Person        → person
            6: 25,   # Safety Cone   → safety_cone
            7: 28,   # Safety Vest   → safety_vest
            8: 31,   # machinery     → machinery
            9: 32,   # vehicle       → vehiculo_generico (SPEC-007 AC-4:
                     #                 was polluting `camion` with 1,628 generic
                     #                 construction vehicles)
        },
    },
    {
        "name": "riskalert",
        "path": PROJECT_ROOT / "datasets/raw/vehicles/riskalert",
        "splits": ["train", "valid", "test"],
        "class_map": {
            0:  29,  # ANIMAL                      → animal
            1:  14,  # CAMIONETA                   → camioneta
            2:  20,  # CARGADOR_FRONTAL             → cargador_frontal
            3:  24,  # CISTERNA_AGUA               → cisterna_agua
            4:  25,  # CONOS_DELIMITADORES          → safety_cone
            5:  18,  # EXCAVADORA                  → excavadora
            6:  15,  # MINIBUS                     → minibus
            7:  21,  # MOTONIVELADORA              → motoniveladora
            8:   0,  # PERSONA                     → person
            9:   1,  # PERSONA_CON_CASCO           → person_con_casco
            10:  5,  # PERSONA_CON_GUANTES         → person_con_guantes
            11:  7,  # PERSONA_CON_LENTES          → person_con_lentes
            12:  9,  # PERSONA_CON_RESPIRADOR      → person_con_respirador
            13: 11,  # PERSONA_ROPA_CINTA_REFLECTIVA→ person_ropa_reflectiva
            14:  2,  # PERSONA_SIN_CASCO           → person_sin_casco
            15:  4,  # PERSONA_SIN_CHALECO         → person_sin_chaleco
            16:  6,  # PERSONA_SIN_GUANTES         → person_sin_guantes
            17:  8,  # PERSONA_SIN_LENTES          → person_sin_lentes
            18: 10,  # PERSONA_SIN_RESPIRADOR      → person_sin_respirador
            19: 12,  # PERSONA_SIN_ROPA_CINTA_REFLECTIVA→ person_sin_ropa_reflectiva
            20: 30,  # POLVO                       → polvo
            21: 19,  # RETRO_EXCAVADORA            → retro_excavadora
            22: 23,  # RODILLO                     → rodillo
            23: 26,  # SENALIZACION                → senalizacion
            24: 22,  # TRACTOR                     → tractor
            25: None, # VIA_BUEN_ESTADO            → skip
            26: None, # VIA_CON_MURO_SEGURIDAD     → skip
            27: None, # VIA_EN_MAL_ESTADO          → skip
            28: None, # VIA_NO_REGADA              → skip
            29: None, # VIA_OBSTACULIZADA          → skip
            30: None, # VIA_SATURADA               → skip
            31: None, # VIA_SENALIZADA             → skip
            32: None, # VIA_SIN_MURO_SEGURIDAD     → skip
            33: 16,  # VOLQUETE                    → volquete
        },
    },
    {
        "name": "deteccion_escenarios",
        "path": PROJECT_ROOT / "datasets/raw/vehicles/deteccion_escenarios",
        "splits": ["train", "valid", "test"],
        "class_map": {
            0:  29,   # ANIMAL                          → animal
            1:  None, # ARNES                           → skip
            2:  None, # BANO_QUIMICO                   → skip
            3:  None, # BANO_QUIMICO_SIN_MURO          → skip
            4:  None, # BEBEDERO                        → skip
            5:  14,   # CAMIONETA                       → camioneta
            6:  20,   # CARGADOR_FRONTAL                → cargador_frontal
            7:  None, # CASETA_VIGIA                   → skip
            8:  None, # CERCANIA_VOLQUETE_EXCAVADORA   → skip (relación, no objeto)
            9:  24,   # CISTERNA_DE_AGUA               → cisterna_agua
            10: None, # CLIMA_ADVERSO                  → skip
            11: 25,   # CONOS_DELIMITADORES            → safety_cone
            12: None, # DELIMITACION_DE_AREA           → skip
            13: None, # DESCARGA_VOLQUETE_CON_CUADRADOR→ skip
            14: None, # ESPEJO_OJO_PEZ                 → skip
            15: None, # ESTACIONAMIENTO_CON_SENALETICA → skip
            16: None, # ESTACIONAMIENTO_LIVIANO_SIN_SENALETICA → skip
            17: None, # ESTACIONAMIENTO_VEHICULO_LIVIANO → skip
            18: None, # ETIQUETA_BUEN_ESTADO           → skip
            19: None, # ETIQUETA_MAL_ESTADO            → skip
            20: 18,   # EXCAVADORA                     → excavadora
            21: 18,   # EXCAVADORA_ESTACIONADA         → excavadora (mismo objeto)
            22: None, # LAVAMANOS                      → skip
            23: None, # LLUVIA                         → skip
            24: None, # MARTILLO_SIN_MURO              → skip
            25: 15,   # MINIBUS                        → minibus
            26: 21,   # MOTONIVELADORA                 → motoniveladora
            27: None, # MUROS_CASETA_VIGIA             → skip
            28: None, # MURO_SEGURIDAD_CON_MATERIAL_GRUESO → skip
            29: None, # NEBLINA                        → skip
            30: None, # OPERACION_OBSTACULO_VIA        → skip
            31: 6,    # PERSONA _SIN_GUANTE_SEGURIDAD  → person_sin_guantes
            32: 1,    # PERSONA_CASCO_BLANCO           → person_con_casco
            33: 13,   # PERSONA_CON_BARBIJO            → mask
            34: 1,    # PERSONA_CON_CASCO              → person_con_casco
            35: 1,    # PERSONA_CON_CASCO_AMARILLO     → person_con_casco
            36: 1,    # PERSONA_CON_CASCO_AZUL         → person_con_casco
            37: 5,    # PERSONA_CON_GUANTES            → person_con_guantes
            38: 7,    # PERSONA_CON_LENTES_CLARO       → person_con_lentes
            39: 7,    # PERSONA_CON_LENTES_OSCURA      → person_con_lentes
            40: 9,    # PERSONA_CON_RESPIRADOR         → person_con_respirador
            41: None, # PERSONA_CON_TRAJE_DESCARTABLE  → skip
            42: None, # PERSONA_CON_TRAJE_DESCARTABLE_SIN_CINTAS → skip
            43: 0,    # PERSONA_LEJOS_MAQUINARIA       → person
            44: 11,   # PERSONA_ROPA_CINTA_REFLECTIVA  → person_ropa_reflectiva
            45: 2,    # PERSONA_SIN_CASCO              → person_sin_casco
            46: 8,    # PERSONA_SIN_LENTES_SEGURIDAD   → person_sin_lentes
            47: 10,   # PERSONA_SIN_RESPIRADOR         → person_sin_respirador
            48: None, # PLATAFORMA_CON_MURO_DE_SEGURIDAD → skip
            49: 30,   # POLVO                          → polvo
            50: None, # REGADIO_VIA                    → skip
            51: 19,   # RETROEXCAVADORA                → retro_excavadora
            52: 23,   # RODILLO                        → rodillo
            53: 26,   # SENALETICA_VEHICULO_LIVIANO    → senalizacion
            54: None, # TRABATUERCA_GOTA               → skip
            55: None, # TRABATUERCA_NO_ESTANDAR        → skip
            56: 22,   # TRACTOR                        → tractor
            57: 22,   # TRACTOR_ESTACIONADO            → tractor
            58: None, # VIA_CON_MURO_SEGURIDAD         → skip
            59: None, # VIA_EN_MAL_ESTADO              → skip
            60: None, # VIA_NO_REGADA                  → skip
            61: None, # VIA_REGADA                     → skip
            62: None, # VIA_SATURADA                   → skip
            63: None, # VIA_SENALIZADA                 → skip
            64: None, # VIA_SIN_MURO_SEGURIDAD         → skip
            65: 16,   # VOLQUETE                       → volquete
            66: 16,   # VOLQUETE_DESCARGA              → volquete
        },
    },
    # ── mining_area: EXCLUIDO del merge de detección (SPEC-007 AC-3) ──────────
    # Sus 3 clases son eventos de zona ("Kendaraan masuk tambang" = vehículo
    # entra al área), no tipos de objeto: mapearlas a `camion` inyectaba 2.551
    # falsas instancias (61% de la clase). Además es la única fuente con labels
    # corruptos (185 líneas malformadas). Los datos quedan en raw/ para la
    # futura capa de eventos/geofencing.
    # {
    #     "name": "mining_area",
    #     "path": PROJECT_ROOT / "datasets/raw/vehicles/mining_area",
    #     "splits": ["train", "valid", "test"],
    #     "class_map": {0: None, 1: None, 2: None},
    # },
    # ── Add new datasets here when available ──────────────────────────────────
]


def validate_line(parts: list[str]) -> str | None:
    """Return a reason string if a YOLO label line is invalid, else None."""
    if len(parts) != 5:
        return f"expected 5 fields, got {len(parts)}"
    try:
        int(parts[0])
    except ValueError:
        return f"class id not an int: {parts[0]!r}"
    try:
        coords = [float(x) for x in parts[1:]]
    except ValueError:
        return "non-numeric coordinate"
    if any(c < 0.0 or c > 1.0 for c in coords):
        return f"coordinate out of [0,1]: {coords}"
    return None


def process_label_file(
    src_path: Path,
    class_map: dict,
    skip_counter: dict[int, int],
    kept_counter: dict[int, int],
    quarantine: list[dict],
    source_name: str,
    split: str,
) -> tuple[list[str], list[str]]:
    """Validate + remap one label file.

    Returns (v1_lines, core_lines). Invalid lines go to `quarantine` and are
    never written; skipped classes update `skip_counter`.
    """
    v1_lines: list[str] = []
    core_lines: list[str] = []
    with open(src_path) as f:
        raw_lines = f.readlines()
    for lineno, line in enumerate(raw_lines, start=1):
        parts = line.strip().split()
        if not parts:
            continue
        reason = validate_line(parts)
        if reason is not None:
            quarantine.append({
                "source": source_name,
                "split": split,
                "file": src_path.name,
                "line": lineno,
                "content": line.strip()[:120],
                "reason": reason,
            })
            continue
        orig_id = int(parts[0])
        new_id = class_map.get(orig_id)
        if new_id is None:
            skip_counter[orig_id] = skip_counter.get(orig_id, 0) + 1
            continue
        kept_counter[orig_id] = kept_counter.get(orig_id, 0) + 1
        coords = " ".join(parts[1:])
        v1_lines.append(f"{new_id} {coords}\n")
        core_id = UNIFIED_TO_CORE.get(new_id)
        if core_id is not None:
            core_lines.append(f"{core_id} {coords}\n")
    return v1_lines, core_lines


def _reset_output_dirs() -> None:
    """Remove previously generated corpora so stale files never survive."""
    for d in (MERGED_DIR, CORE_DIR):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)


def _write_yamls() -> Path:
    for base, classes, cfg_name in (
        (MERGED_DIR, UNIFIED_CLASSES, "smartmine_unified.yaml"),
        (CORE_DIR,   CORE_CLASSES,    "smartmine_core.yaml"),
    ):
        block = {
            "train": "train/images",
            "val":   "valid/images",
            "test":  "test/images",
            "nc":    len(classes),
            "names": classes,
        }
        with open(base / "data.yaml", "w") as f:
            yaml.dump({"path": "."} | block, f, allow_unicode=True, sort_keys=False)
        cfg_yaml = PROJECT_ROOT / "configs/yaml" / cfg_name
        rel = f"../../datasets/merged/{base.name}"
        with open(cfg_yaml, "w") as f:
            yaml.dump({"path": rel} | block, f, allow_unicode=True, sort_keys=False)
    return PROJECT_ROOT / "configs/yaml"


def merge():
    print(f"\nMerging {len(SOURCES)} datasets -> {MERGED_DIR} + {CORE_DIR}\n")
    _reset_output_dirs()

    counts = {s: {"images": 0, "labels": 0, "backgrounds": 0}
              for s in ["train", "valid", "test"]}
    per_source_stats: dict[str, dict] = {}
    quarantine: list[dict] = []
    v1_class_totals: dict[int, int] = {}
    core_class_totals: dict[int, int] = {}

    for source in SOURCES:
        name      = source["name"]
        src_root  = Path(source["path"])
        class_map = source["class_map"]
        skip_counter: dict[int, int] = {}
        kept_counter: dict[int, int] = {}
        backgrounds = 0
        print(f"  [{name}]  {src_root}")

        for split in source["splits"]:
            img_src = src_root / split / "images"
            lbl_src = src_root / split / "labels"
            if not img_src.exists():
                continue
            for base in (MERGED_DIR, CORE_DIR):
                (base / split / "images").mkdir(parents=True, exist_ok=True)
                (base / split / "labels").mkdir(parents=True, exist_ok=True)

            for img_file in sorted(img_src.iterdir()):
                if img_file.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue

                new_stem = f"{name}_{img_file.stem}"
                lbl_file = lbl_src / (img_file.stem + ".txt")

                v1_lines: list[str] = []
                core_lines: list[str] = []
                if lbl_file.exists():
                    v1_lines, core_lines = process_label_file(
                        lbl_file, class_map, skip_counter, kept_counter,
                        quarantine, name, split,
                    )

                for base, lines, totals in (
                    (MERGED_DIR, v1_lines, v1_class_totals),
                    (CORE_DIR, core_lines, core_class_totals),
                ):
                    shutil.copy2(img_file, base / split / "images" / (new_stem + img_file.suffix))
                    # Empty file = explicit intentional background (SPEC-007
                    # AC-2): the validator must never see a missing label.
                    with open(base / split / "labels" / (new_stem + ".txt"), "w") as f:
                        f.writelines(lines)
                    for ln in lines:
                        cid = int(ln.split()[0])
                        totals[cid] = totals.get(cid, 0) + 1

                counts[split]["images"] += 1
                if v1_lines:
                    counts[split]["labels"] += 1
                else:
                    counts[split]["backgrounds"] += 1
                    backgrounds += 1

        per_source_stats[name] = {
            "kept": kept_counter, "skipped": skip_counter,
            "backgrounds": backgrounds,
        }

    cfg_dir = _write_yamls()

    # ── Manifests (SPEC-007 AC-1/AC-2/AC-5) ──────────────────────────────────
    quarantine_dir = MERGED_DIR / "_quarantine"
    quarantine_dir.mkdir(exist_ok=True)
    with open(quarantine_dir / "manifest.json", "w") as f:
        json.dump({"invalid_lines": quarantine, "total": len(quarantine)},
                  f, indent=1, ensure_ascii=False)

    manifest = {
        "generated_by": "scripts/merge_datasets.py (SPEC-007)",
        "sources": {
            name: {
                "kept_annotations": sum(s["kept"].values()),
                "skipped_annotations": sum(s["skipped"].values()),
                "skipped_by_original_id": s["skipped"],
                "background_images": s["backgrounds"],
            }
            for name, s in per_source_stats.items()
        },
        "quarantined_lines": len(quarantine),
        "v1": {
            "nc": len(UNIFIED_CLASSES),
            "class_counts": {UNIFIED_CLASSES[i]: v1_class_totals.get(i, 0)
                             for i in range(len(UNIFIED_CLASSES))},
        },
        "core": {
            "nc": len(CORE_CLASSES),
            "class_counts": {CORE_CLASSES[i]: core_class_totals.get(i, 0)
                             for i in range(len(CORE_CLASSES))},
            "dropped_from_core": [
                UNIFIED_CLASSES[i] for i in range(len(UNIFIED_CLASSES))
                if i not in UNIFIED_TO_CORE
            ],
        },
        "excluded_sources": {
            "mining_area": "clases de evento de zona, no objetos; 185 líneas "
                           "corruptas; reservado para capa de eventos (AC-3)",
        },
    }
    with open(MERGED_DIR / "merge_manifest.json", "w") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)

    # ── Console summary ──────────────────────────────────────────────────────
    print("\n-- Split totals --")
    total_imgs = 0
    for split, c in counts.items():
        print(f"  {split:6s}: {c['images']:4d} imgs  {c['labels']:4d} labeled  "
              f"{c['backgrounds']:3d} backgrounds")
        total_imgs += c["images"]
    print(f"  TOTAL : {total_imgs} images")

    print("\n-- Per-source coverage --")
    for name, stats in per_source_stats.items():
        kept = sum(stats["kept"].values())
        skipped = sum(stats["skipped"].values())
        total = kept + skipped
        pct = (100.0 * kept / total) if total else 0.0
        print(f"  [{name}] kept {kept:5d} / {total:5d} annotations ({pct:.1f}%)  "
              f"backgrounds: {stats['backgrounds']}")
        if stats["skipped"]:
            top = sorted(stats["skipped"].items(), key=lambda kv: -kv[1])[:5]
            preview = ", ".join(f"id{k}={v}" for k, v in top)
            print(f"           skipped breakdown (top 5 ids): {preview}")

    print(f"\n  Quarantined lines : {len(quarantine)} -> {quarantine_dir / 'manifest.json'}")
    print(f"  Merge manifest    -> {MERGED_DIR / 'merge_manifest.json'}")
    print(f"  Configs           -> {cfg_dir}/smartmine_unified.yaml + smartmine_core.yaml")
    print(f"  v1 data   ({len(UNIFIED_CLASSES)} cls) -> {MERGED_DIR}")
    print(f"  core data ({len(CORE_CLASSES)} cls) -> {CORE_DIR}")
    print("\nDone.\n")


if __name__ == "__main__":
    merge()
