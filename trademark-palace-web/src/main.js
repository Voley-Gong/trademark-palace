import {
  loadProgress,
  markMoldy,
  clearMoldy,
  bumpDrill,
  setPalaceId,
  getPalaceId,
  getLastPalaceId,
} from "./storage.js";
import {
  buildFloorScript,
  playScript,
  stopListen,
  pauseListen,
  resumeListen,
  setListenRate,
  getListenRate,
  isPaused,
  hasSession,
  supportsSpeech,
} from "./listen.js";
import { registerPwa } from "./pwa.js";

const app = document.getElementById("app");
const asset = (path) => `${import.meta.env.BASE_URL}${path.replace(/^\//, "")}`;

const PALACES = [
  {
    id: "trademark",
    file: "data/trademark-palace.json",
    label: "商标馆",
    motto: "问来源混淆",
    blurb: "注册边界、近似混淆、救济阶梯与程序期限",
  },
  {
    id: "patent",
    file: "data/patent-palace.json",
    label: "专利馆",
    motto: "问特征落入",
    blurb: "权要视图、全面覆盖与等同、无效衔接与赔偿",
  },
];

/** @type {any} */
let data = null;
let route = { name: "hall" };
let progress = loadProgress();

/** Keep corridor shell mounted to avoid full-page flash */
let corridorMounted = false;
let corridorFloorId = null;

function palaceMeta(id = getPalaceId()) {
  return PALACES.find((p) => p.id === id) || PALACES[0];
}

async function loadPalace(id, nextRoute = { name: "home" }) {
  const meta = palaceMeta(id);
  stopListen();
  corridorMounted = false;
  corridorFloorId = null;
  setPalaceId(meta.id);
  progress = loadProgress();
  app.innerHTML = `<main class="app-shell"><p class="empty">正在进入${meta.label}…</p></main>`;
  const res = await fetch(asset(meta.file));
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  data = await res.json();
  document.title = `${data.title || meta.label} · 知产诉讼城`;
  route = nextRoute;
  render();
}

function findFloor(floorId) {
  return data.floors.find((f) => f.id === floorId);
}

function findRoom(roomId) {
  for (const floor of data.floors) {
    const room = floor.rooms.find((r) => r.id === roomId);
    if (room) return { floor, room };
  }
  return null;
}

function allRooms() {
  return data.floors.flatMap((f) =>
    f.rooms.map((r) => ({ ...r, floorId: f.id, floorName: f.name, level: f.level }))
  );
}

function formatFloorChip(f) {
  if (f.level === 0) return `B0 补丁 ${f.rooms.length} 房`;
  return `${f.level}F ${f.name.replace(/层$/, "")} ${f.rooms.length} 房`;
}

function formatFloorMenuTitle(f) {
  if (f.level === 0) return `地下室 · ${f.name.replace(/层$/, "")}`;
  const ord = ["", "一", "二", "三", "四"][f.level] || String(f.level);
  return `${ord}楼 · ${f.name.replace(/层$/, "")}`;
}

function formatFloorTab(f) {
  if (f.level === 0) return `B0<br/>补丁`;
  return `${f.level}F<br/>${f.name.replace(/层$/, "").slice(0, 4)}`;
}

function getArticle(ref) {
  return data.articles?.[ref] || null;
}

/** Collect primary + related + linked-room articles (deduped, primary first). */
function collectArticleBundle(room) {
  const primary = [...(room.articleRefs || [])];
  const related = [...(room.relatedArticleRefs || [])];
  for (const linkId of room.links || []) {
    const hit = findRoom(linkId);
    if (!hit) continue;
    for (const ref of hit.room.articleRefs || []) {
      if (!primary.includes(ref) && !related.includes(ref)) related.push(ref);
    }
  }
  return { primary, related };
}

function renderExplainPanel(art, ref) {
  if (!art.plain && !(art.examples && art.examples.length) && !art.apply) {
    return `<p class="muted explain-missing">暂无通俗解释</p>`;
  }
  const examples = (art.examples || [])
    .map((e) => `<li>${escapeHtml(e)}</li>`)
    .join("");
  return `
    <button type="button" class="btn-explain" data-explain-toggle aria-expanded="false">
      <span data-explain-open>展开通俗解释与举例</span>
      <span data-explain-close hidden>收起解释</span>
    </button>
    <div class="explain-panel" hidden data-explain-panel>
      <p class="explain-plain">${escapeHtml(art.plain || "")}</p>
      ${
        examples
          ? `<label class="eyebrow explain-label">举例</label><ul class="list explain-examples">${examples}</ul>`
          : ""
      }
      ${
        art.apply
          ? `<label class="eyebrow explain-label">怎么用</label><p class="explain-apply">${escapeHtml(art.apply)}</p>`
          : ""
      }
    </div>
  `;
}

