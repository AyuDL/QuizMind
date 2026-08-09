// Contexte d'authentification : rend l'état "connecté / pas connecté"
// disponible partout dans l'app, sans le repasser en props à chaque écran.

import { createContext, useContext, useEffect, useState } from "react";
import { tokenStore } from "../api/client";
import { getMe, login as apiLogin, logout as apiLogout } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Au chargement de l'app : si un token existe déjà, on récupère le profil
  useEffect(() => {
    if (!tokenStore.access) {
      setLoading(false);
      return;
    }
    getMe()
      .then((me) => setUser(me))
      .catch(() => apiLogout())
      .finally(() => setLoading(false));
  }, []);

  async function login(credentials) {
    await apiLogin(credentials);
    const me = await getMe();
    setUser(me);
    return me;
  }

  function logout() {
    apiLogout();
    setUser(null);
  }

  const value = { user, loading, login, logout, isAuthenticated: !!user };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Hook pratique : useAuth() dans n'importe quel composant
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth doit être utilisé dans <AuthProvider>");
  return ctx;
}
