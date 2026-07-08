// Simple numbering for non-book documents
#let equation-numbering = "(1)"
#let callout-numbering = "1"
#let subfloat-numbering(n-super, subfloat-idx) = {
  numbering("1a", n-super, subfloat-idx)
}

// Theorem configuration for theorion
// Simple numbering for non-book documents (no heading inheritance)
#let theorem-inherited-levels = 0

// Theorem numbering format (can be overridden by extensions for appendix support)
// This function returns the numbering pattern to use
#let theorem-numbering(loc) = "1.1"

// Default theorem render function
#let theorem-render(prefix: none, title: "", full-title: auto, body) = {
  if full-title != "" and full-title != auto and full-title != none {
    strong[#full-title.]
    h(0.5em)
  }
  body
}
// Some definitions presupposed by pandoc's typst output.
#let content-to-string(content) = {
  if content.has("text") {
    content.text
  } else if content.has("children") {
    content.children.map(content-to-string).join("")
  } else if content.has("body") {
    content-to-string(content.body)
  } else if content == [ ] {
    " "
  }
}

#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

// Some quarto-specific definitions.

#show raw.where(block: true): set block(
    fill: luma(230),
    width: 100%,
    inset: 8pt,
    radius: 2pt
  )

#let block_with_new_content(old_block, new_content) = {
  let fields = old_block.fields()
  let _ = fields.remove("body")
  if fields.at("below", default: none) != none {
    // TODO: this is a hack because below is a "synthesized element"
    // according to the experts in the typst discord...
    fields.below = fields.below.abs
  }
  block.with(..fields)(new_content)
}

#let empty(v) = {
  if type(v) == str {
    // two dollar signs here because we're technically inside
    // a Pandoc template :grimace:
    v.matches(regex("^\\s*$")).at(0, default: none) != none
  } else if type(v) == content {
    if v.at("text", default: none) != none {
      return empty(v.text)
    }
    for child in v.at("children", default: ()) {
      if not empty(child) {
        return false
      }
    }
    return true
  }

}

// Subfloats
// This is a technique that we adapted from https://github.com/tingerrr/subpar/
#let quartosubfloatcounter = counter("quartosubfloatcounter")

#let quarto_super(
  kind: str,
  caption: none,
  label: none,
  supplement: str,
  position: none,
  subcapnumbering: "(a)",
  body,
) = {
  context {
    let figcounter = counter(figure.where(kind: kind))
    let n-super = figcounter.get().first() + 1
    set figure.caption(position: position)
    [#figure(
      kind: kind,
      supplement: supplement,
      caption: caption,
      {
        show figure.where(kind: kind): set figure(numbering: _ => {
          let subfloat-idx = quartosubfloatcounter.get().first() + 1
          subfloat-numbering(n-super, subfloat-idx)
        })
        show figure.where(kind: kind): set figure.caption(position: position)

        show figure: it => {
          let num = numbering(subcapnumbering, n-super, quartosubfloatcounter.get().first() + 1)
          show figure.caption: it => block({
            num.slice(2) // I don't understand why the numbering contains output that it really shouldn't, but this fixes it shrug?
            [ ]
            it.body
          })

          quartosubfloatcounter.step()
          it
          counter(figure.where(kind: it.kind)).update(n => n - 1)
        }

        quartosubfloatcounter.update(0)
        body
      }
    )#label]
  }
}

