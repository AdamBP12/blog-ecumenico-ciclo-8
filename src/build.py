"""Genera index.html a partir de src/template.html, src/chapters/*.html y src/cuestionarios.json.

Uso: python src/build.py
"""
import html, json, pathlib, re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
TPL = (SRC / "template.html").read_text(encoding="utf-8")
CQ = json.loads((SRC / "cuestionarios.json").read_text(encoding="utf-8"))

META = [
    dict(id="cap1", n="01", kicker="Contexto del negocio", short="Planteamiento y Contexto",
         dek="Quiénes somos, qué frena hoy al almacén y qué nos proponemos lograr en seis meses.",
         img="assets/images/figura-2-almacen-piso-as-is.jpg",
         cap="Figura 2: Almacenamiento directo a nivel de piso y pasillo saturado (Estado AS-IS)"),
    dict(id="cap2", n="02", kicker="Entorno y evidencias", short="Entorno y Evidencias",
         dek="Entrevistas en piso, fotografías reales y el contraste entre el almacén de hoy (AS-IS) y el que proponemos (TO-BE).",
         img="assets/images/figura-1-nota-pedido-manual.jpg",
         cap="Figura 1: Comprobante y nota de pedido manual en talonario físico (Estado AS-IS)"),
    dict(id="cap3", n="03", kicker="Stakeholders", short="Stakeholders & RACI",
         dek="Quién decide, quién opera y quién recibe: poder, interés, prominencia y la matriz RACI del proyecto.",
         art="c3"),
    dict(id="cap4", n="04", kicker="Metodología", short="Metodología y Scrum",
         dek="Cuatro fases, cuatro sprints y un mapa de historias de usuario priorizado por valor y esfuerzo.",
         art="c4"),
    dict(id="cap5", n="05", kicker="Propuesta TO-BE", short="Propuesta TO-BE",
         dek="Zonas A, B y C, arquitectura WMS y el recorrido de un pedido desde la nota de venta hasta el despacho de las 06:00 am.",
         art="c5"),
    dict(id="cap6", n="06", kicker="Control y viabilidad", short="Control y Viabilidad",
         dek="Indicadores con semáforos, auditoría de eventos y un plan frente a los riesgos que pueden frenar la operación.",
         art="c6"),
    dict(id="cap7", n="07", kicker="Trabajo de campo", short="Trabajo de Campo", art="c8"),
    dict(id="cap8", n="08", kicker="Árbol de problemas", short="Árbol de Problemas",
         dek="Las causas, el problema central y sus efectos en un solo diagrama: de dónde nacen los retrasos y hasta dónde llegan.",
         art="c7"),
    dict(id="cap9", n="09", kicker="Objetivos y alternativas", short="Objetivos y Alternativas",
         dek="Del problema a la solución: árbol de objetivos, acciones por medio fundamental y la evaluación que define el proyecto a ejecutar.",
         art="c9"),
]

