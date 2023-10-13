<template>
    <el-container>
        <el-header>
            <h1>My Application</h1>
        </el-header>

        <el-main>
            <el-button type="primary" @click="goToVisualPage">Go to Visualization Page</el-button>
            <el-button type="success" @click="goToAnalysisPage">Go to Statistical Analysis Page</el-button>
        </el-main>

        <el-footer>
            <p>©2023 My Company</p>
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
/* Your CSS styles here */
</style>
