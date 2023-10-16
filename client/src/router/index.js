import { createRouter, createWebHistory } from 'vue-router';
import Navigation from '@/components/Navigation.vue';
import VisualizationPage from '@/views/VisualizationPage.vue';
import AnalysisPage from '@/views/AnalysisPage.vue';
import UploadPage from '@/components/UploadFile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Navigation
  },
  {
    path: '/visualization',
    name: 'Visualization',
    component: VisualizationPage
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisPage
  },
  {
    path: '/upload',
    name: 'Upload',
    component: UploadPage
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
