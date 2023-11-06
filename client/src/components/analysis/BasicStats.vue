<template>
  <div>
    <!-- 下拉选择数据列 -->
    <el-select :value="selectedColumn" @change="updateSelectedColumn" placeholder="请选择列" class="select-style">
      <el-option
          v-for="column in columns"
          :key="column"
          :label="column"
          :value="column">
      </el-option>
    </el-select>

    <!-- 按钮触发统计 -->
    <el-button @click="$emit('getStats')" type="primary" class="button-style">获取统计</el-button>

    <!-- 展示统计数据 -->
    <div v-if="stats" class="stats-container">
      <p><strong>均值:</strong> {{ stats.mean }}</p>
      <p><strong>中位数:</strong> {{ stats.median }}</p>
      <p><strong>最小值:</strong> {{ stats.min }}</p>
      <p><strong>最大值:</strong> {{ stats.max }}</p>
      <p><strong>四分位数:</strong> {{ stats.quartiles.join(', ') }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    columns: Array,
    stats: Object,
    selectedColumn: String // 接收父组件传递的当前选中列
  },
  methods: {
    updateSelectedColumn(value) {
      this.$emit('update:selectedColumn', value);
    }
  },
  emits: ['getStats', 'update:selectedColumn']
};
</script>

<!-- 相同的样式可以保留 -->
