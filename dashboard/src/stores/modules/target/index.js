import axios from "axios";

const state = {
  target_list: [],
  platform_list: [],
  mission_list: [],
};

const mutations = {
  GET_TARGET_LIST(state, payload) {
    state.target_list = payload;
  },
  GET_PLATFORM_LIST(state, payload) {
    state.platform_list = payload;
  },
  GET_MISSION_LIST(state, payload) {
    state.mission_list = payload;
  },
};

const actions = {
  async getTargetList({ commit }, token) {
    let res = await axios.get("/targets", {
      headers: { Authorization: `Bearer ${token}` },
    });
    commit("GET_TARGET_LIST", res.data);
  },

  async addTarget({ dispatch }, payload) {
    await axios.post("/targets/new", [payload.new_target], {
      headers: { Authorization: `Bearer ${payload.token}` },
    });

    await dispatch("getTargetList", payload.token);
  },

  updateTarget({ dispatch }, payload) {
    axios
      .put(`/targets/${payload.updatedItemId}`, payload.updatedItem, {
        headers: { Authorization: `Bearer ${payload.token}` },
      })
      .then((response) => {
        dispatch("getTargetList", payload.token);
      });
  },

  deleteTarget({ dispatch }, payload) {
    axios
      .delete(`/targets/${payload.target_id}`, {
        headers: { Authorization: `Bearer ${payload.token}` },
      })
      .then((response) => {
        dispatch("getTargetList", payload.token);
      });
  },

  async getPlatformList({ commit }, token) {
    let res = await axios.get("/platforms", {
      headers: { Authorization: `Bearer ${token}` },
    });
    commit("GET_PLATFORM_LIST", res.data);
  },

  async getMissionList({ commit }, token) {
    let res = await axios.get("/missions", {
      headers: { Authorization: `Bearer ${token}` },
    });
    commit("GET_MISSION_LIST", res.data);
  },
};

const getters = {
  target_list: (state) => state.target_list,
  platform_list: (state) => state.platform_list,
  mission_list: (state) => state.mission_list,
};

const targetModule = {
  state,
  mutations,
  actions,
  getters,
};

export default targetModule;
