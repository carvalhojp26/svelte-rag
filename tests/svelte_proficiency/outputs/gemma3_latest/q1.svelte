<script>
  let count = 0;

  function increment() {
    count += 1;
  }

  function decrement() {
    count -= 1;
  }
</script>

<h1>Counter</h1>

<p>Count: {count}</p>

<button on:click={increment}>Increment</button>
<button on:click={decrement}>Decrement</button>

<style>
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }

  p {
    font-size: 1.5rem;
    margin: 0;
  }

  button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-right: 10px;
  }

  button:hover {
    background-color: #3e8e41;
  }
</style>