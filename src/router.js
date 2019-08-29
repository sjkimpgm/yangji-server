import Vue from 'vue'
import Router from 'vue-router'
import VueDemo from '@/components/VueDemo'
import Messages from '@/components/Messages'

import MeasurementTable from '@/components/MeasurementTable'
import MeasurementTableDay from '@/components/MeasurementTableDay'
import MeasurementGraph from '@/components/MeasurementGraph'
import Measurement3D from '@/components/Measurement3D'
import DeviceSetup from '@/components/DeviceSetup'
import ChangeMeasurement from '@/components/ChangeMeasurement'

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
      path: '/measurement_table_day',
      name: 'measurement_table_day',
      component: MeasurementTableDay
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
      path: '/device_setup',
      name: 'device_setup',
      component: DeviceSetup
    },
    {
      path: '/change_measurement',
      name: 'change_measurement',
      component: ChangeMeasurement
    },
  ]
})
