import { defineConfig } from 'vite'

// GitHub Pages project site: set env BASE_PATH=/<repo>/  (with trailing slash)
// Or use relative './' which works for project pages and local preview.
const base = process.env.BASE_PATH || './'

export default defineConfig({
  base,
  server: {
    port: 5177,
    host: true,
  },
  preview: {
    port: 5177,
    host: true,
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
})
