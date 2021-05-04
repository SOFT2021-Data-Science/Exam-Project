<template>
    <div>
        <p>Stuff</p>
        <p>{{ flerp }}</p>
        <img src="@/assets/logo.png" />
        <img :src="$store.state.currentDiagram">
        <div v-for="n in $store.state.inputFields.length" :key=n>
          <input type="text" id=paramInput{{n}}>
        </div>
        <button>Submit</button>
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
      //return require("@/assets/logo.png")
      return require(process.env.VUE_APP_RESOURCES_DIRECTORY+img)
    }
  }
})
export default class GuideComponent extends Vue {
}
</script>

<style lang="scss">

</style>