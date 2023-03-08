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

      <div class="control">
        <div class="select">
          <select v-model="current_mission_name">
            <option v-for="{ mission_name } in mission_list">
              {{ mission_name }}
            </option>
          </select>
        </div>
      </div>

      <div class="control" @click="handleAddButton">
        <a class="button has-text-white has-background-info-dark"
          >Thêm mục tiêu</a
        >
      </div>
    </div>
  </div>

  <va-data-table
    :items="filtered_targets"
    :wrapper-size="500"
    :item-size="50"
    :columns="columns"
    :filter="search_input"
    @filtered="filtered_count = $event.items.length"
    @row:dblclick=""
    hoverable
    clickable
    animated
    virtual-scroller
    sticky-header
  >
    <!-- <template #cell(cat)="{ rowData }">
      <p>
        {{ getCatName(rowData.cat) }}
      </p>
    </template> -->
    <template #cell(status)="{ rowData }">
      <p :style="getColor(rowData.status)">
        {{ getStatus(rowData.status) }}
      </p>
    </template>
    <template #cell(actions)="{ rowData }">
      <a class="button" @click="">
        <span class="icon is-small has-text-info">
          <i class="fas fa-pen"></i>
        </span>
      </a>

      <a class="button" @click="">
        <span class="icon is-small has-text-danger">
          <i class="fas fa-trash"></i>
        </span>
      </a>
    </template>
  </va-data-table>

  <!-- <va-modal
    ref="edit_modal"
    stateful
    blur
    size="large"
    no-outside-dismiss
    fixed-layout
    title="CẬP NHẬT MỤC TIÊU"
    ok-text="Cập nhật"
    cancel-text="Hủy"
    @ok="
      updateProduct({
        updated_product_code,
        updated_product,
        token: access_token,
      })
    "
    @cancel=""
  >
    <template #default>
      <template v-for="key in Object.keys(updated_product)" :key="key">
        <div class="field">
          <label class="label">{{ name_map[key] }}</label>
          <div class="control">
            <input class="input" type="text" v-model="updated_product[key]" />
          </div>
        </div>
      </template>
    </template>
  </va-modal> -->

  <va-modal
    ref="add_modal"
    stateful
    blur
    size="large"
    no-outside-dismiss
    fixed-layout
    title="THÊM SẢN PHẨM"
    ok-text="Thêm"
    cancel-text="Hủy"
    @ok="
      {
        addTarget({ new_target, token: access_token });
        reset();
      }
    "
    @cancel=""
  >
    <template #default>
      <template v-for="key in Object.keys(new_target)" :key="key">
        <div class="field">
          <label class="label">{{ name_map[key] }}</label>
          <div
            v-if="!['platform_id', 'mission_id'].includes(key)"
            class="control"
          >
            <input class="input" type="text" v-model="new_target[key]" />
          </div>

          <div v-if="key == 'mission_id'" class="control">
            <div class="select">
              <select v-model="new_target_mission_name">
                <option v-for="{ mission_name } in mission_list">
                  {{ mission_name }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="key == 'platform_id'" class="control">
            <div class="select">
              <select v-model="new_target_platform_name">
                <option v-for="{ platform_name } in platform_list">
                  {{ platform_name }}
                </option>
              </select>
            </div>
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
  name: "TargetList",
  created() {
    this.getTargetList(this.access_token);
    this.getPlatformList(this.access_token);
    this.getMissionList(this.access_token).then(
      (res) => (this.current_mission_name = this.mission_list[0].mission_name)
    );
  },
  methods: {
    ...mapActions([
      "getTargetList",
      "addTarget",
      "getPlatformList",
      "getMissionList",
      "updateCurrentMission",
    ]),
    // confirmDeleteTarget(payload) {
    //   let text = `Xác nhận xóa sản phẩm ${payload.product_code}?`;

    //   if (confirm(text) == true) {
    //     this.deleteProduct(payload);
    //   }
    // },

    // handleEditButton(data) {
    //   this.this_mission_name = this.getCatName(data.cat);

    //   this.updated_product.code = data.code;
    //   this.updated_product.name = data.name;
    //   this.updated_product.desc = data.desc;
    //   this.updated_product.packing = data.packing;
    //   this.updated_product.image = data.image;
    //   this.updated_product.cat = data.cat;
    //   this.updated_product.quantity = data.quantity;
    //   this.updated_product.sale_price = data.sale_price;
    //   this.updated_product.warehouse_price = data.warehouse_price;

    //   this.updated_product_code = data.code;

    //   this.$refs.edit_modal.show();
    // },

    handleAddButton() {
      this.$refs.add_modal.show();
    },

    // handleDblClick(event) {
    //   this.$router.push({
    //     name: "ProductDetail",
    //     params: { code: event.item.code },
    //   });
    // },

    getStatus(status) {
      if (status == false) {
        return "Đã bóc gỡ";
      }

      if (status == true) {
        return "Đang hoạt động";
      }
    },
    getColor(status) {
      if (status === true) {
        return "color: green;";
      }

      if (status === false) {
        return "color: red;";
      }
    },

    getPlatformId(name) {
      return this.platform_list.filter((item) => item.platform_name === name)[0]
        .id;
    },

    getMissionId(name) {
      return this.mission_list.filter((item) => item.mission_name === name)[0]
        .id;
    },

    reset() {
      this.new_target = {
        url: "",
        profile_id: "",
        platform_id: "",
        mission_id: "",
        active_img: "",
        disabled_img: "",
      };
    },
  },
  computed: {
    ...mapGetters([
      "target_list",
      "access_token",
      "platform_list",
      "mission_list",
      "filtered_targets",
    ]),
  },
  data() {
    const name_map = {
      url: "Đường dẫn",
      profile_id: "Tài khoản đăng tải",
      platform_id: "Nền tảng",
      mission_id: "Vụ việc",
      active_img: "Lưu vết 1",
      disabled_img: "Lưu vết 2",
    };

    let new_target = {
      url: "",
      profile_id: "",
      platform_id: "",
      mission_id: "",
      active_img: "",
      disabled_img: "",
    };

    let status_list = [
      { label: "Đang hoạt động", value: true },
      { label: "Đã bóc gỡ", value: false },
    ];

    const columns = [
      {
        key: "url",
        label: "Đường dẫn",
        width: 300,
        thAlign: "left",
      },
      {
        key: "profile_id",
        label: "Tài khoản đăng tải",
        thAlign: "left",
      },
      {
        key: "platform.platform_name",
        label: "Nền tảng",
        thAlign: "left",
        tdAlign: "left",
      },
      {
        key: "mission.mission_name",
        label: "Vụ việc",
        thAlign: "left",
        tdAlign: "left",
      },
      {
        key: "status",
        label: "Trạng thái",
        width: 80,
        thAlign: "left",
        tdAlign: "left",
      },
      {
        key: "actions",
        label: "Chỉnh sửa",
        width: 80,
        thAlign: "left",
        tdAlign: "left",
      },
    ];

    return {
      columns,
      search_input: "",
      filtered_count: 0,
      name_map,
      current_mission_name: "",
      new_target_mission_name: "",
      new_target_platform_name: "",
      new_target_status: "",
      updated_target: {},
      updated_product_code: null,
      new_target,
      status_list,
    };
  },
  watch: {
    current_mission_name(value) {
      let mission = this.mission_list.filter(
        (item) => item.mission_name == value
      )[0];
      this.updateCurrentMission(mission.id);
    },

    new_target_mission_name(value) {
      this.new_target.mission_id = this.getMissionId(value);
    },

    new_target_platform_name(value) {
      this.new_target.platform_id = this.getPlatformId(value);
    },
  },
});
</script>

<style lang="scss" scoped></style>
