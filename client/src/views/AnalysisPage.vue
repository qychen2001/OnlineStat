<template>
    <el-container>
        <el-header>OnlineStat: 一个在线统计分析平台</el-header>

        <el-aside>
            <el-menu default-active="2">
                <el-sub-menu index="1">
                    <template #title>
                        <span>描述性统计</span>
                    </template>
                    <el-menu-item-group title="Group One">
                        <el-menu-item index="1-1">均值</el-menu-item>
                        <el-menu-item index="1-2">item two</el-menu-item>
                    </el-menu-item-group>
                    <el-menu-item-group title="Group Two">
                        <el-menu-item index="1-3">item three</el-menu-item>
                    </el-menu-item-group>
                    <el-sub-menu index="1-4">
                        <template #title>item four</template>
                        <el-menu-item index="1-4-1">item one</el-menu-item>
                    </el-sub-menu>
                </el-sub-menu>


                <el-sub-menu index="2">
                        <template #title>
                            <span>机器学习</span>
                        </template>
                        <el-menu-item-group title="Group One">
                            <el-menu-item index="1-1">item one</el-menu-item>
                            <el-menu-item index="1-2">item two</el-menu-item>
                        </el-menu-item-group>
                        <el-menu-item-group title="Group Two">
                            <el-menu-item index="1-3">item three</el-menu-item>
                        </el-menu-item-group>
                        <el-sub-menu index="1-4">
                            <template #title>item four</template>
                            <el-menu-item index="1-4-1">item one</el-menu-item>
                        </el-sub-menu>
                    </el-sub-menu>
            </el-menu>
        </el-aside>


        <el-main>

        </el-main>



        <el-footer>©2023 由陈启源开发</el-footer>
    </el-container>
</template>

<script>
import axios from "axios";
import { ref, computed } from "vue";
import { useStore } from "vuex";

export default {
    name: "AnalysisPage",
    setup() {
        const store = useStore();
        const selectedColumn = ref("");
        const stats = ref(null);

        const data = computed(() => store.state.tableData);
        const columns = computed(() => {
            if (data.value.length > 0) {
                return Object.keys(data.value[0]);
            }
            return [];
        });

        const getStats = async () => {
            const requestData = {
                column: selectedColumn.value,
                data: data.value,
            };
            console.log("Sending request with data:", requestData);
            try {
                const response = await axios.post("http://localhost:5000/api/stats", requestData);
                stats.value = response.data;
            } catch (error) {
                console.error("An error occurred while fetching the stats", error);
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    console.error("Error response data:", error.response.data);
                } else if (error.request) {
                    // The request was made but no response was received
                    console.error("Error request data:", error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.error("Error message:", error.message);
                }
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
};
</script>

<style scoped></style>
