import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { auth } from '$lib/auth';

const RAG_API_URL = process.env.RAG_API_URL ?? 'http://localhost:8000';
const MAX_QUESTION_LENGTH = 500;
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX_REQUESTS = 10;

const requestLog = new Map<string, number[]>();

function isRateLimited(userId: string): boolean {
  const now = Date.now();
  const timestamps = (requestLog.get(userId) ?? []).filter(t => now - t < RATE_LIMIT_WINDOW_MS);
  timestamps.push(now);
  requestLog.set(userId, timestamps);
  return timestamps.length > RATE_LIMIT_MAX_REQUESTS;
}

export const POST: RequestHandler = async ({ request }) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session) {
    return json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (isRateLimited(session.user.id)) {
    return json({ error: 'Too many requests. Please try again in a minute.' }, { status: 429 });
  }

  const { question, mode } = await request.json();

  if (!question?.trim()) {
    return json({ error: 'No question provided' }, { status: 400 });
  }

  if (question.length > MAX_QUESTION_LENGTH) {
    return json({ error: `The question exceeds the limit of ${MAX_QUESTION_LENGTH} characters.` }, { status: 400 });
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