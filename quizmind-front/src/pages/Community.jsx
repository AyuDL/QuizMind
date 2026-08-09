// Écran Communauté — placeholder pour l'instant.
// Sert à vérifier que la protection de route fonctionne (accessible uniquement connecté).
// On le remplira avec la vraie liste des quiz au prochain écran.

import { useAuth } from "../auth/AuthContext";

export default function Community() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-lavender px-6 py-12">
      <div className="mx-auto max-w-2xl">
        <div className="flex items-center justify-between">
          <span className="font-display text-xl font-semibold text-ink">QuizMind</span>
          <button onClick={logout} className="font-body text-sm text-violet hover:underline">
            Se déconnecter
          </button>
        </div>

        <h1 className="mt-10 font-display text-4xl font-semibold text-ink">Communauté.</h1>
        <p className="mt-2 font-body text-ink/70">
          Connecté en tant que <span className="font-medium text-ink">{user?.username}</span>.
          La liste des QCM viendra ici.
        </p>
      </div>
    </div>
  );
}
