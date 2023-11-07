<template>
  <el-container>
    <el-header :style="{fontsize: '12px'}">决策树</el-header>
    <el-main>
      <el-form @submit.prevent="submitData">
        <el-form-item label="选择特征">
          <el-checkbox-group v-model="selectedFeatures">
            <el-checkbox
                v-for="feature in featureOptions"
                :key="feature"
                :label="feature"
                :value="feature">
              {{ feature }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="选择目标">
          <el-select v-model="selectedTarget" placeholder="请选择">
            <!-- 循环遍历所有可能的列名 -->
            <el-option
                v-for="feature in featureOptions"
                :key="feature"
                :label="feature"
                :value="feature">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitData">训练模型</el-button>
        </el-form-item>
      </el-form>

      <!-- 模型训练结果展示区域 -->
      <div v-if="modelInfo">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span class="result-header">决策树模型信息</span>
          </div>
          <el-descriptions bordered column="1">
            <!-- 根据实际情况来显示模型的详细信息 -->
            <el-descriptions-item label="模型精度：" class="result-content">
              {{ modelInfo.accuracy }}
            </el-descriptions-item>
            <el-descriptions-item label="Precision（查准率）：" class="result-content">
              {{ modelInfo.precision }}
            </el-descriptions-item>
            <el-descriptions-item label="Recall（查全率）：" class="result-content">
              {{ modelInfo.recall }}
            </el-descriptions-item>
            <el-descriptions-item label="F1：" class="result-content">
              {{ modelInfo.f1 }}
            </el-descriptions-item>
            <el-descriptions-item label="模型深度：" class="result-content">
              {{ modelInfo.maxDepth }}

            </el-descriptions-item>
            <!-- 你可以继续添加更多相关信息 -->
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
              v-for="column in selectedFeatures"
              :key="column"
              :label="`输入 ${column}`">
            <el-input v-model.number="predictValues[column]" type="number"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="submitPrediction">提交预测</el-button>
          </el-form-item>

          <!-- 预测结果展示区域 -->
          <div v-if="predictionResult" class="box-card">
            <div slot="header" class="clearfix">
              <span class="result-header">预测结果</span>
            </div>
            <div>
              预测的Y值是：<span class="predict-content">{{ predictionResult }}</span>
            </div>
          </div>
        </el-form>


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
const selectedFeatures = ref([]);
const selectedTarget = ref(null);
const modelInfo = ref(null);
const featureOptions = computed(() => {
  if (data.value && data.value.length > 0) {
    return Object.keys(data.value[0]);
  }
  return [];
});
const error = ref(null);
const predictValues = reactive({});
const predictionResult = ref(null);
const data = computed(() => store.state.tableData);

const submitData = async () => {
  if (selectedFeatures.value.length === 0 || !selectedTarget.value) {
    ElMessage.error('请选择特征和目标列');
    return;
  }
  if (selectedFeatures.value.includes(selectedTarget.value)) {
    ElMessage.error('目标不能是一个特征');
    return;
  }

  try {
    const payload = {
      features: selectedFeatures.value,
      target: selectedTarget.value,
      data: data.value
    };

    const response = await axios.post('http://localhost:5000/api/dt', payload);
    modelInfo.value = response.data;
    error.value = null;
    ElMessage.success('模型训练成功');
  } catch (e) {
    ElMessage.error('模型训练失败');
    if (e.response && e.response.data && e.response.data.error) {
      error.value = e.response.data.error;
    } else {
      error.value = e.message || '未知错误';
    }
  }
};

// 提交预测的方法
const submitPrediction = async () => {
  if (selectedFeatures.value.length === 0 || !selectedTarget.value) {
    ElMessage.error('请先训练模型');
    return;
  }

  for (const key in predictValues) {
    if (predictValues[key] === undefined) {
      ElMessage.error(`请输入 ${key} 的值`);
      return;
    }
  }

  try {
    const response = await axios.post('http://localhost:5000/api/dt/predict', {
      features: selectedFeatures.value,
      predictValues: predictValues
    });
    predictionResult.value = response.data.prediction;
    ElMessage.success('预测成功');
  } catch (error) {
    ElMessage.error('预测失败');
    console.error(error);
  }
};

watch(selectedFeatures, (newFeatures) => {
  newFeatures.forEach(feature => {
    if (!(feature in predictValues)) {
      predictValues[feature] = '';
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
