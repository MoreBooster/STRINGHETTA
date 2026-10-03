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
            "name": "Clínica Stringhetta – Tatuapé",
            "address": "R. Coelho Lisboa, 544 – Tatuapé",
            "city": "São Paulo – SP · CEP 03323-040",
        },
    ],
}

# category: "odonto" | "estetica" | "saude"
PROCEDURES = [
    {
        "slug": "botox", "title": "Botox", "category": "estetica", "icon": "✦",
        "image": "/assets/img/botox.jpg", "image_alt": "Paciente da clínica após aplicação de botox",
        "short": "Suaviza linhas de expressão da testa, glabela e olhos com aplicação precisa e resultado natural.",
        "intro": "A toxina botulínica relaxa temporariamente os músculos responsáveis pelas rugas dinâmicas, deixando o rosto com aparência descansada sem perder a expressividade.",
        "benefits": ["Aplicação rápida, em cerca de 30 minutos", "Retorno imediato à rotina",
                     "Prevenção de rugas profundas", "Resultado natural e personalizado"],
        "faq": [("Quanto tempo dura o efeito?", "Em média de 4 a 6 meses, variando conforme o metabolismo e a musculatura de cada paciente."),
                ("Quando vejo o resultado?", "Os primeiros efeitos aparecem entre 3 e 5 dias, com resultado completo em cerca de 15 dias."),
                ("Dói?", "O desconforto é mínimo. Utilizamos agulhas ultrafinas e, se necessário, anestésico tópico.")],
    },
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
        "slug": "gluteo-max", "title": "Harmonização de glúteos", "category": "estetica", "icon": "◠",
        "short": "Volume, contorno e firmeza para os glúteos sem cirurgia.",
        "intro": "A harmonização de glúteos combina bioestimuladores e técnicas de preenchimento para melhorar contorno, projeção e firmeza, de forma segura e sem cortes.",
        "benefits": ["Mais projeção e contorno", "Melhora da flacidez e da celulite",
                     "Procedimento sem cortes", "Resultado progressivo"],
        "faq": [("Precisa de repouso?", "Recomendamos evitar exercícios intensos por alguns dias. As atividades leves podem ser retomadas logo.")],
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
        "slug": "ultraformer", "title": "Ultraformer", "category": "estetica", "icon": "≋",
        "short": "Ultrassom microfocado para lifting sem cortes, firmeza e contorno facial e corporal.",
        "intro": "O Ultraformer utiliza ultrassom microfocado para estimular colágeno nas camadas profundas da pele, promovendo efeito lifting e melhora do contorno sem cirurgia.",
        "benefits": ["Efeito lifting sem cortes", "Estímulo natural de colágeno",
                     "Melhora da flacidez de rosto e corpo", "Sem tempo de recuperação"],
        "faq": [("Em quanto tempo vejo o resultado?", "Há melhora imediata, e o resultado evolui ao longo de 60 a 90 dias."),
                ("Quantas sessões?", "Normalmente uma sessão, com manutenção anual.")],
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
        "slug": "implante-dentario", "title": "Implante dentário", "category": "odonto", "icon": "⚲",
        "short": "Reposição de dentes perdidos com segurança, estética e função mastigatória.",
        "intro": "O implante dentário substitui a raiz do dente perdido por um pino de titânio biocompatível, sobre o qual é instalada uma coroa com aparência natural.",
        "benefits": ["Planejamento digital com tomografia", "Devolve a mastigação e o sorriso",
                     "Preserva o osso da face", "Solução duradoura"],
        "faq": [("O implante dói?", "O procedimento é feito com anestesia local e o pós-operatório costuma ser tranquilo."),
                ("Quanto tempo leva?", "Depende do caso. Em algumas situações é possível a carga imediata.")],
    },
    {
        "slug": "protese-dentaria", "title": "Prótese dentária", "category": "odonto", "icon": "⌒",
        "short": "Próteses fixas, móveis e sobre implantes, confortáveis e com estética natural.",
        "intro": "Confeccionamos próteses sob medida para recuperar a função e a estética do sorriso, com materiais de alta resistência e acabamento natural.",
        "benefits": ["Próteses fixas, removíveis e protocolos", "Materiais de alta resistência",
                     "Ajuste confortável", "Cor e formato personalizados"],
        "faq": [("Qual tipo de prótese é o ideal?", "Isso é definido na avaliação, considerando sua saúde bucal e expectativas.")],
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
    {
        "slug": "ortodontia", "title": "Ortodontia e alinhadores", "category": "odonto", "icon": "⌇",
        "short": "Aparelhos convencionais, estéticos e alinhadores transparentes.",
        "intro": "Corrigimos o alinhamento dos dentes e a mordida com aparelhos fixos, estéticos ou alinhadores transparentes praticamente invisíveis.",
        "benefits": ["Alinhadores transparentes", "Aparelhos estéticos",
                     "Planejamento digital do tratamento", "Para adolescentes e adultos"],
        "faq": [("Alinhador funciona para todos os casos?", "Atende grande parte dos casos. A indicação é feita na avaliação.")],
    },
    {
        "slug": "nutricionista", "title": "Nutricionista", "category": "saude", "icon": "❦",
        "short": "Acompanhamento nutricional para saúde, emagrecimento e performance.",
        "intro": "Nosso acompanhamento nutricional cria um plano alimentar realista e personalizado, integrado aos seus objetivos estéticos e de saúde.",
        "benefits": ["Plano alimentar individual", "Avaliação de composição corporal",
                     "Acompanhamento contínuo", "Integração com tratamentos estéticos"],
        "faq": [("Preciso fazer exames antes?", "Se necessário, a nutricionista solicitará exames na primeira consulta.")],
    },
]

