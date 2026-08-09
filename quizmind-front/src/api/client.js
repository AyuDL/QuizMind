// Couche unique qui parle à ton API Django.
// Tout appel réseau passe par ici — un seul endroit à changer si l'URL bouge.

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

// --- Gestion des tokens JWT en mémoire + localStorage ---
// access  : token court, envoyé à chaque requête
// refresh : token long, sert à obtenir un nouveau access quand il expire

const TOKEN_KEYS = { access: "qm_access", refresh: "qm_refresh" };

export const tokenStore = {
  get access() {
    return localStorage.getItem(TOKEN_KEYS.access);
  },
  get refresh() {
    return localStorage.getItem(TOKEN_KEYS.refresh);
  },
  set({ access, refresh }) {
    if (access) localStorage.setItem(TOKEN_KEYS.access, access);
    if (refresh) localStorage.setItem(TOKEN_KEYS.refresh, refresh);
  },
  clear() {
    localStorage.removeItem(TOKEN_KEYS.access);
    localStorage.removeItem(TOKEN_KEYS.refresh);
  },
};

// --- Le cœur : une fonction request() unique ---
// Elle ajoute le token, envoie la requête, et si l'access est expiré (401),
// tente un refresh automatique puis rejoue la requête une fois.

async function request(path, { method = "GET", body, auth = true, _retry = false } = {}) {
  const headers = { "Content-Type": "application/json" };

  if (auth && tokenStore.access) {
    headers["Authorization"] = `Bearer ${tokenStore.access}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  // Access expiré → on tente un refresh une seule fois, puis on rejoue
  if (res.status === 401 && auth && !_retry && tokenStore.refresh) {
    const refreshed = await tryRefresh();
    if (refreshed) {
      return request(path, { method, body, auth, _retry: true });
    }
  }

  return handleResponse(res);
}

async function tryRefresh() {
  const res = await fetch(`${BASE_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: tokenStore.refresh }),
  });
  if (!res.ok) {
    tokenStore.clear();
    return false;
  }
  const data = await res.json();
  tokenStore.set({ access: data.access });
  return true;
}

async function handleResponse(res) {
  // 204 No Content : rien à parser
  if (res.status === 204) return null;

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    // On renvoie une erreur portant le détail de l'API pour l'afficher au user
    const message = extractError(data) || `Erreur ${res.status}`;
    throw new ApiError(message, res.status, data);
  }
  return data;
}

// DRF renvoie les erreurs sous des formes variées ({detail:...} ou {champ:[...]})
function extractError(data) {
  if (!data) return null;
  if (typeof data.detail === "string") return data.detail;
  // Prend le premier message du premier champ en erreur
  const firstKey = Object.keys(data)[0];
  if (firstKey) {
    const val = data[firstKey];
    return Array.isArray(val) ? val[0] : String(val);
  }
  return null;
}

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

// --- Raccourcis pour ne pas répéter method partout ---
export const api = {
  get: (path, opts) => request(path, { ...opts, method: "GET" }),
  post: (path, body, opts) => request(path, { ...opts, method: "POST", body }),
  patch: (path, body, opts) => request(path, { ...opts, method: "PATCH", body }),
  delete: (path, opts) => request(path, { ...opts, method: "DELETE" }),
};
