<template>
  <div>
    <p>Graph stuff goes here</p>
    <DiagramSelectionDropdown />
    <DiagramAlt />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
// import HelloWorld from '@/components/HelloWorld.vue' // @ is an alias to /src
import DiagramAlt from "@/components/DiagramAlt.vue";
import DiagramSelectionDropdown from "@/components/DiagramSelectionDropdown.vue";

export default defineComponent({
  components: {
    DiagramAlt,
    DiagramSelectionDropdown,
  },
  setup() {
    return {
    };
  },
});
</script>
