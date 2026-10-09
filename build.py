#!/usr/bin/env python3
"""Gera o site estático da Clínica Stringhetta.

Edite os dados em CONFIG e PROCEDURES e rode:  python3 build.py
Cada procedimento vira uma página em /<slug>/index.html.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).parent

CONFIG = {
    "name": "Clínica Stringhetta",
    "whatsapp": "5511933537351",
    "phone": "(11) 93353-7351",
    "instagram": "https://www.instagram.com/clinicastringhetta/",
    "instagram_user": "clinicastringhetta",
    "facebook": "https://www.facebook.com/profile.php?id=100075366247737",
    "hours": "Atendimento com hora marcada",
    "units": [
        {
            "name": "Unidade Tatuapé",
            "address": "R. Coelho Lisboa, 544 – Tatuapé",
            "city": "São Paulo – SP · CEP 03323-040",
        },
        {
            "name": "Unidade Moema",
            "address": "Alameda dos Maracatins, 176 – Moema",
            "city": "São Paulo – SP",
        },
    ],
}

# category: "odonto" | "estetica" | "saude"
PROCEDURES = [
    {
        "slug": "preenchimento-labial", "title": "Preenchimento labial", "category": "estetica", "icon": "◡",
        "image": "/assets/img/preenchimento-labial.jpg", "image_alt": "Lábios de paciente após preenchimento labial",
        "short": "Volume, contorno e hidratação para lábios mais harmoniosos com ácido hialurônico.",
        "intro": "Com ácido hialurônico de alta qualidade, o preenchimento labial devolve volume, define o contorno e melhora a hidratação, sempre respeitando as proporções do seu rosto.",
        "benefits": ["Contorno e volume sob medida", "Correção de assimetrias",
                     "Hidratação profunda dos lábios", "Produto absorvível e reversível"],
        "faq": [("O resultado fica artificial?", "Não. Planejamos a quantidade e a técnica para valorizar seus traços com naturalidade."),
                ("Quanto tempo dura?", "Geralmente de 9 a 12 meses."),
                ("Tem inchaço?", "Pode haver um leve inchaço nas primeiras 48 horas, que regride espontaneamente.")],
    },
    {
        "slug": "ulthera", "title": "Ulthera", "category": "estetica", "icon": "◌",
        "short": "Ultrassom microfocado com visualização em tempo real para lifting e firmeza sem cirurgia.",
        "intro": "O Ulthera permite visualizar as camadas da pele durante a aplicação, direcionando a energia com precisão para estimular colágeno e promover efeito lifting em rosto, pescoço e colo.",
        "benefits": ["Lifting não cirúrgico", "Aplicação guiada por imagem",
                     "Estímulo de colágeno de longa duração", "Sem afastamento da rotina"],
        "faq": [("Quando aparece o resultado?", "A melhora é progressiva, com pico entre 2 e 3 meses após a sessão.")],
        "wa": "Vi sobre os protocolos com Ulthera no site e quero saber mais!",
    },
    {
        "slug": "lavieen", "title": "Laser Lavieen", "category": "estetica", "icon": "✧",
        "short": "Laser para viço, textura, manchas e poros, com recuperação rápida.",
        "intro": "O Lavieen é um laser de túlio que renova a superfície da pele, tratando manchas, poros dilatados e textura irregular, e devolvendo o viço com pouco tempo de recuperação.",
        "benefits": ["Pele mais uniforme e luminosa", "Tratamento de manchas e melasma",
                     "Redução de poros e textura", "Recuperação rápida"],
        "faq": [("Quantas sessões são indicadas?", "Normalmente de 3 a 5 sessões, com intervalo mensal, conforme avaliação.")],
        "wa": "Vi sobre os protocolos com Laser Lavieen no site e quero saber mais!",
    },
    {
        "slug": "harmonizacao-facial", "title": "Harmonização facial", "category": "estetica", "icon": "◇",
        "short": "Conjunto de procedimentos que equilibra proporções e realça a beleza do rosto.",
        "intro": "A harmonização facial combina técnicas como preenchimentos, toxina botulínica e bioestimuladores em um plano único, desenhado a partir da análise do seu rosto.",
        "benefits": ["Planejamento facial individual", "Equilíbrio entre queixo, mandíbula e maçãs do rosto",
                     "Combinação de técnicas minimamente invasivas", "Resultados progressivos e naturais"],
        "faq": [("Quantas sessões são necessárias?", "Depende do plano. Muitos casos são resolvidos em 1 ou 2 sessões."),
                ("Quem pode fazer?", "Adultos saudáveis após avaliação presencial com nossos especialistas.")],
    },
    {
        "slug": "bioestimulador", "title": "Bioestimulador de colágeno", "category": "estetica", "icon": "✺",
        "short": "Estimula a produção de colágeno para mais firmeza e qualidade da pele.",
        "intro": "Os bioestimuladores ativam a produção natural de colágeno, tratando flacidez e melhorando a textura da pele de forma gradual e duradoura.",
        "benefits": ["Mais firmeza e sustentação", "Melhora da textura da pele",
                     "Efeito gradual e natural", "Resultados que duram até 2 anos"],
        "faq": [("Indicado para qual idade?", "A partir dos 30 anos, ou quando surgem os primeiros sinais de flacidez.")],
    },
    {
        "slug": "clareamento-dental", "title": "Clareamento dental", "category": "odonto", "icon": "☼",
        "short": "Dentes mais brancos com técnicas seguras em consultório ou em casa.",
        "intro": "O clareamento dental remove pigmentações e deixa o sorriso vários tons mais claro, com protocolos que preservam o esmalte e controlam a sensibilidade.",
        "benefits": ["Opções em consultório e caseira", "Controle de sensibilidade",
                     "Resultados visíveis desde a primeira sessão", "Acompanhamento profissional"],
        "faq": [("O clareamento enfraquece os dentes?", "Não, quando feito com acompanhamento profissional e produtos adequados.")],
    },
    {
        "slug": "lentes-em-resina-estratificada", "title": "Lentes em resina estratificada", "category": "odonto", "icon": "◎",
        "image": "/assets/img/lentes-em-resina-estratificada.jpg", "image_alt": "Sorriso de paciente com lentes em resina estratificada",
        "short": "Facetas em resina aplicadas em camadas para corrigir cor, formato e proporção do sorriso.",
        "intro": "A técnica estratificada aplica a resina em camadas, reproduzindo a translucidez do dente natural. O resultado é um sorriso mais harmônico, em poucas sessões e sem desgastes agressivos.",
        "benefits": ["Planejamento estético do sorriso", "Mínimo ou nenhum desgaste dental",
                     "Aparência natural, com camadas de cor", "Reparos simples quando necessário"],
        "faq": [("Quanto tempo duram?", "Com higiene adequada e consultas de manutenção, duram vários anos."),
                ("Qual a diferença para a porcelana?", "A resina é feita direto no consultório, com menor custo e reparo mais simples; a porcelana tem maior resistência a manchas.")],
    },
]

FEATURED = ["preenchimento-labial", "harmonizacao-facial", "ulthera", "lavieen", "bioestimulador", "lentes-em-resina-estratificada"]

CATEGORIES = {
    "estetica": "Estética facial",
    "odonto": "Odontologia",
    "saude": "Saúde e bem-estar",
}

TESTIMONIALS = [
    # Trechos de avaliações públicas do Google
    ("Atendimento impecável desde a recepção. Tratamento humanizado e personalizado.", "Claudeny Matos"),
    ("Apaixonada pelo atendimento e por todos os serviços prestados na clínica. Confio 100%.", "Kellen Sanches"),
    ("Clínica maravilhosa, meninas atenciosas. Feliz em conhecer vocês!", "Priscila Raposo Vieira"),
]

# Vídeos do Instagram (assets/video/). Adicione mais itens para ampliar o carrossel.
VIDEOS = [
    {"file": "video-1", "label": "Paciente vendo o resultado no espelho"},
    {"file": "video-2", "label": "Consulta de avaliação na clínica"},
    {"file": "video-3", "label": "Te recebendo, te escutando, te realçando"},
    {"file": "video-4", "label": "Paciente após o procedimento"},
]

WHATS_ICON = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.3.6 4.5 1.8 6.4L3 29l7.2-1.9c1.8 1 3.8 1.5 5.8 1.5 7 0 12.7-5.7 12.7-12.6C28.7 8.6 23 3 16 3zm0 23.2c-1.9 0-3.7-.5-5.3-1.4l-.4-.2-4.3 1.1 1.1-4.2-.3-.4a10.4 10.4 0 0 1-1.6-5.5C5.2 9.8 10 5.1 16 5.1s10.8 4.7 10.8 10.5S22 26.2 16 26.2zm5.9-7.8c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.8.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.7 1.2 3.2 1.4 3.4 2.4 3.6 5.7 5c2.1.9 2.9 1 4 .8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5l-.6-.4z"/></svg>'


def wa_link(text="Olá! Gostaria de agendar uma avaliação."):
    return f"https://wa.me/{CONFIG['whatsapp']}?text={quote(text)}"


def placeholder(label, w=800, h=1000):
    """Cria uma imagem SVG provisória. Substitua pelas fotos reais em assets/img/."""
    name = label.lower().replace(" ", "-")
    path = ROOT / "assets" / "img" / f"{name}.svg"
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#efe3cc"/><stop offset="1" stop-color="#c9a464"/></linearGradient></defs>'
        f'<rect width="100%" height="100%" fill="url(#g)"/>'
        f'<text x="50%" y="50%" text-anchor="middle" font-family="Manrope,Arial,sans-serif" font-weight="300" font-size="{w//18}" fill="#5a4626" opacity=".6">{escape(label)}</text>'
        f'</svg>', encoding="utf-8")
    return f"/assets/img/{name}.svg"


def socials():
    ig = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>'
    fb = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.9v3h2.6V21z"/></svg>'
    wa = WHATS_ICON
    return (f'<a href="{CONFIG["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{ig}</a>'
            f'<a href="{CONFIG["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook">{fb}</a>'
            f'<a href="{wa_link()}" target="_blank" rel="noopener" aria-label="WhatsApp">{wa}</a>')


def nav(current):
    def cur(key):
        return ' aria-current="page"' if current == key else ""
    sub = "".join(f'<li><a href="/{p["slug"]}/">{escape(p["title"])}</a></li>' for p in PROCEDURES)
    return f"""
