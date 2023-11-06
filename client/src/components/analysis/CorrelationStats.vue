<template>
  <el-container>
    <el-header :style="{fontsize: '12px'}">相关系数</el-header>
    <el-main>
      <el-form @submit.prevent="submitData">
        <el-form-item label="选择第一列">
          <el-select v-model="selectedColumn1" placeholder="请选择">
            <!-- 循环遍历所有可能的列名 -->
            <el-option
                v-for="column in columnOptions"
                :key="column"
                :label="column"
                :value="column">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择第二列">
          <el-select v-model="selectedColumn2" placeholder="请选择">
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
      <!-- 条件渲染，当statistics有数据时显示 -->
      <div v-if="statistics">
        <p>相关系数: {{ statistics.correlation }}</p>
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
const selectedColumn1 = ref(null);
const selectedColumn2 = ref(null);
const statistics = ref(null);
const data = computed(() => store.state.tableData);
const columnOptions = computed(() => {
  if (data.value.length > 0) {
    return Object.keys(data.value[0]);
  }
  return [];
});

const submitData = async () => {
  if (!selectedColumn1.value || !selectedColumn2.value) {
    ElMessage.error('请选择一个列');
    return;
  }

  try {
    const payload = {
      column1: selectedColumn1.value,
      column2: selectedColumn2.value,
      data: store.state.tableData
    };

    const response = await axios.post('http://localhost:5000/api/corr', payload);
    statistics.value = response.data;
  } catch (error) {
    ElMessage.error('数据提交失败');
    console.error(error);
  }
};
</script>

<style scoped>
</style>
