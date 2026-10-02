# Villa Manuela · Visor clientes v01

Fuente visual y geometría: `VILLA_MANUELA_VISOR_RECONSTRUIDO-v02.html` (separación con S0 fijo). `latest` se utilizó únicamente para el método de carga externa, la clasificación validada de elementos del entorno y el sistema nocturno de 29 luminarias y mapas de sombras. La geometría de origen conserva sus **8.266 objetos** sin cambios semánticos; no se editó el visor previo.

`index.html` pesa **0.008 MiB** (8298 bytes). Los recursos están en `assets/`: nueve bloques `geometry-01.json`…`geometry-09.json`, `viewer.js`, `viewer.css`, `load-viewer.js`, inventario `night-lights.json` y clasificación `external-indices.json`. El archivo individual más grande ocupa **14.165 MiB**, por debajo de 25 MiB.

Para publicarlo, subir **toda esta carpeta** manteniendo las rutas relativas. `index.html` es la entrada. En Cloudflare Pages, usar esta carpeta como directorio de publicación, sin proceso de compilación. Para probar localmente: `python3 -m http.server 8000` dentro de la carpeta y abrir la dirección HTTP indicada por el servidor. La carga de JSON requiere HTTP; abrir `index.html` directamente desde disco no es equivalente.

La interfaz conserva Vistas, Plantas, Fachadas y Visualización. Se eliminaron la sección de cámaras de marketing/interiores, los controles de formato/captura limpia y el botón de verja. Se añadieron Iluminación Día/Noche y Contexto Entorno/Solo parcela. La verja permanece cerrada en la geometría, sin eliminarse.

Validación: carga HTTP sin errores ni 404, WebGL sin errores, Día↔Noche, Entorno↔Solo parcela, plantas, fachadas, vistas, visualización y combinación Noche + Solo parcela + separación + planta/fachada oculta. A 6 m de separación: terreno y S0 = 0, PB = 6, P1 = 12, P2 = 18, cubierta = 24 m. Restaurar a 0 recupera las posiciones iniciales.

El GLB histórico no se incluye porque el visor ejecuta directamente la geometría JSON y el GLB aumentaría el paquete sin intervenir en la carga web.
