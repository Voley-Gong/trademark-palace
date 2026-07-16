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

export function buildFloorScript(floor, articles = {}, meta = {}) {
  const lines = [];
  if (meta.intro) lines.push(meta.intro);
  lines.push(`现在进入${floorSpokenName(floor)}。本层任务：${floor.mission}。`);
  for (const room of floor.rooms) {
    lines.push(`下一间，${room.id}，${room.title}，${room.articleLabel}。`);
    if (room.sceneHook) lines.push(`场景：${room.sceneHook}`);
    if (room.oral30s) lines.push(`口述：${room.oral30s}`);
    const refs = room.articleRefs || [];
    if (refs[0] && articles[refs[0]]?.plain) {
      lines.push(`人话：${articles[refs[0]].plain}`);
    }
    if (room.caseAnchor?.length) {
      lines.push(`案例锚：${room.caseAnchor.join("，")}。`);
    }
  }
  lines.push(
    meta.outro ||
      `${floor.level === 0 ? "地下室" : `${floor.level}楼`}走廊结束。可以回到馆门，或换一层继续听。`
  );
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
