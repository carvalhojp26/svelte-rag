<script lang="ts">
    import WelcomeScreen from './components/WelcomeScreen.svelte';
    import ChatScreen from './components/ChatScreen.svelte';
  
    let started = $state(false);
    let firstMessage = $state('');
  
    function handleStart(content: string) {
      firstMessage = content;
      started = true;
    }
  </script>
  
  {#if !started}
    <WelcomeScreen onstart={handleStart} />
  {:else}
    <ChatScreen {firstMessage} />
  {/if}