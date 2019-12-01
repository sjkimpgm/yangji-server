<template>
  <div>
    <div>
      <span>계측기 선택: </span>
      <select v-model="device" @change="onChangeDevice()">
        <option v-for="option in devices" :key="option.name">
          {{ option.name }}
        </option>
      </select>
    </div>
    <div>
      <input type="checkbox" id="check_x" v-model="check_x" @change="drawGraph()"><label for="check_x">X</label>
      &nbsp;
      <input type="checkbox" id="check_y" v-model="check_y" @change="drawGraph()"><label for="check_y">Y</label>
      &nbsp;
      <input type="checkbox" id="check_z" v-model="check_z" @change="drawGraph()"><label for="check_z">Z</label>
      &nbsp;
      <input type="checkbox" id="check_theta" v-model="check_theta" @change="drawGraph()"><label for="check_x">Theta</label>
    </div>

    <div>
      <el-alert type="warning" title="X축 값이 정상범위를 벗어났습니다." v-if="error_x" />
      <el-alert type="warning" title="Y축 값이 정상범위를 벗어났습니다." v-if="error_y" />
      <el-alert type="warning" title="Z축 값이 정상범위를 벗어났습니다." v-if="error_z" />
      <el-alert type="warning" title="θ축 값이 정상범위를 벗어났습니다." v-if="error_theta" />
    </div>


    <GChart
      type="LineChart"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import axios from 'axios'
import { GChart } from 'vue-google-charts'

