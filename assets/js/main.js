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
const heroVideo = document.querySelector(".hero-video");
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
    if (heroVideo) heroVideo.style.transform = `translateY(${y * 0.35}px) scale(1.06)`;
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

// Carrossel de vídeos: todos tocam sem som; o som só liga no vídeo que o usuário tocar
document.querySelectorAll(".reels-section").forEach((section) => {
  const track = section.querySelector(".reels-track");
  const reels = [...section.querySelectorAll(".reel")];
  const dots = [...section.querySelectorAll(".reels-dots button")];
  const arrows = [...section.querySelectorAll(".reels-arrow")];
  let active = null;

  const setMuted = (reel, muted) => {
    const video = reel.querySelector("video");
    video.muted = muted;
    reel.classList.toggle("is-playing", !muted);
    reel.querySelector(".reel-toggle").setAttribute("aria-pressed", String(!muted));
    if (!muted) active = reel;
    else if (active === reel) active = null;
  };

  reels.forEach((reel) => {
    const video = reel.querySelector("video");
    const bar = reel.querySelector(".reel-progress span");
    video.muted = true;
    video.addEventListener("timeupdate", () => {
      if (video.duration) bar.style.transform = `scaleX(${video.currentTime / video.duration})`;
    });
    reel.querySelector(".reel-toggle").addEventListener("click", () => {
      if (active === reel) { setMuted(reel, true); return; }
      if (active) setMuted(active, true);
      setMuted(reel, false);
      video.currentTime = 0;
      video.play().catch(() => {});
    });
  });

  // Só toca o que está visível (economiza bateria e dados); som desliga ao sair da tela
  const visibility = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const video = e.target.querySelector("video");
      if (e.isIntersecting) video.play().catch(() => {});
      else {
        video.pause();
        if (active === e.target) setMuted(e.target, true);
      }
    });
  }, { threshold: 0.35 });
  reels.forEach((r) => visibility.observe(r));

  // Navegação: setas, pontos e estado atual
  const step = () => reels[0].offsetWidth + parseFloat(getComputedStyle(track).columnGap || 20);
  const update = () => {
    const idx = Math.round(track.scrollLeft / step());
    dots.forEach((d, i) => d.classList.toggle("active", i === Math.min(idx, dots.length - 1)));
    const max = track.scrollWidth - track.clientWidth - 2;
    arrows.forEach((a) => { a.disabled = a.dataset.dir === "-1" ? track.scrollLeft <= 2 : track.scrollLeft >= max; });
  };
  arrows.forEach((a) => a.addEventListener("click", () => track.scrollBy({ left: step() * Number(a.dataset.dir) })));
  dots.forEach((d, i) => d.addEventListener("click", () => track.scrollTo({ left: step() * i })));
  track.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
  window.addEventListener("resize", update);
  track.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowRight") track.scrollBy({ left: step() });
    if (ev.key === "ArrowLeft") track.scrollBy({ left: -step() });
  });
  update();

  // Arrastar com o mouse no desktop
  let startX = 0, startScroll = 0, moved = false, down = false;
  track.addEventListener("pointerdown", (ev) => {
    if (ev.pointerType !== "mouse") return;
    down = true; moved = false; startX = ev.clientX; startScroll = track.scrollLeft;
  });
  window.addEventListener("pointermove", (ev) => {
    if (!down) return;
    const dx = ev.clientX - startX;
    if (Math.abs(dx) > 5) { moved = true; track.classList.add("dragging"); }
    if (moved) track.scrollLeft = startScroll - dx;
  });
  window.addEventListener("pointerup", () => {
    if (!down) return;
    down = false;
    if (moved) {
      track.classList.remove("dragging");
      track.scrollTo({ left: Math.round(track.scrollLeft / step()) * step() });
    }
  });
});

// Vídeos decorativos: sempre mudos, tocam sozinhos quando visíveis
const autoVideos = document.querySelectorAll("video[data-autoplay]");
if (autoVideos.length) {
  const vio = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const v = e.target;
      v.muted = true;
      if (e.isIntersecting) v.play().catch(() => {});
      else v.pause();
    });
  }, { threshold: 0.2 });
  autoVideos.forEach((v) => { v.muted = true; vio.observe(v); });
}
