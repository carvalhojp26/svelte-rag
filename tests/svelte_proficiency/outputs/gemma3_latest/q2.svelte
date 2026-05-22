<script>
  // You can define global variables here for your layout
  // For example, a dark mode toggle
  let darkMode = false;
</script>

<svelte:head>
  <title>My Svelte Layout</title>
  <meta name="description" content="A basic Svelte 5 layout example">
</svelte:head>

<div class="layout">
  <header class="layout-header">
    <h1>My App</h1>
    <button on:click={() => darkMode = !darkMode}>Toggle Dark Mode</button>
  </header>

  <aside class="layout-aside">
    <h2>Sidebar</h2>
    <ul>
      <li><a href="#">Link 1</a></li>
      <li><a href="#">Link 2</a></li>
      <li><a href="#">Link 3</a></li>
    </ul>
  </aside>

  <main class="layout-main">
    <p>This is the main content area of your layout.</p>
    <h2>Main Content</h2>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
  </main>

  <footer class="layout-footer">
    <p>&copy; 2023 My App</p>
  </footer>
</div>

<style>
  .layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh; /* Ensure the layout takes up the full viewport height */
  }

  .layout-header,
  .layout-footer {
    background-color: #333;
    color: white;
    padding: 1em;
    text-align: center;
  }

  .layout-aside {
    background-color: #f0f0f0;
    padding: 1em;
    border-right: 1px solid #ccc;
  }

  .layout-main {
    padding: 1em;
  }

  /* Dark Mode Styles (Apply if darkMode is true) */
  :global([data-theme="dark"]) {
    body {
      background-color: #222;
      color: #eee;
    }
    .layout-header,
    .layout-footer {
      background-color: #444;
    }
  }
</style>