<header class="header{' header--overlay' if current == 'home' else ''}"><div class="container">
  <a href="/" class="logo" aria-label="{CONFIG['name']} – início"><span class="logo-img" role="img" aria-label="{CONFIG['name']}"></span></a>
  <button class="menu-toggle" aria-label="Abrir menu" aria-expanded="false">☰</button>
  <div class="header-right">
  <div class="social social--header">{socials()}</div>
  <nav class="nav" aria-label="Principal"><ul>
    <li><a href="/"{cur('home')}>Início</a></li>
    <li><a href="/#sobre">A clínica</a></li>
    <li class="has-sub"><a href="/procedimentos/"{cur('procedimentos')}>Procedimentos</a><ul class="submenu">{sub}</ul></li>
    <li><a href="/#espaco-kids" class="nav-kids">Espaço Kids</a></li>
    <li><a href="/#unidades">Unidades</a></li>
    <li><a href="/contato/"{cur('contato')}>Contato</a></li>
    <li><a class="btn btn--primary" href="{wa_link()}" target="_blank" rel="noopener">Agende ↗</a></li>
  </ul></nav>
  </div>
</div></header>"""


def footer():
    estetica = "".join(f'<li><a href="/{p["slug"]}/">{escape(p["title"])}</a></li>' for p in PROCEDURES if p["category"] == "estetica")
    odonto = "".join(f'<li><a href="/{p["slug"]}/">{escape(p["title"])}</a></li>' for p in PROCEDURES if p["category"] != "estetica")
    units = "".join(f'<li><strong>{escape(u["name"])}</strong><br>{escape(u["address"])}<br>{escape(u["city"])}</li>' for u in CONFIG["units"])
    return f"""
