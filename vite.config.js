import { defineConfig } from "vite";

export default defineConfig({
    build: {
        outDir: "app/static/dist",
        emptyOutDir: false,
        rollupOptions: {
            input: "frontend/main.js",
            output: {
                entryFileNames: "app.js",
            },
        },
    },
});