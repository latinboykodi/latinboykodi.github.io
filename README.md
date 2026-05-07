# Latin Boy Repository para Kodi

Repositorio de add-ons para Kodi 21 Omega (compatible con versiones anteriores).

## Estructura del repositorio

```
latinboy-repo/
│
├── repository.latinboy/        ← Addon del repositorio en sí
│   ├── addon.xml               ← Definición del repo (ID, URLs, metadata)
│   ├── icon.png                ← Ícono del repositorio
│   └── fanart.jpg              ← Fanart del repositorio
│
├── zips/                       ← Aquí van todos tus add-ons
│   ├── repository.latinboy/    ← Zip del repo mismo
│   │   └── repository.latinboy-1.0.0.zip
│   └── plugin.tu.addon/        ← Ejemplo de un add-on
│       ├── addon.xml           ← addon.xml de ESE add-on
│       └── plugin.tu.addon-1.0.0.zip
│
├── addons.xml                  ← Generado automáticamente (NO editar a mano)
├── addons.xml.md5              ← Generado automáticamente (NO editar a mano)
└── generate_repo.py            ← Script para regenerar addons.xml
```

## Pasos para publicar el repositorio

### 1. Subir a GitHub Pages

1. Crea un repositorio en GitHub llamado `latinboykodi.github.io`
2. Sube todos los archivos de esta carpeta a la raíz del repo
3. En Settings → Pages → activa GitHub Pages desde la rama `main`
4. Tu repositorio estará en: `https://latinboykodi.github.io/`

### 2. Generar el zip del repositorio

```bash
cd latinboy-repo
python generate_repo.py
```

Esto crea/actualiza `addons.xml` y `addons.xml.md5`.

Luego crea el zip del addon del repo:
```bash
cd zips/repository.latinboy
zip -r repository.latinboy-1.0.0.zip ../../../repository.latinboy/
```

### 3. Agregar un nuevo add-on

1. Crea la carpeta: `zips/plugin.tu.addon/`
2. Pon el `addon.xml` de tu add-on dentro
3. Crea el zip del add-on dentro de esa carpeta
4. Ejecuta `python generate_repo.py`
5. Sube los cambios a GitHub

### 4. Instalar en Kodi

1. En Kodi ve a: **Configuración → Administrador de archivos → Añadir fuente**
2. URL: `https://latinboykodi.github.io`
3. Nombre: `latinboy`
4. Luego ve a: **Add-ons → Instalar desde zip → latinboy**
5. Selecciona `repository.latinboy-1.0.0.zip`
6. Finalmente: **Add-ons → Instalar desde repositorio → Latin Boy Repository**

## Notas importantes

- Cada vez que actualices un add-on o agregues uno nuevo, **debes volver a ejecutar** `generate_repo.py`
- El archivo `addons.xml` debe ser accesible públicamente en la URL configurada
- El ID del repositorio (`repository.latinboy`) debe coincidir **exactamente** con el nombre de la carpeta y el zip
