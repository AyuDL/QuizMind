// Champ de formulaire réutilisable — label + input, style QuizMind.
// Reprend l'apparence de tes maquettes (label mono, bordure encre).

export default function Field({ label, type = "text", value, onChange, placeholder, name, required }) {
  return (
    <label className="flex flex-col gap-2">
      <span className="font-mono text-[10px] font-medium uppercase tracking-wide text-ink">
        {label}
      </span>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="rounded border-[1.5px] border-ink bg-white px-4 py-3 font-body text-[15px] text-ink outline-none transition focus:border-violet focus:ring-2 focus:ring-violet/20"
      />
    </label>
  );
}
