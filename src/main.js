import Vue from 'vue'
import App from '@/App.vue'

import store from '@/store' 
import router from '@/router'

import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-theme-default'

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.config.productionTip = false

// Vue.use(VueRouter)
Vue.use(Vuetify)
Vue.use(ElementUI, { locale })

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
