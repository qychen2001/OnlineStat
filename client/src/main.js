import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';   // 确保正确导入
import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/index.css';

createApp(App)
    .use(router)
    .use(store)
    .use(ElementPlus)
    .mount('#app');
