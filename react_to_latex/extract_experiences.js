// extract_experiences.js
// Usage: node extract_experiences.js /path/to/Experience.tsx
const fs = require('fs');
const path = require('path');

if (process.argv.length < 3) {
  console.error('Usage: node extract_experiences.js /path/to/Experience.tsx');
  process.exit(1);
}

const filePath = process.argv[2];
const fileContent = fs.readFileSync(filePath, 'utf-8');

// Find the experiences array (assumes: export const experiences = [ ... ];)
const match = fileContent.match(/experiences\s*=\s*(\[[\s\S]*?\]);/);
if (!match) {
  console.error('Could not find experiences array in file.');
  process.exit(2);
}

let arrayStr = match[1];

// Try to make it valid JSON (very basic, assumes no functions or complex expressions)
arrayStr = arrayStr
  .replace(/([a-zA-Z0-9_]+)\s*:/g, '"$1":') // quote keys
  .replace(/'/g, '"') // single to double quotes
  .replace(/,\s*([}\]])/g, '$1'); // remove trailing commas

try {
  const arr = JSON.parse(arrayStr);
  console.log(JSON.stringify(arr, null, 2));
} catch (e) {
  console.error('Failed to parse experiences array as JSON:', e.message);
  process.exit(3);
}
