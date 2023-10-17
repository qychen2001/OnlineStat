<template>
    <el-container class="select-container">
        <el-header>
            <h1 class="app-title">OnlineStat: 一个在线统计分析平台</h1>
        </el-header>
        <el-main class="main-content">
            <!-- 数据表格展示区域 -->
            <el-table :data="data" style="width: 100%">
                <el-table-column v-for="(item, index) in columns" :key="index" :prop="item" :label="item"
                    :min-width="100"></el-table-column>
            </el-table>

            <div class="button-group">
                <router-link to="/visual"> <!-- 使用 router-link 组件实现跳转 -->
                    <el-button class="app-button" type="primary">
                        可视化分析
                    </el-button>
                </router-link>
                <router-link to="/analysis">
                    <el-button class="app-button" type="success">
                        统计分析
                    </el-button>
                </router-link>
            </div>
        </el-main>
        <el-footer>
            <p class="footer-text">©2023 由陈启源开发</p>
        </el-footer>
    </el-container>
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
.select-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 90vh;
}

.app-title {
    margin: 0;
    color: #333;
    font-size: 24px;
}

.main-content {
    width: 80%;
    /* 你可以根据需要调整这个宽度 */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.button-group {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.show-table {
    width: 80%;
}

.footer-text {
    margin: 0;
    color: #666;
}
</style>
