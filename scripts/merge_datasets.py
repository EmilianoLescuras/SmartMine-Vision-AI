"""
Merge multiple YOLOv8 datasets into one unified dataset.

Usage:
    python scripts/merge_datasets.py

Add new datasets to SOURCES list before running.
Each source needs: path, split dirs, and a class_map that remaps
original class IDs to the unified schema IDs defined in UNIFIED_CLASSES.
"""
from __future__ import annotations

import os
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
    "camion",                        # 17  (generic truck from other datasets)
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
]

PROJECT_ROOT = Path(__file__).parent.parent
MERGED_DIR   = PROJECT_ROOT / "datasets" / "merged" / "smartmine_v1"

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
            9: 17,   # vehicle       → camion (generic)
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
    {
        "name": "mining_area",
        "path": PROJECT_ROOT / "datasets/raw/vehicles/mining_area",
        "splits": ["train", "valid", "test"],
        "class_map": {
            0: None, # Area Tambang (zona minera)              → skip (zona, no objeto)
            1: 17,   # Kendaraan asing masuk area tambang      → camion (vehículo genérico)
            2: 17,   # Kendaraan masuk tambang                 → camion (vehículo genérico)
        },
    },
    # ── Add new datasets here when available ──────────────────────────────────
    # {
    #     "name": "nuevo_dataset",
    #     "path": PROJECT_ROOT / "datasets/raw/vehicles/nuevo",
    #     "splits": ["train", "valid", "test"],
    #     "class_map": { 0: X, 1: Y, ... },
    # },
]


def remap_label_file(src_path: Path, dst_path: Path, class_map: dict) -> int:
    """Rewrite a YOLO label file with remapped class IDs. Returns lines written."""
    lines_written = 0
    with open(src_path) as f:
        lines = f.readlines()
    out = []
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        orig_id = int(parts[0])
        new_id = class_map.get(orig_id)
        if new_id is None:
            continue  # skip unmapped / explicitly excluded class
        out.append(f"{new_id} {' '.join(parts[1:])}\n")
        lines_written += 1
    if out:
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dst_path, "w") as f:
            f.writelines(out)
    return lines_written


def merge():
    print(f"\nMerging {len(SOURCES)} datasets → {MERGED_DIR}\n")

    counts: dict[str, dict[str, int]] = {s: {"images": 0, "labels": 0} for s in ["train", "valid", "test"]}

    for source in SOURCES:
        name      = source["name"]
        src_root  = Path(source["path"])
        class_map = source["class_map"]
        print(f"  [{name}]  {src_root}")

        for split in source["splits"]:
            img_src = src_root / split / "images"
            lbl_src = src_root / split / "labels"
            img_dst = MERGED_DIR / split / "images"
            lbl_dst = MERGED_DIR / split / "labels"
            img_dst.mkdir(parents=True, exist_ok=True)
            lbl_dst.mkdir(parents=True, exist_ok=True)

            if not img_src.exists():
                continue

            for img_file in img_src.iterdir():
                if img_file.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue

                # Prefix filename with source name to avoid collisions
                new_stem  = f"{name}_{img_file.stem}"
                dst_img   = img_dst / (new_stem + img_file.suffix)
                lbl_file  = lbl_src / (img_file.stem + ".txt")
                dst_lbl   = lbl_dst / (new_stem + ".txt")

                shutil.copy2(img_file, dst_img)
                counts[split]["images"] += 1

                if lbl_file.exists():
                    written = remap_label_file(lbl_file, dst_lbl, class_map)
                    if written:
                        counts[split]["labels"] += 1

    # Write unified data.yaml
    yaml_path = MERGED_DIR / "data.yaml"
    yaml_content = {
        "path":  str(MERGED_DIR),
        "train": "train/images",
        "val":   "valid/images",
        "test":  "test/images",
        "nc":    len(UNIFIED_CLASSES),
        "names": UNIFIED_CLASSES,
    }
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

    # Also write to configs/yaml/
    cfg_yaml = PROJECT_ROOT / "configs/yaml/smartmine_unified.yaml"
    shutil.copy2(yaml_path, cfg_yaml)

    print("\n── Results ──────────────────────────")
    total_imgs = 0
    for split, c in counts.items():
        print(f"  {split:6s}: {c['images']:4d} imgs  {c['labels']:4d} labels")
        total_imgs += c["images"]
    print(f"  TOTAL : {total_imgs} images")
    print(f"\n  Unified YAML → {cfg_yaml}")
    print(f"  Merged data  → {MERGED_DIR}")
    print("\nDone.\n")


if __name__ == "__main__":
    merge()
