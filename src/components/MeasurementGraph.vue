<template>
  <div>
    <div>
      <span>계측기 선택: </span>
      <select v-model="device" @change="onChangeDevice()">
        <option v-for="option in devices" :key="option.name">
          {{ option.name }}
        </option>
      </select>

      &nbsp;
      &nbsp;
      &nbsp;

      <span>시작 날짜 선택: </span>
      <select v-model="start_date" @change="onChangeStartDate()">
        <option v-for="option in dates" :key="option">
          {{ option }}
        </option>
      </select>

      &nbsp;
      &nbsp;
      &nbsp;

      <span>종료 날짜 선택: </span>
      <select v-model="end_date" @change="onChangeEndDate()">
        <option v-for="option in dates2" :key="option">
          {{ option }}
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
      <label>{{selected_label}}의 최소값: {{selected_min}} / 최대값: {{selected_max}}</label>
    </div>

    <GChart
      type="LineChart"
      :data="chartData"
      :options="chartOptions"
      :events="chartEvents" 
      ref="gChart"
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
    var vm = this;
    return {
      device: '--',
      selected_device: null,
      devices: ['--'],
      start_date: '--',
      end_date: '--',
      dates: ['--'],
      dates2: ['--'],
      chartData: null,
      check_x: true,
      check_y: true,
      check_z: true,
      check_theta: true,
      value_min: null,
      value_max: null,
      selected_min: null,
      selected_max: null,
      selected_label: null,
      origin_data: [],
      chartOptions: {
        height: 600,
        curveType: 'function',
        vAxis: { 
          title: '측정값',
          maxValue: 4,
          minValue: 0,
        },
        timeline: { groupByRowLabel: true },
        explorer: { axis: 'horizontal', keepInBounds: true, maxZoomIn: 0.05, maxZoomOut: 1 },
        lineWidth: 4,
      },
      chartEvents: {
        select: () => {
          const table = this.$refs.gChart.chartObject;
          const selection = table.getSelection();          
          if(selection.length == 0) {
            vm.selected_max = null;
            vm.selected_min = null;
            return;
          }

          var chart_idx = selection[0].column-1;
          vm.selected_label = vm.chartData[0][chart_idx+1];
          vm.selected_min = vm.value_min[chart_idx].toFixed(1);
          vm.selected_max = vm.value_max[chart_idx].toFixed(1);
        }
      }
    }
  },
  methods: {
    measurement_formatter(row, column, value) {
      return value.toFixed(1);
    },

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

    onChangeDevice() {
      var vm = this;
      vm.dates = ['--'];
      vm.start_date = '--';
      vm.dates2 = ['--'];
      vm.end_date = '--';

      vm.selected_device = this.devices.find(function(d) { return d.name == vm.device});

      axios
        .get('/api/measurement_dates/?device_id=' + vm.selected_device.device_id)
        .then(function(response) {
          vm.dates = ['--'].concat(response.data);
        });

      vm.dates.forEach(element => {
        if(element >= vm.start_date) {
          vm.dates2.push(element);
        }
      });
    },

    onChangeStartDate() {
      var vm = this;
      vm.dates2 = ['--'];
      vm.end_date = '--';

      vm.dates.forEach(element => {
        if(element >= vm.start_date) {
          vm.dates2.push(element);
        }
      });
    },
  
    onChangeEndDate() {
      var vm = this;
      vm.origin_data = []

      axios
        .get('/api/measurement/?device_id=' + vm.selected_device.device_id + '&start_date=' + vm.start_date + '&end_date=' + vm.end_date)
        .then(function(response) {
          vm.origin_data = response.data
          vm.drawGraph()
        });
    }
  },

  mounted() {
    var vm = this;

    axios
      .get('/api/device/')
      .then(function(response) {
        vm.devices = [{'name': '--'}].concat(response.data);
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

