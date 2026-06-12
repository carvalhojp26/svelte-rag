<script lang="ts">
  import ChatInput from './ChatInput.svelte';
  import Logo from './Logo.svelte';
  import { createAuthClient } from 'better-auth/svelte';

  const { signOut } = createAuthClient();
  let { onstart }: { onstart?: (content: string) => void } = $props();

  async function handleLogout() {
    await signOut({ fetchOptions: { onSuccess: () => window.location.href = '/login' } });
  }
</script>

<div class="relative flex flex-col items-center justify-center h-screen space-y-6">
  <div class="absolute top-6 left-6">
    <Logo size={28} />
  </div>

  <div class="absolute top-6 right-6">
    <button onclick={handleLogout} class="text-stone-400 hover:text-green-400 text-sm transition-colors">
      Sign out
    </button>
  </div>

  <h2 class="text-4xl font-normal tracking-tight" style="font-family: 'Lora', Georgia, serif; color: #c8c3bc;">
    How can I help you today?
  </h2>
  <ChatInput onsubmit={(content) => onstart?.(content)} />
</div>