<template>
  <div class="guide">
    <h1>Guide page</h1>
    <p>Guide page</p>
  </div>
</template>

<script lang="ts">
import GuideComponent from '@/components/GuideComponent.vue'
import { Options, Vue } from 'vue-class-component'

@Options({
  components: {
    GuideComponent
  },
  computed: {
    get (): string {
      return this.$store.state.helloMessage
    }
  }
})
export default class Guide extends Vue {}
</script>
