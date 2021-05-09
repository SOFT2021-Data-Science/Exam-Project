<template>
  <div>
    <button @click="toggleDropdown">Toggle</button>
    <label for="dropped-down"></label>
    <select v-model="selected">
      <option disabled value="">Available diagram options:</option>
      <option>sdg - basic</option>
      <option>sdg - Linear Regression</option>
    </select>
    <span>Selected: {{ selected }}</span>
    <div v-if="toggle">
      <p>Toggled</p>
    </div>
    <p>{{ helloMsg }}</p>
    <p>{{ helloMsgProp }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  props: {
    helloMsgProp: String,
  },
  setup() {
    let helloMsg = "Hello from dropdown";
    let toggle = ref(true);
    let selected = ref("");

    let selectionOptions = {
        sdgBasic: ["min","max"],
        sdgLinearRegression: ["gender"]
    };

    // let sdgBasicOptions = ["min", "max"];
    // let sdgLinearRegression = ["gender"];

    const toggleDropdown = () => {
      console.log(toggle);

      toggle.value = !toggle.value;
    };

    return { helloMsg, toggleDropdown, toggle, selected };
  },
});
</script>

<style scoped>
</style>