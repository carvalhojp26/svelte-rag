import { auth } from '$lib/auth';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async (event) => {
  return auth.handler(event.request);
};

export const POST: RequestHandler = async (event) => {
  return auth.handler(event.request);
};