document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("[data-text-input]");
  const counter = document.querySelector("[data-char-count]");
  if (input && counter) {
    const update = () => counter.textContent = `${input.value.length.toLocaleString("fr-FR")} / 5 000 caractères`;
    input.addEventListener("input", update);
    update();
  }
  document.querySelectorAll("[data-confirm-delete]").forEach(form => form.addEventListener("submit", event => {
    if (!window.confirm("Supprimer définitivement ce texte ? Cette action est irréversible.")) event.preventDefault();
  }));
});
