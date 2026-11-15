(function () {
const J = id => JSON.parse(document.getElementById(id).textContent);
const P = J("products-data"), CATS = J("cats-data"), SLOTS = J("slots-data"), SHOP = J("shop-data");
const TAG = { ru: J("tag-ru"), ky: J("tag-ky") }, PROMO = { ru: J("promo-ru"), ky: J("promo-ky") };
const CSRF = document.querySelector("[name=csrfmiddlewaretoken]").value;

const T = {
ru: {
 cart: "Корзина", sub: "Выберите букет, укажите дату и время — мы соберём и доставим по Ошу. Заказ уходит прямо в наш WhatsApp.",
 toCat: "Выбрать букет", howBtn: "Как заказать", p1: "Доставка от 60 минут", free: "Бесплатная доставка от {n} сом", p3: "Фото букета перед отправкой",
 promoS: "Закажите заранее — в праздник букеты разбирают за часы.", d: "дней", h: "часов", m: "минут",
 catT: "Каталог", all: "Все", add: "В корзину", added: "В корзине ✓", hit: "Хит", new: "Новинка", som: "сом",
 howT: "Как сделать заказ", s1t: "Выберите букет", s1p: "Все цены видны сразу — не нужно спрашивать в директ.",
 s2t: "Укажите дату и адрес", s2p: "Выберите время доставки, добавьте текст открытки.",
 s3t: "Подтвердите в WhatsApp", s3p: "Заказ открывается в WhatsApp — остаётся нажать «Отправить».",
 cartT: "Ваш заказ", empty: "Корзина пуста. Добавьте букет из каталога 🌷",
 delivery: "Доставка", pickup: "Самовывоз", date: "Дата", time: "Время", addr: "Адрес доставки", addrPh: "улица, дом, ориентир",
 rname: "Имя получателя", phone: "Ваш телефон", card: "Текст открытки (необязательно)", cardPh: "С любовью…",
 items: "Товары", fee: "Доставка", freeW: "бесплатно", total: "Итого", order: "Оформить в WhatsApp", sending: "Отправляем…",
 errEmpty: "Добавьте хотя бы один букет", errReq: "Заполните дату, время, телефон и адрес", errNet: "Не удалось отправить. Проверьте интернет и попробуйте ещё раз.",
 errItem: "Один из товаров больше недоступен. Обновите страницу.",
 okT: "Заказ №{n} принят!", okP: "Откройте WhatsApp и нажмите «Отправить» — мы подтвердим заказ.",
 openWa: "Открыть WhatsApp", close: "Закрыть", toast: "Добавлено в корзину", noItems: "Скоро здесь появятся букеты"
},
ky: {
 cart: "Себет", sub: "Гүл десте тандап, күнүн жана убактысын белгилеңиз — биз чогултуп, Ош боюнча жеткиребиз. Буйрутма түз биздин WhatsApp'ка келет.",
 toCat: "Гүл тандоо", howBtn: "Кантип буйрутма берем", p1: "60 мүнөттөн жеткирүү", free: "{n} сомдон акысыз жеткирүү", p3: "Жөнөтүүдөн мурун сүрөтү",
 promoS: "Алдын ала буйрутма бериңиз — майрамда гүлдөр бат түгөнөт.", d: "күн", h: "саат", m: "мүнөт",
 catT: "Каталог", all: "Баары", add: "Себетке", added: "Себетте ✓", hit: "Хит", new: "Жаңы", som: "сом",
 howT: "Кантип буйрутма берүү керек", s1t: "Гүл тандаңыз", s1p: "Бардык баалар дароо көрүнөт — директке жазып суроонун кереги жок.",
 s2t: "Күнүн жана даректи жазыңыз", s2p: "Жеткирүү убактысын тандап, открытканын текстин кошуңуз.",
 s3t: "WhatsApp'та ырастаңыз", s3p: "Буйрутма WhatsApp'та ачылат — «Жөнөтүү» баскычын басуу гана калат.",
 cartT: "Сиздин буйрутма", empty: "Себет бош. Каталогдон гүл кошуңуз 🌷",
 delivery: "Жеткирүү", pickup: "Өзүм алам", date: "Күнү", time: "Убактысы", addr: "Жеткирүү дареги", addrPh: "көчө, үй, белги",
 rname: "Алуучунун аты", phone: "Сиздин телефон", card: "Открытканын тексти (милдеттүү эмес)", cardPh: "Сүйүү менен…",
 items: "Товарлар", fee: "Жеткирүү", freeW: "акысыз", total: "Жалпы", order: "WhatsApp аркылуу буйрутма", sending: "Жөнөтүлүүдө…",
 errEmpty: "Жок дегенде бир гүл кошуңуз", errReq: "Күнүн, убактысын, телефонду жана даректи толтуруңуз", errNet: "Жөнөтүлгөн жок. Интернетти текшерип, кайра аракет кылыңыз.",
 errItem: "Товарлардын бири азыр жок. Баракты жаңыртыңыз.",
 okT: "№{n} буйрутма кабыл алынды!", okP: "WhatsApp'ты ачып, «Жөнөтүү» баскычын басыңыз — биз буйрутманы ырастайбыз.",
 openWa: "WhatsApp'ты ачуу", close: "Жабуу", toast: "Себетке кошулду", noItems: "Жакында бул жерде гүлдөр пайда болот"
}};

let lang = "ru", cat = "all", cart = {}, mode = "del", busy = false;
try { const s = JSON.parse(localStorage.getItem("gul_shop") || "{}"); if (s.lang) lang = s.lang; if (s.cart) cart = s.cart; } catch (e) {}
// Сайттан алынып салынган товарларды себеттен тазалоо
Object.keys(cart).forEach(id => { if (!P.find(p => p.id == id)) delete cart[id]; });
const save = () => { try { localStorage.setItem("gul_shop", JSON.stringify({ lang, cart })); } catch (e) {} };
const $ = id => document.getElementById(id);
const fmt = n => n.toLocaleString("ru-RU").replace(/ |,/g, " ");
const tr = k => T[lang][k];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const pic = p => p.img ? `<img src="${esc(p.img)}" alt="${esc(p[lang][0])}" loading="lazy">` : bouquet({ ...p.art, n: p.art.t === "peony" ? 7 : 11, wrap: "#efe6da" }, p.id * 7);

function renderTexts() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-t]").forEach(el => el.textContent = tr(el.dataset.t));
  $("tagline").textContent = TAG[lang];
  $("perkFree").textContent = tr("free").replace("{n}", fmt(SHOP.free));
  if ($("promoTitle")) $("promoTitle").textContent = PROMO[lang];
  document.querySelectorAll(".lang button").forEach(b => b.classList.toggle("on", b.dataset.l === lang));
}
function renderChips() {
  const list = [{ slug: "all", ru: T.ru.all, ky: T.ky.all }, ...CATS];
  $("chips").innerHTML = list.map(c => `<button class="chip ${c.slug === cat ? "on" : ""}" data-c="${esc(c.slug)}">${esc(c[lang])}</button>`).join("");
}
function renderGrid() {
  const list = P.filter(p => cat === "all" || p.cat === cat);
  if (!list.length) { $("grid").innerHTML = `<p style="color:var(--muted)">${tr("noItems")}</p>`; return; }
  $("grid").innerHTML = list.map(p => {
    const inC = cart[p.id];
    return `<article class="card"><div class="img">${p.badge ? `<span class="badge ${p.badge === "new" ? "new" : ""}">${tr(p.badge)}</span>` : ""}${pic(p)}</div>
    <div class="body"><h4>${esc(p[lang][0])}</h4><div class="desc">${esc(p[lang][1] || "")}</div>
    <div class="row"><span class="price">${fmt(p.price)} ${tr("som")}</span><button class="add ${inC ? "in" : ""}" data-add="${p.id}">${inC ? tr("added") : tr("add")}</button></div></div></article>`;
  }).join("");
}
const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
const subtotal = () => Object.entries(cart).reduce((s, [id, q]) => s + P.find(p => p.id == id).price * q, 0);
const fee = () => mode !== "del" ? 0 : (subtotal() >= SHOP.free ? 0 : SHOP.fee);

