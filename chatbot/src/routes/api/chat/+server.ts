import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  const { question, mode } = await request.json();
  const RAG_API_URL = process.env.RAG_API_URL ?? 'http://localhost:8000';
  
  if (!question?.trim()) {
    return json({ error: 'No question provided' }, { status: 400 });
  }

  try {
    const res = await fetch(`${RAG_API_URL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, mode }),
    });

    const data = await res.json();
    return json({ answer: data.answer });
  } catch (err) {
    console.error(err);
    return json({ error: 'RAG API failed' }, { status: 500 });
  }
};