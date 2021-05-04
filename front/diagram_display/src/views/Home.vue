<template>
  <div>
    <p>Graph stuff goes here</p>
    <DiagramAlt />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
// import HelloWorld from '@/components/HelloWorld.vue' // @ is an alias to /src
import DiagramAlt from "@/components/DiagramAlt.vue";

@Options({
  components: {
    DiagramAlt,
  },
})
export default class Home extends Vue {}
</script>
