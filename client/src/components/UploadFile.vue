<template>
    <div>
        <el-upload ref="upload" action="http://localhost:5000/upload"
            accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
            :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload">
            <el-button slot="trigger" type="primary">点击上传</el-button>
        </el-upload>

        <!-- 数据表格展示区域 -->
        <el-table :data="tableData" style="width: 100%" v-if="tableData.length">
            <el-table-column v-for="(item, index) in columns" :key="index" :prop="item" :label="item"></el-table-column>
        </el-table>
    </div>
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