ICONS = {
    "c3": '<path d="M17 20h5v-2a3 3 0 00-5.4-1.9M17 20H7m10 0v-2c0-.7-.1-1.3-.4-1.9M7 20H2v-2a3 3 0 015.4-1.9M7 20v-2c0-.7.1-1.3.4-1.9m0 0a5 5 0 019.2 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>',
    "c4": '<path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>',
    "c5": '<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>',
    "c6": '<path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>',
    "c7": '<path d="M12 21V11m0 0L7 7m5 4l5-4M7 7V3m10 4V3M4 21h16"/>',
    "c9": '<path d="M12 21a9 9 0 100-18 9 9 0 000 18zm0-4a5 5 0 100-10 5 5 0 000 10zm0-4a1 1 0 100-2 1 1 0 000 2z"/>',
    "c8": '<path d="M12 3a3 3 0 00-3 3v6a3 3 0 006 0V6a3 3 0 00-3-3zM5 11a7 7 0 0014 0M12 18v3m-4 0h8"/>',
}
PATTERNS = {
    "c3": '<pattern id="p{u}" width="40" height="40" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="2" fill="#fff"/><circle cx="20" cy="20" r="12" fill="none" stroke="#fff" stroke-width=".8"/></pattern>',
    "c4": '<pattern id="p{u}" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M0 18h36M18 0v36" stroke="#fff" stroke-width=".8"/></pattern>',
    "c5": '<pattern id="p{u}" width="44" height="26" patternUnits="userSpaceOnUse"><rect x="3" y="3" width="38" height="20" fill="none" stroke="#fff" stroke-width=".9"/></pattern>',
    "c6": '<pattern id="p{u}" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M0 28L28 0" stroke="#fff" stroke-width=".9"/></pattern>',
    "c7": '<pattern id="p{u}" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M17 6l7 12H10z" fill="none" stroke="#fff" stroke-width=".9"/></pattern>',
    "c9": '<pattern id="p{u}" width="38" height="38" patternUnits="userSpaceOnUse"><circle cx="19" cy="19" r="13" fill="none" stroke="#fff" stroke-width=".8"/><circle cx="19" cy="19" r="6" fill="none" stroke="#fff" stroke-width=".8"/></pattern>',
    "c8": '<pattern id="p{u}" width="40" height="30" patternUnits="userSpaceOnUse"><path d="M6 8h22a3 3 0 013 3v7a3 3 0 01-3 3H14l-5 4v-4H6a3 3 0 01-3-3v-7a3 3 0 013-3z" fill="none" stroke="#fff" stroke-width=".9"/></pattern>',
}
TEAM = [("MR", "Modesto Romero Bryan Adam", "a1"), ("JA", "Julca Achas Cristian Sebastian", "a2"),
        ("FC", "Felix Cecinario Hernan", "a3"), ("AM", "Avalos Mendoza Jeshua Raul", "a4")]
ARROW = '<svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M5 12h14M13 6l6 6-6 6"/></svg>'
esc = lambda s: html.escape(s, quote=False)


def read_chapter(cid):
    raw = (SRC / "chapters" / f"{cid}.html").read_text(encoding="utf-8")
    m = re.match(r"<!-- title: (.*?) -->\n", raw)
    return m.group(1), raw[m.end():]


# ---------- Chapter 8: field questionnaires (generated from cuestionarios.json) ----------
fmt = lambda x: f"{x:.2f}".replace(".", ",")


def q_stats():
    for f in CQ["formularios"]:
        k = 0
        for i, d in enumerate(f["dimensiones"]):
            d["letra"], d["desde"] = chr(65 + i), k + 1
            k += len(d["items"])
            d["hasta"] = k
            vals = f["likert"][d["desde"] - 1:d["hasta"]]
            d["media"] = sum(vals) / len(vals)
            m, fav = d["media"], d["tipo"] == "f"
            lvl = 0 if m <= 2.33 else 1 if m <= 3.66 else 2
            d["nivel"] = (["Baja", "Media", "Alta"] if fav else ["Bajo", "Medio", "Alto"])[lvl]
            d["pill"] = (["pill-red", "pill-amber", "pill-green"] if fav else ["pill-green", "pill-amber", "pill-red"])[lvl]
        f["total"] = k
        assert len(f["likert"]) == k, f"F{f['n']}: {len(f['likert'])} respuestas para {k} items"


q_stats()
SHORT = {1: "Gerencia", 2: "Supervisión", 3: "Operarios", 4: "Reparto"}
SCALE = ["", "Totalmente en desacuerdo", "En desacuerdo", "Ni de acuerdo ni en desacuerdo", "De acuerdo", "Totalmente de acuerdo"]
DIM = lambda n, l: next(d for d in CQ["formularios"][n - 1]["dimensiones"] if d["letra"] == l)
ITEM = lambda n, i: CQ["formularios"][n - 1]["likert"][i - 1]
H3 = '<h3 class="text-base sm:text-lg font-bold text-neutral-950 mt-6 mb-2">'


FIELD_PHOTOS = [
    ("figura-5-almacen-columnas-cajas.jpg", "Almacén", "Columnas de cajas apiladas en el piso, sin racks"),
    ("figura-6-furgon-carga-sin-divisiones.jpg", "Unidad de reparto", "Carga sin divisiones junto a la carretilla"),
    ("figura-10-furgon-carga-lateral.jpg", "Unidad de reparto", "Cajas marcadas a mano y productos sueltos"),
    ("figura-7-bultos-unidad-reparto.jpg", "Despacho", "Líquidos y secos juntos en cajas abiertas"),
    ("figura-11-bultos-reparto-vista-general.jpg", "Despacho", "Bultos sin rotular por cliente"),
    ("figura-8-hoja-consolidacion-carga.jpg", "Control manual", "Salida de carga contada con palotes"),
]
FIELD_GALLERY = '<div class="q-gal">' + "".join(
    f'<figure onclick="openLightbox(\'assets/images/{f}\', \'{k}: {c}\')"><img src="assets/images/{f}" alt="{k}: {c}" loading="lazy"><figcaption><span>{k}</span>{c}</figcaption></figure>'
    for f, k, c in FIELD_PHOTOS) + '</div>'


