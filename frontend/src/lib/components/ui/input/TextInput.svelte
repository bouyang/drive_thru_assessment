<script lang="ts">
	export let value: string = "";
	export let type: "text" = "text";
  export let placeholder: string = "Drive thru message:";

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
  }
</script>

<input
  type={type}
  placeholder={placeholder}
  bind:value
  on:input={handleInput}
  class="message-input"
/>

<style>
  .message-input {
    width: 90%;
    height: 100px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid;
    border-radius: 5px;
  }
</style>
