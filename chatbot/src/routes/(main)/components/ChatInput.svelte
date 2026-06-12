<script lang="ts">
  import { ArrowUp, ChevronDown } from 'lucide-svelte';

  let { disabled = false, onsubmit }: {
    disabled?: boolean;
    onsubmit?: (content: string, mode: string) => void;
  } = $props();

  let value = $state('');
  let mode = $state('RAG');
  let dropdownOpen = $state(false);

  const modes = ['RAG', 'MCP', 'RAG + MCP'];

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleSubmit() {
    if (!value.trim() || disabled) return;
    onsubmit?.(value, mode);
    value = '';
  }

  function selectMode(m: string) {
    mode = m;
    dropdownOpen = false;
  }
</script>

<div class="w-[660px] bg-stone-700 rounded-2xl p-4">
  <textarea
    bind:value
    onkeydown={handleKeydown}
    placeholder="Ask me anything about Svelte..."
    rows="3"
    class="w-full bg-transparent outline-none resize-none text-orange-100 placeholder-stone-400 text-sm"
  ></textarea>

  <div class="flex items-center justify-end mt-2 gap-2">
    <!-- Mode dropdown -->
    <div class="relative">
      <button
        onclick={() => dropdownOpen = !dropdownOpen}
        class="flex items-center gap-1 text-stone-400 hover:text-green-400 text-sm transition-colors"
      >
        {mode}
        <ChevronDown size={14} />
      </button>

      {#if dropdownOpen}
        <div class="absolute bottom-8 right-0 min-w-[140px] bg-stone-800 border border-stone-600 rounded-xl overflow-hidden shadow-lg z-10">
          {#each modes as m}
            <button
              onclick={() => selectMode(m)}
              class="block w-full text-left px-4 py-2.5 text-sm transition-colors
                {mode === m ? 'text-green-400 bg-stone-700' : 'text-stone-300 hover:bg-stone-700 hover:text-green-400'}"
            >
              {m}
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <button
      onclick={handleSubmit}
      disabled={!value.trim() || disabled}
      class="bg-green-600 hover:bg-green-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-lg p-1.5 transition-colors"
    >
      <ArrowUp size={18} />
    </button>
  </div>
</div>