def field_chapter():
    fs = CQ["formularios"]
    title = "Trabajo de Campo: Cuestionarios por Perfil"
    dek = "Gerencia, supervisión, operarios y reparto: lo que marcó cada perfil en la escala Likert, lo que respondió con sus propias palabras y cómo confirma el diagnóstico."
    frows = "".join(
        f'<tr><td style="text-align: center;">{f["n"]}</td><td><strong>{esc(f["perfil"])}</strong></td><td>{esc(f["dirigido"])}</td>'
        f'<td>{esc(f["nivel"])}</td><td style="text-align: center;">{f["total"]}</td><td style="text-align: center;">{len(f["abiertas"])}</td></tr>' for f in fs)
    out = [f'''{H3}7.1 Instrumento y Aplicación</h3>
<p class="text-justify mb-4">Para validar el diagnóstico con las personas que viven la operación día a día, se aplicó un cuestionario a cada uno de los cuatro perfiles de la empresa en {esc(CQ["aplicacion"])}. La aplicación fue presencial y cada cuestionario tiene dos tipos de preguntas:</p>
<ul class="list-disc pl-6 space-y-2 mb-4">
<li><strong>Preguntas Likert (afirmaciones):</strong> son frases como «La unidad de reparto sale después de las 6:00 a. m. con frecuencia». La persona no responde con palabras: marca en el papel un número del 1 al 5 según qué tan de acuerdo está (1 = totalmente en desacuerdo, 2 = en desacuerdo, 3 = ni de acuerdo ni en desacuerdo, 4 = de acuerdo, 5 = totalmente de acuerdo). Cada cuestionario tiene entre 16 y 19 preguntas Likert.</li>
<li><strong>Preguntas abiertas:</strong> cinco preguntas que la persona responde con sus propias palabras; el equipo anotó las respuestas tal como fueron dichas.</li>
</ul>
<p class="text-justify mb-4">Las preguntas Likert se agrupan en temas o dimensiones (por ejemplo, salida y horario o planificación de rutas), que luego sirven para construir el árbol de problemas del capítulo 8; la última dimensión de cada cuestionario mide la disposición al cambio. </p>
<div class="lk-how">
<div class="lk-how-t">Cómo se obtiene cada número</div>
<ol>
<li><strong>Se agrupan las preguntas Likert por tema.</strong> Por ejemplo, en el cuestionario de Personal de Reparto, las preguntas 1, 2, 3 y 4 tratan sobre la salida y el horario de la unidad.</li>
<li><strong>Se suman los números que marcó la persona y se dividen entre la cantidad de preguntas.</strong> El chofer marcó 4, 4, 4 y 4: (4 + 4 + 4 + 4) ÷ 4 = <strong>4,00</strong>.</li>
<li><strong>Ese promedio se lee con tres niveles:</strong> de 1,00 a 2,33 es bajo, de 2,34 a 3,66 es medio y de 3,67 a 5,00 es alto. En los temas que describen un problema, «alto» significa que el problema sí ocurre; en el tema de disposición al cambio, «alta» significa que la persona está a favor de las mejoras.</li>
</ol>
</div>
<figure class="q-fig"><img src="assets/images/figura-9-instrumento-campo.jpg" alt="Figura 9: Cuestionarios impresos para su aplicación en campo" loading="lazy" class="figure-zoom" onclick="openLightbox('assets/images/figura-9-instrumento-campo.jpg', 'Figura 9: Juego de cuestionarios impreso para su aplicación en campo')"><figcaption><b>Figura 9.</b> Juego de cuestionarios impreso, con los integrantes del equipo, listo para su aplicación en campo.</figcaption></figure>
<h4>Registro fotográfico de la visita</h4>
<p class="text-justify mb-4">Durante la aplicación de los cuestionarios, el equipo recorrió el almacén y la unidad de reparto para registrar las condiciones que describían los trabajadores. Haz clic en cualquier fotografía para ampliarla.</p>
{FIELD_GALLERY}
<div class="overflow-x-auto"><table><thead><tr>
<th style="width: 7%; text-align: center;">N.°</th><th style="width: 23%;">Perfil</th><th style="width: 32%;">Dirigido a</th><th style="width: 12%;">Nivel</th><th style="width: 13%; text-align: center;">Preguntas Likert</th><th style="width: 13%; text-align: center;">Preguntas abiertas</th>
</tr></thead><tbody>{frows}</tbody></table></div>''']

    for i, f in enumerate(fs, 1):
        calc = lambda d: f'({" + ".join(str(v) for v in f["likert"][d["desde"] - 1:d["hasta"]])}) ÷ {d["hasta"] - d["desde"] + 1}'
        drows = "".join(
            f'<tr><td>{d["letra"]}. {esc(d["t"])}</td>'
            f'<td style="text-align: center;">{d["desde"]} a {d["hasta"]}</td>'
            f'<td style="white-space: nowrap;">{calc(d)}</td>'
            f'<td><div class="lk"><span class="lk-bar"><i style="width:{(d["media"] - 1) / 4 * 100:.0f}%"></i></span><b>{fmt(d["media"])}</b></div></td>'
            f'<td style="text-align: center;"><span class="pill {d["pill"]}">{d["nivel"]}</span></td></tr>' for d in f["dimensiones"])
        dg = [d for d in f["dimensiones"] if d["tipo"] == "d"]
        lst = lambda ds: ", ".join(x["t"].lower() for x in ds[:-1]) + (" y " if len(ds) > 1 else "") + (ds[-1]["t"].lower() if ds else "")
        alto, medio = [d for d in dg if d["nivel"] == "Alto"], [d for d in dg if d["nivel"] != "Alto"]
        fav = f["dimensiones"][-1]
        reading = ("<b>Cómo leerlo:</b> cada fila suma los números que marcó la persona en las preguntas Likert de ese tema y los divide entre la cantidad de preguntas. "
                   + (f"Para este perfil, {lst(alto)} {'sale' if len(alto) == 1 else 'salen'} en nivel alto: el problema sí ocurre con frecuencia. " if alto else "")
                   + (f"{lst(medio).capitalize()} {'queda' if len(medio) == 1 else 'quedan'} en nivel medio: ocurre, pero no siempre. " if medio else "")
                   + f"La disposición al cambio es {fav['nivel'].lower()} ({fmt(fav['media'])}): {'aceptan' if fav['nivel'] == 'Alta' else 'tienen reservas sobre'} las mejoras propuestas.")
        items = "".join(
            f'<tr><td style="text-align: center;">{d["desde"] + k}</td><td>{esc(it)}</td><td>{SCALE[f["likert"][d["desde"] + k - 1]]} ({f["likert"][d["desde"] + k - 1]})</td></tr>'
            for d in f["dimensiones"] for k, it in enumerate(d["items"]))
        qa = "".join(
            f'<li><div class="iv-q"><span class="iv-n">P{j}</span><p>{esc(x["p"])}</p></div>'
            f'<div class="iv-a"><span class="iv-a-l">Respuesta{" (monto expresado de forma cualitativa por confidencialidad)" if x.get("confidencial") else ""}</span><p>{esc(x["r"])}</p></div></li>'
            for j, x in enumerate(f["abiertas"], 1))
        out.append(f'''<section class="iv iv-done">
  <div class="iv-head">
    <span class="iv-av {f["color"]}">{f["siglas"]}</span>
    <div class="iv-who"><div class="iv-kick">Cuestionario {i} de {len(fs)}</div><h3 class="iv-role" data-toc="7.{i + 1} {esc(f["perfil"])}">{esc(f["perfil"])}</h3><div class="iv-meta">Nivel {esc(f["nivel"]).lower()} · {esc(f["area"])} · {f["total"]} preguntas Likert y {len(f["abiertas"])} preguntas abiertas</div></div>
    <span class="pill pill-green">Aplicado</span>
  </div>
  <p class="iv-goal"><span>Objetivo</span>{esc(f["objetivo"])}</p>
  <div class="iv-sec"><span class="iv-sec-l">Preguntas Likert · promedio por tema</span>
  <div class="overflow-x-auto"><table class="wide"><thead><tr>
  <th style="width: 28%;">Tema (dimensión)</th><th style="width: 13%; text-align: center;">Preguntas Likert N.°</th><th style="width: 21%;">Números marcados ÷ cantidad</th><th style="width: 24%;">Promedio (1 a 5)</th><th style="width: 14%; text-align: center;">Nivel</th>
  </tr></thead><tbody>{drows}</tbody></table></div>
  <p class="lk-read">{reading}</p>
  <details class="lk-items"><summary>Ver las {f["total"]} preguntas Likert (afirmaciones) y el número que marcó este perfil</summary>
  <div class="overflow-x-auto"><table><thead><tr><th style="width: 8%; text-align: center;">N.°</th><th style="width: 62%;">Pregunta Likert (afirmación)</th><th style="width: 30%;">Número marcado</th></tr></thead><tbody>{items}</tbody></table></div>
  </details></div>
  <div class="iv-sec"><span class="iv-sec-l">Preguntas abiertas</span></div>
  <ol class="iv-qa">{qa}</ol>
</section>''')

    D = lambda n, l: f'{SHORT[n]} · {DIM(n, l)["t"].lower()}: <strong>{fmt(DIM(n, l)["media"])}</strong>'
    IT = lambda n, i: f'{SHORT[n]} · pregunta Likert {i}: <strong>{ITEM(n, i)}</strong>'
    hall = [
        ("La mercadería se guarda donde hay espacio, sin zonas definidas.", f'{D(2, "A")}<br>{D(3, "C")}', "Mercadería apilada en el piso y los pasillos (causa indirecta 1.1)"),
        ("Hay derrames que malogran otros productos y el personal se agacha constantemente para sacar cajas del piso.", D(3, "B"), "Líquidos y secos juntos (causa indirecta 1.2) y mermas y sobreesfuerzo (efecto directo 3)"),
        ("En la práctica sale primero lo que está a la mano y no lo más antiguo.", f'{D(2, "C")}<br>{IT(3, 12)}', "Sin registro de lotes ni PEPS (causa indirecta 1.3)"),
        ("El registro es manual: el stock registrado no aparece de 4 a 6 veces por semana y el conteo completo toma un día al mes.", f'{D(1, "B")}<br>{D(2, "B")}', "Pedidos sin validar el stock y conteo manual (causas indirectas 2.1 y 2.2)"),
        ("No hay manual; el trabajo se aprende mirando a los compañeros.", f'{D(1, "D")}<br>{D(2, "D")}<br>{IT(3, 13)}', "Sin manuales ni capacitación (causa indirecta 3.1)"),
        ("La ruta se ordena por experiencia y con un plano marcado a mano; las direcciones nuevas generan demoras.", D(4, "B"), "Rutas trazadas a mano (causa indirecta 4.2)"),
        ("Armar los pedidos de una zona toma de 1 a 3 horas y la unidad sale entre las 7:00 y las 8:00 a. m., cuando debería salir a las 6:00.", f'{D(3, "A")}<br>{D(4, "A")}', "Salida tardía del reparto (efecto directo 2)"),
        ("Las horas extra, las segundas entregas (3 o 4 al mes) y las mermas generan sobrecostos.", f'{D(1, "A")}<br>{D(4, "C")}', "Sobrecostos operativos (efecto indirecto 1)"),
    ]
    hrows = "".join(f'<tr><td>{esc(h)}</td><td>{e}</td><td>{c}</td></tr>' for h, e, c in hall)
    n = len(fs) + 2
    out.append(f'''{H3}7.{n} Hallazgos del Trabajo de Campo</h3>
<p class="text-justify mb-4">Cada hallazgo combina lo marcado en la escala con lo respondido en las preguntas abiertas. Estos hallazgos son la base con la que se construye el árbol de problemas del capítulo 8: la última columna indica qué causa o efecto de ese árbol sustenta cada uno.</p>
<div class="overflow-x-auto"><table><thead><tr>
<th style="width: 40%;">Hallazgo</th><th style="width: 30%;">Evidencia en la escala (promedio de 1 a 5)</th><th style="width: 30%;">Sustenta en el árbol (capítulo 8)</th>
</tr></thead><tbody>{hrows}</tbody></table></div>''')

    diag = [d for f in fs for d in f["dimensiones"] if d["tipo"] == "d"]
    fav = [d["media"] for f in fs for d in f["dimensiones"] if d["tipo"] == "f"]
    out.append(f'''{H3}7.{n + 1} Conclusiones del Trabajo de Campo</h3>
<ul class="list-disc pl-6 space-y-2 mb-4">
<li><strong>El diagnóstico se confirma:</strong> {sum(d["nivel"] == "Alto" for d in diag)} de las {len(diag)} dimensiones de diagnóstico alcanzan un nivel alto en los cuatro perfiles.</li>
<li><strong>El control manual es la causa con más respaldo:</strong> registro e inventario obtiene {fmt(DIM(2, "B")["media"])} y la supervisión reporta faltantes de stock varias veces por semana.</li>
<li><strong>La salida tardía nace en el almacén:</strong> armar los pedidos de una zona toma de 1 a 3 horas y la unidad sale entre las 7:00 y las 8:00 a. m. para atender alrededor de 100 clientes, con una ruta que termina cerca de las 6:00 p. m.</li>
<li><strong>El costo es relevante:</strong> la gerencia estima pérdidas de aproximadamente S/ 3,500 al mes y considera viable invertir entre S/ 5,000 y S/ 8,000 en una primera etapa, sin detener las ventas.</li>
<li><strong>Niveles medios:</strong> rotación y vencimientos ({fmt(DIM(2, "C")["media"])}), esfuerzo físico y seguridad ({fmt(DIM(3, "B")["media"])}) y calidad de la entrega ({fmt(DIM(4, "C")["media"])}) se presentan con menor intensidad que el desorden y el control manual.</li>
<li><strong>Disposición favorable:</strong> todos los perfiles muestran una disposición alta al cambio (de {fmt(min(fav))} a {fmt(max(fav))}); los temores se concentran en que los equipos fallen o en no saber usarlos, lo que pide una capacitación práctica.</li>
</ul>''')
    return title, dek, "\n".join(out)

