#!/usr/bin/env python3
"""
clingo_graph_visualizer.py

Ejecuta clingo con un programa lógico dado, extrae predicados `nodo(X)` y `arista(X,Y)`
(y solo esos), y genera una página HTML que visualiza el grafo usando Bulma CSS y vis-network.

Uso:
    python clingo_graph_visualizer.py --program programa.lp --output grafo.html

Requisitos: tener instalado `clingo` accesible desde la línea de comandos.
"""
import re
import json
import argparse
import subprocess
import sys

PRED_NODO = re.compile(r"\bnodo\s*\(\s*([^(),\s]+)\s*\)")
PRED_ARISTA = re.compile(r"\barista\s*\(\s*([^(),\s]+)\s*,\s*([^(),\s]+)\s*\)")

# Códigos de salida aceptables de clingo
CLINGO_OK_CODES = {0, 10, 20, 30}


def run_clingo(program_file, extra_args=None):
    """Ejecuta clingo y devuelve su salida como string."""
    cmd = ["clingo", program_file]
    if extra_args:
        cmd.extend(extra_args)
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode not in CLINGO_OK_CODES:
        print("❌ Error al ejecutar clingo:", res.stderr, file=sys.stderr)
        sys.exit(res.returncode)

    # Mensajes lindos según código de salida
    if res.returncode == 0:
        print("✨ Clingo ejecutado correctamente (código 0)")
    elif res.returncode == 10:
        print("✅ Resultado: SATISFACIBLE (¡Se encontró un modelo!) 😍")
    elif res.returncode == 20:
        print("⚠️ Resultado: INSATISFACIBLE (no hay solución posible) 😢")
    elif res.returncode == 30:
        print("🏆 Resultado: ÓPTIMO ENCONTRADO (¡La mejor solución!) 🌟")

    return res.stdout


def parse_clingo_output(text):
    """Extrae nodos y aristas del texto de salida de clingo."""
    nodos = set(PRED_NODO.findall(text))
    aristas = set(PRED_ARISTA.findall(text))

    for u, v in aristas:
        nodos.add(u)
        nodos.add(v)

    return nodos, aristas


HTML_TEMPLATE = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Grafo - Visualización</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
  <link href="https://unpkg.com/vis-network/styles/vis-network.css" rel="stylesheet" type="text/css" />
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    #network {
      width: 100%;
      height: 70vh;
      border: 1px solid #ddd;
      border-radius: 8px;
    }
  </style>
</head>
<body>
<section class="section">
  <div class="container">
    <h1 class="title">🌈 Visualizador de grafo (clingo) 🌈</h1>
    <div class="box">
      <p><strong>Nodos:</strong> <span id="node-count"></span> • <strong>Aristas:</strong> <span id="edge-count"></span></p>
      <div id="network"></div>
    </div>
    <p class="has-text-centered">Hecho con ❤️ y ✨ usando <code>clingo</code> + <code>Python</code> + <code>Bulma</code></p>
  </div>
</section>
<script>
const nodesData = {nodes_json};
const edgesData = {edges_json};

document.getElementById('node-count').textContent = nodesData.length;
document.getElementById('edge-count').textContent = edgesData.length;

const container = document.getElementById('network');
const data = {
  nodes: new vis.DataSet(nodesData),
  edges: new vis.DataSet(edgesData)
};
const options = {
  nodes: { shape: 'dot', size: 16, font: {size: 14} },
  edges: { smooth: {type:'dynamic'} },
  physics: { stabilization: true, barnesHut: {gravitationalConstant: -2000} }
};
new vis.Network(container, data, options);
</script>
</body>
</html>
"""


def build_html(nodes, edges):
    nodes_list = [{"id": n, "label": str(n)} for n in sorted(nodes, key=str)]
    # Para grafo no dirigido, aseguramos aristas únicas (u,v) con u<=v
    unique_edges = set()
    for u, v in edges:
        if u > v:
            u, v = v, u
        unique_edges.add((u, v))
    edges_list = [{"from": u, "to": v} for u, v in sorted(unique_edges, key=lambda x: (str(x[0]), str(x[1])))]

    html = HTML_TEMPLATE.replace('{nodes_json}', json.dumps(nodes_list))
    html = html.replace('{edges_json}', json.dumps(edges_list))
    return html


def main():
    parser = argparse.ArgumentParser(description='Ejecuta clingo y genera una visualización HTML del grafo.')
    parser.add_argument('--program', '-p', required=True, help='Archivo del programa en ASP para clingo.')
    parser.add_argument('--output', '-o', help='Archivo HTML de salida. Si se omite, escribe stdout.')
    parser.add_argument('--clingo-args', nargs=argparse.REMAINDER, help='Argumentos extra para clingo (opcionales).')
    args = parser.parse_args()

    clingo_output = run_clingo(args.program, args.clingo_args)
    nodes, edges = parse_clingo_output(clingo_output)
    html = build_html(nodes, edges)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"🎉 Archivo HTML generado: {args.output} 🌐")
    else:
        sys.stdout.write(html)


if __name__ == '__main__':
    main()
