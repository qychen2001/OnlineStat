import { createStore } from 'vuex';

export default createStore({
    state: {
        tableData: []
    },
    mutations: {
        SET_TABLE_DATA(state, data) {
            state.tableData = data;
        }
    },
    actions: {
        updateTableData({ commit }, data) {
            // 对数据进行处理或API调用
            commit('SET_TABLE_DATA', data);
        }
    }
});
