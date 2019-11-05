<template>
  <div>
    <div>
      <span>계측기 선택: </span>
      <select v-model="device" @change="onChangeDevice()">
        <option v-for="option in devices">
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
      &nbsp;
      <span>/</span>
      &nbsp;
      <input type="checkbox" id="check_a" v-model="check_a" @change="drawGraph()"><label for="check_a">A</label>
      &nbsp;
      <input type="checkbox" id="check_b" v-model="check_b" @change="drawGraph()"><label for="check_b">B</label>
      &nbsp;
      <input type="checkbox" id="check_c" v-model="check_c" @change="drawGraph()"><label for="check_c">C</label>
      &nbsp;
      <input type="checkbox" id="check_d" v-model="check_d" @change="drawGraph()"><label for="check_d">D</label>
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
      check_a: false,
      check_b: false,
      check_c: false,
      check_d: false,
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
      }
    }
  },
  methods: {
    measurement_formatter(row, column, value) {
      return value.toFixed(1);
    },

    drawGraph() {
      var vm = this;

      var converted_data = ['datetime']
      if(vm.check_x) converted_data.push('X')
      if(vm.check_y) converted_data.push('Y')
      if(vm.check_z) converted_data.push('Z')
      if(vm.check_theta) converted_data.push('Theta')
      if(vm.check_a) converted_data.push('A')
      if(vm.check_b) converted_data.push('B')
      if(vm.check_c) converted_data.push('C')
      if(vm.check_d) converted_data.push('D')

      converted_data = [converted_data]
      
      for(let m of vm.origin_data) {
        let array_m = [new Date(m.datetime)]
        if(vm.check_x) array_m.push(m.diff_x)
        if(vm.check_y) array_m.push(m.diff_y)
        if(vm.check_z) array_m.push(m.diff_z)
        if(vm.check_theta) array_m.push(m.diff_a)
        if(vm.check_a) array_m.push(m.measure_a)
        if(vm.check_b) array_m.push(m.measure_b)
        if(vm.check_c) array_m.push(m.measure_c)
        if(vm.check_d) array_m.push(m.measure_d)

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

