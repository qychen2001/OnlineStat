<template>
    <el-container>
        <el-header>
            <h1 class="app-title">OnlineStat: 一个在线统计分析平台</h1>
        </el-header>

        <el-main class="main-content">
            <img src="@/assets/BigData.png" alt="Descriptive text" class="your-image-class" />
            <div>
                <p class="btn-description">点击下方的按钮来上传您的文件。确保文件格式正确，以便于我们为您处理和分析。</p>
            </div>
            <div>
                <el-upload ref="upload" action="http://localhost:5000/upload"
                    accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                    :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload">
                    <el-button slot="trigger" type="primary" class="upload-btn">点击上传</el-button>
                </el-upload>

                <!-- 数据表格展示区域 -->
                <el-table :data="tableData" style="width: 100%" v-if="tableData.length">
                    <el-table-column v-for="(item, index) in columns" :key="index" :prop="item"
                        :label="item"></el-table-column>
                </el-table>
            </div>
        </el-main>

        <el-footer>
            <p class="footer-text">©2023 由陈启源开发</p>
        </el-footer>
    </el-container>
</template>



<script>
import { ref } from "vue";

export default {
    name: "UploadComponent",
    setup() {
        const tableData = ref([]);
        const columns = ref([]);

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
                tableData.value = parsedData.data;
                if (parsedData.data.length > 0) {
                    columns.value = Object.keys(parsedData.data[0]);
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
            tableData,
            columns,
            handleSuccess,
            handleError,
            beforeUpload,
        };
    },
};
</script>

<style scoped>
.el-header {
    text-align: center;
    padding: 20px;
    background-color: #f8f8f8;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.app-title {
    margin: 0;
    color: #333;
    font-size: 24px;
}

.main-content {
    display: flex;
    flex-direction: column;
    /* stack items vertically */
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 140px);
}

.upload-btn {
    background-color: #3498db;
    color: #ffffff;
    border-radius: 5px;
    padding: 20px 30px;
    font-size: 30px;
    transition: background-color 0.3s;
}

.btn-description {
    font-size: 20px;
}

.your-image-class {
    width: 50%;
    height: auto;
    margin-bottom: 20px;
    /* space below the image */
}

.el-footer {
    text-align: center;
    padding: 10px;
    background-color: #f8f8f8;
    box-shadow: 0px -2px 4px rgba(0, 0, 0, 0.1);
}

.footer-text {
    margin: 0;
    color: #666;
}
</style>

