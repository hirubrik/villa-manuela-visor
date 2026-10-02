# Villa Manuela · estado del proyecto para GitHub

- Proyecto actual conservado: landing editorial, imágenes y etiquetas, media.json, lightbox, vídeos, descargas y página propia del visor.
- Presentación: un único elemento de Documentación con VER PRESENTACIÓN como acción principal y VER / DESCARGAR PDF como acción secundaria. Ambos abren una pestaña nueva con rel=noopener y sin descargar automáticamente.
- Presentación HTML con 40 imágenes embebidas; fuentes externas de Google Fonts conservadas.
- PDF sustituido por el usuario: 16.904.694 bytes (16,9 MB / 16,1 MiB), sin modificación posterior. Peso retirado de la landing.
- Todos los archivos individuales están bajo el límite de 25 MiB de Cloudflare Pages. No queda el bloqueo de publicación anterior por tamaño del PDF.
- Rama 3D: Clientes v01, con una sola copia del motor y nueve bloques de geometría. HTML, lógica, estilos y datos del visor intactos.
- Rutas relativas. Sin rutas del Mac ni direcciones locales en los archivos de texto del proyecto.
- Pruebas anteriores por HTTP: presentación completa en pestaña nueva, PDF visualizado en el navegador, navegación, imágenes, lightbox y responsive. Visor con 8.266 objetos; regreso a landing, controles y fullscreen verificados sin errores de consola ni WebGL.
- Pendientes de incorporar: ZIP de Imágenes HD, Vídeos, Planos y Material gráfico; también los tres archivos de vídeo. Sus elementos y miniaturas se conservan y los enlaces inexistentes permanecen desactivados.
- Estructura compatible con GitHub y Cloudflare Pages, sin backend ni compilación. No se ha hecho push ni despliegue.

## Uso del ZIP

Descomprimir y subir el contenido de villa-manuela-landing al directorio servido por el repositorio. Mantener las subcarpetas, nombres y rutas. La raíz publicada debe contener index.html. No hace falta subir el ZIP como archivo de la web.

El ZIP excluye únicamente metadatos del sistema (.DS_Store, AppleDouble y __MACOSX); incluye los archivos de la web y su documentación.
