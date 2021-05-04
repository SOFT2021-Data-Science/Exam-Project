import Vue from 'vue';
import { createStore } from 'vuex'
import { RootState } from '@/store/types';
 
export default createStore({
  state: {
    helloMessage: 'hello',
    currentDiagram: "",
    // Placeholder. Must be made dynamic.
    inputFields: [null, null, null, null],
    currentInputIterationId: 0
  },
  mutations: {
    SET_DIAGRAM(state, imgName) {
      let resourcesDirectory = "../../../../resources"
      if (process.env.VUE_APP_RESOURCES_DIRECTORY != null || process.env.VUE_APP_RESOURCES_DIRECTORY != "") {
        resourcesDirectory = process.env.VUE_APP_RESOURCES_DIRECTORY;
      }
      state.currentDiagram = resourcesDirectory + "/" + imgName;
    },
  },
  getters: {
    getCurrentInputIterationId: state => state.currentInputIterationId
  },
  actions: {
    setDiagramFromResources(context, imgName){
      context.commit('SET_DIAGRAM', imgName);
    }
  },
  modules: {
  }
})