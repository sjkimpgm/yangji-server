<template>
  <div>
    <div>
      <span>날짜 선택: </span>
      <select v-model="selected" @change="onChange()">
        <option v-for="option in dates">
          {{ option }}
        </option>
      </select>
    </div>
    <div>
      <button class="btn btn-secondary" v-on:click="start()">Play</button>
      &nbsp;
      <button class="btn btn-secondary" v-on:click="stop()">Stop</button>
      &nbsp;
      <input type="range" v-model.number="idx" min="0" max="100" step="0.1" @change="sliderChange()">
    </div>
    <div>
      <span>{{ current_time }}</span>
    </div>

    <br />

    <div style="width: 800px; height: 600px;" @mousedown="dragStart" @mouseup="dragStop" @mousemove="move" @mousewheel="wheel">
      <vgl-renderer antialias style="width: 800px; height: 600px;">
          <vgl-scene>

            <vgl-ambient-light color="#bbbbbb" intensity="1" />

            <vgl-mesh-lambert-material name="mat_left" color="#000055" />
            <vgl-box-geometry name="slab_left" width=50 height=2 depth=20 />
            <vgl-mesh geometry="slab_left" material="mat_left" :position="`${-x/2-30} ${-z/2 + 2} ${-y/2}`" />

            <vgl-mesh-lambert-material name="mat_right" color="#005500" />
            <vgl-box-geometry name="slab_right" width=50 height=2 depth=20 />
            <vgl-mesh geometry="slab_right" material="mat_right" :position="`${x/2+30} ${z/2 + 2} ${y/2}`" />

            <vgl-directional-light position="0 1 2" intensity="2" />

            <vgl-grid-helper size="100" divisions="20" position="0 0 0" />
            <vgl-grid-helper size="100" divisions="20" position="0 0 20" />
            <vgl-grid-helper size="100" divisions="20" position="0 0 -20" />

          </vgl-scene>
        <vgl-perspective-camera :orbit-position="`${r} ${pi} ${theta}`" />
      </vgl-renderer>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import * as VueGL from "vue-gl";
import { setInterval, clearInterval } from 'timers';

Object.keys(VueGL).forEach(name => {
    Vue.component(name, VueGL[name]);
});

export default {
  components: {
  },
  data() {
    return {
      selected: '--',
      dates: ['--'],
      current_time: null,
      data: null,
      idx: 0,
      isDrag: false,
      timer: null,
      prev_mouse_x: 0,
      prev_mouse_y: 0,
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
    },

    onChange() {
      var vm = this;

      this.idx = 0;

      axios
        .get('/api/measurement/?target_date=' + vm.selected)
        .then(function(response) {
          vm.data = response.data
        });
    },

    sliderChange() {
      if(this.data == null) return;

      var idx = parseInt(this.idx * this.data.length / 100.0)
      console.log(idx)

      // for this change, axis are changed
      this.y = this.data[idx].diff_x
      this.x = this.data[idx].diff_y
      this.z = this.data[idx].diff_z
      this.current_time = this.data[idx].datetime
    },

    update() {
      if(this.idx > 100) {
        this.idx = -1
      }
      this.idx += 1

      this.sliderChange()
    },

    start() {
      if(this.timer != null) return 

      this.timer = setInterval(this.update, 100)
    },

    stop() {
      if(this.timer == null) return 

      clearInterval(this.timer)
      this.timer = null
    },

    dragStart(event) {
      this.isDrag = true
      this.prev_mouse_x = event.offsetX
      this.prev_mouse_y = event.offsetY

      console.log("start")
    },

    dragStop() {
      this.isDrag = false
      console.log("stop")
    },

    move(event) {
      if(this.isDrag == false) return

      var diff_x = event.offsetX - this.prev_mouse_x
      var diff_y = event.offsetY - this.prev_mouse_y

      this.prev_mouse_x = event.offsetX
      this.prev_mouse_y = event.offsetY

      var theta_modifier = 1.0 / 3
      this.theta -= (diff_x) / 400 * 3.14 * theta_modifier

      var pi_modifier = 1.0 / 3
      this.pi -= (diff_y) / 300 * 3.14 * pi_modifier

      if(this.pi < 0) this.pi = 0
      if(this.pi > 3.14) this.pi = 3.14
    },

    wheel(event) {
      var r_modifier = 5
      this.r += event.deltaY / 100 * r_modifier

      // disable parent scroll
      event.stopPropagation()
      event.preventDefault()
    }
  },
  mounted() {
    var vm = this;

    axios
      .get('/api/measurement_dates/')
      .then(function(response) {
        vm.dates = ['--'].concat(response.data);
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