FEATURED = ["botox", "preenchimento-labial", "gluteo-max", "lentes-em-resina-estratificada", "ulthera", "lavieen"]

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
    <li><a href="/#localizacao">Localização</a></li>
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
    <div><h4>Odonto e saúde</h4><ul>{odonto}</ul></div>
    <div><h4>Endereço</h4><ul>{units}</ul></div>
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
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">
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
    u = CONFIG["units"][0]
    q = quote(f"{u['address']}, {u['city']}")
    return f"""<section class="section" id="localizacao"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Onde estamos</span><h2>Venha nos visitar no Tatuapé</h2>
  <p>Um espaço pensado para o seu conforto, na Zona Leste de São Paulo.</p></div>
  <div class="location reveal">
    <iframe loading="lazy" title="Mapa – {escape(u['name'])}" src="https://maps.google.com/maps?q={q}&output=embed"></iframe>
    <div class="location-body">
      <span class="location-mark" aria-hidden="true">✳</span>
      <h3>{escape(u['name'])}</h3>
      <p>{escape(u['address'])}<br>{escape(u['city'])}</p>
      <p>{escape(CONFIG['hours'])}</p>
      <p><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {CONFIG['phone']}</a></p>
      <div class="location-actions">
        <a class="btn btn--primary" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">Como chegar ↗</a>
        <a class="btn btn--outline" href="https://waze.com/ul?q={q}&navigate=yes" target="_blank" rel="noopener">Waze</a>
      </div>
    </div>
  </div>
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


def home():
    featured = "".join(card(p) for p in PROCEDURES if p['slug'] in FEATURED)
    body = f"""
<section class="hero">
  <video class="hero-video" data-autoplay src="/assets/video/hero.mp4" poster="/assets/video/hero.jpg" muted autoplay loop playsinline preload="auto" aria-hidden="true"></video>
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="hero-rays" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div class="hero-copy" data-hero-copy>
      <span class="hero-kicker">+10.000 autoestimas renovadas</span>
      <h1>Realce a sua <br>beleza natural</h1>
      <p class="lead">Odontologia e estética com planejamento individual <br>e resultados naturais, no coração do Tatuapé.</p>
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
      <p>R. Coelho Lisboa, 544 · Tatuapé</p>
      <a class="link-arrow" href="{wa_link()}" target="_blank" rel="noopener">Agendar ↗</a>
      <span class="strip-mark" aria-hidden="true">✳</span>
    </div>
  </div>
</section>

{marquee([p["title"] for p in PROCEDURES])}

