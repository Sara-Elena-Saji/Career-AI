document.addEventListener("DOMContentLoaded", function () {
  // ── Theme toggle (dark/light mode) ───────────────────────
  const themeToggle = document.getElementById("themeToggle");
  const root = document.documentElement;

  function applyToggleIcon() {
    if (!themeToggle) return;
    const isLight = root.getAttribute("data-theme") === "light";
    themeToggle.textContent = isLight ? "☀️" : "🌙";
    themeToggle.setAttribute(
      "aria-label",
      isLight ? "Switch to dark mode" : "Switch to light mode"
    );
  }

  applyToggleIcon();

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const isLight = root.getAttribute("data-theme") === "light";
      if (isLight) {
        root.removeAttribute("data-theme");
        localStorage.setItem("theme", "dark");
      } else {
        root.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
      }
      applyToggleIcon();
    });
  }

  // ── Form submit handler ──────────────────────────────────
  const form = document.getElementById("careerForm");
  const btn  = document.getElementById("submitBtn");

  if (form && btn) {
    form.addEventListener("submit", function (e) {
      const name      = document.getElementById("name").value.trim();
      const skills    = document.getElementById("skills").value.trim();
      const interests = document.getElementById("interests").value.trim();

      if (!name || !skills || !interests) {
        e.preventDefault();
        alert("Please fill in all three fields before continuing.");
        return;
      }

      btn.classList.add("loading");
      btn.querySelector(".btn-text").textContent = "Analysing your profile…";
    });
  }

  // ── Animate score bars on results page ──────────────────
  const bars = document.querySelectorAll(".score-bar-fill");
  if (bars.length) {
    // Start at 0, then animate to target after a brief delay
    bars.forEach(bar => { bar.style.width = "0%"; });
    requestAnimationFrame(() => {
      setTimeout(() => {
        bars.forEach(bar => {
          // Read the --score CSS custom property set inline on the element
          const score = getComputedStyle(bar).getPropertyValue("--score").trim();
          if (score) bar.style.width = score;
        });
      }, 200);
    });
  }

  // ── Subtle input focus glow ──────────────────────────────
  document.querySelectorAll(".field input").forEach(input => {
    input.addEventListener("focus", () => {
      input.closest(".field").classList.add("focused");
    });
    input.addEventListener("blur", () => {
      input.closest(".field").classList.remove("focused");
    });
  });

  // ── Career card tabs (Overview / Roadmap / AI Coach / Skill Gap) ──
  document.querySelectorAll(".suggestion-card").forEach(card => {
    const tabButtons = card.querySelectorAll(".career-tab-btn");
    const tabPanels  = card.querySelectorAll(".career-tab-panel");

    tabButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const target = btn.getAttribute("data-tab");

        tabButtons.forEach(b => {
          const isActive = b === btn;
          b.classList.toggle("is-active", isActive);
          b.setAttribute("aria-selected", isActive ? "true" : "false");
        });

        tabPanels.forEach(panel => {
          panel.classList.toggle("is-active", panel.getAttribute("data-panel") === target);
        });
      });
    });
  });
});