function renderArticleBlocks(primaryRefs, relatedRefs) {
  const blocks = [];
  const pushBlock = (ref, kind) => {
    const art = getArticle(ref);
    if (!art) return;
    const tag = kind === "primary" ? "本法条" : "关联";
    const tagClass = kind === "primary" ? "law-tag" : "law-tag related";
    blocks.push(`
      <article class="law-block ${kind}" data-art-ref="${ref}">
        <header><span class="${tagClass}">${tag}</span><strong>${art.label}</strong></header>
        <pre class="law-text">${escapeHtml(art.text)}</pre>
        ${renderExplainPanel(art, ref)}
      </article>`);
  };
  for (const ref of primaryRefs) pushBlock(ref, "primary");
  for (const ref of relatedRefs) {
    if (primaryRefs.includes(ref)) continue;
    pushBlock(ref, "related");
  }
  if (!blocks.length) return "";
  return `<div class="law-stack">${blocks.join("")}</div>`;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function navigate(next, opts = {}) {
  const prevName = route.name;
  route = next;
  progress = loadProgress();

  if (route.name === "corridor" && prevName === "corridor" && corridorMounted) {
    const floorChanged = route.floorId !== corridorFloorId;
    if (floorChanged) {
      updateCorridorFloorChrome();
      rebuildDoorGrid();
      corridorFloorId = route.floorId;
    } else {
      syncDoorActiveState();
    }
    updateRoomPanel();
    if (!opts.skipScroll) {
      /* keep scroll position when switching doors */
    }
    return;
  }

  corridorMounted = false;
  corridorFloorId = null;
  render();
  if (!opts.keepScroll) {
    window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
  }
}

function dock(active) {
  return `
    <nav class="nav-dock" aria-label="主导航">
      <button type="button" class="${active === "home" ? "active" : ""}" data-nav="home">
        <span class="ico">馆</span>馆门
      </button>
      <button type="button" class="${active === "corridor" ? "active" : ""}" data-nav="corridor">
        <span class="ico">廊</span>走廊
      </button>
      <button type="button" class="${active === "listen" ? "active" : ""}" data-nav="listen">
        <span class="ico">听</span>听过
      </button>
      <button type="button" class="${active === "drill" ? "active" : ""}" data-nav="drill">
        <span class="ico">问</span>五问
      </button>
    </nav>
  `;
}

function bindDock() {
  app.querySelectorAll("[data-nav]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-nav");
      if (id === "home") {
        stopListen();
        navigate({ name: "home" });
      }
      if (id === "corridor") {
        stopListen();
        navigate({
          name: "corridor",
          floorId: route.floorId || data.floors.find((f) => f.level === 1)?.id || data.floors[0].id,
        });
      }
      if (id === "listen") {
        navigate({ name: "listen", floorId: route.floorId || data.floors[0].id });
      }
      if (id === "drill") {
        stopListen();
        navigate({ name: "drill" });
      }
    });
  });
}

function renderHall() {
  const last = getLastPalaceId();
  app.innerHTML = `
    <main class="app-shell hall-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">IP LITIGATION CITY</p>
          <h1>知产诉讼城</h1>
        </div>
      </header>
      <p class="hall-motto">商标问来源混淆，专利问特征落入。</p>
      <p class="muted">选一栋馆进入记忆宫殿。走廊、听过、五问共用同一套引擎。</p>
      <div class="menu-grid hall-grid">
        ${PALACES.map(
          (p) => `
          <button type="button" class="menu-btn hall-card ${last === p.id ? "hall-recent" : ""}" data-palace="${p.id}">
            <span class="kicker">${last === p.id ? "上次进入" : "PALACE"}</span>
            <strong>${p.label}</strong>
            <span class="hall-tag">${p.motto}</span>
            <span class="muted">${p.blurb}</span>
          </button>`
        ).join("")}
      </div>
    </main>
  `;
  app.querySelectorAll("[data-palace]").forEach((btn) => {
    btn.onclick = async () => {
      try {
        await loadPalace(btn.getAttribute("data-palace"), { name: "home" });
      } catch (err) {
        app.innerHTML = `
          <main class="app-shell">
            <h1>未能加载馆数据</h1>
            <p class="muted">${String(err)}</p>
            <button type="button" class="btn btn-primary" data-back-hall style="margin-top:14px">返回选馆</button>
          </main>`;
        app.querySelector("[data-back-hall]").onclick = () => navigate({ name: "hall" });
      }
    };
  });
}

function renderHome() {
  const moldCount = Object.keys(progress.moldyRooms || {}).length;
  const floorsSorted = data.floors.slice().sort((a, b) => a.level - b.level);
  const meta = palaceMeta();
  app.innerHTML = `
    <main class="app-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">${data.building} · ${data.lawEdition}</p>
          <h1>${data.title}</h1>
        </div>
        <button type="button" class="btn btn-ghost btn-switch" data-hall>换馆</button>
      </header>
      <p class="muted hall-inline-motto">${meta.motto}</p>
      <p class="muted">${data.description}</p>
      <div class="chip-row">
        ${floorsSorted.map((f) => `<span class="chip">${formatFloorChip(f)}</span>`).join("")}
        <span class="chip">发霉门 ${moldCount}</span>
      </div>
      <div class="search-bar card">
        <input
          id="home-search"
          type="search"
          placeholder="搜索：条号 / 房间 / 关键词 / 案例"
          value="${escapeHtml(route.q || "")}"
          autocomplete="off"
        />
        <button type="button" class="btn btn-primary" data-go-search>搜索</button>
      </div>
      <div class="menu-grid">
        ${floorsSorted
          .map(
            (f) => `
          <button type="button" class="menu-btn" data-go-floor="${f.id}">
            <span class="kicker">COMMUTE · ${f.commuteMinutes || 10} MIN</span>
            <strong>${formatFloorMenuTitle(f)}</strong>
            <span class="muted">${f.mission}</span>
          </button>`
          )
          .join("")}
        <button type="button" class="menu-btn" data-go="moldy">
          <span class="kicker">REVIEW · MOLDY</span>
          <strong>发霉复习</strong>
          <span class="muted">${moldCount ? `优先过 ${moldCount} 扇发霉门` : "暂无发霉门，答错五问会出现"}</span>
        </button>
        <button type="button" class="menu-btn" data-go="search">
          <span class="kicker">SEARCH</span>
          <strong>全馆搜索</strong>
          <span class="muted">条号、门牌、口述、人话、案例</span>
        </button>
        <button type="button" class="menu-btn" data-go="listen">
          <span class="kicker">COMMUTE · EARS OPEN</span>
          <strong>通勤听过</strong>
          <span class="muted">语音导览整层走廊 · 可锁屏听（部分浏览器）</span>
        </button>
        <button type="button" class="menu-btn" data-go="peg">
          <span class="kicker">FLASH · EYES CLOSED</span>
          <strong>数字桩闪过</strong>
          <span class="muted">含程序期限桩 · 通勤闭眼点名</span>
        </button>
        <button type="button" class="menu-btn" data-go="drill">
          <span class="kicker">CASE DRILL</span>
          <strong>五问办案</strong>
          <span class="muted">侵权向 + 程序向假想案</span>
        </button>
      </div>
    </main>
    ${dock("home")}
  `;
  bindDock();
  app.querySelectorAll("[data-go-floor]").forEach((btn) => {
    btn.onclick = () =>
      navigate({ name: "corridor", floorId: btn.getAttribute("data-go-floor") });
  });
  const goSearch = () => {
    const q = app.querySelector("#home-search")?.value?.trim() || "";
    navigate({ name: "search", q });
  };
  app.querySelector("[data-go-search]")?.addEventListener("click", goSearch);
  app.querySelector("#home-search")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") goSearch();
  });
  app.querySelector('[data-go="moldy"]')?.addEventListener("click", () => navigate({ name: "moldy" }));
  app.querySelector('[data-go="search"]')?.addEventListener("click", () =>
    navigate({ name: "search", q: "" })
  );
  app.querySelector('[data-go="listen"]')?.addEventListener("click", () =>
    navigate({
      name: "listen",
      floorId: data.floors.find((f) => f.level === 1)?.id || data.floors[0].id,
    })
  );
  app.querySelector('[data-go="peg"]')?.addEventListener("click", () =>
    navigate({ name: "peg", idx: 0, revealed: false })
  );
  app.querySelector('[data-go="drill"]')?.addEventListener("click", () => navigate({ name: "drill" }));
  app.querySelector("[data-hall]")?.addEventListener("click", () => {
    stopListen();
    data = null;
    corridorMounted = false;
    corridorFloorId = null;
    navigate({ name: "hall" });
  });
}

