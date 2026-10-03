const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

// Menu mobile
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
}

// Título surgindo palavra por palavra
document.querySelectorAll(".hero h1, .page-hero h1").forEach((h1) => {
  let i = 0;
  const wrap = (node) => {
    [...node.childNodes].forEach((child) => {
      if (child.nodeType === Node.TEXT_NODE) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(part); return; }
          const outer = document.createElement("span");
          outer.className = "word";
          const inner = document.createElement("span");
          inner.textContent = part;
          inner.style.transitionDelay = `${0.15 + i++ * 0.08}s`;
          outer.append(inner);
          frag.append(outer);
        });
        child.replaceWith(frag);
      } else if (child.nodeType === Node.ELEMENT_NODE && child.tagName !== "BR") {
        wrap(child);
      }
    });
  };
  wrap(h1);
  h1.classList.add("split-ready");
  requestAnimationFrame(() => requestAnimationFrame(() => h1.classList.add("in")));
});

// Entradas em sequência: cada grupo de .reveal ganha um atraso escalonado
document.querySelectorAll(".grid, .stats, .hero-strip, .footer-grid").forEach((group) => {
  group.querySelectorAll(":scope > .reveal, :scope > * > .reveal").forEach((el, idx) => {
    el.style.transitionDelay = `${idx * 0.09}s`;
  });
});
document.querySelectorAll(".split").forEach((split) => {
  const [a, b] = split.children;
  if (a && !a.classList.contains("reveal--clip")) a.classList.add("reveal--left");
  if (b) b.classList.add("reveal--right");
});
document.querySelectorAll(".hero-strip > .reveal").forEach((el, idx) => {
  el.style.transitionDelay = `${0.6 + idx * 0.12}s`;
});

// Contadores
const runCounter = (el) => {
  const target = parseFloat(el.dataset.count);
  const decimals = parseInt(el.dataset.decimals || "0", 10);
  const prefix = el.dataset.prefix || "";
  const suffix = el.dataset.suffix || "";
  const duration = 1600;
  const start = performance.now();
  const tick = (now) => {
    const t = clamp((now - start) / duration, 0, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = prefix + (target * eased).toFixed(decimals).replace(".", decimals ? "." : "") + suffix;
    if (t < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
};

// Revelar ao entrar na tela
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    const el = e.target;
    el.classList.add("visible");
    el.querySelectorAll("[data-count]").forEach(runCounter);
    // depois da entrada, volta às transições rápidas de hover
    setTimeout(() => { el.style.transitionDelay = ""; el.classList.add("settled"); }, 1800);
    io.unobserve(e.target);
  });
}, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// Texto que acende conforme a rolagem
const scrubs = [...document.querySelectorAll(".scrub-text")].map((el) => {
  const words = el.textContent.trim().split(/\s+/);
  el.innerHTML = words.map((w) => `<span>${w}</span>`).join(" ");
  return { el, spans: [...el.children] };
});

// Cards com inclinação 3D
if (finePointer && !reduceMotion) {
  document.querySelectorAll(".card, .strip-card, .testimonial").forEach((card) => {
    card.addEventListener("mousemove", (ev) => {
      const r = card.getBoundingClientRect();
      const x = (ev.clientX - r.left) / r.width - 0.5;
      const y = (ev.clientY - r.top) / r.height - 0.5;
      card.style.setProperty("--rx", `${(-y * 6).toFixed(2)}deg`);
      card.style.setProperty("--ry", `${(x * 8).toFixed(2)}deg`);
      card.style.setProperty("--mx", `${(x + 0.5) * 100}%`);
      card.style.setProperty("--my", `${(y + 0.5) * 100}%`);
      card.classList.add("tilting");
    });
    card.addEventListener("mouseleave", () => {
      card.classList.remove("tilting");
      card.style.removeProperty("--rx");
      card.style.removeProperty("--ry");
    });
  });
}