// callout rendering
// this is a figure show rule because callouts are crossreferenceable
#show figure: it => {
  if type(it.kind) != str {
    return it
  }
  let kind_match = it.kind.matches(regex("^quarto-callout-(.*)")).at(0, default: none)
  if kind_match == none {
    return it
  }
  let kind = kind_match.captures.at(0, default: "other")
  kind = upper(kind.first()) + kind.slice(1)
  // now we pull apart the callout and reassemble it with the crossref name and counter

  // when we cleanup pandoc's emitted code to avoid spaces this will have to change
  let old_callout = it.body.children.at(1).body.children.at(1)
  let old_title_block = old_callout.body.children.at(0)
  let children = old_title_block.body.body.children
  let old_title = if children.len() == 1 {
    children.at(0)  // no icon: title at index 0
  } else {
    children.at(1)  // with icon: title at index 1
  }

  // TODO use custom separator if available
  // Use the figure's counter display which handles chapter-based numbering
  // (when numbering is a function that includes the heading counter)
  let callout_num = it.counter.display(it.numbering)
  let new_title = if empty(old_title) {
    [#kind #callout_num]
  } else {
    [#kind #callout_num: #old_title]
  }

  let new_title_block = block_with_new_content(
    old_title_block,
    block_with_new_content(
      old_title_block.body,
      if children.len() == 1 {
        new_title  // no icon: just the title
      } else {
        children.at(0) + new_title  // with icon: preserve icon block + new title
      }))

  align(left, block_with_new_content(old_callout,
    block(below: 0pt, new_title_block) +
    old_callout.body.children.at(1)))
}

// 2023-10-09: #fa-icon("fa-info") is not working, so we'll eval "#fa-info()" instead
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: false, 
    fill: background_color, 
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"), 
    width: 100%, 
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%, 
      below: 0pt, 
      block(
        fill: background_color,
        width: 100%,
        inset: 8pt)[#if icon != none [#text(icon_color, weight: 900)[#icon] ]#title]) +
      if(body != []){
        block(
          inset: 1pt, 
          width: 100%, 
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}




#let article(
  title: none,
  subtitle: none,
  authors: none,
  keywords: (),
  date: none,
  abstract-title: none,
  abstract: none,
  thanks: none,
  cols: 1,
  lang: "en",
  region: "US",
  font: none,
  fontsize: 11pt,
  title-size: 1.5em,
  subtitle-size: 1.25em,
  heading-family: none,
  heading-weight: "bold",
  heading-style: "normal",
  heading-color: black,
  heading-line-height: 0.65em,
  mathfont: none,
  codefont: none,
  linestretch: 1,
  sectionnumbering: none,
  linkcolor: none,
  citecolor: none,
  filecolor: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
) = {
  // Set document metadata for PDF accessibility
  set document(title: title, keywords: keywords)
  set document(
    author: authors.map(author => content-to-string(author.name)).join(", ", last: " & "),
  ) if authors != none and authors != ()
  set par(
    justify: true,
    leading: linestretch * 0.65em
  )
  set text(lang: lang,
           region: region,
           size: fontsize)
  set text(font: font) if font != none
  show math.equation: set text(font: mathfont) if mathfont != none
  show raw: set text(font: codefont) if codefont != none

  set heading(numbering: sectionnumbering)

  show link: set text(fill: rgb(content-to-string(linkcolor))) if linkcolor != none
  show ref: set text(fill: rgb(content-to-string(citecolor))) if citecolor != none
  show link: this => {
    if filecolor != none and type(this.dest) == label {
      text(this, fill: rgb(content-to-string(filecolor)))
    } else {
      text(this)
    }
   }

  let has-title-block = title != none or (authors != none and authors != ()) or date != none or abstract != none
  if has-title-block {
    place(
      top,
      float: true,
      scope: "parent",
      clearance: 4mm,
      block(below: 1em, width: 100%)[

        #if title != none {
          align(center, block(inset: 2em)[
            #set par(leading: heading-line-height) if heading-line-height != none
            #set text(font: heading-family) if heading-family != none
            #set text(weight: heading-weight)
            #set text(style: heading-style) if heading-style != "normal"
            #set text(fill: heading-color) if heading-color != black

            #text(size: title-size)[#title #if thanks != none {
              footnote(thanks, numbering: "*")
              counter(footnote).update(n => n - 1)
            }]
            #(if subtitle != none {
              parbreak()
              text(size: subtitle-size)[#subtitle]
            })
          ])
        }

        #if authors != none and authors != () {
          let count = authors.len()
          let ncols = calc.min(count, 3)
          grid(
            columns: (1fr,) * ncols,
            row-gutter: 1.5em,
            ..authors.map(author =>
                align(center)[
                  #author.name \
                  #author.affiliation \
                  #author.email
                ]
            )
          )
        }

        #if date != none {
          align(center)[#block(inset: 1em)[
            #date
          ]]
        }

        #if abstract != none {
          block(inset: 2em)[
          #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
          ]
        }
      ]
    )
  }

  if toc {
    let title = if toc_title == none {
      auto
    } else {
      toc_title
    }
    block(above: 0em, below: 2em)[
    #outline(
      title: toc_title,
      depth: toc_depth,
      indent: toc_indent
    );
    ]
  }

  doc
}

#set table(
  inset: 6pt,
  stroke: none
)
#let brand-color = (:)
#let brand-color-background = (:)
#let brand-logo = (:)

#set page(
  paper: "us-letter",
  margin: (x: 1.25in, y: 1.25in),
  numbering: "1",
  columns: 1,
)

#show: doc => article(
  title: [Aprendizaje No Supervisado y Clustering],
  subtitle: [Técnicas de aprendizaje de máquina],
  authors: (
    ( name: [Oscar Bustos],
      affiliation: [],
      email: [] ),
    ),
  date: [Invalid Date],
  toc_title: [Table of contents],
  toc_depth: 3,
  doc,
)

== Agenda
<agenda>
= Repaso
<repaso>
== Icebreaker: Trabajo Futuro
<icebreaker-trabajo-futuro>
#box(image("assets/FurureWork.png", width: 50.0%))

- ¿Cómo se realizará el trabajo en el futuro y quién lo llevará a cabo?

== Capítulos sobre Similaridad
<capítulos-sobre-similaridad>
#block[
#block[
#box(image("assets/IntroStatisticalLearning.png", width: 60.0%)) \\ Capítulo 12

]
#block[
#box(image("assets/DataScienceBusiness.jpg", width: 60.0%)) \\ Capítulo 6

]
]
== Comparación de Algoritmos
<comparación-de-algoritmos>
Comparación de distintos algoritmos para clasificación

