import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const caseRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(caseRoot, '../..');
const qaRoot = join(caseRoot, 'docs/qa');
const docsRoot = join(caseRoot, 'docs');

function filesUnder(directory, suffix) {
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? filesUnder(path, suffix) : path.endsWith(suffix) ? [path] : [];
  });
}

const problems = [];
const markdownFiles = [
  join(repoRoot, 'README.md'),
  join(caseRoot, 'README.md'),
  join(caseRoot, 'performance/config/README.md'),
  ...filesUnder(docsRoot, '.md'),
];

for (const file of markdownFiles) {
  const source = readFileSync(file, 'utf8');
  if ([...source.matchAll(/^```/gm)].length % 2 !== 0) problems.push(`${file}: bloco de código sem fechamento`);
  const content = source.replace(/```[\s\S]*?```/g, '');
  for (const match of content.matchAll(/!?\[[^\]]*]\(([^)]+)\)/g)) {
    const raw = match[1].replace(/^<|>$/g, '');
    if (/^(?:https?:|mailto:|#)/.test(raw)) continue;
    const target = decodeURIComponent(raw.split('#')[0]);
    if (!existsSync(resolve(dirname(file), target))) {
      problems.push(`${file}: link ausente: ${raw}`);
    }
  }
}

const seen = new Set();
for (const file of filesUnder(join(qaRoot, 'bdd'), '.feature')) {
  const content = readFileSync(file, 'utf8');
  const features = [...content.matchAll(/^Funcionalidade:/gm)].length;
  const scenarios = [...content.matchAll(/^\s*Cenário:/gm)].length;
  const ids = [...content.matchAll(/@BDD-\d+/g)].map(match => match[0]);
  if (!content.startsWith('# language: pt') || features !== 1 || scenarios === 0 || scenarios !== ids.length) {
    problems.push(`${file}: cabeçalho, funcionalidade, cenários ou IDs BDD inconsistentes`);
  }
  for (const scenario of content.split(/^\s*Cenário:/m).slice(1)) {
    if (!/^\s+Dado /m.test(scenario) || !/^\s+Quando /m.test(scenario) || !/^\s+Então /m.test(scenario)) {
      problems.push(`${file}: cenário sem Dado, Quando e Então`);
    }
  }
  for (const id of ids) {
    if (seen.has(id)) problems.push(`${file}: ID duplicado: ${id}`);
    seen.add(id);
  }
}

const matrix = readFileSync(join(qaRoot, 'traceability.md'), 'utf8');
for (const id of seen) {
  if (!matrix.includes(id.slice(1))) problems.push(`traceability.md: ${id} sem mapeamento`);
}

if (problems.length) {
  console.error(problems.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Documentação: ${markdownFiles.length} arquivos Markdown, ${seen.size} cenários BDD e links locais verificados.`);
}
