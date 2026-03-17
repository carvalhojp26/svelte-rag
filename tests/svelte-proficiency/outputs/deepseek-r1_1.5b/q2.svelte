import { 
  svelte, 
  export,
} from 'svelte'

<app>

{svelte:template}

<div>
  <div svelte:component name="home">
    <h1>Home</h1>
    <p>This is the home section.</p>
  </div>

  <div svelte:component name="about">
    <h2>About</h2>
    <p>This is the about section.</p>
  </div>
</div>

{svelte:template}