// Efeitos ligados à rolagem (um único loop por frame)
const header = document.querySelector(".header");
const progress = document.querySelector(".scroll-progress");
const hero = document.querySelector(".hero");
const heroCopy = document.querySelector("[data-hero-copy]");
const heroRays = document.querySelector(".hero-rays");
const parallaxImgs = [...document.querySelectorAll("[data-parallax]")];
const spinners = [...document.querySelectorAll("[data-spin], .strip-mark")];
const marquees = [...document.querySelectorAll(".marquee-track")].map((el) => ({
  el, reverse: el.parentElement.classList.contains("marquee--reverse"), x: 0,
}));
const steps = document.querySelector(".steps-line span");

let lastY = window.scrollY;
let velocity = 0;
let ticking = false;

function onFrame() {
  ticking = false;
  const y = window.scrollY;
  const vh = window.innerHeight;
  const docH = document.documentElement.scrollHeight - vh;
  velocity = y - lastY;
  lastY = y;

  if (progress) progress.style.transform = `scaleX(${docH > 0 ? y / docH : 0})`;
  if (header) header.classList.toggle("is-scrolled", y > (hero ? vh * 0.7 : 10));

  if (reduceMotion) return;

  if (hero && y < hero.offsetHeight) {
    const p = y / hero.offsetHeight;
    hero.style.backgroundPosition = `center, center ${50 + p * 30}%, center`;
    if (heroCopy) {
      heroCopy.style.transform = `translateY(${y * 0.35}px)`;
      heroCopy.style.opacity = String(clamp(1 - p * 2.2, 0, 1));
    }
    if (heroRays) heroRays.style.transform = `skewX(-8deg) translateX(${p * -120}px)`;
  }

  parallaxImgs.forEach((img) => {
    const r = img.parentElement.getBoundingClientRect();
    if (r.bottom < 0 || r.top > vh) return;
    const offset = (r.top + r.height / 2 - vh / 2) * parseFloat(img.dataset.parallax);
    img.style.transform = `translateY(${offset.toFixed(1)}px) scale(1.18)`;
  });

  spinners.forEach((el) => { el.style.transform = `rotate(${y * 0.15}deg)`; });

  scrubs.forEach(({ el, spans }) => {
    const r = el.getBoundingClientRect();
    const p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1);
    const lit = Math.round(p * spans.length);
    spans.forEach((s, i) => s.classList.toggle("lit", i < lit));
  });

  if (steps) {
    const r = steps.parentElement.getBoundingClientRect();
    steps.style.transform = `scaleX(${clamp((vh * 0.8 - r.top) / (vh * 0.5), 0, 1)})`;
  }
}

function requestFrame() {
  if (!ticking) { ticking = true; requestAnimationFrame(onFrame); }
}
window.addEventListener("scroll", requestFrame, { passive: true });
window.addEventListener("resize", requestFrame);
onFrame();

// Faixas deslizantes: andam sempre e aceleram com a rolagem
if (!reduceMotion && marquees.length) {
  const loop = () => {
    const boost = clamp(Math.abs(velocity), 0, 40) * 0.25;
    velocity *= 0.9;
    marquees.forEach((m) => {
      const third = m.el.scrollWidth / 3;
      m.x += (m.reverse ? 1 : -1) * (0.5 + boost);
      if (m.x <= -third) m.x += third;
      if (m.x > 0) m.x -= third;
      m.el.style.transform = `translate3d(${m.x}px,0,0)`;
    });
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
}

// Formulários: enviam a mensagem pelo WhatsApp
document.querySelectorAll("form[data-whatsapp]").forEach((form) => {
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    const data = new FormData(form);
    const lines = ["Olá! Gostaria de agendar uma avaliação."];
    for (const [key, value] of data.entries()) {
      if (value) lines.push(`${key}: ${value}`);
    }
    const url = `https://wa.me/${form.dataset.whatsapp}?text=${encodeURIComponent(lines.join("\n"))}`;
    window.open(url, "_blank", "noopener");
  });
});

// Ano no rodapé
document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
