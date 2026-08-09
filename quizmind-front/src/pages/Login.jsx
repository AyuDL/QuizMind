// Écran de connexion — teste le flux JWT de bout en bout.
// Envoie username/password à /auth/token/, stocke les tokens, redirige.

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import Field from "../components/Field";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function update(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit() {
    setError(null);
    setSubmitting(true);
    try {
      await login(form);
      navigate("/"); // succès → communauté
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-lavender px-6 py-16">
      <div className="mx-auto flex max-w-sm flex-col gap-8">
        <header className="flex flex-col gap-2">
          <span className="font-display text-xl font-semibold text-ink">QuizMind</span>
          <h1 className="font-display text-4xl font-semibold text-ink">Content de te revoir.</h1>
          <p className="font-body text-sm text-ink/70">Connecte-toi pour reprendre tes quiz.</p>
        </header>

        <div className="flex flex-col gap-4">
          <Field label="Identifiant" name="username" value={form.username} onChange={update} placeholder="ton_pseudo" />
          <Field label="Mot de passe" type="password" name="password" value={form.password} onChange={update} placeholder="8 caractères minimum" />

          {error && (
            <p className="rounded border-[1.5px] border-red-300 bg-red-50 px-4 py-3 font-body text-sm text-red-700">
              {error}
            </p>
          )}

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="mt-2 rounded bg-violet px-4 py-3 font-body font-medium text-white transition hover:bg-violet-deep disabled:opacity-60"
          >
            {submitting ? "Connexion…" : "Se connecter"}
          </button>

          <div className="flex justify-between font-body text-sm text-ink/70">
            <Link to="/register" className="text-violet hover:underline">Créer un compte</Link>
            <Link to="/password-reset" className="text-violet hover:underline">Mot de passe oublié ?</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