function renderCart() {
  $("cartN").textContent = count();
  const ids = Object.keys(cart);
  const iso = d => { const z = new Date(d.getTime() - d.getTimezoneOffset() * 6e4); return z.toISOString().slice(0, 10); };
  const today = iso(new Date());
  const v = id => $(id) ? $(id).value : "";
  const prev = { date: v("fDate") || today, time: v("fTime"), addr: v("fAddr"), name: v("fName"), phone: v("fPhone"), card: v("fCard") };
  if (!ids.length) $("drBody").innerHTML = `<div class="empty">${tr("empty")}</div>`;
  else {
    $("drBody").innerHTML = ids.map(id => {
      const p = P.find(x => x.id == id);
      return `<div class="line"><div class="th">${pic(p)}</div><div class="nm">${esc(p[lang][0])}<small>${fmt(p.price)} ${tr("som")}</small></div>
      <div class="qty"><button data-q="${id}" data-d="-1">−</button><span>${cart[id]}</span><button data-q="${id}" data-d="1">+</button></div></div>`;
    }).join("") + `<div class="form">
      <div class="seg"><button data-m="del" class="${mode === "del" ? "on" : ""}">${tr("delivery")}</button><button data-m="pick" class="${mode === "pick" ? "on" : ""}">${tr("pickup")}</button></div>
      <div class="two"><label>${tr("date")}<input type="date" id="fDate" min="${today}" value="${esc(prev.date)}"></label>
      <label>${tr("time")}<select id="fTime"><option value="">—</option>${SLOTS.map(s => `<option ${prev.time === s ? "selected" : ""}>${s}</option>`).join("")}</select></label></div>
      ${mode === "del" ? `<label>${tr("addr")}<input id="fAddr" maxlength="200" placeholder="${tr("addrPh")}" value="${esc(prev.addr)}"></label>
      <label>${tr("rname")}<input id="fName" maxlength="80" value="${esc(prev.name)}"></label>` : ""}
      <label>${tr("phone")}<input id="fPhone" type="tel" maxlength="30" placeholder="+996 ___ ___ ___" value="${esc(prev.phone)}"></label>
      <label>${tr("card")}<textarea id="fCard" maxlength="300" placeholder="${tr("cardPh")}">${esc(prev.card)}</textarea></label></div>`;
  }
  const st = subtotal(), f = fee();
  $("drFoot").innerHTML = `<div class="err" id="err"></div>
    <div class="sum"><span>${tr("items")}</span><span>${fmt(st)} ${tr("som")}</span></div>
    ${mode === "del" ? `<div class="sum"><span>${tr("fee")}</span><span>${f ? fmt(f) + " " + tr("som") : tr("freeW")}</span></div>` : ""}
    <div class="sum tot"><span>${tr("total")}</span><span>${fmt(st + f)} ${tr("som")}</span></div>
    <button class="order" id="doOrder" ${ids.length && !busy ? "" : "disabled"}>${busy ? tr("sending") : tr("order")}</button>`;
}
function renderCount() {
  if (!$("count") || !SHOP.promo) return;
  const tgt = new Date(SHOP.promo + "T00:00:00");
  let ms = Math.max(0, tgt - new Date());
  const d = Math.floor(ms / 864e5); ms -= d * 864e5; const h = Math.floor(ms / 36e5); ms -= h * 36e5; const m = Math.floor(ms / 6e4);
  if (tgt < new Date()) { $("count").closest(".promo").style.display = "none"; return; }
  $("count").innerHTML = `<div><b>${d}</b><small>${tr("d")}</small></div><div><b>${h}</b><small>${tr("h")}</small></div><div><b>${m}</b><small>${tr("m")}</small></div>`;
}
function renderAll() {
  renderTexts(); renderChips(); renderGrid(); renderCart(); renderCount();
  $("heroArt").innerHTML = bouquet({ t: "mix", c: ["#f2a7bb", "#c8243b", "#ffffff", "#e889a3"], n: 15, wrap: "#fbe9ee" }, 42);
}
setInterval(renderCount, 30000);

