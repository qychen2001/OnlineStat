<template>
    <el-container>
        <el-header>
            <h1 class="app-title">OnlineStat: 一个在线统计分析平台</h1>
        </el-header>

        <el-main class="main-content">
            <img src="@/assets/BigData.png" alt="Descriptive text" class="your-image-class" />
            <div class="button-group">
                <el-button class="app-button" type="primary" @click="goToVisualPage">
                    可视化分析
                </el-button>
                <el-button class="app-button" type="success" @click="goToAnalysisPage">
                    统计分析
                </el-button>
            </div>
        </el-main>

        <el-footer>
            <p class="footer-text">©2023 由陈启源开发</p>
        </el-footer>
    </el-container>
</template>



<script>
export default {
    methods: {
        goToVisualPage() {
            this.$router.push('/visualization');
        },
        goToAnalysisPage() {
            this.$router.push('/analysis');
        }
    }
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
    flex-direction: column;  /* stack items vertically */
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 140px);
}

.button-group {
    display: flex;
    flex-direction: row; /* arrange buttons horizontally */
    align-items: center;
    justify-content: center;
    gap: 15px; /* provides space between buttons */
}

.app-button {
    /* other styles remain unchanged */
    flex: 1; 
    max-width: 200px; 
    text-align: center;
}

.your-image-class {
    width: 50%;  
    height: auto; 
    margin-bottom: 20px; /* space below the image */
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

