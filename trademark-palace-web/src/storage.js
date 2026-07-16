const LAST_PALACE_KEY = "ip-palace-last-id";

let palaceId = "trademark";

function storageKey() {
  return `palace-progress-v1:${palaceId}`;
}

export function getPalaceId() {
  return palaceId;
}

export function setPalaceId(id) {
  palaceId = id || "trademark";
  try {
    localStorage.setItem(LAST_PALACE_KEY, palaceId);
  } catch {
    /* ignore */
  }
}

export function getLastPalaceId() {
  try {
    return localStorage.getItem(LAST_PALACE_KEY) || null;
  } catch {
    return null;
  }
}

export function loadProgress() {
  try {
    const raw = localStorage.getItem(storageKey());
    if (!raw) return { moldyRooms: {}, pegSeen: 0, drillsDone: 0 };
    return JSON.parse(raw);
  } catch {
    return { moldyRooms: {}, pegSeen: 0, drillsDone: 0 };
  }
}

export function saveProgress(progress) {
  localStorage.setItem(storageKey(), JSON.stringify(progress));
}

export function markMoldy(roomId) {
  const p = loadProgress();
  p.moldyRooms[roomId] = (p.moldyRooms[roomId] || 0) + 1;
  saveProgress(p);
  return p;
}

export function clearMoldy(roomId) {
  const p = loadProgress();
  delete p.moldyRooms[roomId];
  saveProgress(p);
  return p;
}

export function bumpDrill() {
  const p = loadProgress();
  p.drillsDone = (p.drillsDone || 0) + 1;
  saveProgress(p);
  return p;
}
