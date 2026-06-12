<script lang="ts">
    import { marked } from 'marked';
  
    let { message }: { message: { role: 'user' | 'assistant'; content: string } } = $props();
  
    const rendered = $derived(
      message.role === 'assistant' ? marked(message.content) : message.content
    );
  </script>
  
  {#if message.role === 'user'}
    <div class="flex justify-end">
      <div class="bg-stone-600 text-orange-100 rounded-2xl rounded-br-sm px-4 py-2.5 max-w-[75%] text-sm">
        {message.content}
      </div>
    </div>
  {:else}
    <div class="flex justify-start gap-3 items-start">
      <div class="text-green-400 mt-1 text-lg">✳</div>
      <div class="prose prose-invert prose-sm max-w-[75%] text-stone-200 leading-relaxed">
        {@html rendered}
      </div>
    </div>
  {/if}