<footer class="footer"><div class="container">
  <div class="footer-grid">
    <div>
      <a href="/" class="logo" aria-label="{CONFIG['name']} – início"><span class="logo-img" role="img" aria-label="{CONFIG['name']}"></span></a>
      <p style="margin-top:14px">Odontologia e estética com atendimento humanizado, tecnologia e resultados naturais.</p>
      <div class="social">{socials()}</div>
    </div>
    <div><h4>Estética</h4><ul>{estetica}</ul></div>
    <div><h4>Odontologia</h4><ul>{odonto}</ul></div>
    <div><h4>Unidades</h4><ul>{units}</ul></div>
  </div>
  <div class="footer-bottom">
    <span>© <span data-year></span> {CONFIG['name']}. Todos os direitos reservados.</span>
    <span>Desenvolvido por Mathews Laragnoit</span>
  </div>
</div></footer>
<a class="whats-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Fale conosco no WhatsApp">{WHATS_ICON}</a>
<script src="/assets/js/main.js" defer></script>"""


def page(title, description, body, current=""):
    full_title = f"{title} | {CONFIG['name']}" if title != CONFIG["name"] else title
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description)}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#c9a464">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Fredoka:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
{nav(current)}
<div class="scroll-progress" aria-hidden="true"></div>
<main>
{body}
</main>
{footer()}
</body>
</html>
"""


def card(p):
    img = p.get("image") or placeholder(p["title"], 1000, 800)
    alt = escape(p.get("image_alt", p["title"]))
    return f"""<a class="card card--media reveal" href="/{p['slug']}/">
  <div class="card-media">
    <img src="{img}" alt="{alt}" loading="lazy" width="1000" height="800">
    <span class="tag">{CATEGORIES[p['category']]}</span>
  </div>
  <div class="card-body">
    <span class="icon">{p['icon']}</span>
    <h3>{escape(p['title'])}</h3>
    <p>{escape(p['short'])}</p>
    <span class="more">Saiba mais</span>
  </div>
</a>"""


def units_section():
    blocks = ""
    for u in CONFIG["units"]:
        q = quote(f"{u['address']}, {u['city'].split(' · ')[0]}")
        blocks += f"""<div class="unit reveal">
    <iframe loading="lazy" title="Mapa – {escape(u['name'])}" src="https://maps.google.com/maps?q={q}&output=embed"></iframe>
    <div class="unit-body">
      <span class="location-mark" aria-hidden="true">✳</span>
      <h3>{escape(u['name'])}</h3>
      <p>{escape(u['address'])}<br>{escape(u['city'])}</p>
      <p>{escape(CONFIG['hours'])}</p>
      <div class="location-actions">
        <a class="btn btn--primary" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">Como chegar ↗</a>
        <a class="btn btn--outline" href="https://waze.com/ul?q={q}&navigate=yes" target="_blank" rel="noopener">Waze</a>
      </div>
    </div>
  </div>"""
    return f"""<section class="section" id="unidades"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Onde estamos</span><h2>Duas unidades em São Paulo</h2>
  <p>Escolha a mais perto de você: Tatuapé, na Zona Leste, ou Moema, na Zona Sul.</p></div>
  <div class="grid grid-2">{blocks}</div>
</div></section>"""


def cta_section(text="Agende sua avaliação"):
    return f"""<section class="section section--cta"><div class="container reveal">
  <h2>{escape(text)}</h2>
  <p>Converse com nossa equipe pelo WhatsApp e encontre o tratamento ideal para você.</p>
  <a class="btn btn--whats" href="{wa_link()}" target="_blank" rel="noopener">Falar no WhatsApp</a>
</div></section>"""


