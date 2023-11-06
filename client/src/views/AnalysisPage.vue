<template>
  <el-container>
    <el-header>OnlineStat: 一个在线统计分析平台</el-header>

    <el-aside>
      <el-menu default-active="1-1" @select="handleSelect" unique-opened>
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
          <!-- 添加机器学习的菜单项 -->
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-main>
      <!-- 只有当选中 "基本数据" 时，BasicStats 组件才显示 -->
      <BasicStats
          v-if="activeIndex === '1-1'"
          :columns="columns"
          :selectedColumn="selectedColumn"
          :stats="stats"
          @getStats="getStats"
          @update:selectedColumn="selectedColumn = $event"
      />
    </el-main>

    <el-footer>©2023 由陈启源开发</el-footer>
  </el-container>
</template>

<script>
import axios from "axios";
import {ref, computed} from "vue";
import {useStore} from "vuex";
import BasicStats from "@/components/analysis/BasicStats.vue";

export default {
  components: {
    BasicStats,
  },
  data() {
    return {
      activeIndex: '1-1', // 默认激活的菜单项
    };
  },
  setup() {
    const store = useStore();
    const selectedColumn = ref("");
    const stats = ref(null);

    const data = computed(() => store.state.tableData);
    const columns = computed(() => {
      if (data.value && data.value.length > 0) {
        return Object.keys(data.value[0]);
      }
      return [];
    });

    const getStats = async () => {
      const requestData = {
        column: selectedColumn.value,
        data: data.value,
      };
      try {
        const response = await axios.post("http://localhost:5000/api/stats", requestData);
        stats.value = response.data;
      } catch (error) {
        console.error("An error occurred while fetching the stats:", error);
      }
    };

    return {
      data,
      columns,
      selectedColumn,
      getStats,
      stats,
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      this.activeIndex = key;
    },
  },
};
</script>

<style scoped>
/* 在这里添加你的样式 */
</style>
