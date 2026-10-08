"use strict";

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#primary-nav");

function closeMenu() {
  menuButton.setAttribute("aria-expanded", "false");
  navigation.classList.remove("is-open");
}

menuButton.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  navigation.classList.toggle("is-open", open);
});
navigation.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (
    event.key === "Escape" &&
    menuButton.getAttribute("aria-expanded") === "true"
  ) {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".site-header")) closeMenu();
});
const mobileQuery = window.matchMedia("(max-width: 640px)");
mobileQuery.addEventListener("change", closeMenu);

function setUpFilter(
  buttonSelector,
  itemSelector,
  buttonKey,
  itemKey,
  statusSelector,
  unit,
) {
  const buttons = [...document.querySelectorAll(buttonSelector)];
  const items = [...document.querySelectorAll(itemSelector)];
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const selection = button.dataset[buttonKey];
      buttons.forEach((candidate) => {
        const active = candidate === button;
        candidate.classList.toggle("is-active", active);
        candidate.setAttribute("aria-pressed", String(active));
      });
      let visibleCount = 0;
      items.forEach((item) => {
        item.hidden =
          selection !== "all" && item.dataset[itemKey] !== selection;
        if (!item.hidden) visibleCount += 1;
      });
      document.querySelector(statusSelector).textContent =
        `${visibleCount}${unit}を表示しています`;
    });
  });
}

setUpFilter(
  "[data-star-filter]",
  "[data-star-category]",
  "starFilter",
  "starCategory",
  "#star-status",
  "人",
);
setUpFilter(
  "[data-music-filter]",
  "[data-music-mood]",
  "musicFilter",
  "musicMood",
  "#music-status",
  "曲",
);

if ("IntersectionObserver" in window) {
  const links = [...navigation.querySelectorAll("a")];
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => {
          if (link.hash === `#${entry.target.id}`)
            link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      });
    },
    { rootMargin: "-12% 0px -65% 0px", threshold: 0 },
  );
  links.forEach((link) => {
    const section = document.querySelector(link.hash);
    if (section) observer.observe(section);
  });
  observer.observe(document.querySelector(".hero"));
}
