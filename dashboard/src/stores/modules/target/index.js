import axios from "axios";

const state = {
  target_list: [],
};

const mutations = {
  GET_TARGET_LIST(state, payload) {
    state.target_list = payload;
  },
};

const actions = {
  async getTargetList({ commit }, token) {
    let res = await axios.get("/api/targets", {
      headers: { Authorization: `Bearer ${token}` },
    });
    commit("GET_TARGET_LIST", res.data);
  },

  updateTarget({ dispatch }, payload) {
    axios
      .put(`/api/targets/${payload.updatedItemId}`, payload.updatedItem, {
        headers: { Authorization: `Bearer ${payload.token}` },
      })
      .then((response) => {
        dispatch("getTargetList", payload.token);
      });
  },

  deleteTarget({ dispatch }, payload) {
    axios
      .delete(`/api/targets/${payload.target_id}`, {
        headers: { Authorization: `Bearer ${payload.token}` },
      })
      .then((response) => {
        dispatch("getTargetList", payload.token);
      });
  },
};

const getters = {
  target_list: (state) => state.target_list,
};

const targetModule = {
  state,
  mutations,
  actions,
  getters,
};

export default targetModule;
