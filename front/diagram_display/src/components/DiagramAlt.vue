<template>
  <div>
    <p>{{ name }}</p>
    <p> {{ lastName }}</p>
    <input type="text">
    <button @click="someFunction">Click me daddy</button>
    <button @click="anotherFunction">Click me daddy</button>
  </div>
</template>

<script lang="ts">
import { ref } from "vue"
export default {
  // Static. Not reactive by default.
  setup() {
      // Not reactive
    let name = "Bob";

    const someFunction = () => {
      console.log(name);
    };

    // Reactive
    const lastName = ref("Johnson")

    const anotherFunction = () => {
        lastName.value = "John"
    }

    return {
      name,
      someFunction,
      lastName,
      anotherFunction
    };
  },
};
</script>

<style lang="scss">
</style>