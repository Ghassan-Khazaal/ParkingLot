import Vue from 'vue'
import App from './App.vue'

import axios from 'axios'
import VueAxios from 'vue-axios'
import vuetify from '@/plugins/vuetify'

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

Vue.prototype.$axios = axios
Vue.prototype.$api = 'http://localhost:8088/'
export const EventBus = new Vue();

new Vue({
  vuetify,
  render: h => h(App),
}).$mount('#app')
