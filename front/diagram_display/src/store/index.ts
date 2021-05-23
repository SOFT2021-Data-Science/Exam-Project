import { createStore } from 'vuex'
import axios from "axios";

export class Map<T> {
  [key: string]: T
}

function fetchBase(url: string) {
  let data = null
  try {
    data = axios
      .get(url)
      .then((res) => res)
      .then((data) => data.data);
  } catch (error) {
    data = error
  }
  return data
}

export default createStore({
  state: {
    availableDatasets: [],
    instructions: null,
    selectedDataset: null,
    selectedModel: null,
    selectionOptions: {
      sdgBasic: ["min", "max"],
      sdgLinearRegression: ["gender"],
    },
    selected: null,
    inputValues: {},
    URLParams: new Map(),
    imgTagValue: ""
  },
  mutations: {
    SET_SELECTED_DIAGRAM(state, selectedName) {
      state.selected = selectedName;
    },
    SET_INPUT_VALUES(state, inputValues) {
      state.inputValues = inputValues;
    },
    SET_INSTRUCTIONS(state, instructions) {
      state.instructions = instructions
    },
    SET_AVAILABLE_DATASETS(state, availableDatasets) {
      state.availableDatasets = availableDatasets
    },
    SET_SELECTED_MODEL(state, selectedModel) {
      state.selectedModel = selectedModel
    },
    APPEND_TO_URL_PARAMS(state, params: Array<string>) {
      state.URLParams[params[0]] = params[1]
    },
    SET_IMG_TAG_VALUE(state, value) {
      state.imgTagValue = value
    },
    RESET_URL_PARAMS(state){
      state.URLParams = new Map();
    },
    SET_URL_PARAMS_INITIAL_VALUES(state, URLParams){
      state.URLParams = URLParams
    }
  },
  getters: {
    selected: state => state.selected,
    instructions: state => state.instructions,
    availableDatasets: state => state.availableDatasets,
    selectedModel: state => state.selectedModel,
    imgTagValue: state => state.imgTagValue
  },
  actions: {
    setSelectedDiagram(context, selectedName) {
      context.commit("SET_SELECTED_DIAGRAM", selectedName);
    },
    setSelectedModel(context, selectedModel) {
      context.commit("SET_SELECTED_MODEL", selectedModel);
    },
    setInputValues(context, inputValues) {
      context.commit("SET_INPUT_VALUES", inputValues);
    },
    async fetchInstructions(context) {
      const instruction = await fetchBase(
        process.env.VUE_APP_BACKEND + "/instructions/" + this.state.selected
      )
      context.commit("SET_INSTRUCTIONS", instruction)
    },
    async fetchAvailableDatasets(context) {
      const availableDatasets = await fetchBase(process.env.VUE_APP_BACKEND + "/instructions/available_datasets")
      context.commit("SET_AVAILABLE_DATASETS", availableDatasets)
    },
    appendToURLParams(context, values) {
      console.log(values);
      context.commit("APPEND_TO_URL_PARAMS", values)
    },
    rerouteToTemplate() {
      const model = this.state.selectedModel as any | null;
      let stuff

      for (const value in Object.values(model)) {
        console.log(value);
      }

      if (typeof model !== null) {
        stuff = Object.entries(model)
        console.log(stuff);
        
      }
      stuff = Object.values(model)[0]
      console.log(stuff);
      


      let url_string = process.env.VUE_APP_BACKEND + "/" + this.state.selected + "/" + stuff + "/template/"
      for (const key_val in this.state.URLParams) {
        url_string += key_val + "=" + this.state.URLParams[key_val] + "&"
      }
      url_string = url_string.substring(0, url_string.length - 1);

      //window.open(url_string, "_blank")
    },
    setURLParamsInitialValues(context, URLParams){
      context.commit("SET_URL_PARAMS_INITIAL_VALUES", URLParams)
    },
    setImgTagValue(context) {
      let url_string = process.env.VUE_APP_BACKEND + "/" + this.state.selected + "/preview/"
      for (const key_val in this.state.URLParams) {
        url_string += key_val + "=" + this.state.URLParams[key_val] + "&"
      }
      url_string = url_string.substring(0, url_string.length - 1);
      context.commit("SET_IMG_TAG_VALUE", url_string)
    },
    resetURLParams(context){
      context.commit("RESET_URL_PARAMS")
    }
  },
  modules: {
  }
})