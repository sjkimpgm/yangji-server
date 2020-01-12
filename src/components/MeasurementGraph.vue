<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="3">
        <v-select label="계측기 선택" :items="devices" item-text="name" return-object v-model="selected_device" />
      </v-col>

      <v-col cols="3">
        <v-select label="시작 날짜 선택" :items="dates" v-model="start_date" />
      </v-col>

      <v-col cols="3">
        <v-select label="종료 날짜 선택" :items="dates2" v-model="end_date" />
      </v-col>

      <v-col>
        <v-btn color="primary" @click="fetchAndDraw">그래프 그리기</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="isLoading" justify="center">
      <v-col cols="2">
        <p>데이터 로딩: </p>
      </v-col>
      <v-col cols="4">
        <v-progress-linear :value="progress"></v-progress-linear>
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
      selected_device: null,
      devices: [],
      start_date: null,
      end_date: null,
      dates: [],
      dates2: [],
      isLoading: false,
      progress: 0,
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
          title: '측정값 (단위: mm)',
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

  watch: {
    selected_device: function() {
      this.start_date = null
      this.end_date = null
      this.dates = []
      this.dates2 = []
      this.chartData = null

      axios
        .get(`/api/measurement_dates/?device_id=${this.selected_device.device_id}`)
        .then((response) => {
          this.dates = response.data
        })
    },

    start_date: function() {
      this.end_date = null
      this.dates2 = this.dates.filter((date) => date >= this.start_date)
    },
  },

  methods: {
    fetchAndDraw() {
      if(!this.selected_device) {
        alert('계측기를 먼저 선택해주세요.')
        return
      }
      if(!this.start_date || !this.end_date) {
        alert('날짜를 먼저 선택해주세요.')
        return
      }

      this.fetchData()
    },

    async fetchData() {
      this.origin_data = []
      this.isLoading = true

      let response = await axios
        .get('/api/measurement_graph/', { params: {
          device_id: this.selected_device.device_id, 
          start_date: this.start_date,
          end_date: this.end_date,
          page_size: 200,
        }})

      const total_count = response.data.count
      while(response.data.next) {
        this.origin_data = this.origin_data.concat(response.data.results)
        this.progress = this.origin_data.length / total_count * 100

        let nextLink = new URL(response.data.next)
        nextLink = nextLink.pathname + nextLink.search

        response = await axios.get(nextLink)
      }

      this.origin_data = this.origin_data.concat(response.data.results)
      this.progress = this.origin_data.length / total_count * 100
      this.isLoading = false
      this.drawGraph()
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
  },

  mounted() {
    axios
      .get('/api/device/')
      .then((response) => {
        this.devices = response.data
      })
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

