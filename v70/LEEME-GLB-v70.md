# Villa Manuela V70 · GLB completo

Archivo: `Villa-Manuela-v70.glb`. Exportación de la última versión validada V70, sin alterar sus archivos.

## Contenido

- Dos escenas glTF: **VILLA PRINCIPAL — ACTUAL** y **VILLA PRINCIPAL — REFORMADA**. Actual es la escena predeterminada.
- 4.021 objetos comunes compartidos entre ambas escenas, 355 exclusivos de Actual y 3.810 exclusivos de Reformada: 8.186 objetos únicos.
- Envolvente, interiores, escaleras, cubiertas, carpinterías, mobiliario, terreno, cerramientos, accesos, carretera y vegetación completos, según su pertenencia a cada estado en V70.
- Anexo visible únicamente en Actual. Escalera común y demás elementos compartidos referenciados sin duplicar sus mallas.
- Nombres originales, grupos, plantas y metadatos de procedencia conservados.
- 222 texturas PNG incrustadas, 407 materiales PBR. No necesita archivos externos.
- No se incluyen las 195 piezas históricas que V70 mantiene inactivas en ambos estados: no forman parte del modelo visible de ninguna de sus configuraciones.

## Blender

Importar mediante **Archivo → Importar → glTF 2.0 (.glb/.gltf)**. El archivo contiene ambos estados como escenas glTF; su presentación como escenas o colecciones depende de las opciones y versión del importador. Mantener visible solo un estado completo a la vez para no superponer sus interiores. La geometría común es compartida.

Unidades: metros. El eje vertical del visor es Z; el contenedor utiliza una rotación de raíz para respetar el eje Y vertical de glTF. Esta conversión de sistema de coordenadas no escala ni desplaza la villa respecto a la parcela.

Referencia del importador: https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html

## Fidelidad y comprobaciones

Los 306.275 triángulos únicos conservan sus posiciones y orientación, comparados uno a uno con el origen tras la conversión a float32 que también utiliza el visor. No se han recortado, reconstruido, simplificado ni añadido caras. La diferencia numérica máxima frente a los valores decimales del JSON es 0,000000954 m.

Ambas escenas se han importado además con un lector glTF independiente: 177.397 triángulos en Actual y 270.669 en Reformada. Comprobadas jerarquías, pertenencia a estados, referencias de materiales, normales, coordenadas UV y todos los PNG incrustados. No se ha ejecutado Blender en este equipo; no se presenta la comprobación independiente como una prueba realizada dentro de Blender.

Los acabados procedurales del visor se han horneado en texturas; las caras inferiores de cubierta orientadas hacia abajo conservan su blanco. La iluminación y la respuesta de reflejos/transparencia dependen del motor de Blender y no serán idénticas al shader de pantalla del visor. Los controles JavaScript, recorrido y apertura interactiva de puertas no se exportan como comportamiento; las hojas conservan su geometría y posición guardadas en V70.

Informe técnico y huellas de integridad: `auxiliar-exportacion-glb-v70/verificacion-glb-v70.json` y `source-hashes.json`.
