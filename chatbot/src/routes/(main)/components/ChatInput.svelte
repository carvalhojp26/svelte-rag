<script lang="ts">
    import { ArrowUp } from 'lucide-svelte';
  
    let value = '';
  
    function handleKeydown(e: KeyboardEvent) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
    }
  
    function handleSubmit() {
      if (!value.trim()) return;
      console.log('Submitted:', value);
      value = '';
    }
  </script>
  
  <div class="w-[660px] bg-stone-700 rounded-2xl p-4">
    <textarea
      bind:value
      on:keydown={handleKeydown}
      placeholder="Ask me anything about Svelte..."
      rows="3"
      class="w-full bg-transparent outline-none resize-none text-orange-100 placeholder-stone-400 text-sm"
    />
  
    <div class="flex items-center justify-end mt-2 gap-2">
      <span class="text-stone-400 text-sm">RAG</span>
  
      <button
        on:click={handleSubmit}
        disabled={!value.trim()}
        class="bg-orange-500 hover:bg-orange-400 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-lg p-1.5 transition-colors"
      >
        <ArrowUp size={18} />
      </button>
    </div>
  </div>