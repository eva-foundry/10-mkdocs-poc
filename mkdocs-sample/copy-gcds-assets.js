const fs = require(\"fs\");
const path = require(\"path\");
const source = path.join(__dirname, \"node_modules\", \"@cdssnc\", \"gcds-components\", \"dist\", \"gcds\");
const destination = path.join(__dirname, \"docs\", \"assets\", \"gcds\");
function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) { fs.mkdirSync(dest, { recursive: true }); }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) { copyDirectory(srcPath, destPath); }
    else { fs.copyFileSync(srcPath, destPath); }
  }
}
console.log(\"[GCDS Asset Copy] Starting...\");
console.log(\"Source:\", source);
console.log(\"Destination:\", destination);
try {
  if (!fs.existsSync(source)) { console.error(\"[ERROR] GCDS not found\"); process.exit(1); }
  copyDirectory(source, destination);
  console.log(\"[SUCCESS] GCDS assets copied!\");
} catch (error) { console.error(\"[ERROR]\", error.message); process.exit(1); }
