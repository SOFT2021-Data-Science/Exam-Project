import { createStore } from 'vuex'
// import { RootState } from '@/store/types';
export default createStore({
  state: {
    helloMessage: 'hello',
    currentDiagram: "https://www.steadygo.digital/wp-content/uploads/2016/09/12.jpg"
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
