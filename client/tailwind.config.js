import daisyui from "daisyui";

export default {
  content: ['./src/**/*.{html,js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        'saved-by-zero': ['"Saved by Zero"', 'sans-serif'],
        'pacifico': ['Pacifico', 'cursive'],
        'poppins': ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [daisyui],
};
