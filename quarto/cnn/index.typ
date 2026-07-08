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
  title: [Visión por Computador Profunda con CNNs],
  subtitle: [Redes Neuronales Convolucionales],
  authors: (
    ( name: [Oscar Bustos],
      affiliation: [],
      email: [] ),
    ),
  toc_title: [Table of contents],
  toc_depth: 3,
  doc,
)

= Introducción a la Corteza Visual
<introducción-a-la-corteza-visual>
== La Arquitectura de la Corteza Visual
<la-arquitectura-de-la-corteza-visual>
#box(image("assets/visual_cortex.png", width: 70.0%))

- Experimentos de Hubel y Wiesel (1958) en gatos y monos.
- Muchas neuronas tienen un #strong[campo receptivo local] pequeño (solo reaccionan a estímulos en una región limitada).
- Las neuronas de nivel superior se basan en salidas de neuronas de nivel inferior para detectar patrones complejos.
- Inspiró la arquitectura #strong[LeNet-5] (1998) introducida por Yann LeCun.

= Componentes de una CNN
<componentes-de-una-cnn>
== Capas Convolucionales
<capas-convolucionales>
#box(image("assets/conv_layer.png", width: 60.0%))

- Las neuronas no están conectadas a todos los píxeles, solo a los de su campo receptivo.
- Permite concentrarse en características de bajo nivel y luego ensamblarlas en características de alto nivel.
- #strong[Zero padding:] Añadir ceros alrededor de los bordes para mantener dimensiones.
- #strong[Stride (Paso):] Distancia entre campos receptivos consecutivos para reducir la dimensionalidad.

== Filtros y Mapas de Características
<filtros-y-mapas-de-características>
#box(image("assets/filters.png", width: 60.0%))

- Los pesos de una neurona se representan como un pequeño #strong[filtro] o #strong[kernel].
- Una capa completa aplicando el mismo filtro produce un #strong[Mapa de Características] (Feature Map).
- Una capa convolucional aplica múltiples filtros simultáneamente, detectando múltiples características (ej. líneas, bordes, texturas).

== Capas de Agrupación (Pooling)
<capas-de-agrupación-pooling>
#box(image("assets/max_pooling.png", width: 70.0%))

- #strong[Objetivo:] Submuestrear la imagen para reducir la carga computacional, la memoria y los parámetros.
- Funciona con un kernel y un stride, pero no tiene pesos. Aplica una función de agregación.
- #strong[Max Pooling:] Mantiene solo el valor máximo. Introduce invarianza a pequeñas traslaciones.
- #strong[Global Average Pooling:] Calcula la media de cada mapa de características entero.

= Arquitecturas Famosas de CNN
<arquitecturas-famosas-de-cnn>
== Evolución de las Arquitecturas CNN
<evolución-de-las-arquitecturas-cnn>
- #strong[LeNet-5 (1998):] Utilizada para reconocimiento de dígitos manuscritos. Usa convoluciones y average pooling.
- #strong[AlexNet (2012):] Ganadora de ILSVRC. Red mucho más grande y profunda, introdujo apilamiento directo de capas convolucionales y #emph[Data Augmentation].
- #strong[GoogLeNet (2014):] Introdujo módulos #emph[Inception] con capas de cuello de botella (kernels 1x1) para eficiencia de parámetros.
- #strong[ResNet (2015):] #emph[Residual Networks] de hasta 152 capas. Utiliza #strong[conexiones de salto (skip connections)] para evitar el desvanecimiento del gradiente.

== Conexiones Residuales (ResNet)
<conexiones-residuales-resnet>
#box(image("assets/residual_learning.png", width: 50.0%))

- Se añade la entrada $x$ a la salida de la capa: el modelo aprende $f \( x \) = h \( x \) - x$.
- Facilita el entrenamiento de redes extremadamente profundas al permitir que la señal fluya directamente.

= Implementación con Keras
<implementación-con-keras>
== Ejemplo de Código: Capas Convolucionales en Keras
<ejemplo-de-código-capas-convolucionales-en-keras>
== Ejemplo de Código: Transfer Learning con Modelos Preentrenados
<ejemplo-de-código-transfer-learning-con-modelos-preentrenados>
= Visión más allá de la Clasificación
<visión-más-allá-de-la-clasificación>
== Detección de Objetos
<detección-de-objetos>
#box(image("assets/object_detection.png", width: 60.0%))

- Clasificar y localizar múltiples objetos. El modelo predice un cuadro delimitador (bounding box) y una puntuación de "objetualidad" (objectness score).
- #strong[Métrica principal:] #emph[Intersection over Union] (IoU) y #emph[Mean Average Precision] (mAP).
- #strong[YOLO (You Only Look Once):] Arquitectura extremadamente rápida de un solo paso. Predice múltiples bounding boxes y probabilidades directamente de una cuadrícula.

== Segmentación Semántica
<segmentación-semántica>
#box(image("assets/semantic_segmentation.png", width: 70.0%))

- Clasificar cada píxel individual de la imagen según la clase a la que pertenece.
- Utiliza Redes Totalmente Convolucionales (#strong[FCNs]).
- Emplea capas convolucionales transpuestas (#emph[Transposed Convolution]) y conexiones de salto desde capas inferiores para recuperar la resolución espacial perdida en el proceso.

== Referencias
<referencias>



#bibliography(("references.bib"))

