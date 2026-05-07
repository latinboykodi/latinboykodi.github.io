#!/usr/bin/env python3
"""
Generador de addons.xml para repositorio Kodi - Latinboy
Uso: python generate_repo.py
"""

import os
import hashlib
import xml.etree.ElementTree as ET
from xml.dom import minidom

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
ZIPS_DIR = os.path.join(REPO_DIR, "zips")
OUTPUT_XML = os.path.join(REPO_DIR, "addons.xml")
OUTPUT_MD5 = os.path.join(REPO_DIR, "addons.xml.md5")


def get_addon_info(addon_xml_path):
    """Lee el addon.xml y extrae la info del addon."""
    try:
        tree = ET.parse(addon_xml_path)
        return tree.getroot()
    except Exception as e:
        print(f"  [ERROR] No se pudo leer {addon_xml_path}: {e}")
        return None


def generate_addons_xml():
    """Genera el archivo addons.xml con todos los addons del repo."""
    print("Generando addons.xml...")

    addons_element = ET.Element("addons")

    # Incluir el addon del propio repositorio
    repo_addon_xml = os.path.join(REPO_DIR, "repository.latinboy", "addon.xml")
    if os.path.exists(repo_addon_xml):
        addon_root = get_addon_info(repo_addon_xml)
        if addon_root is not None:
            addons_element.append(addon_root)
            print(f"  + repository.latinboy (el repo mismo)")

    # Buscar addons en la carpeta zips/
    if os.path.exists(ZIPS_DIR):
        for addon_id in sorted(os.listdir(ZIPS_DIR)):
            addon_folder = os.path.join(ZIPS_DIR, addon_id)
            if not os.path.isdir(addon_folder):
                continue

            addon_xml_path = os.path.join(addon_folder, "addon.xml")
            if not os.path.exists(addon_xml_path):
                print(f"  [SKIP] {addon_id} — sin addon.xml")
                continue

            addon_root = get_addon_info(addon_xml_path)
            if addon_root is not None:
                addons_element.append(addon_root)
                version = addon_root.get("version", "?")
                print(f"  + {addon_id} v{version}")

    # Escribir XML con formato bonito
    raw_xml = ET.tostring(addons_element, encoding="unicode")
    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="    ")
    # Quitar la línea <?xml?> duplicada que agrega minidom
    lines = pretty_xml.splitlines()
    clean_xml = "\n".join(lines[1:])  # saltar la primera línea del minidom
    final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + clean_xml

    with open(OUTPUT_XML, "w", encoding="utf-8") as f:
        f.write(final_xml)

    print(f"\narchivo creado: addons.xml ({len(final_xml)} bytes)")
    return final_xml


def generate_md5(content):
    """Genera el archivo addons.xml.md5."""
    md5 = hashlib.md5(content.encode("utf-8")).hexdigest()
    with open(OUTPUT_MD5, "w", encoding="utf-8") as f:
        f.write(md5)
    print(f"archivo creado: addons.xml.md5 ({md5})")


def create_zip_for_addon(addon_id):
    """
    Crea el zip de un addon dentro de zips/<addon_id>/
    Uso: llama esto manualmente cuando agregues un nuevo addon.
    """
    import zipfile
    addon_src = os.path.join(ZIPS_DIR, addon_id)
    addon_xml = os.path.join(addon_src, "addon.xml")

    if not os.path.exists(addon_xml):
        print(f"No existe {addon_xml}")
        return

    tree = ET.parse(addon_xml)
    version = tree.getroot().get("version", "0.0.1")
    zip_name = f"{addon_id}-{version}.zip"
    zip_path = os.path.join(ZIPS_DIR, addon_id, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(addon_src):
            # No incluir zips dentro del zip
            dirs[:] = [d for d in dirs if not d.endswith(".zip")]
            for file in files:
                if file.endswith(".zip"):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ZIPS_DIR)
                zf.write(file_path, arcname)

    print(f"Zip creado: {zip_path}")


if __name__ == "__main__":
    xml_content = generate_addons_xml()
    generate_md5(xml_content)
    print("\n¡Listo! Sube los archivos a GitHub Pages.")
