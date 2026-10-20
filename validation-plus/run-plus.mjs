// Archive-only path wrapper; check-plus.mjs is copied byte-for-byte from allmeta.
import { fileURLToPath } from 'node:url';
const args = process.argv.slice(2);
if (args.includes('--index')) throw Error('The archive wrapper always checks the archived page');
process.argv = [process.argv[0], fileURLToPath(new URL('check-plus.mjs', import.meta.url)),
  '--index', fileURLToPath(new URL('../app/mh-peto/index.html', import.meta.url)), ...args];
await import('./check-plus.mjs');