function doorButtonHtml(r, selectedId) {
  const mold = progress.moldyRooms?.[r.id];
  return `
    <button type="button" class="door ${mold ? "mold" : ""} ${r.id === selectedId ? "active" : ""}" data-room="${r.id}" title="${r.title} · ${r.articleLabel}">
      <span class="num">${r.id}</span>
      <span class="title">${r.title}</span>
      <span class="art">${r.article}</span>
    </button>`;
}

function roomPanelHtml(selected, revealed) {
  const { primary, related } = collectArticleBundle(selected);
  return `
    <p class="eyebrow">${selected.articleLabel}${selected.peg != null ? ` · 桩 ${selected.peg}` : ""}</p>
    <h2>${selected.title}</h2>
    <p class="muted room-space">${selected.space}</p>
    <div class="sense-row">
      ${(selected.senses || []).map((s) => `<span class="sense">${s}</span>`).join("")}
    </div>
    <div class="meta-grid">
      <div class="meta-item">
        <label>场景钩</label>
        <div class="muted">${selected.sceneHook}</div>
      </div>
      <div class="meta-item">
        <label>案例锚</label>
        <div class="muted">${(selected.caseAnchor || []).join(" · ")}</div>
      </div>
    </div>
    ${
      selected.classicCases?.length
        ? `<div class="classic-box">
            <label class="eyebrow">经典案例</label>
            ${selected.classicCases
              .map(
                (c) => `
              <div class="classic-item">
                <strong>${escapeHtml(c.name)}</strong>
                <div class="muted">${escapeHtml(c.hook || "")}</div>
                <div class="classic-take">${escapeHtml(c.takeaway || "")}</div>
              </div>`
              )
              .join("")}
          </div>`
        : ""
    }
    <div class="reveal-box ${revealed ? "" : "hidden-oral"}" data-reveal-box>
      <label class="eyebrow">30 秒口述</label>
      <p class="oral">${selected.oral30s}</p>
      ${
        revealed
          ? `
        <label class="eyebrow block-label">要件</label>
        <ul class="list">${(selected.elements || []).map((e) => `<li>${e}</li>`).join("")}</ul>
        ${
          selected.exceptions?.length
            ? `<label class="eyebrow block-label">例外/注意</label>
               <ul class="list">${selected.exceptions.map((e) => `<li>${e}</li>`).join("")}</ul>`
            : ""
        }
        ${
          selected.stations
            ? `<label class="eyebrow block-label">阶梯站位</label>
               <ul class="list">${selected.stations.map((s) => `<li>${s.label}${s.peg != null ? `（桩 ${s.peg}）` : ""}</li>`).join("")}</ul>`
            : ""
        }
        <label class="eyebrow block-label">法条原文</label>
        ${renderArticleBlocks(primary, related)}
        <label class="eyebrow block-label">自测</label>
        <p class="muted drill-q">${selected.drillPrompt || ""}</p>
      `
          : `<p class="muted hint-hide">先自己说一遍，再点「揭晓」对照法条原文。</p>`
      }
    </div>
    <div class="btn-row" data-room-actions>
      ${
        revealed
          ? `<button type="button" class="btn btn-ghost" data-hide>先藏口述再练</button>`
          : `<button type="button" class="btn btn-primary" data-reveal>揭晓口述与法条</button>`
      }
      <button type="button" class="btn btn-warn" data-mold>这间记错了（发霉）</button>
      ${
        progress.moldyRooms?.[selected.id]
          ? `<button type="button" class="btn btn-ghost" data-clean>清除发霉</button>`
          : ""
      }
    </div>
    ${
      selected.links?.length
        ? `<div class="chip-row link-row">
            ${selected.links
              .map((id) => {
                const hit = findRoom(id);
                if (!hit) return "";
                return `<button type="button" class="chip" data-link="${id}">→ ${id} ${hit.room.title}</button>`;
              })
              .join("")}
          </div>`
        : ""
    }
  `;
}

