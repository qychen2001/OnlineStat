// src/main.js

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // make sure to import your router
import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/index.css';

createApp(App)
    .use(router)  // use your router
    .use(ElementPlus)
    .mount('#app');
