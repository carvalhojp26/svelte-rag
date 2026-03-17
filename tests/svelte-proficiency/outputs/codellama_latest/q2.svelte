<html>
  <head>
    <title>My App</title>
  </head>
  <body>
    <header>
      <!-- Header content -->
    </header>
    <main>
      {#each routes as route}
        <Route {...route} />
      {/each}
    </main>
    <footer>
      <!-- Footer content -->
    </footer>
  </body>
</html>