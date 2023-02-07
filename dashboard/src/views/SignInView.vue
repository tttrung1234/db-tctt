<template>
  <div class="container" style="width: fit-content; text-align: center">
    <div class="field">
      <p class="control has-icons-left has-icons-right">
        <input
          class="input"
          type="username"
          placeholder="Username"
          v-model="form.username"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-user"></i>
        </span>
      </p>
    </div>
    <div class="field">
      <p class="control has-icons-left">
        <input
          class="input"
          type="password"
          placeholder="Password"
          v-model="form.password"
          @keyup.enter="submit"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-lock"></i>
        </span>
      </p>
    </div>
    <div class="field">
      <p class="control">
        <a
          :class="[{ 'is-loading': loading }, 'button is-primary']"
          @click="submit"
        >
          Đăng nhập
        </a>
      </p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { mapActions, mapGetters } from "vuex";

export default defineComponent({
  name: "LoginView",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  computed: {
    ...mapGetters(["loading"]),
  },
  methods: {
    ...mapActions(["signIn"]),
    async submit() {
      const User = new FormData();
      User.append("username", this.form.username);
      User.append("password", this.form.password);
      this.signIn(User)
        .then(() => this.$router.push("/dashboard"))
        .catch((error) => alert("Không thể đăng nhập"));
    },
  },
});
</script>
