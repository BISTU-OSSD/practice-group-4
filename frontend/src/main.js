import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'

Vue.use(ElementUI)

import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:5000/api'
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')