def testimonials_section():
    items = "".join(f"""<blockquote class="testimonial reveal"><div class="stars">★★★★★</div>
  <p>“{escape(t)}”</p><cite>{escape(a)}</cite></blockquote>""" for t, a in TESTIMONIALS)
    return f"""<section class="section section--alt"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Depoimentos</span><h2>Nota máxima de avaliação no Google!</h2>
  <p>Confira alguns comentários de pacientes que frequentaram nosso espaço.</p></div>
  <div class="grid grid-3">{items}</div>
</div></section>"""


def marquee(items, reverse=False):
    row = "".join(f"<span>{escape(t)}</span><i>✳</i>" for t in items)
    cls = " marquee--reverse" if reverse else ""
    return f'''<div class="marquee{cls}" aria-hidden="true"><div class="marquee-track">{row}{row}{row}</div></div>'''


def videos_section():
    sound_icon = ('<svg class="i-muted" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/>'
                  '<path d="M16 9l5 5M21 9l-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
                  '<svg class="i-sound" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/>'
                  '<path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>')
    reels = "".join(f"""<figure class="reel">
      <video src="/assets/video/{v['file']}.mp4" poster="/assets/video/{v['file']}.jpg" muted loop playsinline autoplay preload="metadata" aria-label="{escape(v['label'])}"></video>
      <button class="reel-toggle" type="button" aria-label="Assistir com som: {escape(v['label'])}" aria-pressed="false">
        <span class="reel-hint">Toque para ouvir</span>
        <span class="reel-sound">{sound_icon}</span>
      </button>
      <span class="reel-progress" aria-hidden="true"><span></span></span>
    </figure>""" for v in VIDEOS)
    dots = "".join(f'<button type="button" aria-label="Ir para o vídeo {i + 1}"></button>' for i in range(len(VIDEOS)))
    return f"""<section class="section reels-section" id="videos"><div class="container">
  <div class="reels-head reveal">
    <div>
      <span class="eyebrow">Instagram</span>
      <h2>A clínica em movimento</h2>
      <p>Bastidores, acolhimento e resultados reais. Toque em um vídeo para assistir com som.</p>
    </div>
    <div class="reels-controls">
      <button class="reels-arrow" type="button" data-dir="-1" aria-label="Vídeo anterior">←</button>
      <button class="reels-arrow" type="button" data-dir="1" aria-label="Próximo vídeo">→</button>
    </div>
  </div>
  <div class="reels-track reveal" tabindex="0" aria-label="Vídeos do Instagram da clínica">{reels}</div>
  <div class="reels-footer">
    <div class="reels-dots">{dots}</div>
    <a class="btn btn--primary" href="{CONFIG['instagram']}" target="_blank" rel="noopener">Seguir @{CONFIG['instagram_user']} ↗</a>
  </div>
</div></section>"""


