import { createWebHistory, createRouter } from "vue-router";
import HomePage from "./components/HomePage.vue"
import RobotProgress from "./components/RobotProgress.vue";
import ComponentsList from "./components/ComponentsList.vue";
import HardwareUpdates from "./components/HardwareUpdates.vue"
import AIUpdates from "./components/AIUpdates.vue";
import PrintingUpdates from "./components/PrintingUpdates.vue";



const routes = [
    { path: "/", component: HomePage },
    { path: "/progress", component: RobotProgress },
    { path: "/components", component: ComponentsList },

    { path: "/hardware-progress", component: HardwareUpdates },
    { path: "/ai-progress", component: AIUpdates },
    { path: "/printing-progress", component: PrintingUpdates },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
