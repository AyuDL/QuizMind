/** @type {import('tailwindcss').Config} */
// Thème repris fidèlement de tes maquettes Figma QuizMind.
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        violet: {
          DEFAULT: "#7C3AED", // violet électrique — couleur primaire
          light: "#9D6EF5",
          deep: "#4B1F9E",
        },
        gold: "#FBBF24", // doré — accent
        lavender: "#F5F3FF", // lavande — fonds clairs
        ink: {
          DEFAULT: "#0A1F44", // encre — texte foncé, fonds sombres
          deep: "#050D24",
        },
      },
      fontFamily: {
        display: ['"Fraunces"', "serif"], // titres
        body: ['"Inter"', "sans-serif"], // corps
        mono: ['"JetBrains Mono"', "monospace"], // labels, data
      },
    },
  },
  plugins: [],
};
