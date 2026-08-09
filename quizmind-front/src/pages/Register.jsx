// Écran d'inscription — reprend les champs de ta maquette Figma
// (prénom, nom, identifiant, email, mot de passe, CGU).

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../api/auth";
import Field from "../components/Field";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    accepted_terms: false,
  });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function update(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit() {
    setError(null);
    if (!form.accepted_terms) {
      setError("Tu dois accepter les conditions d'utilisation.");
      return;
    }
    setSubmitting(true);
    try {
      await register(form);
      // Inscription OK → on renvoie vers la connexion
      navigate("/login", { state: { justRegistered: true } });
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
          <h1 className="font-display text-4xl font-semibold text-ink">Crée ton compte.</h1>
          <p className="font-body text-sm text-ink/70">Trois champs, un mail de confirmation, et c'est parti.</p>
        </header>

        <div className="flex flex-col gap-4">
          <Field label="Prénom" name="first_name" value={form.first_name} onChange={update} placeholder="ton_prenom" />
          <Field label="Nom" name="last_name" value={form.last_name} onChange={update} placeholder="ton_nom" />
          <Field label="Identifiant" name="username" value={form.username} onChange={update} placeholder="ton_pseudo" />
          <Field label="Adresse email" type="email" name="email" value={form.email} onChange={update} placeholder="nom@exemple.com" />
          <Field label="Mot de passe" type="password" name="password" value={form.password} onChange={update} placeholder="8 caractères minimum" />

          <label className="flex items-start gap-3 font-body text-sm text-ink/80">
            <input
              type="checkbox"
              name="accepted_terms"
              checked={form.accepted_terms}
              onChange={(e) => setForm({ ...form, accepted_terms: e.target.checked })}
              className="mt-0.5 h-4 w-4 accent-violet"
            />
            <span>J'accepte les Conditions Générales d'Utilisation et la Politique de confidentialité.</span>
          </label>

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
            {submitting ? "Création…" : "Créer mon compte"}
          </button>

          <p className="text-center font-body text-sm text-ink/70">
            Déjà inscrit ? <Link to="/login" className="text-violet hover:underline">Se connecter</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
