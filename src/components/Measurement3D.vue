<template>
  <div>
    <aside class="control-panel">
      <h3>Camera</h3>
      <label>r<input type="range" v-model="r" min="50" max="100"></label>
      <label>pi<input type="range" v-model="pi" min="0" max="3.14" step="0.01"></label>
      <label>theta<input type="range" v-model="theta" min="-3.14" max="3.14" step="0.01"></label>
      <h3>Gab</h3>
      <label>x<input type="range" v-model="x" min="0" max="10"></label>
      <label>y<input type="range" v-model="y" min="0" max="10"></label>
      <label>z<input type="range" v-model="z" min="0" max="10"></label>
    </aside>
    <vgl-renderer antialias style="width: 800px; height: 600px;">
        <vgl-scene>

          <vgl-ambient-light color="#bbbbbb" intensity="1" />

          <vgl-mesh-lambert-material name="mat_left" color="#cc2323" />
          <vgl-box-geometry name="slab_left" width=50 height=2 depth=20 />
          <vgl-mesh geometry="slab_left" material="mat_left" :position="`${-x/2-25} ${-y/2 + 2} ${-z/2}`" />

          <vgl-mesh-lambert-material name="mat_right" color="#2323cc" />
          <vgl-box-geometry name="slab_right" width=50 height=2 depth=20 />
          <vgl-mesh geometry="slab_right" material="mat_right" :position="`${x/2+25} ${y/2 + 2} ${z/2}`" />

          <vgl-directional-light position="0 1 2" intensity="2" />

          <vgl-grid-helper size="100" divisions="20" position="0 0 0" />
          <vgl-grid-helper size="100" divisions="20" position="0 0 20" />
          <vgl-grid-helper size="100" divisions="20" position="0 0 -20" />
          
        </vgl-scene>
      <vgl-perspective-camera :orbit-position="`${r} ${pi} ${theta}`" />
    </vgl-renderer>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import * as VueGL from "vue-gl";

Object.keys(VueGL).forEach(name => {
    Vue.component(name, VueGL[name]);
});

export default {
  components: {
  },
  data() {
    return {
      x: 0,
      y: 0,
      z: 0,
      r: 50,
      pi: 1,
      theta: 0,
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
