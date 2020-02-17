<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="3">
        <v-select label="계측기 선택" :items="devices" item-text="name" return-object v-model="selected_device" />
      </v-col>
    </v-row>

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
      selected_device: null,
      devices: [],
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
  watch: {
    selected_device: function() {
      this.stop();

      var now = new Date();
      now.setMinutes(now.getMinutes() - 3);
      var now_str = this.date_format(now);

      axios
        .get('/api/measurement_recent/?device_id=' + this.selected_device.device_id + '&last_time=' + now_str)
        .then((response) => {
          this.origin_data = response.data
          this.drawGraph()

          this.start();
        });
    }
  },

  methods: {
    drawGraph() {
      var vm = this;

      if(vm.origin_data.length === 0) return

      vm.chartOptions.series = {}

      let color = ['blue', 'red', 'orange', 'green']
      let dataStyle = {
        lineWidth: 2
      }

      let limitStyle = {
        lineDashStyle: [4, 4],
        lineWidth: 1
      }

      var converted_data = ['datetime']
      var checked_count = 0;
      if(vm.check_x) { 
        converted_data.push('X'); 
        checked_count += 1; 
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[0]
      }
      if(vm.check_y) { 
        converted_data.push('Y'); checked_count += 1; 
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[1]
      }
      if(vm.check_z) { 
        converted_data.push('Z'); checked_count += 1; 
        vm.chartOptions.series[converted_data.length-2] = Object.assign({}, dataStyle);
        vm.chartOptions.series[converted_data.length-2]['color'] = color[2]
      }
      if(vm.check_theta) { 
        converted_data.push('θ');  checked_count += 1; 
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

      vm.value_min = Array(checked_count).fill(Number.MAX_VALUE);
      vm.value_max = Array(checked_count).fill(Number.MIN_VALUE);

      converted_data = [converted_data]
      
      for(let m of vm.origin_data) {
        let array_m = [new Date(m.datetime)]
        var i = 0;
        if(vm.check_x) { array_m.push(m.diff_x); vm.value_min[i] = Math.min(vm.value_min[i], m.diff_x); vm.value_max[i] = Math.max(vm.value_max[i], m.diff_x); i += 1;}
        if(vm.check_y) { array_m.push(m.diff_y); vm.value_min[i] = Math.min(vm.value_min[i], m.diff_y); vm.value_max[i] = Math.max(vm.value_max[i], m.diff_y); i += 1;}
        if(vm.check_z) { array_m.push(m.diff_z); vm.value_min[i] = Math.min(vm.value_min[i], m.diff_z); vm.value_max[i] = Math.max(vm.value_max[i], m.diff_z); i += 1;}
        if(vm.check_theta) {array_m.push(m.diff_a); vm.value_min[i] = Math.min(vm.value_min[i], m.diff_a); vm.value_max[i] = Math.max(vm.value_max[i], m.diff_a); i += 1;}

        if(vm.check_x) {
          array_m.push(vm.selected_device.params.limit_max[0])
          array_m.push(vm.selected_device.params.limit_min[0])
        }

        if(vm.check_y) {
          array_m.push(vm.selected_device.params.limit_max[1])
          array_m.push(vm.selected_device.params.limit_min[1])
        }

        if(vm.check_z) {
          array_m.push(vm.selected_device.params.limit_max[2])
          array_m.push(vm.selected_device.params.limit_min[2])
        }

        if(vm.check_theta) {
          array_m.push(vm.selected_device.params.limit_max[3])
          array_m.push(vm.selected_device.params.limit_min[3])
        }

        converted_data.push(array_m);
      }

      vm.chartData = converted_data;
    },

    update() {
      var last_time = this.origin_data[this.origin_data.length-1].datetime;

      axios
        .get('/api/measurement_recent/?device_id=' + this.selected_device.device_id + '&last_time=' + last_time)
        .then((response) => {
          this.origin_data = this.origin_data.concat(response.data)
          this.origin_data = this.origin_data.slice(this.origin_data.length - 300)
          this.drawGraph()
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
    }
  },

  mounted() {
    axios
      .get('/api/device/')
      .then((response) => {
        this.devices = response.data
      });
  },

  beforeDestroy() {
    this.stop();
  }
};
</script>
