import { redirect } from '@sveltejs/kit';
import { auth } from '$lib/auth';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ request }) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session) throw redirect(302, '/login');
  return { user: session.user };
};