def kids_section():
    """Seção Espaço Kids da home (âncora #espaco-kids)."""
    # Brinquedos ilustrados (desenhos originais em SVG, na paleta creme e dourado)
    ink, ivory, cream, gold, gold2, soft = "#8a6a33", "#fffbf4", "#f4e3c3", "#c9a464", "#b08a4a", "#ead9b6"
    dino = f"""<svg class="kids-toy kids-toy--dino" viewBox="0 0 170 140" aria-hidden="true">
      <ellipse cx="80" cy="132" rx="58" ry="6" fill="rgba(138,106,51,.18)"/>
      <path d="M34 92 Q10 88 6 70 Q26 84 44 82" fill="{cream}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M52 62l6-14 8 13 8-15 8 15 8-13 6 14" fill="{gold}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>
      <ellipse cx="74" cy="90" rx="42" ry="28" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <path d="M100 76 Q108 46 116 32 Q122 16 140 18 Q158 22 154 38 Q150 50 134 48 Q126 64 114 92" fill="{cream}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <rect x="44" y="104" width="16" height="24" rx="7" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <rect x="84" y="104" width="16" height="24" rx="7" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <circle cx="62" cy="88" r="6" fill="{soft}"/><circle cx="80" cy="98" r="4.5" fill="{soft}"/><circle cx="90" cy="82" r="3.5" fill="{soft}"/>
      <circle cx="140" cy="30" r="4.5" fill="#3a2e1c"/><circle cx="141.5" cy="28.5" r="1.5" fill="#fff"/>
      <path d="M140 40q6 4 11-1" fill="none" stroke="#3a2e1c" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="132" cy="38" rx="4" ry="2.5" fill="{soft}"/>
    </svg>"""
    doll = f"""<svg class="kids-toy kids-toy--doll" viewBox="0 0 120 170" aria-hidden="true">
      <ellipse cx="60" cy="164" rx="34" ry="5" fill="rgba(138,106,51,.18)"/>
      <circle cx="26" cy="40" r="12" fill="{gold2}" stroke="{ink}" stroke-width="3.5"/>
      <circle cx="94" cy="40" r="12" fill="{gold2}" stroke="{ink}" stroke-width="3.5"/>
      <rect x="44" y="132" width="10" height="26" rx="5" fill="{cream}" stroke="{ink}" stroke-width="3.5"/>
      <rect x="66" y="132" width="10" height="26" rx="5" fill="{cream}" stroke="{ink}" stroke-width="3.5"/>
      <path d="M32 92 Q20 108 18 118" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
      <path d="M32 92 Q20 108 18 118" stroke="{cream}" stroke-width="4" stroke-linecap="round"/>
      <path d="M88 92 Q100 108 102 118" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
      <path d="M88 92 Q100 108 102 118" stroke="{cream}" stroke-width="4" stroke-linecap="round"/>
      <path d="M42 80 H78 L94 138 H26 Z" fill="{gold}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M32 120 H88" stroke="{ivory}" stroke-width="4" stroke-dasharray="2 7" stroke-linecap="round"/>
      <circle cx="60" cy="50" r="30" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <path d="M31 46 Q34 20 60 20 Q86 20 89 46 Q74 34 60 38 Q46 34 31 46z" fill="{gold2}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>
      <circle cx="50" cy="54" r="3.8" fill="#3a2e1c"/><circle cx="70" cy="54" r="3.8" fill="#3a2e1c"/>
      <ellipse cx="44" cy="63" rx="5" ry="3" fill="{soft}"/><ellipse cx="76" cy="63" rx="5" ry="3" fill="{soft}"/>
      <path d="M54 66q6 5 12 0" fill="none" stroke="#3a2e1c" stroke-width="3" stroke-linecap="round"/>
    </svg>"""
    bow = f"""<svg class="kids-toy kids-toy--bow" viewBox="0 0 140 110" aria-hidden="true">
      <path d="M62 52 L40 98 L54 92 L60 106 L70 60" fill="{gold2}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M78 52 L100 98 L86 92 L80 106 L70 60" fill="{gold2}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M70 50 C50 20 10 14 12 42 C14 70 52 66 70 50z" fill="{gold}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M70 50 C90 20 130 14 128 42 C126 70 88 66 70 50z" fill="{gold}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M28 40 C34 32 48 34 56 44 M112 40 C106 32 92 34 84 44" fill="none" stroke="{ivory}" stroke-width="3" stroke-linecap="round" opacity=".7"/>
      <rect x="60" y="38" width="20" height="24" rx="8" fill="{gold2}" stroke="{ink}" stroke-width="4"/>
    </svg>"""
    car = f"""<svg class="kids-toy kids-toy--car" viewBox="0 0 170 110" aria-hidden="true">
      <ellipse cx="86" cy="104" rx="66" ry="5" fill="rgba(138,106,51,.18)"/>
      <path d="M50 44 Q58 18 84 18 H104 Q122 18 132 44" fill="{ivory}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M62 44 Q66 28 82 28 H90 V44 Z" fill="{soft}" stroke="{ink}" stroke-width="3"/>
      <path d="M98 28 H104 Q116 28 120 44 H98 Z" fill="{soft}" stroke="{ink}" stroke-width="3"/>
      <rect x="16" y="42" width="144" height="40" rx="18" fill="{gold}" stroke="{ink}" stroke-width="4"/>
      <circle cx="150" cy="58" r="5" fill="{ivory}" stroke="{ink}" stroke-width="2.5"/>
      <rect x="22" y="54" width="10" height="7" rx="3" fill="{gold2}"/>
      <path d="M40 52 H140" stroke="{ivory}" stroke-width="3.5" stroke-linecap="round" opacity=".55"/>
      <g class="kids-wheel"><circle cx="50" cy="84" r="16" fill="#5a4626" stroke="{ink}" stroke-width="4"/><circle cx="50" cy="84" r="6" fill="{cream}"/><path d="M50 72v24M38 84h24" stroke="{cream}" stroke-width="2.5"/></g>
      <g class="kids-wheel"><circle cx="126" cy="84" r="16" fill="#5a4626" stroke="{ink}" stroke-width="4"/><circle cx="126" cy="84" r="6" fill="{cream}"/><path d="M126 72v24M114 84h24" stroke="{cream}" stroke-width="2.5"/></g>
    </svg>"""
    mascot = dino + doll + bow + car
    icons = {
        "play": '<svg viewBox="0 0 48 48"><rect x="6" y="20" width="16" height="16" rx="3"/><rect x="26" y="20" width="16" height="16" rx="3"/><rect x="16" y="6" width="16" height="14" rx="3"/></svg>',
        "art": '<svg viewBox="0 0 48 48"><path d="M24 6C13 6 6 14 6 23c0 9 7 15 13 15 4 0 4-3 3-5-1-3 1-5 4-5h6c6 0 10-4 10-10C42 11 34 6 24 6z"/><circle cx="16" cy="20" r="3" fill="#fffbf4"/><circle cx="24" cy="14" r="3" fill="#fffbf4"/><circle cx="33" cy="18" r="3" fill="#fffbf4"/></svg>',
        "safe": '<svg viewBox="0 0 48 48"><path d="M24 5l16 6v11c0 11-7 18-16 21C15 40 8 33 8 22V11z"/><path d="M17 24l5 5 9-10" fill="none" stroke="#fffbf4" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        "heart": '<svg viewBox="0 0 48 48"><path d="M24 41S6 30 6 17c0-6 5-11 11-11 4 0 6 2 7 4 1-2 3-4 7-4 6 0 11 5 11 11 0 13-18 24-18 24z"/></svg>',
    }
    items = [
        ("play", "Brincadeiras", "Brinquedos e livrinhos para os pequenos se divertirem."),
        ("art", "Criatividade", "Atividades para colorir, desenhar e soltar a imaginação."),
        ("safe", "Ambiente seguro", "Um espaço acolhedor, limpo e pensado para crianças."),
        ("heart", "Você tranquila", "Enquanto você se cuida, eles ficam bem pertinho."),
    ]
    cards = "".join(f"""<div class="kids-card reveal">
        <span class="kids-icon">{icons[k]}</span>
        <h3>{t}</h3><p>{d}</p>
      </div>""" for k, t, d in items)
    shapes = "".join(f'<span class="kids-shape kids-shape--{n}" data-float="{f}" aria-hidden="true"></span>'
                     for n, f in [("star", .25), ("circle", -.18), ("cloud", .12), ("squiggle", -.22), ("dot", .3), ("star2", -.15)])
    return f"""<section class="kids" id="espaco-kids">
  <svg class="kids-wave kids-wave--top" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80V40c120-30 240-30 360 0s240 30 360 0 240-30 360 0 240 30 360 0V80z"/></svg>
  {shapes}
  <div class="container">
    <div class="kids-grid">
      <div class="kids-intro reveal">
        <span class="kids-badge">✦ Espaço Kids ✦</span>
        <h2>Um cantinho feito para os pequenos</h2>
        <p>Trouxe as crianças? Elas são super bem-vindas! Nosso Espaço Kids é um ambiente lúdico e aconchegante para os pequenos brincarem enquanto você aproveita o seu momento de autocuidado.</p>
        <a class="btn kids-btn" href="{wa_link("Olá! Quero saber mais sobre o Espaço Kids.")}" target="_blank" rel="noopener">Quero saber mais ↗</a>
      </div>
      <div class="kids-visual reveal">
        <div class="kids-photo"><img src="{placeholder('Foto do Espaço Kids', 800, 800)}" alt="Espaço Kids da Clínica Stringhetta" loading="lazy" width="800" height="800"></div>
        {mascot}
      </div>
    </div>
    <div class="kids-cards">{cards}</div>
  </div>
  <svg class="kids-wave kids-wave--bottom" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0v40c120 30 240 30 360 0s240-30 360 0 240 30 360 0 240-30 360 0V0z"/></svg>
</section>"""


