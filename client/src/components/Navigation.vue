<template>
  <el-container>
    <el-header>OnlineStat: 一个在线统计分析平台</el-header>

    <el-main>
      <div v-if="!showTable">
        <p>点击下方的按钮来上传您的文件。确保文件格式正确，以便于我们为您处理和分析。</p>
        <el-upload ref="upload" :before-upload="beforeUpload"
                   :on-error="handleError"
                   :on-success="handleSuccess" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" action="http://localhost:5000/upload">
          <el-button slot="trigger" type="primary">点击上传</el-button>
        </el-upload>
      </div>
      <router-view v-else></router-view>
    </el-main>

    <el-footer>©2023 由陈启源开发</el-footer>
  </el-container>
</template>

<script>
import {ref} from 'vue';
import {useStore} from 'vuex';
import {useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';

export default {
  name: 'UploadComponent',
  setup() {
    const store = useStore();
    const router = useRouter();
    const showTable = ref(false);

    const handleSuccess = (response) => {
      if (response && response.data && Array.isArray(response.data)) {
        if (response.data.length > 0) {
          showTable.value = true;
          store.dispatch('updateTableData', response.data);
          router.push({name: 'DataTable'});
        }
      } else {
        console.error('Unexpected server response format:', response);
      }
    };

    const handleError = (err) => {
      console.error('Upload failed:', err);
      ElMessage.error('上传失败！');
    };

    const beforeUpload = (file) => {
      const isExcel =
          file.type ===
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
          file.type === 'application/vnd.ms-excel';
      const isCsv = file.type === 'text/csv';
      if (!isExcel && !isCsv) {
        ElMessage.error('上传文件只能是 Excel 或 CSV 格式!');
        return false;
      }
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        ElMessage.error('上传文件大小不能超过 2MB!');
        return false;
      }
      return true;
    };

    return {
      showTable,
      handleSuccess,
      handleError,
      beforeUpload,
    };
  },
};
</script>

<style>
.el-container {
  height: 100vh;
  display: flex;
}

.el-header,
.el-footer {
  /* background-color: #e5eaf3; */
  color: #409eff;
  text-align: center;
  line-height: 60px;
}

.el-header {
  font-size: x-large;
  font-weight: 800;
}

.el-footer {
  font-size: medium;
  font-weight: 400;
}

.el-main {
  color: #409eff;
  text-align: center;
  //display: flex;
  align-items: center;
  /* 垂直居中 */
}

.el-aside {
  color: #409EFF;
//text-align: center; //display: flex; //align-items: center;
  /* 垂直居中 */
}
</style>
