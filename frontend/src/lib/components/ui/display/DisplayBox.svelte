<script lang="ts">
  export let className: string = "";
  export let content: string = "";

  export { className as class };
</script>

<div class={className}>
  <p>{content}</p>
</div>

<style>
  div {
    border: 1px solid;
    border-radius: 5px;
    font-size: 18px;
    padding: 15px;
    width: 200px;
    height: 100px;
  }

  p {
    margin: 0;
    text-align: center;
  }
</style>