function bindRoomPanelActions(floor, selected) {
  const panel = app.querySelector("#room-panel");
  if (!panel) return;
  panel.querySelector("[data-reveal]")?.addEventListener("click", () => {
    navigate({ ...route, revealed: true }, { keepScroll: true });
  });
  panel.querySelector("[data-hide]")?.addEventListener("click", () => {
    navigate({ ...route, revealed: false }, { keepScroll: true });
  });
  panel.querySelector("[data-mold]")?.addEventListener("click", () => {
    progress = markMoldy(selected.id);
    syncDoorActiveState();
    updateRoomPanel();
  });
  panel.querySelector("[data-clean]")?.addEventListener("click", () => {
    progress = clearMoldy(selected.id);
    syncDoorActiveState();
    updateRoomPanel();
  });
  panel.querySelectorAll("[data-link]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-link");
      const hit = findRoom(id);
      if (!hit) return;
      navigate({
        name: "corridor",
        floorId: hit.floor.id,
        roomId: hit.room.id,
        revealed: false,
      });
    });
  });
}

function updateRoomPanel() {
  const floor = findFloor(route.floorId) || data.floors[0];
  const selectedId = route.roomId || floor.rooms[0].id;
  const selected = floor.rooms.find((r) => r.id === selectedId) || floor.rooms[0];
  const revealed = !!route.revealed;
  const panel = app.querySelector("#room-panel");
  if (!panel) return;
  panel.innerHTML = roomPanelHtml(selected, revealed);
  bindRoomPanelActions(floor, selected);
}

function syncDoorActiveState() {
  const floor = findFloor(route.floorId) || data.floors[0];
  const selectedId = route.roomId || floor.rooms[0].id;
  app.querySelectorAll(".door-grid .door").forEach((btn) => {
    const id = btn.getAttribute("data-room");
    const mold = progress.moldyRooms?.[id];
    btn.classList.toggle("active", id === selectedId);
    btn.classList.toggle("mold", !!mold);
  });
}

function rebuildDoorGrid() {
  const floor = findFloor(route.floorId) || data.floors[0];
  const selectedId = route.roomId || floor.rooms[0].id;
  const grid = app.querySelector("#door-grid");
  if (!grid) return;
  grid.innerHTML = floor.rooms.map((r) => doorButtonHtml(r, selectedId)).join("");
}

function updateCorridorFloorChrome() {
  const floor = findFloor(route.floorId) || data.floors[0];
  const eyebrow = app.querySelector("[data-floor-eyebrow]");
  const title = app.querySelector("[data-floor-title]");
  const mission = app.querySelector("[data-floor-mission]");
  if (eyebrow) eyebrow.textContent = floor.level === 0 ? `B0 · ${floor.mapAscii}` : `${floor.level}F · ${floor.mapAscii}`;
  if (title) title.textContent = floor.name;
  if (mission) mission.textContent = floor.mission;
  app.querySelectorAll("[data-floor]").forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-floor") === floor.id);
  });
}

function renderCorridor() {
  const floor = findFloor(route.floorId) || data.floors[0];
  route.floorId = floor.id;
  if (!route.roomId) route.roomId = floor.rooms[0].id;
  const selectedId = route.roomId;
  const selected = floor.rooms.find((r) => r.id === selectedId) || floor.rooms[0];
  const revealed = !!route.revealed;

  app.innerHTML = `
    <main class="app-shell corridor-shell">
      <button type="button" class="back-link" data-back>← 馆门</button>
      <header class="topbar">
        <div>
          <p class="eyebrow" data-floor-eyebrow>${floor.level === 0 ? "B0" : `${floor.level}F`} · ${floor.mapAscii}</p>
          <h1 data-floor-title>${floor.name}</h1>
        </div>
      </header>
      <div class="floor-tabs">
        ${data.floors
          .slice()
          .sort((a, b) => a.level - b.level)
          .map(
            (f) => `
          <button type="button" class="${f.id === floor.id ? "active" : ""}" data-floor="${f.id}">
            ${formatFloorTab(f)}
          </button>`
          )
          .join("")}
      </div>
      <p class="mission" data-floor-mission>${floor.mission}</p>
      <div class="door-grid" id="door-grid">
        ${floor.rooms.map((r) => doorButtonHtml(r, selected.id)).join("")}
      </div>
      <section class="card room-panel" id="room-panel">
        ${roomPanelHtml(selected, revealed)}
      </section>
    </main>
    ${dock("corridor")}
  `;

  corridorMounted = true;
  corridorFloorId = floor.id;
  bindDock();

  app.querySelector("[data-back]").onclick = () => navigate({ name: "home" });

  app.querySelectorAll("[data-floor]").forEach((btn) => {
    btn.onclick = () => {
      const fid = btn.getAttribute("data-floor");
      const f = findFloor(fid);
      navigate({
        name: "corridor",
        floorId: fid,
        roomId: f.rooms[0].id,
        revealed: false,
      });
    };
  });

  // Event delegation: door clicks only patch panel
  app.querySelector("#door-grid").addEventListener("click", (e) => {
    const btn = e.target.closest("[data-room]");
    if (!btn) return;
    const roomId = btn.getAttribute("data-room");
    if (roomId === route.roomId && !route.revealed) return;
    navigate(
      {
        name: "corridor",
        floorId: route.floorId,
        roomId,
        revealed: false,
      },
      { keepScroll: true }
    );
  });

  bindRoomPanelActions(floor, selected);
}

