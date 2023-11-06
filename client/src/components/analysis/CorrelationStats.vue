<template>
  <div>
    <!-- 下拉选择数据列 1 -->
    <el-select v-model="selectedColumn1" placeholder="请选择第一列" class="select-style">
      <el-option
          v-for="column in columns"
          :key="column"
          :label="column"
          :value="column">
      </el-option>
    </el-select>

    <!-- 下拉选择数据列 2 -->
    <el-select v-model="selectedColumn2" placeholder="请选择第二列" class="select-style">
      <el-option
          v-for="column in columns"
          :key="column"
          :label="column"
          :value="column">
      </el-option>
    </el-select>

    <!-- 按钮触发计算相关系数 -->
    <el-button @click="calculateCorrelation" type="primary" class="button-style">计算相关系数</el-button>

    <!-- 展示计算结果 -->
    <div v-if="correlation !== null" class="result-container">
      <p><strong>相关系数:</strong> {{ correlation }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: {
    columns: Array,
    stats: Object,
    selectedColumn: String // 接收父组件传递的当前选中列
  },
  methods: {
    updateSelectedColumn(value) {
      this.$emit('update:selectedColumn1', value);
    }
  },
  emits: ['getStats', 'update:selectedColumn1']
};

</script>

<!-- Add your component specific styles here -->
<style scoped>
.select-style {
  margin-right: 10px;
}
.button-style {
  margin-bottom: 10px;
}
.result-container {
  margin-top: 10px;
}
</style>
