# AGENTS.md

## Meta del Proyecto
Estructurar y estandarizar la documentacion del planteamiento de proyecto y contexto del negocio para Distribuidora Ecumenico, asegurando cumplimiento estricto de estandares editoriales y formato web limpio.

## Requerimientos
- Archivos de salida: `1.html`, `2.html`, `3.html`, `4.html`, `5.html` y `6.html`.
- Formato editorial formal: tipografia Times New Roman 12pt, texto justificado, paleta estricta en blanco y negro (sin colores decorativos).
- Lenguaje humanizado, profesional, fluido y claro, evitando tecnicismos artificiales o metas irreales como tasas de error al 0%.
- Eliminacion de artefactos de copia de procesadores de texto (`docs-internal-guid`, estilos en linea redundantes, etiquetas vacias y espaciados huerfanos).
- Tabla estructurada con encabezados claros y bordes monocromaticos definidos.

## Brief de audiencia (blog)
- Lectores: docentes evaluadores y equipo del curso; lectura ocasional, escritorio y movil.
- Objetivo: leer y revisar el expediente por capitulos; imprimir/exportar a PDF.
- Tono: editorial, logistica B2B; base azul con acento calido tipo especia.

## Decisiones
- Se adapto el codigo a HTML puro compatible con la vista HTML de Blogger (sin etiquetas doctype, html o head que choquen con la plantilla del blog).
- Se elimino el contenedor/recuadro de problema central en 1.html, dejandolo como "Problema General" en texto plano estructurado.
- Se removio la sigla "(SKUs)" tanto en el titulo de la seccion como en el encabezado de la tabla.
- En 2.html se conservo la URL de la imagen del diagrama de Blogger, asegurando adaptabilidad y borde monocromatico.
- Se eliminaron todos los colores decorativos de las tablas (#1f4e79, #c00000, #2e75b6, #f9fafb, #666666, #333333, #c4c7c5), dejandolas estrictamente en blanco y negro con bordes definidos.
- En 3.html se reestructuraron la Matriz Poder/Interes (cuadricula 2x2 formal), el Cubo de Interesados 3D, el Modelo de Prominencia, la Matriz RACI y la Matriz de Involucramiento.
- En 4.html se estructuro el Marco Metodologico con 4 fases del ciclo de vida, planificacion de 4 Sprints, el Mapa de Historias de Usuario (User Story Map) y la Matriz de Priorizacion Valor vs. Esfuerzo (corrigiendo 'Ganas Rapidas' a 'Ganancias Rapidas').
- En 5.html se desarrollo la Ingenieria y Tecnologia Propuesta: zonificacion de almacenes (Zonas A, B y C), arquitectura WMS, flujo de integracion fisico-digital y especificacion de Casos de Uso UML (UC-01 a UC-06).
- En 6.html se estructuro Control y Evaluacion de Viabilidad: analisis financiero/retorno, dashboard de KPIs con semaforos de riesgo, matriz de auditoria de eventos (Audit Trail WMS) y plan de mitigacion de riesgos operativos y tecnicos.
- Se optimizo index.html adoptando una paleta de color corporativa azul cobalto y pizarra profesional (slate/blue), reemplazando el esquema estrictamente blanco y negro para elevar la estetica como blog de ingenieria y gestion logistica.
- Se incorporaron formalmente los 4 integrantes del proyecto tanto en la barra lateral como en la cabecera hero (Modesto Romero Bryan Adam, Julca Achas Cristian Sebastian, Felix Cecinario Hernan, Avalos Mendoza Jeshua Raul).
- Se elimino el bloque Bento redundante y las metricas del sidebar, consolidando la presentacion del Problema General.
- Se coloco como cara principal del blog la evidencia operativa en campo de las rutas de despacho (assets/images/figura-3-mapa-ruta-reparto.jpg) con visor interactivo.
- Se eliminaron todos los enlaces y botones que redirigian al Blogger anterior, convirtiendo esta aplicacion web en el blog definitivo y oficial del proyecto.
- Se retiro la referencia "(como Villa Maria del Triunfo)" en la presentacion comercial para un estilo editorial pulcro.
- Se rediseno index.html como blog real (sin alterar el contenido de los capitulos): portada con foto de rutas a pantalla completa, cifras clave, Problema General como cita destacada, tarjetas de capitulos con portadas, seccion de equipo, vista de articulo con indice lateral, tiempo de lectura, navegacion anterior/siguiente, enlaces por capitulo (#cap1..#cap6, #todo) y acento calido tipo especia sobre la base azul.
- Se agrego el Capitulo 7 (Arbol de Problemas) al blog: diagrama nativo en HTML/CSS con efectos (verde), problema central (naranja) y causas (rojo), tabla de detalle por nivel y descarga del PNG original (assets/images/arbol-problemas.png).
- Fuente del blog en `src/`: `template.html`, `chapters/cap1-7.html` (contenido verbatim), `entrevistas.json`, `build.py`. index.html se genera con `python src/build.py`; no editar index.html a mano.
- Capitulo 8 (Entrevistas de Campo) generado desde `src/entrevistas.json`: 4 perfiles (Gerente General, Supervisor de Almacen, Operario de Picking, Chofer de Reparto). Entrevistas aplicadas: respuestas reales cargadas en `r` (texto literal del entrevistado), `estado: "realizada"`; las preguntas `p` se mantienen segun el instrumento del capitulo 2. `fecha` vacia (no informada).
- Mejoras de diseno: indicador de progreso por capitulo, seccion "Cuatro voces de la operacion" en portada, foco visible en enlaces/botones, tablas de 4+ columnas con ancho minimo y desplazamiento en movil, menu movil sin simbolos.
- Instrumentos de campo ampliados en `instrumentos/cuestionarios-likert-distribuidora-ecumenico.docx` (no publicado; excluido en .vercelignore): guia de aplicacion + 4 formularios (Gerencia/jefaturas 19 items, Supervision 18, Operarios 17, Reparto 16) con escala Likert 1-5 por dimensiones vinculadas al arbol de problemas y 5 preguntas abiertas cada uno. Parte II y III aplicables por separado. Sin items invertidos.
- Capitulo 8 = solo cuestionarios (oct 2026, 1 por perfil) desde `src/cuestionarios.json`: 8.1 instrumento, 8.2-8.5 un bloque por perfil (Likert + abiertas juntas), 8.6 hallazgos, 8.7 conclusiones. Se eliminaron las entrevistas de la primera visita (`entrevistas.json`) por ser inferidas. Perfiles con los nombres del formulario impreso.
- Montos de gerencia: en el blog se publican (S/ 3,500 al mes; S/ 5,000 a 8,000 primera etapa) por pedido del usuario (2026-10-12); Word y PPT siguen en forma cualitativa.
- Orden de capitulos (2026-10-12): 7 = Trabajo de Campo (cuestionarios, generado por build.py, id cap7), 8 = Arbol de Problemas (`chapters/cap8.html`), 9 = Objetivos y Alternativas.
- Correcciones de campo (2026-10-12): armar los pedidos de una zona toma 1 h (pocos) a 2-3 h (bastantes); reparto sale 7-8 a. m. y termina ~6 p. m.; ~100 clientes por ruta (a veces mas de 130), dos personas por unidad. A4.2a = desarrollar software de mapeo digital.
- Arbol de problemas redisenado (2026-10-11) para no calcar la plantilla del docente: 4 causas directas (indirectas 3, 2, 1 y 2), 3 efectos directos que convergen en 2 efectos indirectos y 1 efecto final. PNG regenerado (`assets/images/arbol-problemas.png`) y referencias actualizadas en cap 8, Word, PPT y guia del instrumento.
- Capitulo 9 (Objetivos y Alternativas, `src/chapters/cap9.html`): arbol de objetivos alineado al arbol de problemas de 4 causas (4 medios de 1er nivel, 8 medios fundamentales, 3 fines directos, 2 indirectos, fin ultimo); acciones A1.1a/b y A4.2a/b excluyentes; PA1 (racks nuevos + mapa digital) vs PA2 (anaqueles reacondicionados + software de ruteo); Tarea 3 por juicio de expertos con 5 criterios: PA1 13 pts, PA2 11 pts, se selecciona PA1. Objetivo central y redaccion de acciones tomados del arbol del equipo.
- Observacion del docente (2026-10-12): la solucion elegida debe reflejar el objetivo central completo, sin acotar. PA1 se nombra literal: "Tecnificacion del almacen con racks metalicos nuevos, sistema WMS con terminales moviles y estandarizacion de los procesos logisticos con software de mapeo digital propio"; cap 9 suma composicion de cada PA, tabla de acciones por PA y 9.5 Coherencia objetivo central - proyecto seleccionado (cada parte literal del objetivo -> medio -> acciones).
- Objetivos SMART (2026-10-12): objetivo central con metas medibles (45 a 27 min/pedido, salida 6:00 a. m., <1 % incidencias, 6 meses); 4 objetivos especificos SMART (uno por medio de 1er nivel) en cap 1 y cap 9.2. El texto del objetivo central es identico en cap 1, cap 9, arbol de objetivos e imagenes.
- La propuesta no menciona terminales moviles, lectores ni escaneres (solo racks + WMS + estandarizacion); se retiraron de caps 1-6 y 9. Se conservan solo en los items del cuestionario aplicado (cap 7), por ser datos de campo.
- Word y PPT de emprendimiento: no se continuan; el docente solo evalua el blog.
- Escala Likert en cap 7: se llama "preguntas Likert (afirmaciones)"; cada tema muestra N.° de preguntas, calculo (suma / cantidad), promedio y nivel, con recuadro "Como se obtiene cada numero".
- Diagramas como imagen (2026-10-11), estilo de los graficos del equipo (columna de niveles a la izquierda, cajas y flechas): `arbol-problemas.png` (cap 7), `arbol-objetivos.png`, `medios-acciones-alternativas.png` y `evaluacion-alternativas.png` (cap 9). Generador PIL en scratchpad (`diagramas.py`, no versionado). Cap 8 suma galeria de 6 fotos de la visita (figuras 10 y 11 nuevas).
- Fotos de campo (Fotos ecumenico/) copiadas a `assets/images/figura-5..9-*.jpg`; figuras 5-8 en evidencias del capitulo 2, figura 9 (instrumento) en capitulo 8.
- Portada: se mantiene el mapa de rutas de fondo; cifras del hero con datos de campo; bloque de evidencia unica reemplazado por mosaico "Asi trabaja hoy la distribuidora".
- `instrumentos/trabajo-aplicativo-emprendimiento.docx`: documento de otro curso (Emprendimiento, UNTELS). Carátula segun el formato del plan de Transformacion Digital; no menciona el blog ni otros cursos. Docente pendiente en la caratula. Generador en scratchpad (no versionado).
- `instrumentos/trabajo-aplicativo-emprendimiento.pptx`: resumen de 10 diapositivas del trabajo de emprendimiento (empresa, procesos, situacion, problema, potencial, metodologia, datos, resultados Likert, conclusiones).
- `.vercelignore` excluye `instrumentos/`, `Fotos ecumenico/` y `*.docx`.

## Estado
- Repositorio en GitHub: https://github.com/HernanFxDev/Blog-Distribuidora-ecumenico (rama `main`, un commit inicial firmado HernanFxDev, 2026-10-12). El historial previo queda solo en la rama local `master`; seguir trabajando en `main`.
- index.html actualizado con la paleta de color azul/slate, imagen de portada de rutas de despacho, integrantes y sin enlaces externos a Blogger.
- Documentos 1.html al 6.html preservados para consulta formal o insercion modular.
- Sitio web publicado y desbloqueado en: https://distribuidora-ecumenico-logistica.vercel.app
- Capitulo 8 y mejoras de diseno desplegados en produccion (2026-10-04).
- Capitulo 8 actualizado con las respuestas reales de las 4 entrevistas (2026-10-04) reemplazado por los cuestionarios Likert; desplegado en produccion (2026-10-10).

## Siguiente Paso


- Figura 4 sigue enlazada a blogger.googleusercontent.com; descargarla a `assets/images/`.
