<template>
  <div>
    <div v-if="$store.state.instructions">
      <p>Data link: {{ $store.state.instructions.dataset_link }}</p>
      <p>Description: {{ $store.state.instructions.description }}</p>
      <span>Choose model: </span>
      <select v-model="$store.state.selectedModel" @click="setModel">
        <option
          v-for="selection in Object.values($store.state.instructions)[0]"
          :key="selection.key"
          :value="selection"
        >
          {{ selection.name }}
        </option>
      </select>
    </div>
    <div v-if="$store.state.selectedModel">
      <div
        v-for="selection in Object.entries($store.state.selectedModel.params)"
        :key="selection[1]"
      >
        <br />
        <br />
        <br />
        {{ selection[0] }}:

        <div v-if="(selection.input_type = 'enum')">
          <select
            v-model="tempInputValue"
            @click="
              $store.dispatch('appendToURLParams', [
                selection[0],
                tempInputValue,
              ])
            "
          >
            <option
              v-for="value in Object.values(selection[1])[0]"
              :key="value"
              :value="value"
            >
              {{ value }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div v-if="$store.state.selectedModel">
      <button @click="$store.dispatch('rerouteToTemplate')">
        Reroute to template
      </button>
    </div>
    <div v-if="$store.state.selectedModel">
      <button @click="$store.dispatch('setImgTagValue')">Display image</button>
      <div v-if="$store.getters.imgTagValue">
        <img :src="$store.getters.imgTagValue" alt="" />
      </div>
    </div>
    {{ $store.state.URLParams }}
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";
import { Map } from "@/store/index";

export default defineComponent({
  beforeMount() {
    let store = useStore();
    store.dispatch("fetchAvailableDatasets");
  },
  setup() {
    let store = useStore();
    let tempInputValue = ref("");

    const setModel = () => {
      console.log("bboop");

      console.log(Object.entries(store.state.selectedModel.params));
      const selected_model_params = store.state.selectedModel.params;
      const selected_model_params_keys = Object.keys(selected_model_params);
      let URLParams = new Map();

      selected_model_params_keys.forEach((key, index) => {
        console.log(key + selected_model_params[key]);
        URLParams[key] = selected_model_params[key].values[0];
      });

      store.dispatch("setSelectedModel", store.state.selectedModel);
      store.dispatch("resetURLParams");
      store.dispatch("setURLParamsInitialValues", URLParams);
    };
    return {
      tempInputValue,
      setModel,
    };
  },
});
</script>

<style lang="scss">
</style>