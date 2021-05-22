<template>
  <div>
    <span>Choose dataset:</span>
    <select v-model="$store.state.selected" @click="$store.dispatch('fetchInstructions', $store.state.selected)">
      <option
        v-for="selection in $store.getters.availableDatasets"
        :key="selection.key"
        @click="logStuff"
      >
        {{ selection }}
      </option>
    </select>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  beforeMount() {
    let store = useStore();
    store.dispatch("fetchAvailableDatasets");
  },
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