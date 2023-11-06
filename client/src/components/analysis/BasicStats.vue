<template>
  <el-container>
    <el-header>
      <el-form @submit.prevent="submitData">
        <el-form-item label="选择列">
          <el-select v-model="selectedColumn" placeholder="请选择">
            <!-- 循环遍历所有可能的列名 -->
            <el-option
                v-for="column in columnOptions"
                :key="column"
                :label="column"
                :value="column">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitData">提交</el-button>
        </el-form-item>
      </el-form>
    </el-header>

    <el-main>
      <!-- 条件渲染，当statistics有数据时显示 -->
      <div v-if="statistics">
        <p>平均值: {{ statistics.mean }}</p>
        <p>中位数: {{ statistics.median }}</p>
        <p>最小值: {{ statistics.min }}</p>
        <p>最大值: {{ statistics.max }}</p>
        <p>四分位数: {{ statistics.quartiles }}</p>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import {ref, computed} from 'vue';
import {useStore} from 'vuex';
import axios from 'axios';
import {ElMessage} from 'element-plus';

const store = useStore();

// 选择列的数据模型
const selectedColumn = ref(null);

// 存储从后端获取的统计数据
const statistics = ref(null);

// 自动获取列名


const data = computed(() => store.state.tableData);
const columnOptions = computed(() => {
  if (data.value.length > 0) {
    return Object.keys(data.value[0]);
  }
  return [];
});
// const columnOptions = computed(() => {
//   // 确保数据存在且不为空
//   if (store.state.rawData && store.state.rawData.length > 0) {
//     // 使用Object.keys从数据的第一项获取所有键作为列名
//     return Object.keys(store.state.rawData[0]);
//   }
//   return [];
// });

const submitData = async () => {
  if (!selectedColumn.value) {
    ElMessage.error('请选择一个列');
    return;
  }

  try {
    const payload = {
      column: selectedColumn.value,
      data: store.state.tableData // 确保这是Vuex中的正确路径
    };

    const response = await axios.post('http://localhost:5000/api/stats', payload);
    statistics.value = response.data;
  } catch (error) {
    ElMessage.error('数据提交失败');
    console.error(error);
  }
};
</script>

<style scoped>
/* 你的CSS样式 */
</style>
