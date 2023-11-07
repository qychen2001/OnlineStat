<template>
  <el-container>
    <el-header>OnlineStat: 一个在线统计分析平台</el-header>
    <el-container>
      <el-aside>
        <el-menu :default-active="activeIndex" @select="handleSelect" unique-opened>
          <el-sub-menu index="1">
            <template #title>
              <span>描述性统计</span>
            </template>
            <el-menu-item index="1-1">基本数据</el-menu-item>
            <el-menu-item index="1-2">相关系数</el-menu-item>
          </el-sub-menu>


          <el-sub-menu index="2">
            <template #title>
              <span>机器学习</span>
            </template>
            <el-menu-item-group title="分类">
              <el-menu-item index="2-1">决策树</el-menu-item>
              <el-menu-item index="2-2">Logistic回归</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="回归">
              <el-menu-item index="2-3">线性回归</el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main class="el-main">
          <!-- 动态组件，根据 activeComponent 的值来显示不同的组件 -->
          <component :is="activeComponent"></component>
        </el-main>
      </el-container>

    </el-container>
    <el-footer>©2023 由陈启源开发</el-footer>
  </el-container>
</template>

<script setup>
import {ref} from 'vue';
import BasicStats from '../components/analysis/BasicStats.vue';
import CorrelationStats from '../components/analysis/CorrelationStats.vue';
import LinearRegression from '../components/analysis/LinearRegression.vue';
import {ElContainer, ElHeader, ElAside, ElMenu, ElMenuItem, ElMain, ElFooter, ElSubMenu} from 'element-plus';

// 用于动态切换组件的响应式引用
const activeComponent = ref('');

// 初始化默认活跃索引
const activeIndex = ref('1-1'); // 假设默认显示“基本数据”

// 根据菜单选择来更新 activeComponent
const handleSelect = (index) => {
  switch (index) {
    case '1-1':
      activeComponent.value = BasicStats;
      break;
    case '1-2':
      activeComponent.value = CorrelationStats;
      break;
    case '2-3':
      activeComponent.value = LinearRegression;
      break;
    default:
      activeComponent.value = null;
  }
  activeIndex.value = index;
};

// 初始时加载默认组件
handleSelect(activeIndex.value);
</script>

<style scoped>
.el-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 50%; /* 或具体大小，根据需要 */
  height: 50%; /* 或具体大小，根据需要 */
  margin-top: 100px;
}
</style>
