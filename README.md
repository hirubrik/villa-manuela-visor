# Villa Manuela · landing estática

Versión visual corregida según el mockup. HTML, CSS y JavaScript vanilla, sin dependencias externas, backend ni publicación.

## Revisión local

Desde esta carpeta: `python3 -m http.server 8080`. Abrir la dirección HTTP indicada por el servidor. Usar HTTP para que el navegador pueda cargar el JSON.

## Estructura

```
index.html
css/styles.css
js/main.js
data/media.json
assets/images/imagen-01.jpg … imagen-10.jpg
assets/thumbnails/video-01.jpg … video-03.jpg
assets/videos/
assets/icons/favicon.svg
visor/index.html
visor/motor/index.html
visor/motor/assets/
visor/ORIGEN.json
downloads/presentacion/
downloads/imagenes/
downloads/videos/
downloads/planos/
downloads/material/
```

## Imágenes provisionales

Todos los huecos tienen imágenes existentes de la copia local `Villa_Manuela_copia_2026-10-01_1.zip`, localizada en Descargas. Incluyen imágenes/renderizaciones de la presentación y una vista del entorno. No se ha generado ningún material nuevo ni utilizado stock. Los originales no se han modificado. La fachada se repite temporalmente en el hero y en la galería.

| Etiqueta | Contenido provisional | Archivo sustituible |
|---|---|---|
| IMAGEN 01 | Fachada, jardín y piscina | assets/images/imagen-01.jpg |
| IMAGEN 02 | Fachada y parcela | assets/images/imagen-02.jpg |
| IMAGEN 03 | Exterior | assets/images/imagen-03.jpg |
| IMAGEN 04 | Salón y escalera | assets/images/imagen-04.jpg |
| IMAGEN 05 | Cocina | assets/images/imagen-05.jpg |
| IMAGEN 06 | Dormitorio | assets/images/imagen-06.jpg |
| IMAGEN 07 | Baño | assets/images/imagen-07.jpg |
| IMAGEN 08 | Porche | assets/images/imagen-08.jpg |
| IMAGEN 09 | Vista elevada de la villa | assets/images/imagen-09.jpg |
| IMAGEN 10 | Entorno urbano en Donostia | assets/images/imagen-10.jpg |

Las etiquetas son overlays HTML discretos, no forman parte de las imágenes. Se conservan automáticamente al reemplazar los JPG. El campo `source` del JSON registra el nombre original dentro de la copia del dossier. Las miniaturas de vídeo proceden de la misma copia; todavía no se han incorporado los archivos de vídeo.

## Cambiar una imagen

Reemplazar, por ejemplo, `assets/images/imagen-03.jpg` por la nueva foto con idéntico nombre. Recargar la página. Actualizar `alt` y `title` en `data/media.json` para describir el nuevo contenido; `label` mantiene el identificador IMAGEN 03. No hace falta editar HTML, CSS ni JS.

Los encuadres usan `object-fit: cover`: hero adaptado a pantalla, introducción cuadrada en escritorio, galería uniforme 3:2, visor y versión móvil de introducción 4:3. El lightbox muestra el archivo completo sin recortarlo. Para conservar la proporción de una tarjeta, mantener sus valores de `width` y `height`. Recomendación: fotos optimizadas por debajo de 500 KB y hero por debajo de 1 MB. Se admiten variantes opcionales `srcset` y `sizes` en cada imagen. Carga diferida fuera del hero.

## Añadir una imagen: dos pasos

1. Copiar el JPG a `assets/images/`.
2. Añadir una entrada a `images` del JSON:

```json
{
  "id": "imagen-11",
  "label": "IMAGEN 11",
  "section": "gallery",
  "order": 11,
  "src": "assets/images/imagen-11.jpg",
  "alt": "Descripción de la fotografía",
  "width": 1200,
  "height": 800,
  "title": "Título de la fotografía",
  "download": "assets/images/imagen-11.jpg"
}
```

Galería, etiqueta y lightbox se amplían automáticamente. `order` controla el orden. `download` activa la descarga individual; dejarlo en `null` para ocultarla. No se intenta listar carpetas desde el navegador.

## Añadir o sustituir un vídeo: dos pasos

1. Copiar el MP4 a `assets/videos/` y su miniatura a `assets/thumbnails/`.
2. Editar o añadir una entrada a `videos`:

```json
{
  "id": "video-04",
  "label": "VIDEO 04",
  "title": "Título del vídeo",
  "order": 4,
  "src": "assets/videos/video-04.mp4",
  "poster": "assets/thumbnails/video-04.jpg",
  "duration": "01:30",
  "download": "assets/videos/video-04.mp4",
  "width": 1920,
  "height": 1080
}
```

