/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1e3a8a', // blue-900
        secondary: '#3b82f6', // blue-500
      }
    },
  },
  plugins: [],
}
