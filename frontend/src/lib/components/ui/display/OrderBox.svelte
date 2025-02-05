<script lang="ts">
  interface OrderItems {
    burgers: number;
    fries: number;
    drinks: number;
  }

  export let order: { id: number, items: OrderItems };

  function formatItems(items: OrderItems): string {
    const formattedItems = [];
    for (let key in items) {
      if (items[key as keyof OrderItems] > 0) {
        formattedItems.push(`${items[key as keyof OrderItems]} ${key}`);
      }
    }
    return formattedItems.join(', ');
  }
</script>

<div class="order-box">
  <span>Order #{order.id}</span>
  <span>{formatItems(order.items)}</span>
</div>

<style>
  .order-box {
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: 1px solid;
    border-radius: 5px;
  }

  .order-box span {
    display: inline-block;
    margin-right: 1rem;
  }
</style>