<template>
    <el-container>
        <el-header>OnlineStat: 一个在线统计分析平台</el-header>
        <el-container>
            <el-aside>
                <el-menu default-active="bar" @select="handleSelect">
                    <el-menu-item index="bar">条形图</el-menu-item>
                    <el-menu-item index="column">柱状图</el-menu-item>
                    <el-menu-item index="pie">饼图</el-menu-item>
                    <el-menu-item index="line">折线图</el-menu-item>
                    <el-menu-item index="area">面积图</el-menu-item>
                    <el-menu-item index="scatter">散点图</el-menu-item>
                    <el-menu-item index="radar">雷达图</el-menu-item>
                </el-menu>
            </el-aside>

            <el-main>
                <div class="settings">
                    <el-row>
                        <el-col :span="24">
                            <label for="xField">X轴字段：</label>
                            <el-select v-model="selectedXField" placeholder="请选择X轴字段" id="xField">
                                <el-option v-for="field in fields" :key="field" :label="field" :value="field"></el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    <el-row v-if="chartType !== 'pie'">
                        <el-col :span="24">
                            <label for="yField">Y轴字段：</label>
                            <el-select v-model="selectedYField" placeholder="请选择Y轴字段" id="yField">
                                <el-option v-for="field in fields" :key="field" :label="field" :value="field"></el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                </div>
                <div ref="chartContainer" class="chart-container"></div>
            </el-main>
        </el-container>
        <el-footer>©2023 由陈启源开发</el-footer>
    </el-container>
</template>


<script>
import { Bar, Column, Pie, Line, Area, Scatter, Radar } from '@antv/g2plot';
import { ref, onMounted, watch, computed } from "vue";
import { useStore } from "vuex";

export default {
    name: "VisualizationPage",
    setup() {
        const store = useStore();
        const chartType = ref("bar");
        const selectedXField = ref("");
        const selectedYField = ref("");
        const chartContainer = ref(null);
        let chartInstance = null;

        const data = computed(() => store.state.tableData);
        const fields = computed(() => {
            if (data.value.length > 0) {
                return Object.keys(data.value[0]);
            }
            return [];
        });

        const renderChart = () => {
            if (chartInstance) {
                chartInstance.destroy();
            }

            const chartData = data.value;

            if (chartType.value === "bar") {
                chartInstance = new Bar(chartContainer.value, {
                    data: chartData,
                    xField: selectedXField.value,
                    yField: selectedYField.value,
                });
            } else if (chartType.value === "column") {
                chartInstance = new Column(chartContainer.value, {
                    data: chartData,
                    xField: selectedXField.value,
                    yField: selectedYField.value,
                });
            } else if (chartType.value === "pie") {
                chartInstance = new Pie(chartContainer.value, {
                    data: chartData,
                    angleField: selectedXField.value,
                    colorField: fields.value[0],
                });
            } else if (chartType.value === "line") {
                chartInstance = new Line(chartContainer.value, {
                    data: chartData,
                    xField: selectedXField.value,
                    yField: selectedYField.value,
                });
            } else if (chartType.value === "area") {
                chartInstance = new Area(chartContainer.value, {
                    data: chartData,
                    xField: selectedXField.value,
                    yField: selectedYField.value,
                });
            } else if (chartType.value === "scatter") {
                chartInstance = new Scatter(chartContainer.value, {
                    data: chartData,
                    xField: selectedXField.value,
                    yField: selectedYField.value,
                });
            } else if (chartType.value === "radar") {
                chartInstance = new Radar(chartContainer.value, {
                    data: chartData,
                    xField: selectedXField.value,
                    yField: selectedYField.value,
                });
            }

            chartInstance.render();
        };

        const handleSelect = (index) => {
            chartType.value = index;
        };

        watch([chartType, selectedXField, selectedYField, data], () => {
            if (selectedXField.value && (chartType.value !== "pie" || selectedYField.value)) {
                renderChart();
            }
        });

        onMounted(() => {
            if (fields.value.length > 0) {
                selectedXField.value = fields.value[1] || fields.value[0];
                selectedYField.value = fields.value[0];
            }
        });

        return {
            chartContainer,
            handleSelect,
            selectedXField,
            selectedYField,
            fields,
        };
    },
};
</script>

<style scoped>
.el-main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.settings {
    margin-bottom: 20px;
    text-align: left;
    width: 100%;
    max-width: 300px;
    height: 30%;
}

.chart-container {
    width: 100%;
    max-width: 600px;
    height: 400px;
}
</style>
