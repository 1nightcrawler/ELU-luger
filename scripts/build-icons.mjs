import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { icons } from "lucide";

// Filenames map to the PascalCase names exported by the Lucide package.
const requestedIcons = {
  book: "Book",
  "chart-column": "ChartColumn",
  trophy: "Trophy",
  settings: "Settings",
  sparkles: "Sparkles",
  "log-out": "LogOut",
  "arrow-left": "ArrowLeft",
  search: "Search",
  "pen-line": "PenLine",
  "sliders-horizontal": "SlidersHorizontal",
};

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const outputDirectory = path.resolve(scriptDirectory, "../app/static/icons");
const strokeColor = process.env.LUCIDE_STROKE ?? "#334155";

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;");
}

function renderIconNode([tag, attributes = {}, children = []]) {
  const attributesText = Object.entries(attributes)
    .map(([name, value]) => ` ${name}="${escapeXml(value)}"`)
    .join("");
  const childrenText = (children ?? []).map(renderIconNode).join("");

  return childrenText
    ? `<${tag}${attributesText}>${childrenText}</${tag}>`
    : `<${tag}${attributesText} />`;
}

await mkdir(outputDirectory, { recursive: true });

for (const [filename, exportName] of Object.entries(requestedIcons)) {
  const iconNodes = icons[exportName];
  if (!iconNodes) {
    throw new Error(`Lucide icon export not found: ${exportName}`);
  }

  const body = iconNodes.map(renderIconNode).join("");
  const svg = `<!-- Generated from lucide; run npm run build:icons to regenerate. -->\n` +
    `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" ` +
    `viewBox="0 0 24 24" fill="none" stroke="${escapeXml(strokeColor)}" ` +
    `stroke-width="2" stroke-linecap="round" stroke-linejoin="round">` +
    `${body}</svg>\n`;

  await writeFile(path.join(outputDirectory, `${filename}.svg`), svg, "utf8");
  console.log(`Generated app/static/icons/${filename}.svg`);
}
