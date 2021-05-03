<template>
    <div>
        <p>Stuff</p>
        <p>{{ flerp }}</p>
        <img :src="$store.state.currentDiagram" />

    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import store from "vuex";
@Options({
  computed:{
    flerp(){
      return this.$store.state.helloMessage;
    }
  }
})
export default class GuideComponent extends Vue {
}
</script>