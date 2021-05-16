<template>
  <div>
    <div
      v-for="(selection, index) in Object.entries(
        $store.getters.getSelectedFromOptions
      )"
      :key="selection[0]"
    >
      <label :for="selection[0]">{{ selection[1] }}</label>
      <input :id="selection[0]" v-model="$store.state.inputValues[index]" />
    </div>
    <button @click="loadPreviewGraph($event)">Load resource</button>
    <button @click="$store.dispatch('fetchInstructions')">asdf</button>
    {{ $store.state.inputValues }}
    {{ $store.state.instructions }}
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  setup() {
    let store = useStore();

    const loadExternalGraph = async () => {
      let url_string: string = process.env.VUE_APP_BACKEND + "/basic/2012&2017";
      try {
        let data = await axios
          .get(url_string)
          .then((res) => res)
          .then((data) => data.data);
        console.log(data);

        window.location.href = url_string;
      } catch (error) {
        console.log(error);
      }
    };

    const loadDataset = async () => {
      let url: string = process.env.VUE_APP_BACKEND + "/instructions/sdg";
      try {
        let data = await axios
          .get(url)
          .then((res) => res)
          .then((data) => data.data);
        console.log(data);
      } catch (error) {
        console.log(error);
      }
    };

    const loadPreviewGraph = () => {
      let url_string: string =
        process.env.VUE_APP_BACKEND + "/" + store.state.selected + "/preview/";

      let options = store.getters.getSelectedFromOptions;
      console.log(options);

      for (const [key, value] of Object.entries(store.state.inputValues)) {
        if (parseInt(key) != 0) {
          url_string += "&";
        }
        url_string += options[key] + "=" + value;
      }
      console.log(url_string);
    };
    return {
      loadExternalGraph,
      loadPreviewGraph,
      loadDataset,
    };
  },
});
</script>

<style lang="scss">
</style>