<template>
  <h3 class="title is-3 has-text-centered">TỔNG HỢP ĐƠN HÀNG</h3>
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

      <div
        v-if="selectedOrders.length > 1"
        class="control"
        @click="
          confirmMergeOrders({
            token: access_token,
            order_ids: selectedOrders.map((order) => order.id),
          })
        "
      >
        <a class="button has-text-white has-background-danger-dark">Ghép đơn</a>
      </div>
    </div>
  </div>
  <va-data-table
    :items="order_list"
    :wrapper-size="500"
    :item-size="50"
    virtual-scroller
    sticky-header
    :columns="columns"
    :filter="search_input"
    hoverable
    clickable
    animated
    selectable
    selected-color="primary"
    v-model="selectedOrders"
    @row:dblclick="handleDblClick"
    @filtered="filtered_count = $event.items.length"
  >
    <template #cell(status)="{ rowData }">
      <p :style="getColor(rowData.status)">
        {{ getStatus(rowData.status) }}
      </p>
    </template>

    <template #cell(actions)="{ rowData }">
      <a
        v-if="rowData.status == 1"
        class="button"
        @click="markOrderDone({ order_id: rowData.id, token: access_token })"
      >
        <span class="icon is-small has-text-info">
          <i class="fas fa-check"></i>
        </span>
      </a>
      <a
        v-if="rowData.status == 0"
        class="button"
        @click="markOrderReady({ order_id: rowData.id, token: access_token })"
      >
        <span class="icon is-small has-text-info">
          <i class="fas fa-cube"></i>
        </span>
      </a>
      <a class="button" @click="handleEditButton(rowData)">
        <span class="icon is-small has-text-info">
          <i class="fas fa-pen"></i>
        </span>
      </a>
      <a
        v-if="rowData.status != 2"
        class="button"
        @click="
          confirmDeleteOrder({ order_id: rowData.id, token: access_token })
        "
      >
        <span class="icon is-small has-text-danger">
          <i class="fas fa-trash"></i>
        </span>
      </a>
    </template>
  </va-data-table>

  <va-modal
    ref="modal"
    stateful
    title="CẬP NHẬT ĐƠN HÀNG"
    blur
    no-outside-dismiss
    ok-text="Cập nhật"
    cancel-text="Hủy"
    @ok="updateOrder({ updatedItemId, updatedItem, token: access_token })"
    @cancel=""
  >
    <template #default>
      <template v-for="key in Object.keys(updatedItem)" :key="key">
        <div class="field">
          <label class="label">{{ name_map[key] }}</label>
          <div class="control">
            <input class="input" type="text" v-model="updatedItem[key]" />
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
  name: "Dashboard",
  created() {
    this.getOrderList(this.access_token);
  },
  methods: {
    ...mapActions([
      "getOrderList",
      "markOrderDone",
      "markOrderReady",
      "deleteOrder",
      "updateOrder",
      "mergeOrders",
    ]),
    handleDblClick(event) {
      this.$router.push({ name: "OrderDetail", params: { id: event.item.id } });
    },
    getColor(status) {
      if (status === 2) {
        return "color: green;";
      }

      if (status === 1) {
        return "color: blue;";
      }

      if (status === -1) {
        return "color: red;";
      }

      return "color: black;";
    },

    confirmDeleteOrder(payload) {
      let text = `Xác nhận xóa đơn hàng ${payload.order_id}?`;

      if (confirm(text) == true) {
        this.deleteOrder(payload);
      }
    },

    handleEditButton(data) {
      this.updatedItem.username = data.username;
      this.updatedItem.contact = data.contact;
      this.updatedItem.note = data.note;
      this.updatedItem.cogs = data.cogs;
      this.updatedItem.ship_cost = data.ship_cost;
      this.updatedItemId = data.id;

      this.$refs.modal.show();
    },

    confirmMergeOrders(payload) {
      let text = `Xác nhận ghép đơn hàng ${payload.order_ids.join()}?`;

      if (confirm(text) == true) {
        this.mergeOrders(payload);
      }
    },

    getStatus(status) {
      if (status == -1) {
        return "Đã hủy";
      }

      if (status == 0) {
        return "Đã nhận đơn";
      }

      if (status == 1) {
        return "Đã đóng gói";
      }

      if (status == 2) {
        return "Đã giao";
      }
    },
  },
  computed: {
    ...mapGetters(["order_list", "access_token"]),
  },

  watch: {
    selectedOrders() {
      console.log(this.selectedOrders);
    },
  },
  data() {
    const columns = [
      {
        key: "id",
        label: "Mã đơn hàng",
        sortable: true,
        width: 10,
        sortingFn: (a, b) => parseInt(a) - parseInt(b),
        sortingOptions: ["desc", "asc"],
        thAlign: "center",
        tdAlign: "center",
      },
      { key: "username", label: "Họ tên", thAlign: "center" },
      { key: "contact", label: "Thông tin", thAlign: "center" },
      {
        key: "quantity",
        label: "Số lượng",
        sortable: true,
        sortingFn: (a, b) => parseInt(a) - parseInt(b),
        thAlign: "center",
        tdAlign: "center",
      },
      {
        key: "price",
        label: "Giá trị",
        sortable: true,
        sortingFn: (a, b) => parseInt(a) - parseInt(b),
        sortingOptions: ["desc", "asc"],
        thAlign: "center",
        tdAlign: "center",
      },
      {
        key: "cogs",
        label: "Thực thu",
        sortable: true,
        sortingFn: (a, b) => parseInt(a) - parseInt(b),
        sortingOptions: ["desc", "asc"],
        thAlign: "center",
        tdAlign: "center",
      },
      {
        key: "ship_cost",
        label: "Phí vận chuyển",
        sortable: true,
        thAlign: "center",
        tdAlign: "center",
      },
      { key: "note", label: "Ghi chú", thAlign: "center" },
      { key: "created_time", label: "Thời gian", thAlign: "center" },
      {
        key: "status",
        label: "Trạng thái",
        sortable: true,
        thAlign: "center",
      },
      {
        key: "actions",
        label: "Chỉnh sửa",
        width: 40,
        thAlign: "center",
        tdAlign: "right",
      },
    ];

    const name_map = {
      username: "Họ tên",
      contact: "Thông tin",
      cogs: "Thực thu",
      ship_cost: "Phí vận chuyển",
      note: "Ghi chú",
    };

    return {
      columns,
      search_input: "",
      filtered_count: 0,
      name_map,
      updatedItem: {},
      updatedItemId: null,
      selectedOrders: [],
    };
  },
});
</script>
