# SSOO UCASAL — copia de estudio

Copia estática, **no oficial**, del sitio de apuntes de Sistemas Operativos
[ucasal-ssoo.vercel.app](https://ucasal-ssoo.vercel.app/), tomada el **26/10/2026**
para poder seguir estudiando si el original deja de estar en línea.

**Ver la copia:** https://antonioyurquina.github.io/ucasal-ssoo-estudio/

## Autoría

El contenido pertenece a su autor. El sitio original no lo menciona (el único
enlace a GitHub que tiene es el que VitePress trae por defecto) y su código fuente
no está publicado, así que no se pudo identificar. Esta copia no agrega ni cambia
contenido: sólo adapta las rutas para servirse desde GitHub Pages. Cada página
lleva un aviso con el enlace al original y está marcada `noindex` para que no
compita con él en buscadores.

Si sos el autor y preferís que la copia no esté publicada, abrí un issue y se baja.

## Qué contiene

Las 55 páginas del sitio, con sus imágenes, simuladores y fórmulas:

| Sección | Temas |
|---|---|
| **Unidad 1** — Introducción a los SO | Funciones del SO, lenguaje máquina y microprogramación, latencias de lectura (con visualizaciones interactivas), modo usuario y kernel, shell (simple shell en C y en Node.js), fecha y hora, instrucciones en modo kernel, multiprogramación, spooling, computadoras de segunda generación, tiempo compartido, llamadas al sistema, programas y procesos, sistemas de archivos, dispositivos de E/S, cálculo de tiempo de acceso, máquinas virtuales, unidades |
| **Unidad 2** — Procesos y memoria | Fragmentación, administración de memoria, simulación de particiones, algoritmos de asignación, tiempo de compactación, multiprogramación, simulación de procesos |
| **Unidad 3** — Administración de memoria | Paginación, fallos de página, memoria virtual, algoritmos de reemplazo, segmentación, tamaño óptimo de página |
| **Repaso para el parcial** | Multiprogramación, administración de memoria, fragmentación, modelo probabilístico, cálculos de paginación, tamaño de página, algoritmos de reemplazo, procesos y programas, estados de un proceso, spooling. *En el original no figura en el menú lateral:* se entra por [`/repaso/`](https://antonioyurquina.github.io/ucasal-ssoo-estudio/repaso/). |
| **Conversión de unidades** | Prefijos binarios y decimales, conversores binario/decimal y de tiempo |

Funciona sin conexión salvo dos cosas: la tipografía (Google Fonts; sin internet
se usa la del sistema) y el editor de código en vivo de "Fecha y Hora", que
depende de CodeSandbox.

## Verla sin internet, en tu máquina

```bash
git clone https://github.com/AntonioYurquina/ucasal-ssoo-estudio.git
python3 ucasal-ssoo-estudio/herramientas/servidor_pages.py . 8000
# abrir http://localhost:8000/ucasal-ssoo-estudio/
```

El servidor imita a GitHub Pages (resuelve `/ruta` a `ruta.html`), así que hay
que levantarlo desde la carpeta que **contiene** al repositorio.

## Actualizar la copia

Si el original publica cambios y sigue en línea:

```bash
# 1. Bajar el sitio con el hashmap actual (está incrustado en cualquier página, en __VP_HASH_MAP__)
python3 herramientas/espejar.py /tmp/espejo herramientas/hashmap-26-10-2026.json
# 2. Adaptarlo a la subruta de GitHub Pages
python3 herramientas/rebasar.py /tmp/espejo /ucasal-ssoo-estudio/
# 3. Copiar /tmp/espejo encima de este repo, revisar y commitear
```

## Cómo está hecha

- El original es un sitio [VitePress](https://vitepress.dev/) 1.6.4 desplegado en
  Vercel en la raíz (`/`). GitHub Pages lo sirve en `/ucasal-ssoo-estudio/`, así
  que `herramientas/rebasar.py` cambia la base en los datos del sitio, en el router
  y en el helper de precarga de Vite, y prefija las rutas absolutas de HTML, CSS y
  de los chunks de cada página. No toca los enlaces que el tema ya prefija solo
  (frontmatter y menú) ni los archivos virtuales de Sandpack.
- `.nojekyll` evita que GitHub Pages ignore los archivos que empiezan con `_`.
- Verificación del 26/10/2026: el texto de las 55 páginas coincide con el original,
  salvo "Fecha y Hora", que muestra un reloj en vivo. La navegación del menú, el
  paginador, las fórmulas (MathJax), las imágenes y las visualizaciones de latencia
  funcionan sin errores en consola.
