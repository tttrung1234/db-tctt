<template>
  <div class="field">
    <label class="label">{{ `Tìm kiếm (${filtered_count} kết quả)` }}</label>
    <div class="field is-grouped">
      <div class="control">
        <input
          class="input"
          type="text"
          placeholder="..."
          v-model="search_input"
        />
      </div>

      <div class="control" @click="handleAddButton">
        <a class="button has-text-white has-background-info-dark"
          >Thêm vụ việc</a
        >
      </div>
    </div>
  </div>

  <va-data-table
    :items="mission_list"
    :wrapper-size="300"
    :item-size="50"
    :columns="columns"
    :filter="search_input"
    @filtered="filtered_count = $event.items.length"
    hoverable
    clickable
    animated
    virtual-scroller
    sticky-header
    :row-bind="getRowBind"
  >
    <template #cell(actions)="{ rowData }">
      <a class="button" @click="handleEditButton(rowData)">
        <span class="icon is-small has-text-info">
          <i class="fas fa-pen"></i>
        </span>
      </a>

      <a
        class="button"
        @click="
          confirmDeleteMission({
            mission: { id: rowData.id, mission_name: rowData.mission_name },
            token: access_token,
          })
        "
      >
        <span class="icon is-small has-text-danger">
          <i class="fas fa-trash"></i>
        </span>
      </a>
    </template>
  </va-data-table>

  <va-modal
    ref="edit_modal"
    stateful
    blur
    size="large"
    no-outside-dismiss
    fixed-layout
    title="CẬP NHẬT VỤ VIỆC"
    ok-text="Cập nhật"
    cancel-text="Hủy"
    @ok="
      updateMission({
        updated_category_code,
        updated_category,
        token: access_token,
      })
    "
    @cancel=""
  >
    <template #default>
      <template v-for="key in Object.keys(updated_category)" :key="key">
        <div class="field">
          <label class="label">{{ name_map[key] }}</label>
          <div class="control">
            <input class="input" type="text" v-model="updated_category[key]" />
          </div>
        </div>
      </template>
    </template>
  </va-modal>

  <va-modal
    ref="add_modal"
    stateful
    blur
    size="large"
    no-outside-dismiss
    fixed-layout
    title="THÊM MXH"
    ok-text="Thêm"
    cancel-text="Hủy"
    @ok="
      {
        addMission({ new_mission, token: access_token });
        reset();
      }
    "
    @cancel=""
  >
    <template #default>
      <template v-for="key in Object.keys(new_mission)" :key="key">
        <div class="field">
          <label class="label">{{ name_map[key] }}</label>
          <div class="control">
            <input class="input" type="text" v-model="new_mission[key]" />
          </div>
        </div>
      </template>
    </template>
  </va-modal>
</template>

<script>
import { defineComponent } from "vue";
import { mapGetters, mapActions } from "vuex";

export default defineComponent({
  name: "MissionList",
  created() {
    this.getMissionList(this.access_token);
  },
  methods: {
    ...mapActions([
      "getMissionList",
      "updateMission",
      "toggleMissionStatus",
      "addMission",
      "deleteMission",
    ]),

    confirmDeleteMission(payload) {
      let text = `Xác nhận xóa vụ việc "${payload.mission.mission_name}"?`;

      if (confirm(text) == true) {
        this.deleteMission(payload);
      }
    },

    handleEditButton(data) {
      this.updated_category.code = data.code;
      this.updated_category.label = data.label;
      this.updated_category.desc = data.desc;

      this.updated_category_code = data.code;

      this.$refs.edit_modal.show();
    },

    handleAddButton() {
      this.$refs.add_modal.show();
    },

    getRowBind(row) {
      let classes = [];

      if (row.status == false) {
        classes.push({ disabledRow: true });
      }

      return { class: classes };
    },

    reset() {
      this.new_mission.mission_name = "";
    },
  },
  computed: {
    ...mapGetters(["mission_list", "access_token"]),
  },
  data() {
    const name_map = {
      mission_name: "Vụ việc",
      mission_detail: "Chi tiết",
    };

    let new_mission = {
      mission_name: "",
      mission_detail: "",
    };

    const columns = [
      {
        key: "mission_name",
        label: "Vụ việc",
        thAlign: "left",
        thVerticalAlign: "middle",
        tdAlign: "left",
        tdVerticalAlign: "middle",
      },
      { key: "mission_detail", label: "Chi tiết", width: 300 },
      {
        key: "targets.length",
        label: "Số lượng mục tiêu",
        sortable: true,
        thAlign: "left",
        thVerticalAlign: "middle",
        tdAlign: "left",
        tdVerticalAlign: "middle",
      },
      {
        key: "actions",
        label: "Tùy chỉnh",
        thAlign: "left",
        thVerticalAlign: "middle",
        tdAlign: "left",
        tdVerticalAlign: "middle",
      },
    ];

    return {
      columns,
      search_input: "",
      filtered_count: 0,
      name_map,
      updated_category: {},
      updated_category_code: null,
      new_mission,
    };
  },
});
</script>

<style>
.disabledRow {
  background-color: rgb(122, 131, 134);
}
</style>