function renderPeg() {
  const pegs = data.numberPegs;
  const idx = Math.min(route.idx || 0, pegs.length - 1);
  const peg = pegs[idx];
  const revealed = !!route.revealed;
  const pct = ((idx + (revealed ? 1 : 0.5)) / pegs.length) * 100;

  app.innerHTML = `
    <main class="app-shell">
      <button type="button" class="back-link" data-back>← 馆门</button>
      <header class="topbar">
        <div>
          <p class="eyebrow">NUMBER PEG FLASH</p>
          <h1>数字桩闪过</h1>
        </div>
        <span class="chip">${idx + 1}/${pegs.length}</span>
      </header>
      <div class="progress-bar"><span style="width:${pct}%"></span></div>
      <div class="peg-stage">
        <div class="peg-num">${peg.n}</div>
        <div class="peg-image">${peg.image}</div>
        ${
          revealed
            ? `<div class="answer-card card">
                <label class="eyebrow">挂载要点</label>
                <ul class="list">${peg.bindings.map((b) => `<li>${b}</li>`).join("")}</ul>
                <label class="eyebrow block-label">法条原文</label>
                ${renderArticleBlocks(peg.articleRefs || [], [])}
              </div>`
            : `<p class="muted" style="margin-top:18px">闭眼回忆：这个数字挂着什么？</p>`
        }
      </div>
      <div class="btn-row" style="justify-content:center;margin-top:16px">
        ${
          revealed
            ? `<button type="button" class="btn btn-primary" data-next>${idx < pegs.length - 1 ? "下一桩" : "再来一轮"}</button>
               <button type="button" class="btn btn-ghost" data-hide>再藏一次</button>`
            : `<button type="button" class="btn btn-primary" data-show>揭晓挂载与法条</button>`
        }
      </div>
    </main>
    ${dock("peg")}
  `;
  bindDock();
  app.querySelector("[data-back]").onclick = () => navigate({ name: "home" });
  const show = app.querySelector("[data-show]");
  if (show) show.onclick = () => navigate({ name: "peg", idx, revealed: true });
  const hide = app.querySelector("[data-hide]");
  if (hide) hide.onclick = () => navigate({ name: "peg", idx, revealed: false });
  const next = app.querySelector("[data-next]");
  if (next)
    next.onclick = () => {
      if (idx >= pegs.length - 1) {
        progress = bumpDrill();
        navigate({ name: "peg", idx: 0, revealed: false });
      } else {
        navigate({ name: "peg", idx: idx + 1, revealed: false });
      }
    };
}

function getCaseDrills() {
  return data.caseDrills || [];
}

function renderDrill() {
  const cases = getCaseDrills();
  if (!route.caseId) {
    app.innerHTML = `
      <main class="app-shell">
        <button type="button" class="back-link" data-back>← 馆门</button>
        <header class="topbar">
          <div>
            <p class="eyebrow">CASE DRILLS · ${palaceMeta().label}</p>
            <h1>五问办案</h1>
          </div>
        </header>
        <p class="muted">先选题：程序向练期限与路径；侵权/权属/救济向练主楼调取。</p>
        <div class="menu-grid" style="margin-top:14px">
          ${
            cases.length
              ? cases
                  .map(
                    (c) => `
            <button type="button" class="menu-btn" data-case="${c.id}">
              <span class="kicker">${c.trackLabel || c.track}</span>
              <strong>${c.title}</strong>
              <span class="muted">${c.prompt.slice(0, 72)}${c.prompt.length > 72 ? "…" : ""}</span>
            </button>`
                  )
                  .join("")
              : `<p class="muted">本馆暂无五问假想案。</p>`
          }
        </div>
      </main>
      ${dock("drill")}
    `;
    bindDock();
    app.querySelector("[data-back]").onclick = () => navigate({ name: "home" });
    app.querySelectorAll("[data-case]").forEach((btn) => {
      btn.onclick = () =>
        navigate({
          name: "drill",
          caseId: btn.getAttribute("data-case"),
          step: 0,
          picked: null,
        });
    });
    return;
  }

  const drill = cases.find((c) => c.id === route.caseId) || cases[0];
  const questions = drill.questions || [];
  const step = route.step || 0;
  const finished = step >= questions.length;

  if (finished) {
    const pathArts = [];
    for (const id of drill.suggestedPath || []) {
      const hit = findRoom(id);
      if (!hit) continue;
      for (const ref of hit.room.articleRefs || []) {
        if (!pathArts.includes(ref)) pathArts.push(ref);
      }
    }
    app.innerHTML = `
      <main class="app-shell">
        <header class="topbar">
          <div>
            <p class="eyebrow">CASE COMPLETE</p>
            <h1>${drill.title}</h1>
          </div>
        </header>
        <div class="card">
          <p class="muted">建议对照路径：</p>
          <div class="chip-row">
            ${(drill.suggestedPath || []).map((id) => `<span class="chip">${id}</span>`).join("")}
          </div>
          <p class="muted" style="margin-top:12px">${drill.closingTip || ""}</p>
          <label class="eyebrow block-label">路径相关法条</label>
          ${renderArticleBlocks(pathArts, [])}
          <div class="btn-row">
            <button type="button" class="btn btn-primary" data-again>再练本案</button>
            <button type="button" class="btn btn-ghost" data-pick>换一题</button>
            <button type="button" class="btn btn-ghost" data-home>回馆门</button>
          </div>
        </div>
      </main>
      ${dock("drill")}
    `;
    bindDock();
    app.querySelector("[data-again]").onclick = () =>
      navigate({ name: "drill", caseId: drill.id, step: 0, picked: null });
    app.querySelector("[data-pick]").onclick = () => navigate({ name: "drill" });
    app.querySelector("[data-home]").onclick = () => navigate({ name: "home" });
    return;
  }

  const q = questions[step];
  const rooms = allRooms();
  const hintSet = new Set(q.roomHints);
  const options = buildOptions(q.roomHints, rooms, 6);
  const picked = route.picked;

  let feedbackLaw = "";
  if (picked) {
    const refs = [];
    for (const id of q.roomHints) {
      const hit = findRoom(id);
      if (!hit) continue;
      for (const ref of hit.room.articleRefs || []) {
        if (!refs.includes(ref)) refs.push(ref);
      }
    }
    feedbackLaw = `
      <label class="eyebrow block-label">参考法条原文</label>
      ${renderArticleBlocks(refs, [])}
    `;
  }

  app.innerHTML = `
    <main class="app-shell">
      <button type="button" class="back-link" data-back>← 换题</button>
      <header class="topbar">
        <div>
          <p class="eyebrow">${drill.trackLabel || "FIVE QUESTIONS"}</p>
          <h1>${drill.title}</h1>
        </div>
        <span class="chip">${step + 1}/${questions.length}</span>
      </header>
      <div class="progress-bar"><span style="width:${((step + 1) / questions.length) * 100}%"></span></div>
      <div class="card">
        <p class="muted" style="margin:0 0 12px">${drill.prompt}</p>
        <div class="q-step">第 ${step + 1} 问 · ${q.floorHint}</div>
        <h2>${q.label}？</h2>
        <p class="muted" style="margin-top:8px">点选本问最该先打开的房间（可多想，选一个最贴的）。</p>
        <div class="room-pick">
          ${options
            .map((r) => {
              let cls = "";
              if (picked) {
                if (hintSet.has(r.id)) cls = "correct";
                else if (r.id === picked) cls = "wrong";
              }
              return `<button type="button" class="${cls}" data-pick="${r.id}" ${picked ? "disabled" : ""}>
                <strong>${r.id}</strong> ${r.title}<br/><span class="muted">${r.articleLabel}</span>
              </button>`;
            })
            .join("")}
        </div>
        ${
          picked
            ? `<div class="feedback">
                ${
                  hintSet.has(picked)
                    ? "路径正确。参考房间："
                    : "可再对齐参考路径。本问常落："
                }
                ${q.roomHints.join("、")}
                ${!hintSet.has(picked) ? " · 已将该错房标记发霉" : ""}
                ${feedbackLaw}
              </div>
              <div class="btn-row">
                <button type="button" class="btn btn-primary" data-next>下一问</button>
              </div>`
            : ""
        }
      </div>
    </main>
    ${dock("drill")}
  `;
  bindDock();
  app.querySelector("[data-back]").onclick = () => navigate({ name: "drill" });
  app.querySelectorAll("[data-pick]").forEach((btn) => {
    btn.onclick = () => {
      const id = btn.getAttribute("data-pick");
      if (!hintSet.has(id)) progress = markMoldy(id);
      navigate({ name: "drill", caseId: drill.id, step, picked: id });
    };
  });
  const next = app.querySelector("[data-next]");
  if (next)
    next.onclick = () => {
      if (step + 1 >= questions.length) progress = bumpDrill();
      navigate({ name: "drill", caseId: drill.id, step: step + 1, picked: null });
    };
}

