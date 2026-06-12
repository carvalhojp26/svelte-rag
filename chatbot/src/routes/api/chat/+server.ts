import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export const POST: RequestHandler = async ({ request }) => {
  const { question } = await request.json();
  console.log('[API] received question:', question);

  try {
    const { stdout, stderr } = await execAsync(
      `/home/carvalhojp/projects/svelte-rag/venv/bin/python3 -m rag.query "${question.replace(/"/g, '\\"')}"`,
      { cwd: '/home/carvalhojp/projects/svelte-rag' }
    );
    console.log('[API] stdout:', stdout);
    console.log('[API] stderr:', stderr);

    const answer = stdout.split('Answer:\n')[1]?.trim() ?? stderr;

    const cleaned = answer.startsWith("('") 
      ? answer.slice(2, answer.indexOf("', ["))
      : answer;
    
    return json({ answer: cleaned.replace(/\\n/g, '\n').replace(/\\'/g, "'") });
  } catch (err) {
    console.error('[API] error:', err);
    return json({ error: 'RAG failed' }, { status: 500 });
  }
};