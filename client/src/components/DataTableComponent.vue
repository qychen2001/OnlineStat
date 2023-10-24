<template>
    <!-- 数据表格展示区域 -->
    <el-table :data="data" class="table-container">
        <el-table-column v-for="(item, index) in columns" :key="index" :prop="item" :label="item"
            :min-width="100"></el-table-column>
    </el-table>

    <div class="button-container">
        <router-link to="/visual">
            <el-button type="primary">可视化分析</el-button>
        </router-link>
        <router-link to="/analysis">
            <el-button type="success">统计分析</el-button>
        </router-link>
    </div>
</template>


<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
    name: "DataTableComponent",
    setup() {
        const store = useStore();

        // 使用 computed 从 store 中获取数据
        const data = computed(() => store.state.tableData);

        // 根据第一个数据项来获取列名
        const columns = computed(() => {
            if (data.value.length > 0) {
                return Object.keys(data.value[0]);
            }
            return [];
        });

        return {
            data,
            columns
        };
    }
};
</script>

<style scoped>
.table-container {
    height: 90%;
    overflow: auto;
    justify-content: center;
    background-color: #eef5ff;
}

.button-container {
    margin-top: 16px;
    display: flex;
    /*居中显示*/
    justify-content: center;
    gap: 10px;
}
</style>
