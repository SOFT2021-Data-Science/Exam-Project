<template>
  <div class="guide">
    <h1>Guide page</h1>
    <div id="text-container">
      <p>This guide is intended to show you how to operate the site and how to select a machine learning algorithm for a specific dataset.</p>
      <p>To get started, first of you have to navigate to the <a href="#/">home</a> page, where you'll see a <b>dropdown field</b> and a <b>toggle</b> button.</p>
      <p>In the dropdown field, select the desired dataset, followed by one of the listed machine learning algorithms.</p>
      <div class="ex">
        <p>In this example we want to use the <b>Linear Regression</b> model on the <b>kaggle</b> dataset to generate a graph showing the growth or decrease in suicide rates for all males in Denmark between the datasets timeframe.</p>
        <ol>
          <li>Select <b>kaggle linear regression</b> from the dropdown menu.</li>
          <li>You should now see two fields: <b>region</b> and <b>gender</b>, where we'll pick <b>Denmark</b> and <b>Male</b> as our input values.</li>
          <li>There are two options for displaying the images</li>
          <li>The <b>Display image</b> button displays the image on the site</li>
          <li>The <b>Reroute to template</b> button reroutes to a service with some simple tools for managing the image</li>
          <li><span style="color:red">Please be aware, that even if the input fields reset visually, then the internal values still change.
            <br>A dictionary has been placed in the bottom to signify the current set values for diagram creation.
            <br>This is a known bug.
            </span></li>
        </ol>
      </div>
    </div>
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