function renderListen() {
  const floorsSorted = data.floors.slice().sort((a, b) => a.level - b.level);
  const floor = findFloor(route.floorId) || floorsSorted[0];
  const ok = supportsSpeech();
  const lineIndex = route.lineIndex || 0;
  const lineTotal = route.lineTotal || 0;
  const lineText = route.lineText || "选择楼层后点「开始听过」。";

  app.innerHTML = `
    <main class="app-shell">
      <button type="button" class="back-link" data-back>← 馆门</button>
      <header class="topbar">
        <div>
          <p class="eyebrow">COMMUTE AUDIO</p>
          <h1>通勤听过</h1>
        </div>
      </header>
      <p class="muted">${ok ? "用系统中文语音读整层口述与人话解释，适合地铁通勤。" : "当前浏览器不支持语音合成，请换 Chrome / Edge / Safari。"}</p>
      <div class="floor-tabs" style="margin-top:12px">
        ${floorsSorted
          .map(
            (f) => `
          <button type="button" class="${f.id === floor.id ? "active" : ""}" data-floor="${f.id}">
            ${formatFloorTab(f)}
          </button>`
          )
          .join("")}
      </div>
      <p class="mission">${floor.mission} · 约 ${floor.rooms.length} 间</p>
      <div class="card listen-card">
        <div class="listen-progress muted">${lineTotal ? `${lineIndex + 1} / ${lineTotal}` : "待命"}</div>
        <p class="listen-line" id="listen-line">${escapeHtml(lineText)}</p>
        <div class="btn-row" style="margin-top:14px">
          <button type="button" class="btn btn-primary" data-play ${ok ? "" : "disabled"}>开始听过</button>
          <button type="button" class="btn btn-ghost" data-pause ${ok ? "" : "disabled"}>暂停</button>
          <button type="button" class="btn btn-ghost" data-stop>停止</button>
        </div>
        <div class="btn-row">
          <button type="button" class="btn btn-ghost" data-rate="slower">减速</button>
          <button type="button" class="btn btn-ghost" data-rate="reset">语速 ${getListenRate().toFixed(2)}</button>
          <button type="button" class="btn btn-ghost" data-rate="faster">加速</button>
        </div>
        <p class="muted" style="margin-top:12px;font-size:0.82rem">语速范围 0.50～1.50。暂停后可点「继续」接着听；停止会清空进度，需重新开始。</p>
      </div>
      <div class="card" style="margin-top:12px">
        <p class="eyebrow">也可先闭眼走数字桩</p>
        <button type="button" class="btn btn-ghost" data-peg style="margin-top:10px;width:100%">打开数字桩闪过</button>
      </div>
    </main>
    ${dock("listen")}
  `;
  bindDock();
  app.querySelector("[data-back]").onclick = () => {
    stopListen();
    navigate({ name: "home" });
  };
  app.querySelectorAll("[data-floor]").forEach((btn) => {
    btn.onclick = () => {
      stopListen();
      navigate({ name: "listen", floorId: btn.getAttribute("data-floor") });
    };
  });
  app.querySelector("[data-peg]").onclick = () => {
    stopListen();
    navigate({ name: "peg", idx: 0, revealed: false });
  };
  app.querySelector("[data-stop]").onclick = () => {
    stopListen();
    const pauseBtn = app.querySelector("[data-pause]");
    if (pauseBtn) pauseBtn.textContent = "暂停";
    navigate({
      name: "listen",
      floorId: floor.id,
      lineText: "已停止。",
      lineIndex: 0,
      lineTotal: 0,
    });
  };
  app.querySelector("[data-pause]")?.addEventListener("click", () => {
    if (!ok) return;
    const btn = app.querySelector("[data-pause]");
    const el = document.getElementById("listen-line");
    if (isPaused()) {
      resumeListen();
      if (btn) btn.textContent = "暂停";
      if (el && route.lineText) el.textContent = route.lineText;
    } else if (hasSession()) {
      const current = route.lineText || el?.textContent || "";
      pauseListen();
      if (btn) btn.textContent = "继续";
      if (el) el.textContent = current ? `已暂停：${current}` : "已暂停，点「继续」接着听。";
    }
  });
  app.querySelectorAll("[data-rate]").forEach((btn) => {
    btn.onclick = () => {
      const mode = btn.getAttribute("data-rate");
      if (mode === "slower") setListenRate(getListenRate() - 0.1);
      if (mode === "faster") setListenRate(getListenRate() + 0.1);
      if (mode === "reset") setListenRate(1);
      const label = app.querySelector('[data-rate="reset"]');
      if (label) label.textContent = `语速 ${getListenRate().toFixed(2)}`;
    };
  });
  app.querySelector("[data-play]").onclick = () => {
    if (!ok) return;
    const pauseBtn = app.querySelector("[data-pause]");
    if (pauseBtn) pauseBtn.textContent = "暂停";
    const scripts = data.listenScripts || {};
    const lines = buildFloorScript(floor, data.articles || {}, {
      intro: scripts.intro,
      outro: scripts.outro,
    });
    playScript(lines, {
      onProgress: ({ index, total, text }) => {
        const el = document.getElementById("listen-line");
        const prog = app.querySelector(".listen-progress");
        if (el) el.textContent = text;
        if (prog) prog.textContent = `${index + 1} / ${total}`;
        const pbtn = app.querySelector("[data-pause]");
        if (pbtn && !isPaused()) pbtn.textContent = "暂停";
        route = {
          ...route,
          name: "listen",
          floorId: floor.id,
          lineIndex: index,
          lineTotal: total,
          lineText: text,
        };
      },
      onEnd: () => {
        const el = document.getElementById("listen-line");
        if (el) el.textContent = "本层听完。可换一层或回馆门。";
        const pbtn = app.querySelector("[data-pause]");
        if (pbtn) pbtn.textContent = "暂停";
      },
    });
  };
}

