// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

import store from './store'

import global_ from './Base.vue'

Vue.config.productionTip = false;

Vue.prototype.globalURL = global_.BASE_URL;
Vue.prototype.$ajax = axios;

axios.interceptors.request.use(
  config =>{
    if(config.url === '/mine/register'){
    }else {
      if (localStorage.getItem('Authorization')) {
        config.headers.Authorization = localStorage.getItem('Authorization')
      }
    }
    return config;
  }
);

axios.interceptors.response.use(
  response =>{
    return response
  },error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('Authorization');
          this.$router.push('/mine')
      }
    }
  }
);

router.beforeEach((to,from,next)=>{
  if (to.path === '/') {
    next();
  }else {
    let token = localStorage.getItem('Authorization');
    if (token === 'null' || token === '') {
      next('/mine')
    }else {
      next()
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
