<template>
    <div>
        <p>Stuff</p>
        <img :src="$store.state.currentDiagram" />
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";



@Options({
})


export default class GuideComponent extends Vue {

}
</script>
