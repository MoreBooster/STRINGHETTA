# Clínica Stringhetta – site

Site estático (HTML + CSS + JS, sem WordPress) recriado a partir da estrutura do site antigo
`clinicastringhetta.com.br`: Home, Procedimentos, uma página por procedimento e Contato.

## Estrutura

```
build.py              gerador: dados da clínica, procedimentos e templates
index.html            home (gerada)
procedimentos/        lista de procedimentos (gerada)
<slug>/index.html     página de cada procedimento (gerada)
contato/              contato + formulário que envia para o WhatsApp
procedimentos-2-0/, vsl-*/, botox-captura/   redirecionamentos das URLs antigas
assets/css/style.css  estilos
assets/js/main.js     menu mobile, animações, formulário → WhatsApp
assets/img/           imagens (os .svg são provisórios)
sitemap.xml, robots.txt, 404.html
```

## Como editar

1. Altere textos, contatos ou procedimentos em `build.py` (`CONFIG`, `PROCEDURES`, `FEATURED`, `TESTIMONIALS`).
2. Rode `python3 build.py` para regerar as páginas.
3. Teste localmente: `python3 -m http.server 8080` e abra http://localhost:8080

## Espaço Kids

Seção da home com âncora `#espaco-kids` (link no menu). Textos, itens e a foto ficam na função `kids_section()` do `build.py`; para trocar a foto provisória, salve a imagem em `assets/img/` e ajuste o `src` da `kids-photo`.

## Visual

Paleta creme e dourado, com variáveis no topo de `assets/css/style.css`, e fonte sem serifa Manrope.

## Imagens

- **Foto do hero:** salve como `assets/img/hero.jpg` (paisagem, cerca de 2400×1400). Ela aparece automaticamente com uma sobreposição dourada; sem ela, fica o degradê dourado.

- **Fotos dos procedimentos:** salve em `assets/img/` e adicione `"image": "/assets/img/nome.jpg"` (e opcionalmente `"image_alt"`) ao procedimento no `build.py`. A foto aparece no card da home, na página de procedimentos e na página do próprio procedimento.

As imagens em `assets/img/*.svg` são provisórias. Substitua pelas fotos reais (de preferência `.webp`)
mantendo o mesmo nome, ou altere o caminho na função `placeholder()` do `build.py`.

## Publicação

Funciona em qualquer hospedagem estática (Hostinger, Netlify, Vercel, GitHub Pages, cPanel).
Basta enviar todos os arquivos para a raiz do domínio.
