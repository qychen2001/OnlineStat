<template>
    <el-container class="custom-container">
        <el-header>
            <h1 class="app-title">OnlineStat: 一个在线统计分析平台</h1>
        </el-header>

        <el-main class="main-content">
            <div v-if="!showTable">
                <img src="@/assets/BigData.png" alt="Descriptive text" class="index-image-class" />
                <p class="btn-description">点击下方的按钮来上传您的文件。确保文件格式正确，以便于我们为您处理和分析。</p>
                <el-upload class="custom-upload" ref="upload" action="http://localhost:5000/upload"
                    accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                    :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload">
                    <el-button slot="trigger" type="primary" class="upload-btn">点击上传</el-button>
                </el-upload>
            </div>
            <div v-else>
                <DataTableComponent />
            </div>
        </el-main>

        <el-footer>
            <p class="footer-text">©2023 由陈启源开发</p>
        </el-footer>
    </el-container>
</template>



<script>
import { ref } from "vue";
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import DataTableComponent from './DataTableComponent.vue';

export default {
    name: "UploadComponent",
    components: {
        DataTableComponent
    },
    setup() {
        const tableData = ref([]);
        const columns = ref([]);
        const store = useStore();
        const showTable = ref(false);
        const router = useRouter();


        const handleSuccess = (response) => {
            let parsedData;

            if (typeof response === "string") {
                try {
                    parsedData = JSON.parse(response);
                } catch (error) {
                    console.error("Error parsing server response:", error);
                    return;
                }
            } else {
                parsedData = response;
            }

            if (parsedData && typeof parsedData.data === "object" && Array.isArray(parsedData.data)) {
                if (parsedData.data.length > 0) {
                    showTable.value = true;
                    store.dispatch('updateTableData', response.data);
                    router.push({ name: 'DataTable' });
                }
            } else {
                console.error("Unexpected server response format:", parsedData);
            }
        };

        const handleError = (err) => {
            console.error("Upload failed:", err);
        };

        const beforeUpload = (file) => {
            const isExcel = file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || file.type === "application/vnd.ms-excel";
            const isCsv = file.type === "text/csv";
            if (!isExcel && !isCsv) {
                this.$message.error('上传文件只能是 Excel 或 CSV 格式!');
                return false;
            }
            const isLt2M = file.size / 1024 / 1024 < 2;
            if (!isLt2M) {
                this.$message.error('上传文件大小不能超过 2MB!');
                return false;
            }
            return true;
        };

        return {
            columns,
            showTable,
            handleSuccess,
            handleError,
            beforeUpload,
        };
    },
};
</script>

<style scoped>
.custom-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 90vh;
}

.el-header,
.el-main,
.el-footer {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.main-content {
    width: 80%;
    /* 你可以根据需要调整这个宽度 */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.app-title {
    margin: 0;
    color: #333;
    font-size: 24px;
}

.custom-upload {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.upload-btn {
    margin: auto;
}


.btn-description {
    font-size: 20px;
    align-items: center;
}

.footer-text {
    margin: 0;
    color: #666;
}
</style>

