# Villa Manuela · V70 · Implantación de parcela

Base: V69. Se conserva íntegra, sin sobrescritura. No se mueve, gira ni escala ningún objeto de la villa ni del anexo.

## Qué se corrige

Sustituido el contorno completo de parcela por la polilínea vectorial del plano adjunto. Se adaptan conjuntamente terreno, muro norte, muro oeste, remates, verja, accesos, acera y carretera. No se añaden muros sur/este, viviendas, garajes ni ampliaciones.

El plano original correspondiente a la imagen es `VILLA MANUELA - PLANTA PARCELA REFORMADO 1.pdf`, en la carpeta `Planos` del proyecto. La polilínea original, a 1:200, da 1.351,635 m². Se aplica únicamente al plano una calibración uniforme de escala del 0,00425 % para reproducir 1.351,52 m². La orientación se registra mediante las esquinas homólogas noroeste y suroeste de la villa; la vivienda del modelo permanece fija. La segunda esquina tiene un residuo de aproximadamente 6 cm en la dirección longitudinal, sin trasladar ni escalar la casa para eliminarlo.

Se mantienen los quiebros del perímetro. La extensión del terreno se hace horizontalmente: todas las cotas Z de sus vértices se conservan. Se mantienen fijos los encuentros de terreno con vivienda, anexo, plataformas, escalera exterior y apoyos de los cinco árboles. No hay simplificación de la topografía ni modificación del edificio.

## Validación dimensional

| Elemento / referencia | Plano | Modelo V70 | Diferencia |
|---|---:|---:|---:|
| Superficie de parcela | 1.351,520 m² | 1.351,520 m² | 0,000 m² |
| Lado sur, longitud de polilínea | 38,640 m | 38,644 m | +0,004 m |
| Lado este, longitud de polilínea | 34,370 m | 34,384 m | +0,014 m |
| Oeste, sección norte de la villa | 3,030 m | 3,020 m | −0,010 m |
| Norte, sección occidental | 3,580 m | 3,584 m | +0,004 m |
| Oeste, sección sur de la villa | 4,870 m | 4,885 m | +0,015 m |
| Norte, plataforma oriental / alineación interior del cerramiento | 2,870 m | 2,844 m | −0,026 m |

Los lados se miden siguiendo los quiebros. Sus cuerdas entre extremos son 38,643 m (sur) y 34,374 m (este). La superficie se calcula sobre el polígono completo horizontal de parcela, no sobre un rectángulo envolvente ni sobre la superficie inclinada de terreno.

Los retranqueos se comparan con la cara interior/alineación del cerramiento que acotan las líneas del plano, no con el borde exterior de la parcela. La referencia oriental atraviesa el acceso de vehículos: se utiliza la prolongación de la alineación interior del muro, no el plano central de la hoja de la puerta. Los puntos y ejes de sección quedan identificados en `verificacion-v70.json` y en el comprobador auxiliar.

Tolerancias de comprobación adoptadas para este plano: 2 cm para las longitudes principales y 5 cm para retranqueos. Todas las comprobaciones anteriores las cumplen. La máxima desviación de las aristas de malla del perímetro respecto al contorno vectorial es de 0,004 m en 3.214 aristas comprobadas. La superficie exacta es un dato de calibración del contorno; no se presenta como una medición topográfica independiente.

## Anexo oeste y estado de la villa

Las 47 piezas del anexo son idénticas a V69: sin cambio de posición, anchura, tamaño, cubierta o carpintería. La envolvente cerrada sigue abarcando aproximadamente 3,194 × 2,544 m en los ejes locales.

En las tres secciones del anexo, fachada–cara interior del muro = 3,023–3,188 m. Paso anexo–muro = 0,479–0,645 m (0,564 m en la sección central). La distancia mínima perpendicular es 0,479 m. No se fuerza un paso uniforme de 60 cm: esa cifra era aproximada. La cubierta volada conserva al menos 0,267 m de separación respecto al muro y no lo invade.

Villa, interiores, escaleras, carpinterías, materiales, mobiliario y vegetación conservan exactamente sus datos V69. Los estados Actual/Reformada conservan sus índices y funciones. El visor abre en Actual. La casa no se escala ni desplaza y el anexo sigue apareciendo únicamente en Actual.

## Verificación del visor

Superadas las pruebas instrumentadas del código del visor: carga, estados, plantas, cubierta, separación, fachadas N/S/E/O, restauración, vistas, recorrido, puertas, recorridos de escaleras y variantes sin geometría futura. Sin caras invertidas introducidas en las mallas de entorno. Sin intersección anexo–muro.

Revisadas imágenes OpenGL ES generadas con las llamadas de dibujo y shaders del propio visor. No se ha realizado una revisión manual en navegador. No se atribuye a estas pruebas una validación urbanística ni un nuevo levantamiento topográfico.

## Archivos principales

Todos directamente dentro de `Villa-Manuela-v05-trabajo`:

- `Villa-Manuela-visor-v70.html` — visor autónomo, con geometría y contorno incorporados.
- `geometria-v70.json` — geometría completa.
- `estados-villa-v70.json` — estados Actual/Reformada.
- `parcela-v70.json` — contorno completo, sistema local métrico y registro al plano.
- `verificacion-v70.json` — mediciones, invariantes y pruebas.
- `Villa-Manuela-revision-v70.png` — comparación de contornos y vistas de revisión.
- `LEEME-v70.md` — este documento.

Los cálculos, comprobadores y capturas auxiliares quedan en `auxiliar-parcela-v70`, dentro de la misma carpeta de trabajo.