export default {
  components: {
    GChart
  },
  data() {
    return {
      device: '--',
      selected_device: null,
      devices: ['--'],
      origin_data: [],
      timer: null, 
      chartData: null,
      check_x: true,
      check_y: true,
      check_z: true,
      check_theta: true,
      error_x: false,
      error_y: false,
      error_z: false,
      error_theta: false,
      chartOptions: {
        height: 600,
        curveType: 'function',
        vAxis: { 
          title: '측정값',
        },
        timeline: { groupByRowLabel: true },
        explorer: { axis: 'horizontal', keepInBounds: true, maxZoomIn: 0.05, maxZoomOut: 1 },
      }
    }
  },
  methods: {
    measurement_formatter(row, column, value) {
      return value.toFixed(1);
    },

    drawGraph() {
      var vm = this;

      if(vm.origin_data.length == 0) return

      vm.chartOptions.series = {}

      let color = ['blue', 'red', 'orange', 'green']
      let dataStyle = {
        lineWidth: 4
      }

      let limitStyle = {
        lineDashStyle: [4, 4],
        lineWidth: 1
      }

      var converted_data = ['datetime']
      if(vm.check_x) { 
        converted_data.push('X')
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[0]
      }
      if(vm.check_y) { 
        converted_data.push('Y')
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[1]
      }
      if(vm.check_z) { 
        converted_data.push('Z')
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[2]
      }
      if(vm.check_theta) { 
        converted_data.push('θ')
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[3]
      }

      if(vm.check_x) {
        converted_data.push('X limit+');
        converted_data.push('X limit-');
        vm.chartOptions.series[converted_data.length-3] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-3]['color'] = color[0]
        vm.chartOptions.series[converted_data.length-2]['color'] = color[0]
      }
      if(vm.check_y) {
        converted_data.push('Y limit+');
        converted_data.push('Y limit-');
        vm.chartOptions.series[converted_data.length-3] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-3]['color'] = color[1]
        vm.chartOptions.series[converted_data.length-2]['color'] = color[1]
      }
      if(vm.check_z) {
        converted_data.push('Z limit+');
        converted_data.push('Z limit-');
        vm.chartOptions.series[converted_data.length-3] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-3]['color'] = color[2]
        vm.chartOptions.series[converted_data.length-2]['color'] = color[2]
      }
      if(vm.check_theta) {
        converted_data.push('θ limit+');
        converted_data.push('θ limit-');
        vm.chartOptions.series[converted_data.length-3] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, limitStyle)
        vm.chartOptions.series[converted_data.length-3]['color'] = color[3]
        vm.chartOptions.series[converted_data.length-2]['color'] = color[3]
      }

      converted_data = [converted_data]
      
      for(let m of vm.origin_data) {
        let array_m = [new Date(m.datetime)]
        if(vm.check_x) { 
          array_m.push(m.diff_x)
          if(m.diff_x < vm.selected_device.x_min || m.diff_x > vm.selected_device.x_max) {
            vm.error_x = true
          }
        }
        if(vm.check_y) {
          array_m.push(m.diff_y)
          if(m.diff_y < vm.selected_device.y_min || m.diff_y > vm.selected_device.y_max) {
            vm.error_y = true
          }
        }
        if(vm.check_z) {
          array_m.push(m.diff_z)
          if(m.diff_z < vm.selected_device.z_min || m.diff_z > vm.selected_device.z_max) {
            vm.error_z = true
          }
        }
        if(vm.check_theta) {
          array_m.push(m.diff_a)
          if(m.diff_theta < vm.selected_device.t_min || m.diff_theta > vm.selected_device.t_max) {
            vm.error_theta = true
          }
        }

        if(vm.check_x) {
          array_m.push(vm.selected_device.x_max)
          array_m.push(vm.selected_device.x_min)
        }

        if(vm.check_y) {
          array_m.push(vm.selected_device.y_max)
          array_m.push(vm.selected_device.y_min)
        }

        if(vm.check_z) {
          array_m.push(vm.selected_device.z_max)
          array_m.push(vm.selected_device.z_min)
        }

        if(vm.check_theta) {
          array_m.push(vm.selected_device.t_max)
          array_m.push(vm.selected_device.t_min)
        }

        converted_data.push(array_m);
      }

      vm.chartData = converted_data;
    },

    update() {
      var vm = this;
      var last_time = this.origin_data[this.origin_data.length-1].datetime;

      axios
        .get('/api/measurement_recent/?device_id=' + vm.selected_device.device_id + '&last_time=' + last_time)
        .then(function(response) {
          vm.origin_data = vm.origin_data.concat(response.data)
          vm.origin_data = vm.origin_data.slice(vm.origin_data.length - 300)
          vm.drawGraph()
        });
    },

    start() {
      if(this.timer != null) return 

      this.timer = setInterval(this.update, 2000)
    },

    stop() {
      if(this.timer == null) return 

      clearInterval(this.timer)
      this.timer = null
    },

    date_format(d) {
      var year = d.getFullYear();
      var month = d.getMonth()+1;
      var date = d.getDate();
      var hour = d.getHours();
      var min = d.getMinutes();
      var sec = d.getSeconds();

      return year + '-' + month + '-' + date + ' ' + hour + ':' + min + ':' + sec
    },

    onChangeDevice() {
      var vm = this;
      vm.stop();

      vm.selected_device = this.devices.find(function(d) { return d.name == vm.device});

      var now = new Date();
      now.setMinutes(now.getMinutes() - 3);
      var now_str = this.date_format(now);

      axios
        .get('/api/measurement_recent/?device_id=' + vm.selected_device.device_id + '&last_time=' + now_str)
        .then(function(response) {
          vm.origin_data = response.data
          vm.drawGraph()

          vm.start();
        });
    },
  },

  // mounted() {
  //   var vm = this;

  //   var now = new Date();
  //   now.setMinutes(now.getMinutes() - 3);
  //   var now_str = this.date_format(now);

  //   axios
  //     .get('/api/measurement_recent/?last_time=' + now_str)
  //     .then(function(response) {
  //       vm.origin_data = response.data
  //       vm.drawGraph()

  //       vm.start();
  //     });
  // }, 
  mounted() {
    var vm = this;

    axios
      .get('/api/device/')
      .then(function(response) {
        vm.devices = [{'name': '--'}].concat(response.data);
      });
  },

  beforeDestroy() {
    this.stop();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

