<script lang="ts">
  import { createAuthClient } from 'better-auth/svelte';

  const client = createAuthClient();

  let email = $state('');
  let password = $state('');
  let name = $state('');
  let error = $state('');
  let loading = $state(false);
  let isRegistering = $state(false);

  async function handleLogin() {
    loading = true;
    error = '';
    const { error: err } = await client.signIn.email({ email, password, callbackURL: '/' });
    if (err) error = err.message ?? 'Login failed';
    loading = false;
  }

  async function handleRegister() {
    loading = true;
    error = '';
    const { data, error: err } = await client.signUp.email({
      email,
      password,
      name,
      callbackURL: '/',
      fetchOptions: {
        onSuccess: () => window.location.href = '/',
      },
    });
    if (err) error = err.message ?? 'Register failed';
    loading = false;
  }

  async function handleGoogle() {
    await client.signIn.social({ provider: 'google', callbackURL: '/' });
  }
</script>

<div class="flex flex-col items-center justify-center h-screen gap-6">
  <h2 class="text-4xl font-normal tracking-tight" style="font-family: 'Lora', Georgia, serif; color: #c8c3bc;">
    {isRegistering ? 'Create account' : 'Welcome back'}
  </h2>

  <div class="w-[400px] bg-stone-700 rounded-2xl p-8 flex flex-col gap-4">
    {#if error}
      <p class="text-red-400 text-sm">{error}</p>
    {/if}

    {#if isRegistering}
      <input
        bind:value={name}
        type="text"
        placeholder="Full name"
        class="bg-stone-600 text-orange-100 placeholder-stone-400 rounded-lg px-4 py-2.5 outline-none text-sm"
      />
    {/if}

    <input
      bind:value={email}
      type="email"
      placeholder="Email"
      class="bg-stone-600 text-orange-100 placeholder-stone-400 rounded-lg px-4 py-2.5 outline-none text-sm"
    />
    <input
      bind:value={password}
      type="password"
      placeholder="Password"
      class="bg-stone-600 text-orange-100 placeholder-stone-400 rounded-lg px-4 py-2.5 outline-none text-sm"
    />

    {#if isRegistering}
      <button
        onclick={handleRegister}
        disabled={loading}
        class="bg-green-600 hover:bg-green-500  disabled:opacity-40 text-white rounded-lg py-2.5 text-sm transition-colors"
      >
        Create account
      </button>
      <button onclick={() => isRegistering = false} class="text-stone-400 text-sm hover:text-stone-300">
        Already have an account? Sign in
      </button>
    {:else}
      <button
        onclick={handleLogin}
        disabled={loading}
        class="bg-green-600 hover:bg-green-500 disabled:opacity-40 text-white rounded-lg py-2.5 text-sm transition-colors"
      >
        Sign in
      </button>
      <button onclick={() => isRegistering = true} class="text-stone-400 text-sm hover:text-stone-300">
        Don't have an account? Register
      </button>
    {/if}

    <div class="flex items-center gap-3">
      <div class="flex-1 h-px bg-stone-500"></div>
      <span class="text-stone-400 text-xs">or</span>
      <div class="flex-1 h-px bg-stone-500"></div>
    </div>

    <button
      onclick={handleGoogle}
      class="flex items-center justify-center gap-3 bg-stone-600 hover:bg-stone-500 text-stone-100 rounded-lg py-2.5 text-sm transition-colors"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24">
        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
      </svg>
      Continue with Google
    </button>
  </div>
</div>