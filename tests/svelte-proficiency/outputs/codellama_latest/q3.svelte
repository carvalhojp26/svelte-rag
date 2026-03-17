<script>
  import { onMount } from 'runes';

  function MyComponent() {
    return (
      <div>Hello World!</div>
    );
  }

  onMount(() => {
    console.log('MyComponent mounted');
  });

  export default MyComponent;
</script>