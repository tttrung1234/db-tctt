import { createApp } from "vue";
import App from "./App.vue";
import store from "./stores";
import router from "./router";
import { createVuestic } from "vuestic-ui";
import "vuestic-ui/css";
import axios from "axios";

axios.defaults.withCredentials = true;
axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    if (error.response.status === 401) {
      store.dispatch("signOut").then(() => router.push({ name: "SignIn" }));
    }
  }
});

axios.defaults.baseURL = "http://localhost:5000";

const app = createApp(App);
app.use(store);
app.use(router);
app.use(createVuestic());
app.mount("#app");
