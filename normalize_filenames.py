import os
import unicodedata
import shutil
import filecmp
from collections import defaultdict
from datetime import datetime
import sys

# Log file setup
LOG_PATH = os.path.join(sys.argv[1], "log.txt")
log_lines = []

def log(message):
    print(message)
    log_lines.append(message)

stats = {
    'files_renamed': 0,
    'files_deleted': 0,
    'file_conflicts': 0,
    'dirs_renamed': 0,
    'dirs_deleted': 0,
    'dir_conflicts': 0,
    'errors': []
}

def normalize_unicode(name):
    return unicodedata.normalize('NFC', name)

def remove_accents_and_specials(name):
    name = normalize_unicode(name)
    name = name.replace('ñ', 'n').replace('Ñ', 'N')
    nfkd_form = unicodedata.normalize('NFKD', name)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c) and ord(c) < 128])

def safe_file_rename(src, dst):
    try:
        if src == dst:
            return
        if os.path.exists(dst):
            try:
                if filecmp.cmp(src, dst, shallow=False):
                    os.remove(src)
                    log(f"🗑️ Eliminando archivo duplicado (idéntico): {src}")
                    stats['files_deleted'] += 1
                else:
                    log(f"⚠️ Archivo duplicado con conflicto:\n  - {src}\n  - {dst}")
                    stats['file_conflicts'] += 1
            except Exception as e:
                stats['errors'].append(f"[filecmp error] {src} vs {dst}: {e}")
        else:
            os.rename(src, dst)
            log(f"📄 Renombrado archivo:\n  {src}\n  -> {dst}")
            stats['files_renamed'] += 1
    except Exception as e:
        stats['errors'].append(f"[rename file] {src} -> {dst}: {e}")

def safe_dir_rename(src, dst):
    try:
        if src == dst or not os.path.exists(src):
            return
        if os.path.exists(dst):
            if compare_dirs(src, dst):
                shutil.rmtree(src)
                log(f"🗑️ Eliminando carpeta duplicada (idéntica): {src}")
                stats['dirs_deleted'] += 1
            else:
                log(f"⚠️ Carpeta duplicada con conflicto:\n  - {src}\n  - {dst}")
                stats['dir_conflicts'] += 1
        else:
            os.rename(src, dst)
            log(f"📁 Renombrado carpeta:\n  {src}\n  -> {dst}")
            stats['dirs_renamed'] += 1
    except Exception as e:
        stats['errors'].append(f"[rename dir] {src} -> {dst}: {e}")

def compare_dirs(dir1, dir2):
    try:
        cmp = filecmp.dircmp(dir1, dir2)
        if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
            return False
        for sub in cmp.common_dirs:
            if not compare_dirs(os.path.join(dir1, sub), os.path.join(dir2, sub)):
                return False
        return True
    except Exception as e:
        stats['errors'].append(f"[compare_dirs] {dir1} vs {dir2}: {e}")
        return False

def sanitize_all(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            try:
                original = os.path.join(dirpath, filename)
                clean_name = remove_accents_and_specials(filename)
                normalized_name = normalize_unicode(clean_name)
                new_path = os.path.join(dirpath, normalized_name)
                safe_file_rename(original, new_path)
            except Exception as e:
                stats['errors'].append(f"[sanitize file] {original}: {e}")

    folder_map = defaultdict(list)
    for dirpath, dirnames, _ in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            try:
                cleaned = remove_accents_and_specials(dirname)
                normalized = normalize_unicode(cleaned)
                full_path = os.path.join(dirpath, dirname)
                folder_map[(dirpath, normalized)].append(full_path)
            except Exception as e:
                stats['errors'].append(f"[prepare folder] {dirname} in {dirpath}: {e}")

    for (dirpath, clean_name), paths in folder_map.items():
        try:
            if len(paths) > 1:
                paths_sorted = sorted(paths)
                keep = paths_sorted[0]
                for dup in paths_sorted[1:]:
                    safe_dir_rename(dup, keep)
                final_path = os.path.join(dirpath, clean_name)
                if keep != final_path and not os.path.exists(final_path):
                    os.rename(keep, final_path)
                    log(f"📁 Renombrado carpeta (limpia):\n  {keep}\n  -> {final_path}")
                    stats['dirs_renamed'] += 1
            else:
                original = paths[0]
                final_path = os.path.join(dirpath, clean_name)
                safe_dir_rename(original, final_path)
        except Exception as e:
            stats['errors'].append(f"[process folder] {paths}: {e}")

def print_summary():
    log("\n📊 RESUMEN DE OPERACIÓN")
    log("-" * 40)
    log(f"Archivos renombrados            : {stats['files_renamed']}")
    log(f"Archivos eliminados (idénticos) : {stats['files_deleted']}")
    log(f"Archivos con conflicto          : {stats['file_conflicts']}")
    log(f"Carpetas renombradas            : {stats['dirs_renamed']}")
    log(f"Carpetas eliminadas (idénticas) : {stats['dirs_deleted']}")
    log(f"Carpetas con conflicto          : {stats['dir_conflicts']}")
    log(f"Errores durante la operación    : {len(stats['errors'])}")
    log("-" * 40)

    if stats['errors']:
        log("\n❌ ERRORES DETECTADOS:")
        for error in stats['errors']:
            log(" - " + error)

    try:
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            f.write(f"Log de ejecución - {datetime.now()}\n\n")
            f.write('\n'.join(log_lines))
        log(f"\n📝 Log guardado en: {LOG_PATH}")
    except Exception as e:
        print(f"❌ Error al guardar log.txt: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python sanitize_and_deduplicate.py <ruta>")
        sys.exit(1)

    base_path = sys.argv[1]

    if not os.path.isdir(base_path):
        print(f"❌ Ruta no válida: {base_path}")
        sys.exit(1)

    sanitize_all(base_path)
    print_summary()
    print("✅ Proceso completado: nombres limpios y deduplicados.")
    print("Consulta log.txt en la carpeta procesada para el detalle completo.")
    sys.exit(0)
# End of the code snippet
