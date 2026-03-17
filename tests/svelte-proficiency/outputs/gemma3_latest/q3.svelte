<script>
	import { onMount } from 'svelte';

	let runes = [];
	let runeSet = "ᛏᛦᛚᛞᛟᛔᛝᛟᛙᛟᛜᛎᛣᛖᛍ"; // A sample rune set
	let runeLength = runeSet.length;
	let currentIndex = 0;
	let runeDisplay = "";

	onMount(() => {
		// Initialize with the first rune
		runeDisplay = runeSet[currentIndex];
	});

	function nextRune() {
		currentIndex = (currentIndex + 1) % runeLength;
		runeDisplay = runeSet[currentIndex];
	}
</script>

<style>
	.rune-container {
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 3em;
		margin: 20px;
	}

	.rune-display {
		font-size: 3em;
		font-family: 'Noto Sans Devanagari', sans-serif; /* Or another suitable font */
		color: #333;
		/* Add more styling as desired */
	}
</style>

<div class="rune-container">
	<div class="rune-display">{runeDisplay}</div>
</div>

<button on:click={nextRune}>Next Rune</button>

<p>Current Rune: {runeSet[currentIndex]}</p>