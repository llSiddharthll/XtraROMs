/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js',
    './node_modules/flowbite/**/*.css',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
],
}

