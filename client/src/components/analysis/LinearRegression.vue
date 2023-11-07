<template>
  <el-container>
    <el-header :style="{fontsize: '12px'}">线性回归</el-header>
    <el-main>
      <el-form @submit.prevent="submitData">
        <el-form-item label="选择X">
          <el-checkbox-group v-model="selectedColumnX">
            <el-checkbox
                v-for="column in columnOptions"
                :key="column"
                :label="column"
                :value="column">
              {{ column }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="选择Y">
          <el-select v-model="selectedColumnY" placeholder="请选择">
            <!-- 循环遍历所有可能的列名 -->
            <el-option
                v-for="column in columnOptions"
                :key="column"
                :label="column"
                :value="column">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="是否使用截距">
          <el-switch v-model="useIntercept" active-text="使用" inactive-text="不使用"/>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitData">提交</el-button>
        </el-form-item>
      </el-form>

      <div v-if="statistics && statistics.coefficients" class="result-container">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span class="result-header">线性回归结果</span>
          </div>
          <el-descriptions bordered column="1">
            <el-descriptions-item label="回归系数：" class="result-content">
              {{ statistics.coefficients.join(', ') }}
            </el-descriptions-item>
            <el-descriptions-item label="截距：" class="result-content">{{ statistics.intercept }}</el-descriptions-item>
            <el-descriptions-item label="决定系数：" class="result-content">{{ statistics.score }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>

      <!-- 预测值输入区域 -->
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span class="result-header">模型预测</span>
        </div>
        <el-form ref="predictForm" :model="predictValues" @submit.prevent="submitPrediction">
          <el-form-item
              v-for="column in selectedColumnX"
              :key="column"
              :label="`输入 ${column}`">
            <el-input v-model.number="predictValues[column]" type="number"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="submitPrediction">提交预测</el-button>
          </el-form-item>
        </el-form>

        <!-- 预测结果展示区域 -->
        <div v-if="predictionResult" class="box-card">
          <div slot="header" class="clearfix">
            <span class="result-header">预测结果</span>
          </div>
          <div>
            预测的Y值是：<span class="predict-content">{{ predictionResult }}</span>
          </div>
        </div>
      </el-card>


      <!-- 错误信息展示 -->
      <el-alert
          v-if="error"
          :title="error"
          type="error"
          show-icon>
      </el-alert>

    </el-main>
  </el-container>
</template>

<script setup>
import {computed, reactive, ref, watch} from 'vue';
import {useStore} from 'vuex';
import axios from 'axios';
import {ElMessage} from 'element-plus';


const store = useStore();
const selectedColumnX = ref([]);
const selectedColumnY = ref(null);
const statistics = ref(null);
const useIntercept = ref(true);
const data = computed(() => store.state.tableData);
const columnOptions = computed(() => {
  if (data.value.length > 0) {
    return Object.keys(data.value[0]);
  }
  return [];
});
const error = ref(null);
// 新增用于存储预测表单值的响应式对象
const predictValues = reactive({});
// 预测结果
const predictionResult = ref(null);


const submitData = async () => {
  // 要判断Y不能出现在X中，否则报错
  if (!selectedColumnX.value || !selectedColumnY) {
    ElMessage.error('请选择一个列');
    return;
  }
  // 要判断Y不能出现在X中，否则报错
  if (selectedColumnX.value.indexOf(selectedColumnY.value) > -1) {
    ElMessage.error('Y不能出现在X中');
    return;
  }

  try {
    const payload = {
      columnX: selectedColumnX.value,
      columnY: selectedColumnY.value,
      data: store.state.tableData,
      useIntercept: useIntercept.value,
    };

    const response = await axios.post('http://localhost:5000/api/lr', payload, {
      params: {
        type: 'train'
      }
    });
    statistics.value = response.data;
    error.value = null;
  } catch (e) {
    ElMessage.error('数据提交失败');
    if (e.response && e.response.data && e.response.data.error) {
      error.value = e.response.data.error;
    } else {
      error.value = '数据提交失败';
    }
    console.error(e);
  }
};

// 提交预测的方法
const submitPrediction = async () => {
  // 检查是否选择了变量
  if (selectedColumnX.value.length === 0 || !selectedColumnY.value) {
    ElMessage.error('请先完成线性回归分析');
    return;
  }

  // 确认所有的输入都被填写
  for (const key in predictValues) {
    if (predictValues[key] === undefined) {
      ElMessage.error(`请输入 ${key} 的值`);
      return;
    }
  }

  try {
    const response = await axios.post('http://localhost:5000/api/lr', {
      columnX: selectedColumnX.value,
      predictValues: predictValues,
      useIntercept: useIntercept.value,
    }, {
      params: {
        type: 'predict'
      }
    });
    predictionResult.value = response.data.prediction;
    ElMessage.success('预测成功');
  } catch (error) {
    ElMessage.error('预测失败');
    console.error(error);
  }
};

watch(selectedColumnX, (newColumns) => {
  newColumns.forEach(column => {
    // 如果这个键还没有初始化，就设置它的初始值
    if (!(column in predictValues)) {
      predictValues[column] = 0;
    }
  });
}, {immediate: true});
</script>

<style scoped>
.result-header {
  color: #409EFF; /* 标题颜色 */
}

.result-content {
  color: #333; /* 结果文字颜色 */
}

.box-card {
  margin-bottom: 20px;
}

.result-container {
  margin-top: 20px; /* 结果区域与表单间距 */
}
</style>
