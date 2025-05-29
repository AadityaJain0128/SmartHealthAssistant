import Vue from "vue";
import VueRouter from "vue-router";
import Signup from "./components/SignupPage.vue";
import Login from "./components/LoginPage.vue";
import Chat from "./components/ChatPage.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: "/chat" },
  { path: "/signup", component: Signup, meta: {title: "Sign Up"} },
  { path: "/login", component: Login, meta: {title: "Login"} },
  { path: "/chat", component: Chat, meta: {title: "Chat Assistance", requiresAuth: true} },
];

const router = new VueRouter({
  routes,
});

// Protect chat route
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!localStorage.getItem("token")) {
      next("/login");
    } else {
      next();
    }
  } else {
    next();
  }
  document.title = to.meta.title + " | Health Assistant";
});

export default router;
