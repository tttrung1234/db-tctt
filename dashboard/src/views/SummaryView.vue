<template>
  <h3 class="title is-3 has-text-centered">CẤU HÌNH</h3>
  <PlatformList />
  <va-divider />
  <MissionList />
</template>

<script>
import { defineComponent } from "vue";
import PlatformList from "../components/PlatformList.vue";
import MissionList from "../components/MissionList.vue";

export default defineComponent({
  name: "SummaryView",
  components: {
    PlatformList,
    MissionList,
  },
  created() {},
  methods: {},
  computed: {},
  data() {},
  watch: {},
});
</script>

<style lang="scss" scoped></style>
