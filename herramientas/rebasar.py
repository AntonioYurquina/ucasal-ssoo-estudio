"""Adapta el espejo VitePress (base "/") para servirse bajo una subruta, p. ej. /ucasal-ssoo-estudio/."""
import os, re, sys

DIR, BASE = sys.argv[1], sys.argv[2]          # BASE con barras: /ucasal-ssoo-estudio/
assert BASE.startswith("/") and BASE.endswith("/")
SUB = BASE[1:]                                # ucasal-ssoo-estudio/
# Lo que hay en la raíz del espejo (carpetas y archivos) es lo único que se reescribe:
# así no se tocan rutas virtuales de Sandpack (/src, /pages) ni expresiones regulares.
# Sin los .html/.json de la raíz: sólo los nombran las plantillas virtuales de Sandpack
# ("/index.html") y el router, que ya usa la base de los datos del sitio.
_entradas = [e for e in os.listdir(DIR) if not e.startswith(".") and not e.endswith((".html", ".json"))]
RAICES = "(?:" + "|".join(re.escape(e) + (r"(?=[/\"'`#?\\])" if os.path.isdir(os.path.join(DIR, e)) else r"(?![\w.-])")
                          for e in sorted(_entradas, key=len, reverse=True)) + ")"

AVISO = ('<div id="copia-estudio" style="position:fixed;right:10px;bottom:10px;z-index:9999;max-width:260px;'
         'padding:6px 10px;border-radius:8px;font:12px/1.4 system-ui,sans-serif;background:rgba(30,30,30,.82);color:#fff">'
         'Copia de estudio no oficial de '
         '<a href="https://ucasal-ssoo.vercel.app/" style="color:#9cdcfe" rel="noopener">ucasal-ssoo.vercel.app</a> '
         '(26/10/2026). El contenido pertenece a su autor.</div>')

def reescribir_html(s):
    s = s.replace('\\"base\\":\\"/\\"', '\\"base\\":\\"' + BASE + '\\"')
    s = re.sub(r'((?:href|src|content)=")/(?!/)', r'\1' + BASE, s)
    s = re.sub(r'(import\s*["\'])/(?!/)', r'\1' + BASE, s)
    s = re.sub(r'url\(/(?!/)', 'url(' + BASE, s)
    if 'name="robots"' not in s:
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n    <meta name="robots" content="noindex, nofollow">', 1)
    if 'id="copia-estudio"' not in s:
        s = s.replace('</body>', AVISO + '</body>', 1)
    return s

def reescribir_js(s, nombre):
    if nombre.startswith("framework."):
        n_antes = s.count('const n="/";t=_i(')
        s = s.replace('const n="/";t=_i(', 'const n="' + BASE + '";t=_i(')
        p_antes = s.count('function(e){return"/"+e}')
        s = s.replace('function(e){return"/"+e}', 'function(e){return"' + BASE + '"+e}')
        assert n_antes == 1 and p_antes == 1, (n_antes, p_antes)
    # Literales y atributos absolutos dentro de los chunks de páginas y del tema.
    # Los valores de "link" (frontmatter, menú) los prefija el tema con withBase en tiempo de
    # ejecución: reescribirlos daría base duplicada. Sólo se tocan href/src compilados y URLs de assets.
    def prefijar(m):
        previo = s[max(0, m.start() - 10):m.start()]
        if re.search(r'link\\?"?\s*:\s*$', previo):
            return m.group(0)
        return m.group(1) + BASE + m.group(2)
    s = re.sub(r'(["\'`]|\\")/(' + RAICES + ')', prefijar, s)
    return s

def reescribir_css(s):
    return re.sub(r'url\((["\']?)/(?!/)', lambda m: 'url(' + m.group(1) + BASE, s)

contador = {"html": 0, "js": 0, "css": 0}
for raiz, _, archivos in os.walk(DIR):
    if "/.git" in raiz:
        continue
    for a in archivos:
        p = os.path.join(raiz, a)
        if a.endswith(".html"):
            f, k = reescribir_html, "html"
        elif a.endswith(".js"):
            f, k = (lambda s, a=a: reescribir_js(s, a)), "js"
        elif a.endswith(".css"):
            f, k = reescribir_css, "css"
        else:
            continue
        s = open(p, encoding="utf-8").read()
        if BASE in s and k != "html":
            continue  # ya adaptado
        nuevo = f(s)
        if nuevo != s:
            open(p, "w", encoding="utf-8").write(nuevo); contador[k] += 1
print("modificados:", contador)
