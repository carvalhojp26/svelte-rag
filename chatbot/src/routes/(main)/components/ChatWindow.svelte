<script lang="ts">
    import MessageBubble from './MessageBubble.svelte';
  
    let { messages = [], loading = false }: {
      messages: { role: 'user' | 'assistant'; content: string }[];
      loading?: boolean;
    } = $props();
  </script>
  
  <div class="flex flex-col gap-6 w-[660px]">
    {#each messages as message}
      <MessageBubble {message} />
    {/each}
  
    {#if loading}
      <div class="flex justify-start gap-3 items-start">
        <div class="text-orange-400 mt-1 text-lg">✳</div>
        <div class="flex gap-1 mt-2">
          <span class="w-2 h-2 bg-stone-400 rounded-full animate-bounce [animation-delay:0ms]"></span>
          <span class="w-2 h-2 bg-stone-400 rounded-full animate-bounce [animation-delay:150ms]"></span>
          <span class="w-2 h-2 bg-stone-400 rounded-full animate-bounce [animation-delay:300ms]"></span>
        </div>
      </div>
    {/if}
  </div>