module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'sage-teal': '#2A9D8F',
        'sage-teal-dark': '#21867a',
        'warm-sand': '#E9C46A',
        'soft-coral': '#E76F51',
        'bg-main': '#F8F9FA',
      },
      fontFamily: {
        'manrope': ['Manrope', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0,0,0,0.04)',
        'card-hover': '0 8px 24px rgba(0,0,0,0.08)',
        'float': '0 12px 32px rgba(42,157,143,0.15)',
      },
    },
  },
  plugins: [],
};