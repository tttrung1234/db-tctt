<template>
  <h3 class="title is-3 has-text-centered">DANH SÁCH MỤC TIÊU</h3>
  <TargetList />
</template>

<script>
import { defineComponent } from "vue";
import TargetList from "../components/TargetList.vue";

export default defineComponent({
  name: "Dashboard",
  components: {
    TargetList,
  },
  created() {},
  methods: {},
  computed: {},
  data() {},
  watch: {},
});
</script>

<style lang="scss" scoped></style>
