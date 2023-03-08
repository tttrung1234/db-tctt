import { createRouter, createWebHistory } from "vue-router";
import SignInView from "../views/SignInView.vue";
import DashboardView from "../views/DashboardView.vue";
import NotFoundView from "../views/NotFound.vue";
import SummaryView from "../views/SummaryView.vue";

const routes = [
  {
    path: "/signin",
    name: "SignIn",
    component: SignInView,
    beforeEnter: (to, from, next) => {
      const token = sessionStorage.getItem("access_token");
      if (token) next("/dashboard");
      else next();
    },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },

  {
    path: "/summary",
    name: "Summary",
    component: SummaryView,
    meta: { requiresAuth: true },
  },
  //   {
  //     path: "/targets/:id",
  //     name: "TargetDetail",
  //     component: TargetDetailView,
  //     meta: { requiresAuth: true },
  //     props: true,
  //   },
  //   {
  //     path: "/summary/products/:code",
  //     name: "ItemDetail",
  //     component: ItemDetailView,
  //     meta: { requiresAuth: true },
  //     props: (route) => ({
  //       code: route.params.code,
  //       prod_name: route.query.prod_name,
  //     }),
  //   },
  {
    path: "/:pathMatch(.*)*",
    component: NotFoundView,
  },
  {
    path: "/",
    redirect: "/dashboard",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem("access_token");
  if (!token && to.path !== "/signin") next("/signin");
  else next();
});

export default router;
