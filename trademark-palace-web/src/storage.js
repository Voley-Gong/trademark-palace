const STORAGE_KEY = "trademark-palace-progress-v1";

export function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { moldyRooms: {}, pegSeen: 0, drillsDone: 0 };
    return JSON.parse(raw);
  } catch {
    return { moldyRooms: {}, pegSeen: 0, drillsDone: 0 };
  }
}

export function saveProgress(progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
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
