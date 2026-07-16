/** Commute listen mode via Web Speech API */

let queue = [];
let cursor = 0;
let speaking = false;
let paused = false;
let rate = 1;
let hooks = { onProgress: null, onEnd: null };

export function stopListen() {
  speaking = false;
  paused = false;
  queue = [];
  cursor = 0;
  window.speechSynthesis?.cancel();
}

export function setListenRate(r) {
  rate = Math.min(1.5, Math.max(0.5, r));
}

export function getListenRate() {
  return rate;
}

export function isSpeaking() {
  return speaking && !paused;
}

export function isPaused() {
  return paused;
}

/** 是否有可暂停/继续的会话（未播完） */
export function hasSession() {
  return queue.length > 0 && cursor < queue.length;
}

function floorSpokenName(floor) {
  if (floor.level === 0) return `地下室，${floor.name}`;
  return `${floor.level}楼，${floor.name}`;
}

function resolveFloorMeta(floor, meta = {}) {
  const byFloor = meta.byFloor || {};
  const local = byFloor[floor.id] || {};
  return {
    intro: local.intro || meta.intro,
    outro:
      local.outro ||
      meta.outro ||
      `${floor.level === 0 ? "地下室" : `${floor.level}楼`}走廊结束。可以回到馆门，或换一层继续听。`,
    motto: local.motto || meta.motto,
    bridge: local.bridge || "",
  };
}

/**
 * Build spoken lines for a floor.
 * meta: { intro, outro, motto, byFloor: { [floorId]: { intro, outro, motto, bridge } } }
 */
export function buildFloorScript(floor, articles = {}, meta = {}) {
  const lines = [];
  const floorMeta = resolveFloorMeta(floor, meta);
  if (floorMeta.intro) lines.push(floorMeta.intro);
  if (floorMeta.motto) lines.push(`本层口诀：${floorMeta.motto}`);
  lines.push(`现在进入${floorSpokenName(floor)}。本层任务：${floor.mission}。`);
  if (floor.mapAscii) {
    lines.push(`走廊地图：${floor.mapAscii}。`);
  }

  const rooms = floor.rooms || [];
  for (let i = 0; i < rooms.length; i += 1) {
    const room = rooms[i];
    lines.push(`第${i + 1}间，${room.id}，${room.title}，${room.articleLabel}。`);
    if (room.sceneHook) lines.push(`场景钩：${room.sceneHook}。`);
    if (room.oral30s) lines.push(`三十秒口述：${room.oral30s}`);
    const refs = room.articleRefs || [];
    if (refs[0] && articles[refs[0]]?.plain) {
      lines.push(`人话版：${articles[refs[0]].plain}`);
    }
    if (room.elements?.length) {
      lines.push(`要件要点：${room.elements.slice(0, 5).join("，")}。`);
    }
    if (room.caseAnchor?.length) {
      lines.push(`案例锚：${room.caseAnchor.join("，")}。`);
    }
    if (room.stations?.length) {
      lines.push(
        `站位：${room.stations.map((s) => s.label || s.id).join("，再到")}。`
      );
    }
    if (room.peg != null) {
      lines.push(`数字桩${room.peg}挂在这里。`);
    }
    if (room.drillPrompt) {
      lines.push(`自问一句：${room.drillPrompt}`);
    }
    if (room.links?.length) {
      lines.push(`可连房间：${room.links.slice(0, 4).join("、")}。`);
    }
  }

  if (floorMeta.bridge) lines.push(floorMeta.bridge);
  lines.push(floorMeta.outro);
  return lines;
}

function speakNext() {
  if (!speaking || paused) return;
  if (cursor >= queue.length) {
    speaking = false;
    paused = false;
    hooks.onEnd?.();
    return;
  }
  const text = queue[cursor];
  hooks.onProgress?.({ index: cursor, total: queue.length, text });
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "zh-CN";
  u.rate = rate;
  u.onend = () => {
    if (paused) return;
    cursor += 1;
    speakNext();
  };
  u.onerror = () => {
    if (paused) return;
    cursor += 1;
    speakNext();
  };
  window.speechSynthesis.speak(u);
}

export function playScript(lines, { onProgress, onEnd } = {}) {
  stopListen();
  queue = lines.filter(Boolean);
  cursor = 0;
  speaking = true;
  paused = false;
  hooks = { onProgress, onEnd };
  // Chrome sometimes needs a tick after cancel
  setTimeout(speakNext, 60);
}

export function pauseListen() {
  if (!speaking || paused || !hasSession()) return false;
  paused = true;
  window.speechSynthesis?.pause();
  // 部分浏览器 pause 无效：取消当前句，游标停在本句，继续时重读本句
  if (!window.speechSynthesis?.paused) {
    window.speechSynthesis?.cancel();
  }
  return true;
}

export function resumeListen() {
  if (!paused || !hasSession()) return false;
  paused = false;
  speaking = true;
  if (window.speechSynthesis?.paused) {
    window.speechSynthesis.resume();
  } else {
    // 从当前句重新播（pause 取消后的回退）
    setTimeout(speakNext, 60);
  }
  return true;
}

export function supportsSpeech() {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}
