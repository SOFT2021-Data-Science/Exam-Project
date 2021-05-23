<template>
  <div>
    <div v-if="$store.state.instructions">
      <p>Data link: {{ $store.state.instructions.dataset_link }}</p>
      <p>Description: {{ $store.state.instructions.description }}</p>
      <span>Choose model: </span>
      <select v-model="$store.state.selectedModel" @click="setModel">
        <option
          v-for="selection in Object.entries($store.state.instructions.models)"
          :key="selection.key"
          :value="selection[1]"
        >
          {{ selection[0] }}
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
import axios from "axios";
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";
import {Map} from "@/store/index";


export default defineComponent({
  beforeMount() {
    let store = useStore();
    store.dispatch("fetchAvailableDatasets");
  },
  setup() {
    let store = useStore();
    let tempInputValue = ref("");

    const setModel = () => {
      console.log(Object.entries(store.state.selectedModel));
      
      store.dispatch("setSelectedModel", store.state.selectedModel);
      store.dispatch("resetURLParams");
      let entries: any = Object.entries(store.state.selectedModel);
      let values: any = Object.values(entries[0]);
      values = Object.values(values);
      values = Object.values(values[1]);
      let URLParams = new Map();

      for (const entry in entries[0][1]) {
        URLParams[entry] = entries[0][1][entry].values[0];
      }
      store.dispatch("setURLParamsInitialValues", URLParams);
    };

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
      tempInputValue,
      setModel,
    };
  },
});
</script>

<style lang="scss">
</style>