/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'health': {
          primary: '#10b981',
          secondary: '#3b82f6',
          accent: '#06b6d4',
          warning: '#f59e0b',
          danger: '#ef4444',
        }
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
} 