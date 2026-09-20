# Villa Manuela — Visor definitivo v112

## Entrega

`VILLA_MANUELA_VISOR_DEFINITIVO-v112.html` es un único HTML autónomo, con modelos y lógica incorporados. Abrirlo en un navegador moderno con WebGL. Estado inicial: REFORMADA · DÍA · ENTORNO. No requiere cambiar de página ni conexión para conmutar estados.

## Fuentes utilizadas

- **REFORMADA:** `VILLA_MANUELA_REFORMADA_MASTER_FINAL.html`, geometría validada de V111: 7.995 registros originales, incluidos 21 vacíos. Los registros se conservan exactamente, sin editar vértices, caras, nombres, colores, materiales ni posiciones.
- **ACTUAL:** `V70_TECNICA-v79.html`, última versión técnica histórica localizada que incorpora el estado previo a la reforma. Se reutilizan sus 4.376 registros seleccionados por `villaStates.actual`, sus acabados y sus 21 conjuntos de puertas practicables. Las versiones posteriores utilizadas como fuentes son reformadas. No se reconstruye el estado actual.
- **NOCHE:** `V70_REFORMADA_ENTORNO_ILUMINACION-v105.html`, sistema procedente de V104: 29 luces y sus 29 cuerpos, posiciones, haces, intensidades, colores, cielo y shader existentes. Grupos: EXTERIOR_ARQUITECTURA, EXTERIOR_RECORRIDOS, EXTERIOR_PAISAJE e INTERIOR vacío. Se conserva su condición provisional.
- **Entorno compartido:** contexto exterior del MASTER, seleccionado lógicamente; la propiedad reformada nunca se superpone al modelo ACTUAL. Los registros idénticos entre versiones reutilizan los mismos recursos. El conjunto cargado contiene 9.063 registros, no dos copias completas de la casa.

## Funciones recuperadas y reparadas

Se reutilizan cámara orbital, Pan, Recorrer, altura, focal, formato, captura limpia, pantalla completa, controles de niveles/fachadas, materiales visuales y navegación. La animación de verja sigue disponible internamente; su botón se elimina.

La selección de versión, iluminación, contexto, niveles, fachadas, separación y visualización utiliza un estado coordinado. Cada control modifica exclusivamente su propiedad. La cámara y el estado se conservan al conmutar modelos, día/noche y contexto, también en Recorrer. Las puertas de cada versión se vinculan a su modelo correspondiente.

El panel queda ordenado en VERSIÓN, ILUMINACIÓN, CONTEXTO, CÁMARA Y CAPTURA, PLANTAS, FACHADAS y VISUALIZACIÓN. Se eliminan campos y lógica de vistas guardadas, recorridos archivados, selectores de vistas exteriores/interiores y el botón de verja. La barra superior conserva identificación y estado del modelo.

SOLO PARCELA utiliza una clasificación independiente de Terreno. Conserva los elementos propios del MASTER, incluidos jardín, cerramientos, muros, setos, parking, rampa, verjas y mobiliario exterior. Se ocultan las familias del entorno vecino y el viario exterior. Terreno conserva su función histórica de visibilidad de la capa de terreno/contexto, independiente del ámbito elegido.

## Diagnóstico de niveles y fachadas

Se detectaron problemas combinados de lógica, clasificación y mallas que abarcan varios niveles. La búsqueda previa de `reformado_P0_forjado`, inexistente, producía límites no válidos. Se sustituyen por cotas de visualización derivadas de los forjados: −0,25 m, 3,28 m y 6,65 m. Se completan etiquetas cardinales explícitas ausentes en algunos objetos exteriores.

**271 objetos del conjunto de visualización abarcan varios niveles.** El listado exacto, con índice, nombre y niveles, está en [mallas_multiplanta.json](auxiliar-visor-definitivo/mallas_multiplanta.json). Ejemplos: `fachada_norte_escalera_conservado_superior_v22`, `fachada_sur_mirador_baja_conservado_superior_v22` y `fachada_norte_ala_este_conservado_superior_v22`.

Se resuelve mediante franjas lógicas y recorte de fragmentos en la GPU. Las franjas comparten la malla y sus buffers originales. Se desplazan únicamente al mostrar la separación; fachadas, carpinterías y piezas correspondientes responden a su franja. La cubierta conserva su bloque propio. Las sombras nocturnas se recalculan para la visibilidad activa.

No se cortan físicamente las mallas ni se generan tapas nuevas en las secciones: esa operación alteraría la geometría y queda fuera del encargo. Recorrer conserva sus colisiones arquitectónicas físicas; ocultación y separación son representaciones del modelo, no modificaciones del edificio transitable.

## Validación real

Probado en Google Chrome con WebGL: 41 comprobaciones registradas y prueba adicional de Recorrer. Una única carga de página, sin errores JavaScript ni WebGL.

- ACTUAL → REFORMADA → ACTUAL: selección histórica estable y cámara conservada.
- DÍA → NOCHE → DÍA: recuperación diurna idéntica píxel a píxel, sin acumulación de luces.
- ENTORNO → SOLO PARCELA → ENTORNO: recuperación idéntica; cero objetos de entorno exterior visibles en SOLO PARCELA.
- Ocultación individual S0, PB, P1, P2 y CUB; fachadas N/S/E/O y Restaurar.
- Separación de 0, 3 y 6 m y recogida a cero; cámara conservada.
- Las diez combinaciones solicitadas, incluidas P2 con cubierta y Norte ocultos y Noche con Oeste oculto.
- Formato, focal, altura, captura limpia y pantalla completa.
- Recorrer: cambios de versión, iluminación y contexto sin cambiar posición/orientación; ocultaciones conservadas al salir.

Las capturas de las pruebas están en `auxiliar-visor-definitivo/`. Registro detallado: [VALIDACIÓN](VILLA_MANUELA_VISOR_DEFINITIVO-v112_VALIDACION.json).

## Protección y archivos

Los SHA-256 del MASTER HTML, MASTER JSON y MASTER GLB coinciden con el registro previo. Los 7.995 registros del MASTER coinciden exactamente con su copia en el visor. Geometría, arquitectura y materiales del MASTER modificados: **NO**. Objetos originales modificados: **0**. Regresiones detectadas en las pruebas realizadas: **NO**.

Únicos archivos creados o editados en esta tarea: el nuevo HTML v112, este registro, su validación JSON y los archivos de construcción/prueba de `auxiliar-visor-definitivo/`. No se sobrescribe ningún modelo histórico ni archivo MASTER.
