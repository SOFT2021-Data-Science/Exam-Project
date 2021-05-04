<template>
  <div>
    <p>hi</p>
  </div>
</template>

<script lang="ts">
import axios from "axios";
export default {
  // Static. Not reactive by default.
  setup() {

    const load = async () => {
      try {
        let data = await axios.get("${process.env.VUE_APP_RESOURCES_DIRECTORY}/basic/2012&2017")
      } catch (error) {

      }
    };

    return {};
  },
};
</script>

<style lang="scss">
</style>