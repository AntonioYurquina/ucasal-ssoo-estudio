"""Descarga el sitio VitePress ucasal-ssoo.vercel.app a una carpeta, con todos sus assets."""
import json, os, re, sys, time, urllib.parse, urllib.request

ORIGEN = "https://ucasal-ssoo.vercel.app"
DEST = sys.argv[1]
HM = json.load(open(sys.argv[2], encoding="utf-8"))

def bajar(ruta_url, ruta_local):
    destino = os.path.join(DEST, ruta_local)
    if os.path.exists(destino):
        return True
    url = ORIGEN + urllib.parse.quote(ruta_url, safe="/%:")
    for intento in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (copia de estudio)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                datos = r.read()
            os.makedirs(os.path.dirname(destino) or DEST, exist_ok=True)
            open(destino, "wb").write(datos)
            return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("404", ruta_url); return False
            time.sleep(2 ** intento)
        except Exception as e:
            time.sleep(2 ** intento)
    print("FALLO", ruta_url); return False

# 1) Páginas: clave del hashmap -> URL limpia y archivo .html
paginas = []
for clave, h in HM.items():
    base = clave[:-3]  # sin .md
    if base.startswith("public_"):
        continue
    partes = base.split("_")
    if partes[-1] == "index":
        url = "/" + "/".join(partes[:-1]) + ("/" if len(partes) > 1 else "")
        local = "/".join(partes[:-1] + ["index.html"])
    else:
        url = "/" + "/".join(partes)
        local = "/".join(partes) + ".html"
    paginas.append((url, local))
    for suf in (".js", ".lean.js"):
        bajar(f"/assets/{clave}.{h}{suf}", f"assets/{clave}.{h}{suf}")
for url, local in paginas:
    bajar(url, local)
bajar("/404.html", "404.html")
bajar("/vp-icons.css", "vp-icons.css")
print("páginas:", len(paginas))

# 2) Cierre de assets: seguir referencias en HTML, JS y CSS
pat_abs = re.compile(r'["\'(=]\s*(/(?:assets|[\w.-]+\.(?:svg|png|jpe?g|gif|webp|ico|css|js|json|woff2?|ttf|txt|c|h|py|mp4|pdf))[^"\')\s>]*)')
pat_rel_js = re.compile(r'["\'](\./[\w./-]+\.(?:js|css|woff2?))["\']')
pat_css_url = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')
visto = set()
cambios = True
while cambios:
    cambios = False
    for raiz, _, archivos in os.walk(DEST):
        if "/.git" in raiz:
            continue
        for a in archivos:
            p = os.path.join(raiz, a)
            if p in visto or not a.endswith((".html", ".js", ".css")):
                continue
            visto.add(p); cambios = True
            texto = open(p, encoding="utf-8", errors="ignore").read()
            rel_dir = os.path.relpath(raiz, DEST)
            refs = set(m.group(1) for m in pat_abs.finditer(texto))
            if a.endswith(".js"):
                for m in pat_rel_js.finditer(texto):
                    refs.add("/" + os.path.normpath(os.path.join(rel_dir, m.group(1))))
                for m in re.finditer(r'"(assets/[\w./-]+\.(?:js|css|woff2?|svg|png))"', texto):
                    refs.add("/" + m.group(1))
            if a.endswith(".css"):
                for m in pat_css_url.finditer(texto):
                    u = m.group(1)
                    if u.startswith("data:") or u.startswith("http"):
                        continue
                    refs.add(u if u.startswith("/") else "/" + os.path.normpath(os.path.join(rel_dir, u)))
            for r in refs:
                r = r.split("?")[0].split("#")[0]
                if not r or r == "/" or r.startswith("//") or r.endswith("/"):
                    continue
                bajar(r, r.lstrip("/"))
print("archivos revisados:", len(visto))