function searchRooms(q) {
  const needle = (q || "").trim().toLowerCase();
  if (!needle) return [];
  const arts = data.articles || {};
  return allRooms()
    .map((r) => {
      const artTexts = (r.articleRefs || [])
        .map((ref) => {
          const a = arts[ref];
          if (!a) return "";
          return [a.label, a.text, a.plain, ...(a.examples || []), a.apply || ""].join(" ");
        })
        .join(" ");
      const classic = (r.classicCases || [])
        .map((c) => [c.name, c.hook, c.takeaway].join(" "))
        .join(" ");
      const hay = [
        r.id,
        r.title,
        r.article,
        r.articleLabel,
        r.oral30s,
        r.sceneHook,
        r.space,
        ...(r.caseAnchor || []),
        ...(r.elements || []),
        classic,
        artTexts,
        r.floorName,
      ]
        .join(" ")
        .toLowerCase();
      const score =
        (r.id.toLowerCase() === needle ? 50 : 0) +
        (r.article === needle || r.articleLabel?.includes(needle) ? 40 : 0) +
        (hay.includes(needle) ? 10 : 0) +
        (r.title.includes(q) ? 20 : 0);
      return { room: r, score, hay };
    })
    .filter((x) => x.score > 0 || x.hay.includes(needle))
    .sort((a, b) => b.score - a.score)
    .slice(0, 30)
    .map((x) => x.room);
}

function renderSearch() {
  const q = route.q || "";
  const hits = q ? searchRooms(q) : [];
  app.innerHTML = `
    <main class="app-shell">
      <button type="button" class="back-link" data-back>← 馆门</button>
      <header class="topbar">
        <div>
          <p class="eyebrow">SEARCH</p>
          <h1>全馆搜索</h1>
        </div>
      </header>
      <div class="search-bar card">
        <input id="search-input" type="search" placeholder="例如：57、撤三、混淆、乔丹、三年" value="${escapeHtml(q)}" />
        <button type="button" class="btn btn-primary" data-run>搜索</button>
      </div>
      ${
        !q
          ? `<p class="muted">输入条号、门牌号、关键词或案例名。</p>`
          : hits.length
            ? `<p class="muted">找到 ${hits.length} 条</p>
               <div class="menu-grid">
                 ${hits
                   .map(
                     (r) => `
                   <button type="button" class="menu-btn" data-open="${r.floorId}" data-room="${r.id}">
                     <span class="kicker">${r.level === 0 ? "B0" : `${r.level}F`} · ${r.id}</span>
                     <strong>${r.title}</strong>
                     <span class="muted">${r.articleLabel} · ${r.sceneHook || ""}</span>
                   </button>`
                   )
                   .join("")}
               </div>`
            : `<p class="muted">没有匹配结果，换个关键词试试。</p>`
      }
    </main>
    ${dock("home")}
  `;
  bindDock();
  app.querySelector("[data-back]").onclick = () => navigate({ name: "home" });
  const run = () => {
    const next = app.querySelector("#search-input")?.value?.trim() || "";
    navigate({ name: "search", q: next });
  };
  app.querySelector("[data-run]").onclick = run;
  app.querySelector("#search-input")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") run();
  });
  app.querySelectorAll("[data-open]").forEach((btn) => {
    btn.onclick = () =>
      navigate({
        name: "corridor",
        floorId: btn.getAttribute("data-open"),
        roomId: btn.getAttribute("data-room"),
        revealed: false,
      });
  });
  requestAnimationFrame(() => app.querySelector("#search-input")?.focus());
}

