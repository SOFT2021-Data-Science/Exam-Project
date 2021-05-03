import Vue from 'vue';
import { createStore } from 'vuex'
import { RootState } from '@/store/types';
 
export default createStore({
  state: {
    helloMessage: 'hello',
    currentDiagram: require("@/../../../resources/logo.png")
  },
  mutations: {
    SET_DIAGRAM(state, imgName) {
      let resourcesDirectory = "../../../../resources"
      if (process.env.VUE_APP_RESOURCES_DIRECTORY != null || process.env.VUE_APP_RESOURCES_DIRECTORY != "") {
        resourcesDirectory = process.env.VUE_APP_RESOURCES_DIRECTORY;
      }
      state.currentDiagram = resourcesDirectory + "/" + imgName;
    }
  },
  actions: {
    setDiagramFromResources(context, imgName){
      context.commit('SET_DIAGRAM', imgName);
    }
  },
  modules: {
  }
})