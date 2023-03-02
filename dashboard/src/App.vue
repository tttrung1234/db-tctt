<template>
  <div id="app">
    <div v-if="$route.path !== '/signin'" class="navigation-buttons">
      <nav class="navbar" role="navigation" aria-label="main navigation">
        <div id="navbarBasicExample" class="navbar-menu">
          <div class="navbar-start">
            <div class="navbar-item">
              <RouterLink class="navbar-item" to="/abc"> Tổng hợp </RouterLink>
            </div>
          </div>

          <div class="navbar-end">
            <div class="navbar-item">
              <a class="button is-primary" @click="signout">
                <strong>Exit ({{ username }})</strong>
              </a>
            </div>
          </div>
        </div>
      </nav>
    </div>

    <div class="main container">
      <router-view />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "App",
  components: {},
  computed: {
    ...mapGetters(["access_token", "username"]),
  },
  created() {
    this.loadUser();
  },
  methods: {
    ...mapActions(["loadUser"]),
    signout() {
      this.$store
        .dispatch("signOut")
        .then(() => {
          this.$router.push("/signin");
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  watch: {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.main {
  padding-top: 5em;
}
</style>
