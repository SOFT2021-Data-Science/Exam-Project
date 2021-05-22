<template>
  <div>
    <div v-if="$store.state.instructions">
      <p>Data link: {{ $store.state.instructions.dataset_link }}</p>
      <p>Description: {{ $store.state.instructions.description }}</p>
      <span>Choose model: </span>
      <select
        v-model="$store.state.selectedModel"
        @click="$store.dispatch('setSelectedModel', $store.state.selectedModel)"
      >
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
      <button @click="$store.dispatch('setImgTagValue')">
        Display image
      </button>
      <div v-if="$store.getters.imgTagValue">
        <img :src="$store.getters.imgTagValue" alt="">
      </div>
    </div>
    <button @click="boop">
      asd
    </button>
    {{ $store.state.URLParams }}
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  beforeMount() {
    let store = useStore();
    store.dispatch("fetchAvailableDatasets");
  },
  setup() {
    let tempInputValue = ref("");

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

    const boop = () => {
      for (const keyval in store.state.URLParams){
        console.log(keyval + ":" +store.state.URLParams[keyval]);
      }
    }

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
      boop
    };
  },
});
</script>

<style lang="scss">
</style>