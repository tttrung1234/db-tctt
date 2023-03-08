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
        <a class="button has-text-white has-background-info-dark">Thêm MXH</a>
      </div>
    </div>
  </div>

  <va-data-table
    :items="platform_list"
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
          confirmDeletePlatform({
            platform: { id: rowData.id, platform_name: rowData.platform_name },
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
    title="CẬP NHẬT MXH"
    ok-text="Cập nhật"
    cancel-text="Hủy"
    @ok="
      updatePlatform({
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
        addPlatform({ new_platform, token: access_token });
        reset();
      }
    "
    @cancel=""
  >
    <template #default>
      <template v-for="key in Object.keys(new_platform)" :key="key">
        <div class="field">
          <label class="label">{{ name_map[key] }}</label>
          <div class="control">
            <input class="input" type="text" v-model="new_platform[key]" />
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
  name: "PlatformList",
  created() {
    this.getPlatformList(this.access_token);
  },
  methods: {
    ...mapActions([
      "getPlatformList",
      "updatePlatform",
      "togglePlatformStatus",
      "addPlatform",
      "deletePlatform",
    ]),

    confirmDeletePlatform(payload) {
      let text = `Xác nhận xóa nền tảng "${payload.platform.platform_name}"?`;

      if (confirm(text) == true) {
        this.deletePlatform(payload);
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
      this.new_platform.platform_name = "";
    },
  },
  computed: {
    ...mapGetters(["platform_list", "access_token"]),
  },
  data() {
    const name_map = {
      platform_name: "Tên MXH",
    };

    let new_platform = {
      platform_name: "",
    };

    const columns = [
      {
        key: "platform_name",
        label: "MXH",
        thAlign: "left",
        tdAlign: "left",
      },
      {
        key: "targets.length",
        label: "Số lượng mục tiêu",
        sortable: true,
        thAlign: "left",
        tdAlign: "left",
      },
      {
        key: "actions",
        label: "Tùy chỉnh",
        thAlign: "left",
        tdAlign: "left",
      },
    ];

    return {
      columns,
      search_input: "",
      filtered_count: 0,
      name_map,
      updated_platform: {},
      new_platform,
    };
  },
});
</script>

<style>
.disabledRow {
  background-color: rgb(122, 131, 134);
}
</style>
