# 🧼 Sanitize and Deduplicate: Limpieza de nombres de archivos y carpetas

Este script en Python permite limpiar y normalizar los nombres de archivos y carpetas de manera **recursiva** en una ruta especificada. Es útil en entornos con múltiples sistemas operativos (Windows, macOS, Linux), donde los nombres de archivos pueden entrar en conflicto debido a diferencias de codificación UTF-8, uso de caracteres especiales, o problemas con sincronizadores como **Syncthing**.

---

## ✨ Funcionalidades

- ✅ Normaliza todos los nombres a Unicode **NFC**.
- ✅ Elimina acentos, diéresis, eñes y otros caracteres conflictivos.
- ✅ Renombra archivos y carpetas recursivamente.
- ✅ Detecta y elimina **duplicados idénticos**.
- ✅ Detecta conflictos sin borrar nada si los contenidos son diferentes.
- ✅ Maneja errores sin detener la ejecución.
- ✅ Guarda un **log detallado** de todo lo hecho en un archivo `log.txt` dentro de la carpeta procesada.

---

## 🛠️ Requisitos

- Python 3.x  
(No requiere librerías externas.)

---

## 🚀 Uso

Desde terminal o consola:

```bash
python sanitize_and_deduplicate.py "RUTA/A/TU/CARPETA"
```

Ejemplo:

```bash
python sanitize_and_deduplicate.py "D:\Docencia"
```

---

## 📦 Qué hace exactamente

1. **Antes**:
```
Guía de estudio.docx
Diseño y programación.pdf
Bibliografía/
```

2. **Después**:
```
Guia de estudio.docx
Diseno y programacion.pdf
Bibliografia/
```

3. Si existían duplicados como:
```
Guía de estudio.docx  ← codificado en NFD
Guía de estudio.docx  ← codificado en NFC
```
El script detectará si son idénticos y **eliminará uno**.

---

## 📊 Al final, imprime un resumen como este:

```
📊 RESUMEN DE OPERACIÓN
----------------------------------------
Archivos renombrados            : 48
Archivos eliminados (idénticos) : 3
Archivos con conflicto          : 2
Carpetas renombradas            : 19
Carpetas eliminadas (idénticas) : 4
Carpetas con conflicto          : 1
Errores durante la operación    : 0

📝 Log guardado en: D:\Docencia\log.txt
```

---

## 🧠 Consideraciones

- Asegúrate de tener **permisos de escritura** sobre la ruta procesada.
- Cierra programas que estén usando los archivos antes de ejecutar.
- El script es **seguro**: solo elimina duplicados **si el contenido es exactamente igual**.
- Si hay errores de permisos, aparecerán en el log.

---

## 🧑‍💻 Autor

Script creado por mi, ja ja ja!.

---