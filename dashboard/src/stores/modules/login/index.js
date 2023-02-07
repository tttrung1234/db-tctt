import axios from "axios";

let storage = {
  load() {
    return {
      username: sessionStorage.username,
      access_token: sessionStorage.access_token,
    };
  },

  update(data) {
    sessionStorage.username = data.username;
    sessionStorage.access_token = data.access_token;
  },

  clear() {
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("access_token");
  },
};

const state = {
  username: null,
  access_token: null,
  loading: false,
};

const mutations = {
  SET_USER(state, payload) {
    state.username = payload;
  },

  SET_TOKEN(state, payload) {
    state.access_token = payload;
  },
  LOGIN_PENDING(state) {
    state.loading = true;
  },
  LOGIN_SUCCESS(state) {
    state.loading = false;
  },
};

const actions = {
  loadUser({ commit }) {
    let data = storage.load();
    commit("SET_TOKEN", data.access_token);
    commit("SET_USER", data.username);
  },

  async signIn({ commit }, user) {
    commit("LOGIN_PENDING");
    let res = await axios.post("/api/signin", user, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    if (res.status === 200) {
      commit("SET_TOKEN", res.data.access_token);
      commit("SET_USER", res.data.username);
      storage.update(res.data);
    }

    commit("LOGIN_SUCCESS");
    return res.status;
  },

  async signOut({ commit }) {
    return new Promise((resolve) => {
      commit("SET_USER", null);
      commit("SET_TOKEN", null);
      storage.clear();
      resolve();
    });
  },
};

const getters = {
  is_authenticated: (state) => !!state.username,
  username: (state) => state.username,
  access_token: (state) => state.access_token,
  loading: (state) => state.loading,
};

const loginModule = {
  state,
  mutations,
  actions,
  getters,
};

export default loginModule;
