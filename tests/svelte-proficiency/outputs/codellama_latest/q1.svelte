<script>
	let count = 0;

	function increment() {
		count++;
	}

	function decrement() {
		count--;
	}
</script>

<div>
	<button on:click={increment}>Increment</button>
	<p>{count}</p>
	<button on:click={decrement}>Decrement</button>
</div>