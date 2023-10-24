import { createRouter, createWebHistory } from 'vue-router';
import Navigation from '@/components/Navigation.vue';
import VisualizationPage from '@/views/VisualizationPage.vue';
import AnalysisPage from '@/views/AnalysisPage.vue';
import DataTableComponent from '@/components/DataTableComponent.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Navigation,
    children: [
      {
        path: 'table', // 子路由路径
        name: 'DataTable',
        component: DataTableComponent,
      }
    ]
  },
  {
    path: '/visual',
    name: 'Visualization',
    component: VisualizationPage
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisPage
  },
  // {
  //   path: '/table',
  //   name: 'DataTable',
  //   component: DataTableComponent
  // }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