uid = 0
def cover_art(m):
    global uid
    uid += 1
    a = m["art"]
    return (f'<div class="cover-art {a}"><svg class="pattern" aria-hidden="true"><defs>{PATTERNS[a].format(u=uid)}</defs>'
            f'<rect width="100%" height="100%" fill="url(#p{uid})"/></svg><span class="big">{m["n"]}</span>'
            f'<svg class="icon" width="34" height="34" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">{ICONS[a]}</svg></div>')


def cover(m):
    return f'<img src="{m["img"]}" alt="{m["cap"]}" loading="lazy">' if "img" in m else cover_art(m)


chapters = {m["id"]: read_chapter(m["id"]) for m in META if m["id"] != "cap7"}
t8, dek8, body8 = field_chapter()
chapters["cap7"] = (t8, body8)
next(m for m in META if m["id"] == "cap7")["dek"] = dek8

avatars = "".join(f'<span class="avatar {c}" title="{n}">{i}</span>' for i, n, c in TEAM)
total = len(META)

posts, cards, dropdown, mobile, foot = [], [], [], [], []
for idx, m in enumerate(META):
    title, body = chapters[m["id"]]
    m["title"] = title
    prev_m = META[idx - 1] if idx > 0 else None
    next_m = META[idx + 1] if idx < total - 1 else None

    cover_click = f' onclick="openLightbox(\'{m["img"]}\', \'{m["cap"]}\')"' if "img" in m else ""
    figcap = f'<figcaption>{m["cap"]}</figcaption>' if "img" in m else ""
    steps = "".join(f'<a href="#{x["id"]}"{" class=\"on\"" if x is m else (" class=\"done\"" if j < idx else "")} title="Capítulo {x["n"]}: {x["short"]}" aria-label="Capítulo {x["n"]}"></a>'
                    for j, x in enumerate(META))
    pager = ""
    if prev_m:
        pager += f'<a href="#{prev_m["id"]}" class="prev"><div class="l">← Capítulo anterior</div><div class="h">{chapters[prev_m["id"]][0]}</div></a>'
    if next_m:
        pager += f'<a href="#{next_m["id"]}" class="next"><div class="l">Siguiente capítulo →</div><div class="h">{chapters[next_m["id"]][0]}</div></a>'
    else:
        pager += '<a href="#inicio" class="next"><div class="l">Fin del documento</div><div class="h">Volver a la portada</div></a>'

    posts.append(f'''
    <article id="{m["id"]}" class="post">
      <header class="post-head wrap-narrow">
        <a href="#capitulos" class="crumbs">← Todos los capítulos</a>
        <div class="steps"><nav aria-label="Progreso de capítulos">{steps}</nav><span>{m["n"]} / {total:02d}</span></div>
        <div class="kicker">Capítulo {m["n"]} · {m["kicker"]}</div>
        <h1 class="post-title">{title}</h1>
        <p class="post-dek">{m["dek"]}</p>
        <div class="byline">
          <span class="avatar-stack">{avatars}</span>
          <span>Por <b>el equipo del proyecto</b></span>
          <span class="sep"></span>
          <span><span data-rt="{m["id"]}">—</span> min de lectura</span>
        </div>
      </header>
      <figure class="post-cover"><div class="frame"{cover_click}>{cover(m)}</div>{figcap}</figure>
      <div class="post-layout">
        <div class="post-body">{body}</div>
        <aside class="toc">
          <div class="t">En este capítulo</div>
          <nav></nav>
          <div class="share">
            <button type="button" onclick="copyLink('{m["id"]}')">Copiar enlace</button>
            <button type="button" onclick="window.print()">Imprimir</button>
          </div>
        </aside>
      </div>
      <div class="post-end">
        <div class="authors-box per-post">
          <span class="avatar-stack">{avatars}</span>
          <div>
            <div class="t">Escrito por</div>
            <p>Modesto Romero Bryan Adam, Julca Achas Cristian Sebastian, Felix Cecinario Hernan y Avalos Mendoza Jeshua Raul</p>
          </div>
        </div>
        <nav class="pager">{pager}</nav>
      </div>
    </article>''')

    featured = " featured" if idx == 0 else ""
    cards.append(f'''
        <a href="#{m["id"]}" class="card{featured} reveal">
          <div class="card-cover">{cover(m)}<span class="num">Cap {m["n"]}</span></div>
          <div class="card-body">
            <div class="kicker">{m["kicker"]}</div>
            <h3>{title}</h3>
            <p>{m["dek"]}</p>
            <div class="card-foot"><span><span data-rt="{m["id"]}">—</span> min de lectura</span><span class="go">Leer {ARROW}</span></div>
          </div>
        </a>''')
    dropdown.append(f'<a href="#{m["id"]}"><span class="n">{m["n"]}</span><span>{m["short"]}</span></a>')
    mobile.append(f'<a href="#{m["id"]}"><span class="n">{m["n"]}</span>{m["short"]}</a>')
    foot.append(f'<li><a href="#{m["id"]}">{m["n"]} · {m["short"]}</a></li>')