def home():
    featured = "".join(card(p) for p in PROCEDURES if p['slug'] in FEATURED)
    body = f"""
<section class="hero">
  <video class="hero-video" data-autoplay src="/assets/video/hero.mp4" poster="/assets/video/hero.jpg" muted autoplay loop playsinline preload="auto" aria-hidden="true"></video>
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="hero-rays" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div class="hero-copy" data-hero-copy>
      <span class="hero-kicker">+53.000 autoestimas renovadas</span>
      <h1>Realce a sua <br>beleza natural</h1>
      <p class="lead">Odontologia e estética com planejamento individual <br>e resultados naturais, no Tatuapé e em Moema.</p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="{wa_link()}" target="_blank" rel="noopener">Fale com um especialista ↗</a>
        <a class="btn btn--ghost" href="/procedimentos/">Procedimentos</a>
      </div>
    </div>
  </div>
  <div class="container hero-strip" data-hero-strip>
    <div class="strip-card strip-card--photo reveal"><img src="/assets/img/paciente-antes-depois.jpg" alt="Antes e depois de paciente da clínica, perfil do rosto" width="532" height="564"><span class="ba-label"><span>Antes</span><span>Depois</span></span></div>
    <div class="strip-card strip-card--quote reveal">
      <span class="quote-mark">“</span>
      <p>Nossa missão é realçar a sua beleza natural e oferecer a melhor experiência de autocuidado que você merece.</p>
    </div>
    <a class="strip-card strip-card--image reveal" href="/procedimentos/">
      <img src="{placeholder('Procedimentos', 600, 600)}" alt="Procedimentos" width="600" height="600">
      <span class="strip-label">+30 procedimentos ↗</span>
    </a>
    <div class="strip-card strip-card--light reveal">
      <h3>Avaliação personalizada</h3>
      <p>Unidades Tatuapé e Moema</p>
      <a class="link-arrow" href="{wa_link()}" target="_blank" rel="noopener">Agendar ↗</a>
      <span class="strip-mark" aria-hidden="true">✳</span>
    </div>
  </div>
</section>

{marquee([p["title"] for p in PROCEDURES])}

<section class="section section--brand"><div class="container">
  <div class="stats">
    <div class="stat reveal"><strong data-count="53" data-prefix="+" data-suffix=" mil">+53 mil</strong><span>pacientes atendidos</span></div>
    <div class="stat reveal"><strong data-count="30" data-prefix="+">+30</strong><span>procedimentos</span></div>
    <div class="stat reveal"><strong data-count="2">2</strong><span>unidades em São Paulo</span></div>
    <div class="stat reveal"><strong data-count="5" data-decimals="1">5.0</strong><span>nota no Google</span></div>
  </div>
</div></section>

<section class="section" id="sobre"><div class="container split">
  <div class="img-wrap img-wrap--video reveal reveal--clip"><video data-parallax="0.08" data-autoplay src="/assets/video/sobre-clinica.mp4" poster="/assets/video/sobre-clinica.jpg" muted autoplay loop playsinline preload="metadata" aria-label="Conheça a Clínica Stringhetta" width="720" height="960"></video></div>
  <div class="reveal">
    <span class="eyebrow">A clínica</span>
    <h2>Conheça nossa clínica!</h2>
    <p>Somos uma clínica especializada em odontologia e estética, com duas unidades em São Paulo: Tatuapé e Moema. Do primeiro atendimento ao pós-procedimento, nossa missão é realçar a sua beleza natural e oferecer a melhor experiência de autocuidado.</p>
    <ul class="checklist">
      <li>Avaliação detalhada e plano de tratamento personalizado</li>
      <li>Equipamentos modernos e materiais certificados</li>
      <li>Atendimento humanizado e acompanhamento pós-procedimento</li>
      <li>Condições facilitadas de pagamento</li>
    </ul>
    <a class="btn btn--primary" href="{wa_link()}" target="_blank" rel="noopener">Quero conhecer</a>
  </div>
</div></section>

<section class="manifesto"><div class="container">
  <span class="manifesto-mark" data-spin aria-hidden="true">✳</span>
  <p class="scrub-text">Acreditamos que a beleza mais bonita é a que já existe em você. Nosso trabalho é revelar, com técnica, delicadeza e cuidado em cada detalhe.</p>
</div></section>

<section class="section section--alt"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Procedimentos</span><h2>Conheça alguns procedimentos</h2>
  <p>Tratamentos de estética facial e odontologia com resultados naturais.</p></div>
  <div class="grid grid-3">{featured}</div>
  <p style="text-align:center;margin-top:40px"><a class="btn btn--outline" href="/procedimentos/">Ver todos os procedimentos ↗</a></p>
</div></section>

<section class="section"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Como funciona</span><h2>Sua jornada na Stringhetta</h2></div>
  <div class="steps-line" aria-hidden="true"><span></span></div>
  <div class="grid grid-3 steps">
    <div class="step reveal"><h3>Avaliação</h3><p>Conversamos sobre seus objetivos e fazemos uma análise completa.</p></div>
    <div class="step reveal"><h3>Planejamento</h3><p>Montamos um plano sob medida, com prazos e valores claros.</p></div>
    <div class="step reveal"><h3>Tratamento e acompanhamento</h3><p>Realizamos o procedimento e acompanhamos sua evolução de perto.</p></div>
  </div>
</div></section>

{kids_section()}

{testimonials_section()}
{videos_section()}
{units_section()}
{marquee(["Realce a sua beleza natural", "Tatuapé", "Moema", "+53.000 autoestimas renovadas"], reverse=True)}
{cta_section("Fale com um especialista")}
"""
    return page(CONFIG["name"], "Clínica de odontologia e estética com unidades no Tatuapé e em Moema, São Paulo. Harmonização facial, preenchimento labial, Ulthera, lentes em resina e mais.", body, "home")


