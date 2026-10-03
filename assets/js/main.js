// Menu mobile
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
}

// Animação de entrada das seções
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) {
      e.target.classList.add("visible");
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

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
