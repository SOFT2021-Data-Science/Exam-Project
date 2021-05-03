<template>
    <div>
        <p>Stuff</p>
        <p>{{ flerp }}</p>
        <img :src="getCurrentDiagram('logo.png')" />
        <img src="@/assets/logo.png" />
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
  },
  methods:{
    getCurrentDiagram(img: string){
      console.log(process.env.VUE_APP_RESOURCES_DIRECTORY);
      let imgPath: string = process.env.VUE_APP_RESOURCES_DIRECTORY+img
      console.log(imgPath);
      
      return require(imgPath)
    }
  }
})
export default class GuideComponent extends Vue {
}
</script>

<style lang="scss">

</style>