function toast(msg) { const t = $("toast"); t.textContent = msg; t.classList.add("on"); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove("on"), 1600); }
const openCart = () => { $("drawer").classList.add("on"); $("ov").classList.add("on"); };
const closeCart = () => { $("drawer").classList.remove("on"); $("ov").classList.remove("on"); };

document.addEventListener("click", e => {
  const g = s => e.target.closest(s);
  let el;
  if ((el = g(".lang button"))) { lang = el.dataset.l; save(); renderAll(); return; }
  if ((el = g("[data-c]"))) { cat = el.dataset.c; renderChips(); renderGrid(); return; }
  if ((el = g("[data-add]"))) { const id = el.dataset.add; cart[id] = Math.min(99, (cart[id] || 0) + 1); save(); renderGrid(); renderCart(); toast(tr("toast")); return; }
  if ((el = g("[data-q]"))) { const id = el.dataset.q; cart[id] += +el.dataset.d; if (cart[id] <= 0) delete cart[id]; if (cart[id] > 99) cart[id] = 99; save(); renderGrid(); renderCart(); return; }
  if ((el = g("[data-m]"))) { mode = el.dataset.m; renderCart(); return; }
  if (g("#openCart")) return openCart();
  if (g("#closeCart") || e.target === $("ov")) return closeCart();
  if (g("#toCat")) return $("catalog").scrollIntoView({ behavior: "smooth" });
  if (g("#toHow")) return $("how").scrollIntoView({ behavior: "smooth" });
  if (g("#doOrder")) return placeOrder();
  if (g("#mClose") || e.target === $("modal")) return $("modal").classList.remove("on");
});

