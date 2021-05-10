import { createStore } from 'vuex'

export default createStore({
  state: {
    selectionOptions: {
      sdgBasic: ["min", "max"],
      sdgLinearRegression: ["gender"],
    },
    selected: "sdgBasic",
    inputValues: []
  },
  mutations: {
    SET_SELECTED_DIAGRAM(state, selectedName) {
      state.selected = selectedName;
    },
    SET_INPUT_VALUES(state, inputValues) {
      state.inputValues = inputValues;
    }
  },
  getters: {
    getSelectedFromOptions: state => Object(state.selectionOptions)[state.selected]
  },
  actions: {
    setSelectedDiagram(context, selectedName) {
      context.commit("SET_SELECTED_DIAGRAM", selectedName);
    },
    setInputValues(context, inputValues) {
      context.commit("SET_INPUT_VALUES", inputValues);
    }
  },
  modules: {
  }
})