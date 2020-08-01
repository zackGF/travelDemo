import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  // 定义状态
  state: {
    Authorization: localStorage.getItem("Authorization") ? localStorage.getItem("Authorization") : ""
  },
  // 状态管理  登录 退出
  mutations: {
    changeLogin(state, user) {
      state.Authorization = user.Authorization
      console.log("ddd");
      localStorage.setItem('Authorization', user.Authorization)  //将Authorization令牌存入内存
    },
    delLogin(state) {
      state.Authorization = "";
      localStorage.removeItem('Authorization')
    }
  }
})

