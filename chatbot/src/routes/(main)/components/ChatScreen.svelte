<script lang="ts">
    import ChatWindow from './ChatWindow.svelte';
    import ChatInput from './ChatInput.svelte';
    import Logo from './Logo.svelte';
    import { createAuthClient } from 'better-auth/svelte';
    import { onMount } from 'svelte';
  
    const { signOut } = createAuthClient();
    let { firstMessage = '' }: { firstMessage?: string } = $props();
  
    type Message = { role: 'user' | 'assistant'; content: string };
    let messages: Message[] = $state([]);
    let loading = $state(false);
    let scrollContainer: HTMLElement;
  
    $effect(() => {
      messages; loading;
      scrollContainer?.scrollTo({ top: scrollContainer.scrollHeight, behavior: 'smooth' });
    });
  
    onMount(() => {
      if (firstMessage) handleSubmit(firstMessage);
    });
  
    async function handleLogout() {
      await signOut({ fetchOptions: { onSuccess: () => window.location.href = '/login' } });
    }
  
    async function handleSubmit(content: string) {
      messages = [...messages, { role: 'user', content }];
      loading = true;
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: content }),
        });
        const data = await res.json();
        messages = [...messages, { role: 'assistant', content: data.answer ?? data.error }];
      } catch (e) {
        console.error('fetch error:', e);
        messages = [...messages, { role: 'assistant', content: 'Something went wrong.' }];
      } finally {
        loading = false;
      }
    }
  </script>
  
  <div class="relative flex flex-col items-center h-screen py-8 gap-4">
    <div class="absolute top-6 left-6">
      <Logo size={28} />
    </div>
  
    <div class="absolute top-6 right-6">
      <button onclick={handleLogout} class="text-stone-400 hover:text-green-400 text-sm transition-colors">
        Sign out
      </button>
    </div>
  
    <div
      bind:this={scrollContainer}
      class="flex-1 min-h-0 w-[660px] overflow-y-auto overflow-x-hidden scrollbar-hide"
    >
      <ChatWindow {messages} {loading} />
    </div>
    <ChatInput disabled={loading} onsubmit={handleSubmit} />
  </div>