<template v-html=dynamic_html>
  <div>
    <button @click=load()>Load resource</button>
    <button @click=reset()>Reset</button>
    <div v-html=dynamic_html></div>
    
  </div>
</template>

<script lang="ts">
import axios, { AxiosResponse } from "axios";
import { ref } from 'vue';
export default {
  // Static. Not reactive by default.
  setup() {
    const load = async () => {
      let url_string: string = process.env.VUE_APP_BACKEND+"/basic/2012&2017"
      //let url_string = "http://127.0.0.1:5000/basic/2012&2017"
      console.log(url_string);
      try {
        let data = await axios
          .get(url_string)
          .then((res) => res)
          .then((data) => data.data);
        console.log(data);
        
        dynamic_html.value = data
        window.location.href = url_string;
      } catch (error) {
        console.log(error);
      }
    };

    const reset = () => {
      console.log(dynamic_html.value);
      
      dynamic_html.value = "<button>Boop</button>"
    }

    const dynamic_html = ref(`
    <p>Hi from dynamic html</p>
    `)

    return {load, dynamic_html, reset};
  },
};
</script>

<style lang="scss">
</style>