<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="/app.css" />
</svelte:head>

<div class="w-full h-full bg-orange-50">
	{@render children()}
</div>
