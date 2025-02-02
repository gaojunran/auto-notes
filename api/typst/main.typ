#import "/flow/src/lib.typ": *

#import "@preview/cmarker:0.1.1"

#import "@preview/tiaoma:0.2.1"

#import "@preview/mitex:0.2.4": mitex

#let stars = (i) => {
  set text(rgb("#8a3232")) if (i == 4 or i == 5)
  set text(rgb("#976c21")) if (i == 2 or i == 3)
  set text(gray) if (i == 1)
    [★] * i
}

#let content = json("content.json")

#let second = (.., last) => {
  [#last. ]
}

#show: note.with(
  title: content.topic,
  课程摘要: content.abstract,
  生成引擎: "Typst & Auto-Notes" 
)

#show heading.where(level: 1): set block(below: 1em)

#show heading.where(level: 1): set heading(numbering: it => {
  numbering("一、", it) + h(-0.6em)
})

#show heading.where(level: 2): set heading(numbering: second)

#show heading.where(level: 2): set block(below: 1em)



#for point in content.points {
  [
    = #point.name #stars(point.importance)
  ]
  for subtitle in point.subtitles {
    [
      == #subtitle.subtitle

      #cmarker.render(subtitle.md, math: mitex)
    ]
  }

  [#block(fill: rgb("#a4b99340"), inset: 8pt, radius: 4pt)[
    扫描二维码查看相关链接：
    #grid(columns: point.links.len(), gutter: 30pt,
      ..point.links.map(link => {
        set align(center)
        link.name
        tiaoma.qrcode(link.href, options: (
        scale: 1.5
      ))
    }
  ))
    

    
  
  ]]
}