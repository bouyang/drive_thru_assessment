<script lang="ts">
  interface OrderItems {
    burgers: number;
    fries: number;
    drinks: number;
  }

  interface Order {
    id: number;
    items: OrderItems;
  }

  let orderInput = "";
  let burgersText = "";
  let friesText = "";
  let drinksText = "";

  let orders: Order[] = [];
  let isLoading = false;
  let error: string | null = null;

  const API_BASE_URL = "http://localhost:8000";

  onMount(async() => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/items`);
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      orders = await response.json();
      isLoading = false;
      updateDisplayBox(orders);
    } catch (err) {
      if (err instanceof Error) {
        console.error("Error:", err.message);
      } else {
        console.error("Unknown error occurred", err);
      }
      isLoading = false;
    }
  })

  import Button from "$lib/components/ui/button/button.svelte";
  import TextInput from "$lib/components/ui/input/TextInput.svelte";
  import DisplayBox from "$lib/components/ui/display/DisplayBox.svelte";
  import OrderBox from "$lib/components/ui/display/OrderBox.svelte";
  import { onMount } from "svelte";

  const handleClick = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: orderInput })
    });

    if (!response.ok) {
      throw new Error("Failed to submit data");
    }

    const data = await response.json();

    if (data?.message === "Order deleted") {
      handleDeleteOrder(data.order.id);
    } else if (data?.order) {
      handleAddOrder(data.order);
    }

    orderInput = "";
  } catch (err) {
    if (err instanceof Error) {
      console.error("Error:", err);
    } else {
      console.error("Unknown error occurred");
    }
  }
};

function handleDeleteOrder(orderId: number) {
  orders = orders.filter(order => order.id !== orderId);
  console.log("Order deleted:", orderId);
  updateDisplayBox(orders);
}

function handleAddOrder(newOrder: Order) {
  orders = [...orders, newOrder];
  console.log("Order added:", newOrder);
  updateDisplayBox(orders);
}

function updateDisplayBox(orders: Order[]) {
  let totalBurgers = 0;
  let totalFries = 0;
  let totalDrinks = 0;

  orders.forEach(order => {
    totalBurgers += order.items.burgers || 0;
    totalFries += order.items.fries || 0;
    totalDrinks += order.items.drinks || 0;
  });

  burgersText = `Burgers: ${totalBurgers}`;
  friesText = `Fries: ${totalFries}`;
  drinksText = `Drinks: ${totalDrinks}`;
}

</script>

<style>
  .display-section {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
  }

  .input-section {
    margin-bottom: 2rem;
  }

  .order-section {
    margin-top: 2rem;
  }

  h1 {
    margin-bottom: 1rem;
  }
</style>

<div class="display-section">
  <DisplayBox content={burgersText}/>
  <DisplayBox content={friesText}/>
  <DisplayBox content={drinksText}/>
</div>

<div class="input-section">
  <TextInput bind:value={orderInput} placeholder="Drive thru message:" />
  <Button on:click={handleClick}>Run</Button>
</div>

<div class="order-section">
  <h1>Order history</h1>
  {#if isLoading}
    <p>Loading</p>
  {:else if error}
    <p>Error: {error}</p>
  {:else}
    {#each orders as order}
      <OrderBox {order} />
    {/each}
  {/if}
</div>