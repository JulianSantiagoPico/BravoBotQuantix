/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        pascual: {
          blue: '#003366',
          orange: '#FF6600',
          lightBlue: '#004080',
          gray: '#F5F5F5',
        },
      },
    },
  },
  plugins: [],
}
