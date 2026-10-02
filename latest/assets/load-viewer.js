// Restore the exact embedded model payload before running the unchanged viewer.
(() => {
  'use strict';
  const assetBase = new URL('.', document.currentScript.src);
  const files = ["geometry-01.json", "geometry-02.json", "geometry-03.json", "geometry-04.json", "geometry-05.json", "geometry-06.json", "geometry-07.json", "geometry-08.json", "geometry-09.json"];
  async function start() {
    try {
      const parts = await Promise.all(files.map(async name => {
        const response = await fetch(new URL(name, assetBase));
        if (!response.ok) throw new Error(`Recurso ${name}: HTTP ${response.status}`);
        const text = await response.text();
        if (!text.startsWith('[') || !text.endsWith(']')) throw new Error(`Datos inválidos: ${name}`);
        return text.slice(1, -1);
      }));
      document.getElementById('geometry').textContent = '[' + parts.join(',') + ']';
      const script = document.createElement('script');
      script.src = new URL('viewer.js', assetBase).href;
      script.onerror = () => fail(new Error('No se ha podido cargar el código del visor.'));
      document.body.appendChild(script);
    } catch (error) { fail(error); }
  }
  function fail(error) {
    window.__villaReady = false;
    window.__villaLoadError = String(error.message || error);
    document.getElementById('error').textContent = 'No se ha podido iniciar el modelo. Detalle: ' + window.__villaLoadError;
    console.error(error);
  }
  start();
})();