team = "".join(f'<div class="member"><span class="avatar {c}">{i}</span><h4>{n}</h4><span class="role">Integrativo / TI</span></div>' for i, n, c in TEAM)

voices = "".join(
    f'<li><a href="#cap7"><span class="iv-av {f["color"]}">{f["siglas"]}</span>'
    f'<span class="vl-txt"><span class="vl-role">{esc(f["perfil"])}</span><span class="vl-meta">Nivel {esc(f["nivel"]).lower()} · {f["total"]} preguntas Likert y {len(f["abiertas"])} preguntas abiertas</span></span>'
    f'<span class="pill pill-green">Aplicado</span>{ARROW}</a></li>'
    for f in CQ["formularios"])

out = TPL
for key, val in {
    "__DROPDOWN__": "\n            ".join(dropdown),
    "__MOBILEMENU__": "\n      ".join(mobile),
    "__AVATARS__": avatars,
    "__NCHAP__": str(total),
    "__CARDS__": "".join(cards),
    "__VOICES__": voices,
    "__VOICES_LEAD__": dek8,
    "__TEAM__": team,
    "__POSTS__": "".join(posts),
    "__FOOTLINKS__": "".join(foot),
    "__POSTMETA__": json.dumps([{"id": m["id"], "title": m["title"]} for m in META], ensure_ascii=False),
}.items():
    assert key in out, key
    out = out.replace(key, val)
(ROOT / "index.html").write_text(out, encoding="utf-8", newline="\n")
print("index.html", len(out), "bytes,", total, "capitulos")