#box(image("assets/comparacionAlgoritmosANN.png", width: 100.0%))

== Comparación de Algoritmos
<comparación-de-algoritmos-1>
Comparación de distintos algoritmos para regresión

#box(image("assets/ComparacionRegresion.png", width: 80.0%))

= Aprendizaje No Supervisado
<aprendizaje-no-supervisado>
== ¿Qué es el Aprendizaje No Supervisado?
<qué-es-el-aprendizaje-no-supervisado>
- A diferencia del supervisado, no utiliza etiquetas o variables objetivo.
- Se tienen N observaciones $\( X_1 \, X_2 \, . . . \, X_p \)$.
- Objetivo: Análisis exploratorio de datos.
  - Entender la estructura subyacente.
  - Visualizarla y usarla para análisis posteriores.
- Retos: ¿Cómo validar los resultados? ¿Qué características usar?

== Importancia del Aprendizaje No Supervisado
<importancia-del-aprendizaje-no-supervisado>
- La mayoría de problemas reales no tienen datos etiquetados.
- Obtener etiquetas es costoso (tiempo y dinero).
- Permite descubrir patrones y estructuras ocultas.

= Clustering
<clustering>
== Introducción al Clustering
<introducción-al-clustering>
- Tarea fundamental del aprendizaje no supervisado.
- Objetivo: encontrar grupos (clusters) de instancias.
- Alta similaridad intra-cluster, baja inter-cluster.
- Usos: segmentación, resumen, preprocesamiento.

== Tipos de Clustering
<tipos-de-clustering>
- #strong[Particional:] cada instancia en un clúster. Ej: K-Means.
- #strong[Jerárquico:] estructura en forma de árbol (dendrograma).
- #strong[Overlapping:] instancias en múltiples clústeres.
- #strong[Fuzzy:] pertenencia parcial a clústeres.

== Algoritmo K-Means
<algoritmo-k-means>
- Método particional popular.
- Requiere $K$ de antemano.
- Cada clúster representado por un centroide.
- Minimiza SSE: suma de distancias cuadradas al centroide.
- Usa heurísticas (es NP-completo).

== K-Means: Proceso Iterativo
<k-means-proceso-iterativo>
+ #strong[Inicialización:] elegir $K$ centroides (aleatorio o K-means++).
+ #strong[Asignación:] cada punto al centroide más cercano.
+ #strong[Actualización:] recalcular centroides.
+ Repetir hasta convergencia.

== K-Means: Seleccionando K (Método del Codo)
<k-means-seleccionando-k-método-del-codo>
- Ejecutar K-means para varios valores de $K$.
- Calcular SSE o similar.
- Graficar métrica vs.~$K$.
- Buscar el “codo” de la curva.

== K-Means: Limitaciones
<k-means-limitaciones>
- Sensible a inicialización.
- Puede converger a óptimos locales.
- Problemas con:
  - Clústeres de distintos tamaños, densidades, formas.
  - Presencia de outliers.
- $K$ debe definirse previamente.

== Clustering Jerárquico
<clustering-jerárquico>
- Construye una jerarquía de clústeres (dendrograma).
- No requiere $K$ de antemano.
- #strong[Tipos:]
  - Aglomerativo: bottom-up.
  - Divisivo: top-down.

== Visualización: Dendrograma
<visualización-dendrograma>
#box(image("assets/dendrograma.png", width: 80.0%))

#emph[Ejemplo de dendrograma en clustering jerárquico]

== DBSCAN (Density-Based Spatial Clustering)
<dbscan-density-based-spatial-clustering>
- Algoritmo basado en densidad.
- Agrupa puntos densos, separa por baja densidad.
- Detecta outliers naturalmente.
- #strong[Parámetros:] $epsilon$ y MinPts.

== Comparación de Algoritmos de Clustering
<comparación-de-algoritmos-de-clustering>
- #strong[K-Means:] rápido, sensible a outliers.
- #strong[Jerárquico:] interpretable, más costoso.
- #strong[DBSCAN:] robusto, no necesita $K$, falla con densidades variables.

#emph[La elección depende del problema y los datos.]

== Seleccionando Algoritmos
<seleccionando-algoritmos>
¿Cómo elijo el algoritmo más adecuado para mis datos? #box(image("assets/selectingAlgo.png", width: 80.0%))

= Ejemplo de Código
<ejemplo-de-código>
== Ejemplo de Código: RAG usando PDF
<ejemplo-de-código-rag-usando-pdf>
= Cierre
<cierre>
== Resumen y Cierre
<resumen-y-cierre>
- Aprendizaje no supervisado = descubrimiento sin etiquetas.
- Clustering: herramienta fundamental para agrupar.
- Elegir bien el algoritmo = clave del éxito.

#strong[¡Gracias por su atención!]

= Referencias
<referencias>
== References
<references>

#bibliography(("references.bib"))

