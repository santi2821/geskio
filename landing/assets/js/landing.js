"use strict";
(() => {
  const initialProducts = [
    {
      id: "leche",
      name: "Leche entera",
      detail: "1 litro",
      initials: "LE",
      price: 1600,
      stock: 12,
    },
    {
      id: "yerba",
      name: "Yerba mate",
      detail: "500 gramos",
      initials: "YM",
      price: 3200,
      stock: 8,
    },
    {
      id: "galletitas",
      name: "Galletitas",
      detail: "Paquete 170 g",
      initials: "GA",
      price: 1200,
      stock: 5,
    },
  ];
  const currency = new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    maximumFractionDigits: 0,
  });
  const format = (value) => currency.format(value);
  let products, cart, sales, total, debt;
  const byId = (id) => document.getElementById(id);
  const message = (text) => {
    byId("demo-message").textContent = text;
  };
  function render() {
    byId("product-list").replaceChildren(
      ...products.map((product) => {
        const row = document.createElement("div");
        row.className = "product";
        const swatch = document.createElement("span");
        swatch.className = "product-swatch";
        swatch.textContent = product.initials;
        swatch.setAttribute("aria-hidden", "true");
        const name = document.createElement("span");
        name.className = "product-name";
        name.textContent = product.name;
        const price = document.createElement("small");
        price.textContent = format(product.price);
        name.append(price);
        const minus = document.createElement("button");
        minus.type = "button";
        minus.className = "quantity-button";
        minus.textContent = "−";
        minus.setAttribute("aria-label", `Quitar ${product.name}`);
        minus.disabled = !cart[product.id];
        minus.dataset.action = "remove";
        minus.dataset.product = product.id;
        const count = document.createElement("span");
        count.className = "quantity-number";
        count.textContent = cart[product.id] || 0;
        const plus = document.createElement("button");
        plus.type = "button";
        plus.className = "quantity-button";
        plus.textContent = "+";
        plus.setAttribute("aria-label", `Agregar ${product.name}`);
        plus.disabled = (cart[product.id] || 0) >= product.stock;
        plus.dataset.action = "add";
        plus.dataset.product = product.id;
        row.append(swatch, name, minus, count, plus);
        return row;
      }),
    );
    const quantity = Object.values(cart).reduce((sum, count) => sum + count, 0);
    const amount = products.reduce(
      (sum, product) => sum + product.price * (cart[product.id] || 0),
      0,
    );
    byId("cart-count").textContent =
      `${quantity} ${quantity === 1 ? "producto" : "productos"}`;
    byId("cart-total").textContent = format(amount);
    byId("sales-total").textContent = format(total);
    byId("sales-count").textContent =
      `${sales} ${sales === 1 ? "venta registrada" : "ventas registradas"}`;
    byId("sell-button").disabled = quantity === 0;
    byId("sell-button").textContent = quantity
      ? `Registrar venta · ${format(amount)}`
      : "Elegí un producto para empezar";
    byId("stock-list").replaceChildren(
      ...products.map((product) => {
        const row = document.createElement("div");
        row.className = "stock-row";
        const name = document.createElement("span");
        name.textContent = product.name;
        const detail = document.createElement("small");
        detail.textContent = product.detail;
        name.append(detail);
        const stock = document.createElement("strong");
        stock.textContent =
          product.stock === 0 ? "Sin stock" : `${product.stock} unidades`;
        if (product.stock <= 3) stock.className = "low";
        row.append(name, stock);
        return row;
      }),
    );
    byId("workflow-sales").textContent = format(total);
    byId("workflow-stock").textContent =
      `${products.reduce((sum, item) => sum + item.stock, 0)} unidades`;
    byId("workflow-debt").textContent = format(debt);
    byId("workflow-count").textContent = sales
      ? `${sales} ${sales === 1 ? "venta registrada" : "ventas registradas"} en esta demo.`
      : "Todavía no registraste ventas.";
    byId("debt-amount").textContent = format(debt);
    byId("pay-debt").disabled = debt === 0;
    byId("pay-debt").textContent =
      debt === 0
        ? "Cuenta saldada"
        : `Registrar cobro de ${format(Math.min(debt, 1500))}`;
  }
  function reset() {
    products = initialProducts.map((product) => ({ ...product }));
    cart = {};
    sales = 0;
    total = 0;
    debt = 4500;
    render();
  }
  byId("product-list").addEventListener("click", (event) => {
    const button = event.target.closest("button[data-product]");
    if (!button) return;
    const product = products.find((item) => item.id === button.dataset.product);
    const next =
      (cart[product.id] || 0) + (button.dataset.action === "add" ? 1 : -1);
    if (next < 0 || next > product.stock) return;
    cart[product.id] = next;
    const action = button.dataset.action;
    render();
    const replacement = byId("product-list").querySelector(
      `[data-product="${product.id}"][data-action="${action}"]`,
    );
    const alternate = byId("product-list").querySelector(
      `[data-product="${product.id}"][data-action="${action === "add" ? "remove" : "add"}"]`,
    );
    (replacement && !replacement.disabled ? replacement : alternate)?.focus({
      preventScroll: true,
    });
    message(
      next
        ? `${product.name}: ${next} en tu venta.`
        : `${product.name}: quitado de la venta.`,
    );
  });
  byId("sell-button").addEventListener("click", () => {
    const amount = products.reduce(
      (sum, product) => sum + product.price * (cart[product.id] || 0),
      0,
    );
    if (!amount) return;
    for (const product of products) product.stock -= cart[product.id] || 0;
    total += amount;
    sales += 1;
    cart = {};
    render();
    message(
      `Venta de ${format(amount)} registrada. El stock ya se actualizó. Todo es de ejemplo.`,
    );
  });
  byId("pay-debt").addEventListener("click", () => {
    if (!debt) return;
    const paid = Math.min(1500, debt);
    debt -= paid;
    render();
    message(
      `Cobro de ${format(paid)} registrado. ${debt ? `Quedan ${format(debt)} pendientes.` : "La cuenta quedó saldada."}`,
    );
  });
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function selectTab(tab, focus = false) {
    for (const item of tabs) {
      const active = item === tab;
      item.setAttribute("aria-selected", String(active));
      item.tabIndex = active ? 0 : -1;
      byId(item.getAttribute("aria-controls")).hidden = !active;
    }
    if (focus) tab.focus();
    message(
      {
        caja: "Probá sumar productos y registrar una venta.",
        stock: "Las ventas de la demo descuentan unidades del stock.",
        fiados: "Probá registrar un cobro sobre este saldo ficticio.",
      }[tab.dataset.panel],
    );
  }
  for (const tab of tabs) {
    tab.addEventListener("click", () => selectTab(tab));
    tab.addEventListener("keydown", (event) => {
      const index = tabs.indexOf(tab);
      const keys = {
        ArrowRight: (index + 1) % tabs.length,
        ArrowDown: (index + 1) % tabs.length,
        ArrowLeft: (index + tabs.length - 1) % tabs.length,
        ArrowUp: (index + tabs.length - 1) % tabs.length,
        Home: 0,
        End: tabs.length - 1,
      };
      if (Object.hasOwn(keys, event.key)) {
        event.preventDefault();
        selectTab(tabs[keys[event.key]], true);
      }
    });
  }
  byId("reset-demo").addEventListener("click", () => {
    reset();
    selectTab(tabs[0]);
    message("Demo reiniciada. Todos los datos vuelven al inicio.");
  });
  for (const button of document.querySelectorAll("[data-open-panel]")) {
    button.addEventListener("click", () => {
      const tab = tabs.find(
        (item) => item.dataset.panel === button.dataset.openPanel,
      );
      selectTab(tab, true);
      byId("demo").scrollIntoView({
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "instant"
          : "smooth",
        block: "start",
      });
    });
  }
  const menu = document.querySelector(".nav-menu-button");
  const navigation = byId("navigation");
  const closeMenu = () => {
    navigation.classList.remove("is-open");
    menu.setAttribute("aria-expanded", "false");
    menu.setAttribute("aria-label", "Abrir menú");
  };
  menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(open));
    navigation.classList.toggle("is-open", open);
    menu.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menu.getAttribute("aria-expanded") === "true"
    ) {
      closeMenu();
      menu.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".nav-shell")) closeMenu();
  });
  const desktopQuery = matchMedia("(min-width: 761px)");
  desktopQuery.addEventListener("change", closeMenu);
  const navLinks = [...navigation.querySelectorAll("a")];
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          for (const link of navLinks) {
            if (link.hash === `#${entry.target.id}`)
              link.setAttribute("aria-current", "location");
            else link.removeAttribute("aria-current");
          }
        }
      },
      { rootMargin: "-15% 0px -55% 0px", threshold: 0 },
    );
    for (const link of navLinks) {
      const section = document.querySelector(link.hash);
      if (section) observer.observe(section);
    }
    const heroObserver = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting))
          for (const link of navLinks) link.removeAttribute("aria-current");
      },
      { threshold: 0.3 },
    );
    heroObserver.observe(document.querySelector(".hero"));
  }
  byId("year").textContent = new Date().getFullYear();
  reset();
})();