def procedures_index():
    sections = ""
    for key, label in CATEGORIES.items():
        cards = "".join(card(p) for p in PROCEDURES if p["category"] == key)
        if not cards:
            continue
        sections += f"""<div style="margin-bottom:56px"><h2 class="reveal" style="font-size:1.8rem">{label}</h2>
  <div class="grid grid-3">{cards}</div></div>"""
    body = f"""
<section class="page-hero"><span class="page-hero-mark" data-spin aria-hidden="true">✳</span><div class="container">
  <div class="breadcrumb"><a href="/">Início</a> / Procedimentos</div>
  <h1>Procedimentos</h1>
  <p>Conheça os tratamentos de estética facial e odontologia disponíveis na clínica.</p>
</div></section>
<section class="section"><div class="container">{sections}</div></section>
{cta_section("Não sabe qual tratamento é ideal para você?")}
"""
    return page("Procedimentos", "Todos os procedimentos de estética facial e odontologia da Clínica Stringhetta.", body, "procedimentos")


def procedure_page(p):
    benefits = "".join(f"<li>{escape(b)}</li>" for b in p["benefits"])
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in p["faq"])
    related = "".join(card(r) for r in [r for r in PROCEDURES if r["category"] == p["category"] and r is not p][:3])
    msg = p.get("wa", f"Olá! Gostaria de saber mais sobre {p['title']}.")
    body = f"""
<section class="page-hero"><span class="page-hero-mark" data-spin aria-hidden="true">✳</span><div class="container">
  <div class="breadcrumb"><a href="/">Início</a> / <a href="/procedimentos/">Procedimentos</a> / {escape(p['title'])}</div>
  <span class="eyebrow">{CATEGORIES[p['category']]}</span>
  <h1>{escape(p['title'])}</h1>
  <p>{escape(p['short'])}</p>
  <p style="margin-top:28px"><a class="btn btn--primary" href="{wa_link(msg)}" target="_blank" rel="noopener">Agendar avaliação</a></p>
</div></section>

<section class="section"><div class="container split">
  <div class="img-wrap reveal reveal--clip"><img data-parallax="0.12" src="{p.get('image') or placeholder(p['title'], 1000, 800)}" alt="{escape(p.get('image_alt', p['title']))}" width="1000" height="800"></div>
  <div class="reveal">
    <span class="eyebrow">Sobre o tratamento</span>
    <h2>O que é {escape(p['title'].lower())}?</h2>
    <p>{escape(p['intro'])}</p>
    <h3>Benefícios</h3>
    <ul class="checklist">{benefits}</ul>
    <a class="btn btn--whats" href="{wa_link(msg)}" target="_blank" rel="noopener">Tirar dúvidas no WhatsApp</a>
  </div>
</div></section>

<section class="section section--alt"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Dúvidas frequentes</span><h2>Perguntas sobre {escape(p['title'].lower())}</h2></div>
  <div class="faq reveal">{faq}
    <details><summary>Preciso de avaliação antes?</summary><p>Sim. Toda indicação é feita após uma avaliação presencial com nossos profissionais.</p></details>
  </div>
</div></section>

{f'''<section class="section"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Veja também</span><h2>Outros tratamentos</h2></div>
  <div class="grid grid-3">{related}</div>
</div></section>''' if related else ''}

{cta_section(f"Agende sua avaliação de {p['title'].lower()}")}
"""
    return page(p["title"], f"{p['title']} na Clínica Stringhetta (Tatuapé e Moema, São Paulo). {p['short']}", body, "procedimentos")


