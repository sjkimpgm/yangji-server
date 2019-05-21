import Vue from 'vue'
import Router from 'vue-router'
import VueDemo from '@/components/VueDemo'
import Messages from '@/components/Messages'

import MeasurementTable from '@/components/MeasurementTable'
import MeasurementGraph from '@/components/MeasurementGraph'
import Measurement3D from '@/components/Measurement3D'
import Device from '@/components/Device'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: VueDemo
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages
    },
    {
      path: '/measurement_table',
      name: 'measurement_table',
      component: MeasurementTable
    },
    {
      path: '/measurement_graph',
      name: 'measurement_graph',
      component: MeasurementGraph
    },
    {
      path: '/measurement_3d',
      name: 'measurement_3d',
      component: Measurement3D
    },
    {
      path: '/device',
      name: 'device',
      component: Device 
    },
  ]
})
