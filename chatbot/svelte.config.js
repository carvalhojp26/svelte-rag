import adapter from '@sveltejs/adapter-node';
import { relative, sep } from 'node:path';

const config = {
  compilerOptions: {
    runes: ({ filename }) => {
      const relativePath = relative(import.meta.dirname, filename);
      const pathSegments = relativePath.toLowerCase().split(sep);
      const isExternalLibrary = pathSegments.includes('node_modules');
      return isExternalLibrary ? undefined : true;
    }
  },
  kit: {
    adapter: adapter()
  }
};

export default config;