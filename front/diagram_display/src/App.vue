<template>
  <div>
    <Header />
  </div>
</template>

<style>
</style>

<script lang="ts">
import Header from '@/components/layout/Header.vue'
import { Options, Vue } from 'vue-class-component'

@Options({
  components: {
    Header
  }
})
export default class Guide extends Vue {}
</script>