def contact():
    options = "".join(f"<option>{escape(p['title'])}</option>" for p in PROCEDURES)
    units = "".join(f"<option>{escape(u['name'])}</option>" for u in CONFIG["units"])
    body = f"""
<section class="page-hero"><span class="page-hero-mark" data-spin aria-hidden="true">✳</span><div class="container">
  <div class="breadcrumb"><a href="/">Início</a> / Contato</div>
  <h1>Fale com a gente</h1>
  <p>Agende sua avaliação ou tire suas dúvidas. Respondemos rapidinho!</p>
</div></section>

<section class="section"><div class="container split" style="align-items:start">
  <div class="reveal">
    <span class="eyebrow">Contato</span>
    <h2>Atendimento</h2>
    <ul class="checklist">
      <li>WhatsApp: <a href="{wa_link()}" target="_blank" rel="noopener">{CONFIG['phone']}</a></li>
      <li>{escape(CONFIG['hours'])}</li>
    </ul>
    {''.join(f"<p><strong>{escape(u['name'])}</strong><br>{escape(u['address'])}<br>{escape(u['city'])}</p>" for u in CONFIG['units'])}
  </div>
  <form class="form reveal" data-whatsapp="{CONFIG['whatsapp']}">
    <div><label for="nome">Nome</label><input id="nome" name="Nome" required autocomplete="name"></div>
    <div class="form-row">
      <div><label for="tel">Telefone</label><input id="tel" name="Telefone" type="tel" required autocomplete="tel"></div>
      <div><label for="email">E-mail</label><input id="email" name="E-mail" type="email" autocomplete="email"></div>
    </div>
    <div class="form-row">
      <div><label for="proc">Procedimento</label><select id="proc" name="Procedimento"><option value="">Selecione</option>{options}</select></div>
      <div><label for="unid">Unidade</label><select id="unid" name="Unidade">{units}</select></div>
    </div>
    <div><label for="msg">Mensagem</label><textarea id="msg" name="Mensagem" rows="4"></textarea></div>
    <button class="btn btn--primary" type="submit">Enviar pelo WhatsApp</button>
  </form>
</div></section>
{units_section()}
"""
    return page("Contato", "Entre em contato com a Clínica Stringhetta e agende sua avaliação no Tatuapé ou em Moema, São Paulo.", body, "contato")


def not_found():
    body = """<section class="page-hero" style="padding:140px 0"><div class="container">
  <h1>Página não encontrada</h1><p>O endereço acessado não existe ou foi movido.</p>
  <p style="margin-top:28px"><a class="btn btn--primary" href="/">Voltar ao início</a></p>
</div></section>"""
    return page("Página não encontrada", "Página não encontrada.", body)


def write(rel, content):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("✓", rel)


def main():
    (ROOT / "assets" / "img").mkdir(parents=True, exist_ok=True)
    write("index.html", home())
    write("procedimentos/index.html", procedures_index())
    for p in PROCEDURES:
        write(f"{p['slug']}/index.html", procedure_page(p))
    write("contato/index.html", contact())
    write("404.html", not_found())
    # Redirecionamentos de URLs antigas do WordPress
    for old, new in {"procedimentos-2-0": "/procedimentos/", "vsl-botox": "/procedimentos/",
                     "botox-captura": "/procedimentos/", "botox": "/procedimentos/",
                     "ultraformer": "/ulthera/", "implante-dentario": "/procedimentos/",
                     "protese-dentaria": "/procedimentos/", "ortodontia": "/procedimentos/",
                     "nutricionista": "/procedimentos/", "vsl-preenchimento": "/preenchimento-labial/",
                     "vsl-lente-resina": "/lentes-em-resina-estratificada/",
                     "gluteo-max": "/procedimentos/"}.items():
        write(f"{old}/index.html", f'<!doctype html><meta charset="utf-8"><title>Redirecionando…</title>'
              f'<link rel="canonical" href="{new}"><meta http-equiv="refresh" content="0; url={new}">'
              f'<a href="{new}">Clique aqui</a>')

    urls = ["", "procedimentos/", "contato/"] + [f"{p['slug']}/" for p in PROCEDURES]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>https://clinicastringhetta.com.br/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://clinicastringhetta.com.br/sitemap.xml\n")


if __name__ == "__main__":
    main()
