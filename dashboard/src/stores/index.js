import { createStore } from "vuex";
import login from "./modules/login";
import target from "./modules/target";

export default createStore({
  modules: {
    target,
    login,
  },
});
