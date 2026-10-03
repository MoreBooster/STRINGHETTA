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

## Imagens

As imagens em `assets/img/*.svg` são provisórias. Substitua pelas fotos reais (de preferência `.webp`)
mantendo o mesmo nome, ou altere o caminho na função `placeholder()` do `build.py`.

## Publicação

Funciona em qualquer hospedagem estática (Hostinger, Netlify, Vercel, GitHub Pages, cPanel).
Basta enviar todos os arquivos para a raiz do domínio.