async function placeOrder() {
  const err = $("err");
  if (!Object.keys(cart).length) { err.textContent = tr("errEmpty"); return; }
  const body = {
    lang, items: cart, delivery: mode === "del", date: $("fDate").value, time: $("fTime").value,
    phone: $("fPhone").value.trim(), address: mode === "del" ? $("fAddr").value.trim() : "",
    recipient: mode === "del" ? $("fName").value.trim() : "", card: $("fCard").value.trim(),
  };
  if (!body.date || !body.time || body.phone.replace(/\D/g, "").length < 9 || (body.delivery && !body.address)) { err.textContent = tr("errReq"); return; }
  busy = true; $("doOrder").disabled = true; $("doOrder").textContent = tr("sending");
  let res;
  try {
    const r = await fetch("/order/", { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": CSRF }, body: JSON.stringify(body) });
    res = await r.json();
  } catch (x) { res = { ok: false, error: "net" }; }
  busy = false;
  if (!res.ok) {
    $("doOrder").disabled = false; $("doOrder").textContent = tr("order");
    err.textContent = res.error === "item" ? tr("errItem") : res.error === "net" ? tr("errNet") : tr("errReq");
    return;
  }
  cart = {}; save(); renderGrid(); renderCart(); closeCart();
  $("modalBox").innerHTML = `<h3>${tr("okT").replace("{n}", res.order)}</h3><p style="color:var(--muted);font-size:14px">${tr("okP")}</p>
    <pre></pre><div class="acts"><a class="order" href="${esc(res.wa_url)}" target="_blank" rel="noopener">${tr("openWa")}</a>
    <button class="btn" id="mClose" style="color:var(--muted)">${tr("close")}</button></div>`;
  $("modalBox").querySelector("pre").textContent = res.message;
  $("modal").classList.add("on");
}
renderAll();
})();