function renderMoldy() {
  const ids = Object.keys(progress.moldyRooms || {}).sort(
    (a, b) => (progress.moldyRooms[b] || 0) - (progress.moldyRooms[a] || 0)
  );
  const rooms = ids.map((id) => findRoom(id)).filter(Boolean);
  const idx = Math.min(route.moldIdx || 0, Math.max(rooms.length - 1, 0));
  const current = rooms[idx];

  app.innerHTML = `
    <main class="app-shell">
      <button type="button" class="back-link" data-back>← 馆门</button>
      <header class="topbar">
        <div>
          <p class="eyebrow">MOLDY REVIEW</p>
          <h1>发霉复习</h1>
        </div>
        <span class="chip">${rooms.length ? `${idx + 1}/${rooms.length}` : "0"}</span>
      </header>
      ${
        !rooms.length
          ? `<div class="card"><p class="muted">暂无发霉门。去五问答错几题，或在走廊点「记错了」。</p>
             <div class="btn-row"><button type="button" class="btn btn-primary" data-drill>去五问</button></div></div>`
          : `<p class="muted">按发霉次数优先。先自己口述，再进走廊揭晓。</p>
             <div class="card">
               <p class="eyebrow">${current.floor.level === 0 ? "B0" : `${current.floor.level}F`} · 发霉 ${progress.moldyRooms[current.room.id]} 次</p>
               <h2>${current.room.id} ${current.room.title}</h2>
               <p class="muted">${current.room.articleLabel}</p>
               <p class="muted" style="margin-top:8px">场景：${current.room.sceneHook}</p>
               <p class="oral" style="margin-top:12px">${current.room.oral30s}</p>
               ${
                 current.room.classicCases?.length
                   ? `<label class="eyebrow block-label">经典案例</label>
                      ${current.room.classicCases.map((c) => `<p class="muted"><strong>${escapeHtml(c.name)}</strong> — ${escapeHtml(c.takeaway || "")}</p>`).join("")}`
                   : ""
               }
               <div class="btn-row">
                 <button type="button" class="btn btn-primary" data-open>进走廊揭晓</button>
                 <button type="button" class="btn btn-ghost" data-clean>已掌握·除霉</button>
               </div>
               <div class="btn-row">
                 <button type="button" class="btn btn-ghost" data-prev ${idx <= 0 ? "disabled" : ""}>上一扇</button>
                 <button type="button" class="btn btn-ghost" data-next ${idx >= rooms.length - 1 ? "disabled" : ""}>下一扇</button>
               </div>
             </div>`
      }
    </main>
    ${dock("home")}
  `;
  bindDock();
  app.querySelector("[data-back]").onclick = () => navigate({ name: "home" });
  app.querySelector("[data-drill]")?.addEventListener("click", () => navigate({ name: "drill" }));
  if (!current) return;
  app.querySelector("[data-open]").onclick = () =>
    navigate({
      name: "corridor",
      floorId: current.floor.id,
      roomId: current.room.id,
      revealed: false,
    });
  app.querySelector("[data-clean]").onclick = () => {
    progress = clearMoldy(current.room.id);
    navigate({ name: "moldy", moldIdx: Math.min(idx, Math.max(ids.length - 2, 0)) });
  };
  app.querySelector("[data-prev]")?.addEventListener("click", () =>
    navigate({ name: "moldy", moldIdx: idx - 1 })
  );
  app.querySelector("[data-next]")?.addEventListener("click", () =>
    navigate({ name: "moldy", moldIdx: idx + 1 })
  );
}

function buildOptions(hints, rooms, count) {
  const byId = new Map(rooms.map((r) => [r.id, r]));
  const chosen = [];
  for (const id of hints) {
    if (byId.has(id) && !chosen.find((x) => x.id === id)) chosen.push(byId.get(id));
  }
  const rest = rooms.filter((r) => !hints.includes(r.id));
  shuffle(rest);
  for (const r of rest) {
    if (chosen.length >= count) break;
    chosen.push(r);
  }
  return shuffle(chosen).slice(0, count);
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function render() {
  if (route.name === "hall") return renderHall();
  if (!data) {
    app.innerHTML = `<main class="app-shell"><p class="empty">尚未进入馆。请先选馆。</p>
      <button type="button" class="btn btn-primary" data-to-hall style="margin-top:14px">去选馆</button></main>`;
    app.querySelector("[data-to-hall]").onclick = () => navigate({ name: "hall" });
    return;
  }
  progress = loadProgress();
  if (route.name === "home") return renderHome();
  if (route.name === "corridor") return renderCorridor();
  if (route.name === "peg") return renderPeg();
  if (route.name === "drill") return renderDrill();
  if (route.name === "listen") return renderListen();
  if (route.name === "search") return renderSearch();
  if (route.name === "moldy") return renderMoldy();
  renderHome();
}

async function boot() {
  registerPwa();
  app.innerHTML = `<main class="app-shell"><p class="empty">正在打开知产诉讼城…</p></main>`;

  app.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-explain-toggle]");
    if (!btn || !app.contains(btn)) return;
    const block = btn.closest(".law-block");
    const panel = block?.querySelector("[data-explain-panel]");
    if (!panel) return;
    const open = panel.hasAttribute("hidden");
    if (open) panel.removeAttribute("hidden");
    else panel.setAttribute("hidden", "");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    const openLab = btn.querySelector("[data-explain-open]");
    const closeLab = btn.querySelector("[data-explain-close]");
    if (openLab) openLab.hidden = open;
    if (closeLab) closeLab.hidden = !open;
  });

  navigate({ name: "hall" });
}

boot();
