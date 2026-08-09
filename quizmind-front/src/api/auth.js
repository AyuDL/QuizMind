// Appels API spécifiques à l'authentification.
// Chaque fonction correspond à un endpoint de ton backend Django.

import { api, tokenStore } from "./client";

// Inscription — auth:false car on n'est pas encore connecté
export function register(payload) {
  // payload attendu : { username, email, password, first_name, last_name, accepted_terms }
  return api.post("/auth/register/", payload, { auth: false });
}

// Connexion — récupère access + refresh, les stocke
export async function login({ username, password }) {
  const data = await api.post(
    "/auth/token/",
    { username, password },
    { auth: false }
  );
  tokenStore.set({ access: data.access, refresh: data.refresh });
  return data;
}

// Déconnexion — on jette juste les tokens côté client
export function logout() {
  tokenStore.clear();
}

// Confirmation de compte via le token reçu par mail
export function confirmAccount(token) {
  return api.post("/auth/confirm-account/", { token }, { auth: false });
}

// Demande de reset de mot de passe (envoi du mail)
export function requestPasswordReset(email) {
  return api.post("/auth/password-reset/", { email }, { auth: false });
}

// Réinitialisation effective avec le token du mail
export function resetPassword({ token, password }) {
  return api.post("/auth/password-reset-confirm/", { token, password }, { auth: false });
}

// Profil de l'utilisateur connecté
export function getMe() {
  return api.get("/users/me/");
}
