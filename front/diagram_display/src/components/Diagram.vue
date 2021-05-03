<template>
    <div>
        <p>Stuff</p>
        <p>{{ flerp }}</p>
        <img :src="getCurrentDiagram('logo.png')" />
        <img src="@/assets/logo.png" />
        <img :src="stuff" alt="">
        <img src=@/../../../resources/logo.png>
        <img :src="$store.state.currentDiagram">
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import store from "vuex";


@Options({
  computed:{
    flerp(){
      return this.$store.state.helloMessage;
    },
    stuff(){
      return require("@/../../../resources/logo.png");
    }
  },
  methods:{
    getCurrentDiagram(img: string){
      //return require("./assets/logo.png")
      
      return require("@/../../../resources/"+img)
      //return this.$store.state.currentDiagram;
    }
  }
})
export default class GuideComponent extends Vue {
}
</script>

<style lang="scss">

</style>