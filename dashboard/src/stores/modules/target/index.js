import axios from "axios";

const state = {
  target_list: [],
  platform_list: [],
  mission_list: [],
  current_mission: undefined,
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

  UPDATE_CURRENT_MISSION(state, payload) {
    state.current_mission = payload;
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

  async addPlatform({ dispatch }, payload) {
    let res = await axios.post("/platforms/new", payload.new_platform, {
      headers: { Authorization: `Bearer ${payload.token}` },
    });

    await dispatch("getPlatformList", payload.token);
  },

  async deletePlatform({ dispatch }, payload) {
    let res = await axios.delete(`/platforms/${payload.platform.id}`, {
      headers: { Authorization: `Bearer ${payload.token}` },
    });

    await dispatch("getPlatformList", payload.token);
  },

  async getMissionList({ commit }, token) {
    let res = await axios.get("/missions", {
      headers: { Authorization: `Bearer ${token}` },
    });
    commit("GET_MISSION_LIST", res.data);
  },

  async addMission({ dispatch }, payload) {
    let res = await axios.post("/missions/new", payload.new_mission, {
      headers: { Authorization: `Bearer ${payload.token}` },
    });

    await dispatch("getMissionList", payload.token);
  },

  async deleteMission({ dispatch }, payload) {
    let res = await axios.delete(`/missions/${payload.mission.id}`, {
      headers: { Authorization: `Bearer ${payload.token}` },
    });

    await dispatch("getMissionList", payload.token);
  },

  updateCurrentMission({ commit }, payload) {
    commit("UPDATE_CURRENT_MISSION", payload);
  },
};

const getters = {
  target_list: (state) => state.target_list,
  platform_list: (state) => state.platform_list,
  mission_list: (state) => state.mission_list,
  filtered_targets: (state) => {
    return state.target_list.filter(
      (item) => item.mission.id == state.current_mission
    );
  },
};

const targetModule = {
  state,
  mutations,
  actions,
  getters,
};

export default targetModule;
