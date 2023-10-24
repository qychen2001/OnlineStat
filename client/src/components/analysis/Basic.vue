<template>
    <div>
        <h1>Statistical Analysis Page</h1>
        <p>This is the statistical analysis page.</p>

        <div>
            <el-form ref="form" :model="form" label-width="120px">
                <el-form-item label="Choose a column:">
                    <el-select v-model="selectedColumn" placeholder="Please select" @change="getStats">
                        <el-option v-for="item in columns" :key="item" :label="item" :value="item"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
        </div>

        <div v-if="stats">
            <p><strong>Mean:</strong> {{ stats.mean }}</p>
            <p><strong>Median:</strong> {{ stats.median }}</p>
            <p><strong>Min:</strong> {{ stats.min }}</p>
            <p><strong>Max:</strong> {{ stats.max }}</p>
            <p><strong>Quartiles:</strong> {{ stats.quartiles }}</p>
        </div>
    </div>
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
                    console.error("Error response data:", error.response.data);
                } else if (error.request) {
                    console.error("Error request data:", error.request);
                } else {
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
