# Resource Outage Explorer

[Français](README.md) · [English](README.en.md)

**Más capacidad no siempre repara un punto de fallo común. Este laboratorio muestra por qué.**

Asigna recursos compartidos, explora todas las combinaciones permitidas de un catálogo pequeño y compara refuerzos. Cada asignación incluye certificado flujo/corte verificado independientemente. Ejercicio sintético; no se envían recursos reales.

## Probar

Python 3.11 o posterior; biblioteca estándar, sin clave.

```sh
python3 -m outage_explorer serve --lang es
```

Abrir `http://127.0.0.1:8770/?lang=es`. Inicialmente cubre ocho unidades. Perder el depósito compartido deja dos disponibles y **seis sin cubrir**. Añadir cuatro unidades al medio principal o un respaldo en el mismo depósito no cambia el peor caso. Tres unidades independientes reducen el máximo déficit a **tres** en este catálogo.

```sh
python3 -m outage_explorer demo > analisis.json
python3 -m outage_explorer analyze outage_explorer/examples/shared-depot.json
python3 -m outage_explorer verify escenario.json certificado.json
```

`pip install .` ofrece `outage-explorer`. Interfaz y mensajes CLI FR/EN/ES.

## Qué se demuestra

Modelo bipartito: cada recurso tiene capacidad entera y demandas compatibles explícitas; cada demanda exige unidades enteras intercambiables. La capacidad total no permite sustituir recursos incompatibles.

Un cálculo de flujo máximo obtiene la asignación. Otro comprobador verifica capacidades, compatibilidad y demandas, y recalcula la capacidad del corte. **Asignación factible = capacidad de corte** demuestra flujo máximo dentro del modelo: no oculta una distribución mejor bajo las mismas hipótesis. Las huellas vinculan certificado y escenario.

Un evento puede desactivar varios recursos. Enumera todos los subconjuntos cuyo coste declarado respeta el presupuesto, hasta tres puntos. Distingue peor caso, todas las combinaciones y conjuntos mínimos de fallos que causan déficit. **Cantidad de escenarios no equivale a probabilidad de fallo.**

Los refuerzos aumentan capacidad o añaden recursos con exposición explícita a fallos existentes. Elige el mejor **refuerzo único del catálogo dado** dentro del presupuesto, no toda configuración posible de infraestructura.

## Herramientas y límites

[NetworkX ya ofrece algoritmos de flujo/corte](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.minimum_cut.html). No se inventa el teorema: se reúne **fallo común → déficit probado → refuerzo engañoso → alternativa comparada** en una demostración autónoma. Amplía el eje de ejercicios PICS Stress Lab; [CNIG trabaja sobre datos PCS/PICS](https://cnig.gouv.fr/gt-plans-communaux-et-intercommunaux-de-sauvegarde-a30138.html), pero no es una herramienta oficial.

Unidades comparables de ejercicio, sin convertir implícitamente personas, kW o vehículos. Sin viajes, duraciones, competencias ocultas, prioridades, probabilidades ni disponibilidad real. No opera, contacta, reserva ni envía servicios de emergencia. No garantiza continuidad real.

Hasta catorce recursos, doce demandas, doce eventos, diez refuerzos y tres puntos de fallos. Exhaustividad solo dentro del catálogo; fallos omitidos o exposiciones erróneas quedan fuera. Sin afirmar superioridad SOTA ni eficacia operativa real.

## Verificar

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Doce pruebas: fallos comunes, refuerzos, presupuestos, cortes, certificados falsificados, compatibilidad y comparación exhaustiva de asignaciones en veinte redes pequeñas. Navegador FR/EN/ES, exportación y móvil; CI Python 3.11/3.12 y rueda fuera de fuentes. MIT; alfa de ejercicio e investigación.
