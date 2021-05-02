<template>
  <div>
    <p>Graph stuff goes here</p>
    <Diagram />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
// import HelloWorld from '@/components/HelloWorld.vue' // @ is an alias to /src
import Diagram from "@/components/Diagram.vue";

@Options({
  components: {
    Diagram,
  },
})
export default class Home extends Vue {}
</script>
