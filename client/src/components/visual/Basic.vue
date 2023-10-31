<template>
    <div>
        <el-select v-model="currentChart" placeholder="请选择">
            <el-option v-for="item in chartOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
        </el-select>

        <div ref="barChart" v-if="currentChart === 'bar'"></div>
        <div ref="columnChart" v-if="currentChart === 'column'"></div>
        <div ref="pieChart" v-if="currentChart === 'pie'"></div>
    </div>
</template>

<script>
import { Bar, Column, Pie } from '@antv/g2plot';
import { ref, onMounted } from 'vue';

export default {
    name: 'ChartComponent',
    setup() {
        const currentChart = ref('bar');
        const barChart = ref(null);
        const columnChart = ref(null);
        const pieChart = ref(null);

        const chartOptions = [
            { label: '条形图', value: 'bar' },
            { label: '柱状图', value: 'column' },
            { label: '饼图', value: 'pie' },
        ];

        const data = [
            { type: '类别一', value: 27 },
            { type: '类别二', value: 25 },
            { type: '类别三', value: 18 },
            { type: '类别四', value: 15 },
            { type: '类别五', value: 10 },
            { type: '其他', value: 5 },
        ];

        onMounted(() => {
            const bar = new Bar(barChart.value, {
                data,
                xField: 'value',
                yField: 'type',
            });

            const column = new Column(columnChart.value, {
                data,
                xField: 'type',
                yField: 'value',
            });

            const pie = new Pie(pieChart.value, {
                data,
                angleField: 'value',
                colorField: 'type',
            });

            bar.render();
            column.render();
            pie.render();
        });

        return {
            currentChart,
            barChart,
            columnChart,
            pieChart,
            chartOptions,
        };
    },
};
</script>

<style scoped>
/* You can add your styles here */
</style>