<section class="section section--brand"><div class="container">
  <div class="stats">
    <div class="stat reveal"><strong data-count="10" data-prefix="+" data-suffix=" mil">+10 mil</strong><span>pacientes atendidos</span></div>
    <div class="stat reveal"><strong data-count="30" data-prefix="+">+30</strong><span>procedimentos</span></div>
    <div class="stat reveal"><strong data-count="100" data-suffix="%">100%</strong><span>atendimento personalizado</span></div>
    <div class="stat reveal"><strong data-count="5" data-decimals="1">5.0</strong><span>nota no Google</span></div>
  </div>
</div></section>

<section class="section" id="sobre"><div class="container split">
  <div class="img-wrap img-wrap--video reveal reveal--clip"><video data-parallax="0.08" data-autoplay src="/assets/video/sobre-clinica.mp4" poster="/assets/video/sobre-clinica.jpg" muted autoplay loop playsinline preload="metadata" aria-label="Conheça a Clínica Stringhetta" width="720" height="960"></video></div>
  <div class="reveal">
    <span class="eyebrow">A clínica</span>
    <h2>Conheça nossa clínica!</h2>
    <p>Somos uma clínica especializada em odontologia e estética, localizada no Tatuapé, em São Paulo. Do primeiro atendimento ao pós-procedimento, nossa missão é realçar a sua beleza natural e oferecer a melhor experiência de autocuidado.</p>
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
  <p>Mais de 30 procedimentos em odontologia, estética e saúde.</p></div>
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

{testimonials_section()}
{videos_section()}
{units_section()}
{marquee(["Realce a sua beleza natural", "Tatuapé · São Paulo", "+10.000 autoestimas renovadas"], reverse=True)}
{cta_section("Fale com um especialista")}
"""
    return page(CONFIG["name"], "Clínica de odontologia e estética no Tatuapé, São Paulo. Botox, harmonização, implantes, clareamento e mais.", body, "home")


def procedures_index():
    sections = ""
    for key, label in CATEGORIES.items():
        cards = "".join(card(p) for p in PROCEDURES if p["category"] == key)
        sections += f"""<div style="margin-bottom:56px"><h2 class="reveal" style="font-size:1.8rem">{label}</h2>
  <div class="grid grid-3">{cards}</div></div>"""
    body = f"""
<section class="page-hero"><span class="page-hero-mark" data-spin aria-hidden="true">✳</span><div class="container">
  <div class="breadcrumb"><a href="/">Início</a> / Procedimentos</div>
  <h1>Procedimentos</h1>
  <p>Conheça os tratamentos de odontologia, estética e saúde disponíveis na clínica.</p>
</div></section>
<section class="section"><div class="container">{sections}</div></section>
{cta_section("Não sabe qual tratamento é ideal para você?")}
"""
    return page("Procedimentos", "Todos os procedimentos de odontologia, estética facial e saúde da Clínica Stringhetta.", body, "procedimentos")


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
    return page(p["title"], f"{p['title']} na Clínica Stringhetta (Tatuapé, São Paulo). {p['short']}", body, "procedimentos")


def contact():
    options = "".join(f"<option>{escape(p['title'])}</option>" for p in PROCEDURES)
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
    <div><label for="proc">Procedimento</label><select id="proc" name="Procedimento"><option value="">Selecione</option>{options}</select></div>
    <div><label for="msg">Mensagem</label><textarea id="msg" name="Mensagem" rows="4"></textarea></div>
    <button class="btn btn--primary" type="submit">Enviar pelo WhatsApp</button>
  </form>
</div></section>
{units_section()}
"""
    return page("Contato", "Entre em contato com a Clínica Stringhetta e agende sua avaliação no Tatuapé, São Paulo.", body, "contato")


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
    for old, new in {"procedimentos-2-0": "/procedimentos/", "vsl-botox": "/botox/",
                     "botox-captura": "/botox/", "vsl-preenchimento": "/preenchimento-labial/",
                     "vsl-lente-resina": "/lentes-em-resina-estratificada/"}.items():
        write(f"{old}/index.html", f'<!doctype html><meta charset="utf-8"><title>Redirecionando…</title>'
              f'<link rel="canonical" href="{new}"><meta http-equiv="refresh" content="0; url={new}">'
              f'<a href="{new}">Clique aqui</a>')

    urls = ["", "procedimentos/", "contato/"] + [f"{p['slug']}/" for p in PROCEDURES]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>https://clinicastringhetta.com.br/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://clinicastringhetta.com.br/sitemap.xml\n")


if __name__ == "__main__":
    main()