`duration` y `download` son opcionales. Para conservar la presentación visual, proporcionar siempre `poster`. Los tres vídeos iniciales muestran miniaturas reales del proyecto; al abrirlos se mantiene la miniatura y se indica que el vídeo está pendiente. Cuando `src` tiene una ruta válida, se abre el reproductor nativo, sin autoplay; se detiene al cerrar. MP4 H.264 recomendado. Para vídeos con voz, añadir `captions` con ruta a WebVTT y `language: "es"`.

## Visor

`viewerUrl` está configurado como `visor/`. La navegación VISOR 3D y los botones EXPLORAR / ABRIR MODELO 3D abren la página local en la misma pestaña. Su cabecera vuelve a la landing y sus secciones mediante rutas relativas.

`visor/index.html` es una página exterior con iframe que carga `visor/motor/index.html`. Se ha integrado **VILLA_MANUELA_VISOR_CLIENTES-v01**, del 30 de septiembre de 2026, elegida expresamente por el usuario. El HTML y todos sus assets son idénticos byte a byte al original en `Documents/Hirubrik/Villa Manuela/3D/Villa-Manuela-v05-trabajo/`. `visor/ORIGEN.json` registra procedencia, tamaños y SHA-256.

Clientes v01 contiene REFORMADA, Día/Noche, Entorno/Solo parcela, vistas exteriores/interiores, plantas, separación, fachadas, visualización, órbita/pan/recorrido y pantalla completa. Esta rama no contiene ACTUAL, captura ni instalaciones; no se han añadido ni reconstruido.

El modelo tiene una única copia dentro del sitio: `visor/motor/assets/geometry-01.json` … `geometry-09.json`. La landing no carga estos archivos hasta entrar en el visor. No se incluyen GLB, versiones históricas ni assets 3D repetidos. El enlace Notas del visor conserva su destino con una copia de su README, sin editar el HTML interno.

El botón exterior PANTALLA COMPLETA amplía el contenedor del iframe; se puede salir con su botón o Escape. El control de fullscreen original también se conserva. Si el navegador no ofrece la API, el wrapper usa una vista ampliada dentro de la ventana con botón de salida. No cambia controles ni lógica del visor.

Para una futura actualización, sustituir una sola vez el contenido de `visor/motor/` por el paquete validado completo, manteniendo sus rutas internas. No editar geometría, JS ni CSS del motor para cambiar la identidad exterior: usar `css/visor-page.css` y `js/visor-page.js`. La landing conserva IMAGEN 09 como imagen de presentación.

## PDF y descargas

La presentación HTML y el PDF ya están incorporados, con sus nombres originales. `presentationView.path` apunta a `downloads/presentacion/Villa Manuela — Ategorri Enea.html`: VER PRESENTACIÓN abre la página en una pestaña nueva con `target="_blank"`, `rel="noopener"` y sin atributo download. `presentationId` identifica la entrada PDF en `downloads`: DESCARGAR PRESENTACIÓN y su fila de Documentación descargan `downloads/presentacion/Villa Manuela — Ategorri Enea.pdf` con atributo download.

Las demás descargas siguen desactivadas, con `available: false` y `status: "PENDIENTE"`. Para incorporarlas, copiar el archivo, actualizar `path` y `size` y marcarlo disponible. No hay ZIP vacíos ni enlaces activos a archivos inexistentes.

El HTML conserva su contenido intacto y todas sus imágenes embebidas. Depende de Google Fonts para Carlito y EB Garamond; no es completamente autónomo en cuanto a tipografía. No se han modificado sus fuentes ni su diseño.

**PDF actualizado:** el archivo actual pesa 16.904.694 bytes (16,9 MB / 16,1 MiB). La landing no muestra su peso. Todos los archivos del proyecto están por debajo de 25 MiB; el PDF puede incluirse directamente en el artefacto estático de Cloudflare Pages. No hace falta alojarlo en R2 ni configurar redirecciones por tamaño. El archivo se conserva intacto.

Fuentes: [Cloudflare Pages: límites](https://developers.cloudflare.com/pages/platform/limits/) y [GitHub: archivos grandes](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

## GitHub y Cloudflare

Esta carpeta completa es el artefacto estático. Integrar su contenido en el directorio servido por el repositorio existente. No requiere compilación ni framework. Usar rutas relativas sin `/` inicial para GitHub Pages bajo subdirectorio. Los nombres distinguen mayúsculas y minúsculas en producción. No se ha cambiado ninguna configuración de publicación.

Tras sustituir archivos con el mismo nombre, desplegar para actualizar producción. Recarga forzada durante revisión; invalidar la caché del proveedor si conserva recursos antiguos. No hay service worker. Para archivos grandes, el JSON admite URLs HTTPS; la descarga forzada de otro dominio depende de sus cabeceras. Respetar los límites del proveedor.

## Accesibilidad

Alt text, salto al contenido, foco visible, menú móvil, lightbox con flechas, Home/End y Escape, devolución del foco y Tab/Mayús+Tab contenidos en el modal. Movimiento reducido y carga diferida. Véase `VALIDACION.md` para las comprobaciones locales.
