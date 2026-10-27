"""Servidor estático que imita la resolución de rutas de GitHub Pages."""
import http.server, os, sys, urllib.parse
RAIZ = os.path.abspath(sys.argv[1]); PUERTO = int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=RAIZ, **k)
    def log_message(self, *a): pass
    def send_head(self):
        ruta = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        local = os.path.join(RAIZ, ruta.lstrip("/"))
        for cand in (local, local + ".html", os.path.join(local, "index.html")):
            if os.path.isfile(cand):
                self.path = "/" + os.path.relpath(cand, RAIZ)
                return super().send_head()
        partes = ruta.strip("/").split("/")
        cuatro = os.path.join(RAIZ, partes[0], "404.html") if partes and partes[0] else None
        if cuatro and os.path.isfile(cuatro):
            datos = open(cuatro, "rb").read()
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(datos))); self.end_headers()
            self.wfile.write(datos); return None
        self.send_error(404); return None
http.server.ThreadingHTTPServer(("127.0.0.1", PUERTO), H).serve_forever()
