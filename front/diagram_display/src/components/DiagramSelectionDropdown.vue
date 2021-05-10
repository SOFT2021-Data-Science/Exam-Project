<template>
  <div>
    <button @click="toggleDropdown">Toggle</button>
    <select v-model="$store.state.selected" @click="resetInputValues" >
      <option
        v-for="selection in Object.entries($store.state.selectionOptions)"
        :key="selection.key"
        @click="resetInputValues"
      >
        {{ selection[0] }}
      </option>
    </select>
    <span
      >Selected: {{ $store.state.selected }}
      {{ $store.getters.getSelectedFromOptions }}</span
    >
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  setup() {
    let store = useStore();
    const resetInputValues = () => {
      store.dispatch("setInputValues", []);
    };
    return {
      resetInputValues,
    };
  },
});
</script>

<style scoped>
</style>