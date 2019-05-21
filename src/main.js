import Vue from 'vue'
import App from '@/App.vue'

import store from '@/store' 
import router from '@/router'

import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-theme-default'

Vue.config.productionTip = false

// Vue.use(VueRouter)
Vue.use(ElementUI, { locale })

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
