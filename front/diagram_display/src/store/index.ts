import { createStore } from 'vuex'
import axios from "axios";

export default createStore({
  state: {
    instructions: null,
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
    },
    SET_INSTRUCTIONS(state, instructions){
      state.instructions = instructions
    }
  },
  getters: {
    getSelectedFromOptions: state => Object(state.selectionOptions)[state.selected],
    instructions: state => state.instructions
  },
  actions: {
    setSelectedDiagram(context, selectedName) {
      context.commit("SET_SELECTED_DIAGRAM", selectedName);
    },
    setInputValues(context, inputValues) {
      context.commit("SET_INPUT_VALUES", inputValues);
    },
    async fetchInstructions(context){
      const url: string = process.env.VUE_APP_BACKEND + "/instructions/sdg";
      let instruction = null
      try {
        instruction = await axios
          .get(url)
          .then((res) => res)
          .then((instruction) => instruction.data);
        console.log(instruction);
      } catch (error) {
        instruction = error
        console.log(error);
      }
      context.commit("SET_INSTRUCTIONS", instruction)
    }
  },
  modules: {
  }
})