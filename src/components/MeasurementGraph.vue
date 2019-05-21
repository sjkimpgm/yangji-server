<template>
  <div>
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
      chartData: null,
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
      return value.toFixed(2);
    }
  },
  mounted() {
    var vm = this;

    axios
      .get('/api/measurement/')
      .then(function(response) {
        var converted_data = [['datetime', 'A', 'B', 'C', 'D']];
        for(let m of response.data) {
          let array_m = [new Date(m.datetime), m.measure_a, m.measure_b, m.measure_c, m.measure_d];

          converted_data.push(array_m);
        }

        vm.chartData = converted_data;
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

