<script lang="ts">
  let { size = 28 } = $props();
</script>

<svg
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
>
  <!-- Leaf shape -->
  <path
    d="M12 22C12 22 4 16 4 9C4 5 7.5 2 12 2C16.5 2 20 5 20 9C20 16 12 22 12 22Z"
    stroke="#4ade80"
    stroke-width="1.5"
    stroke-linecap="round"
    stroke-linejoin="round"
  />
  <!-- Center vein -->
  <path
    d="M12 22V8"
    stroke="#4ade80"
    stroke-width="1.5"
    stroke-linecap="round"
  />
</svg>
