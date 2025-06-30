// extract_experiences_acorn.js
// Usage: node extract_experiences_acorn.js /path/to/Experience.tsx
const fs = require('fs');
const acorn = require('acorn');

if (process.argv.length < 3) {
  console.error('Usage: node extract_experiences_acorn.js /path/to/Experience.tsx');
  process.exit(1);
}

const filePath = process.argv[2];
const fileContent = fs.readFileSync(filePath, 'utf-8');

let experiencesNode = null;
try {
  const ast = acorn.parse(fileContent, { ecmaVersion: 2020, sourceType: 'module' });
  for (const node of ast.body) {
    if (
      node.type === 'VariableDeclaration' &&
      node.declarations[0].id.name === 'experiences'
    ) {
      experiencesNode = node.declarations[0].init;
      break;
    }
  }
} catch (e) {
  console.error('Failed to parse file with acorn:', e.message);
  process.exit(2);
}

if (!experiencesNode) {
  console.error('Could not find experiences array in file.');
  process.exit(3);
}

function nodeToObj(node) {
  if (!node) return null;
  switch (node.type) {
    case 'ArrayExpression':
      return node.elements.map(nodeToObj);
    case 'ObjectExpression':
      const obj = {};
      for (const prop of node.properties) {
        obj[prop.key.name || prop.key.value] = nodeToObj(prop.value);
      }
      return obj;
    case 'Literal':
      return node.value;
    case 'TemplateLiteral':
      return node.quasis.map(q => q.value.cooked).join('');
    default:
      return null;
  }
}

const experiences = nodeToObj(experiencesNode);
console.log(JSON.stringify(experiences, null, 2));
