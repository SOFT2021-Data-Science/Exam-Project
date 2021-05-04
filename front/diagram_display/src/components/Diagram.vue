<template>
<div>
  {{inputId}}
    <img src="@/assets/logo.png" />
    <img :src="$store.state.currentDiagram" />
    <div v-for="n in $store.state.inputFields.length" :key="n">
        <input type="text" id="paramInput" />
    </div>
    <button @click="populateInputFields">Submit</button>
</div>
</template>

<script lang="ts">
import {
    Options,
    Vue
} from "vue-class-component";
import store from "vuex";


@Options({
    computed: {
        flerp() {
            return this.$store.state.helloMessage;
        },
    },
    methods: {
        getCurrentDiagram(img: string) {
            console.log(process.env.VUE_APP_RESOURCES_DIRECTORY);
            let imgPath: string = process.env.VUE_APP_RESOURCES_DIRECTORY + img
            console.log(imgPath);
            //return require("@/assets/logo.png")
            return require(process.env.VUE_APP_RESOURCES_DIRECTORY + img)
        },
        populateInputFields() {
            let num: number = this.$store.state.inputFields.length
            let i: number;
            

            for (i = 0; i <= num - 1; i++) {
                console.log(this.$store.state.inputFields[i]);
            }
        }
    },
})
export default class GuideComponent extends Vue {
  get inputId(): number {
    return 2
  }
  set inputId(num: number){
    this.inputId = num
  }
}
</script>

<style lang="scss">
</style>
