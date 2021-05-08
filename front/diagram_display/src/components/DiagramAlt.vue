<template>
  <div>
    <button @click=load>Load resource</button>
  </div>
</template>

<script lang="ts">
import axios, { AxiosResponse } from "axios";
export default {
  // Static. Not reactive by default.
  setup() {
    const load = async (): Promise<AxiosResponse<any> | undefined> => {
      let url_string: string = process.env.VUE_APP_BACKEND+"/basic/2012&2017"
      //let url_string = "http://127.0.0.1:5000/basic/2012&2017"
      console.log(url_string);
      
      try {
        let data = await axios
          .get(url_string)
          .then((res) => res)
          .then((data) => data);
        return data;
      } catch (error) {
        console.log(error);
      }
    };

    return {load};
  },
};
</script>

<style lang="scss">
</style>