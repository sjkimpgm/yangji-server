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
        <v-btn color="primary" @click="fetchAndDraw">데이터 로딩</v-btn>
      </v-col>
    </v-row>

    <v-row justify="start">
      <v-col cols="1">
        <v-btn color="primary" @click="start()" :disabled="isLoading || Boolean(timer)">Play</v-btn>
      </v-col>
      <v-col cols="1">
        <v-btn color="primary" @click="stop()" :disabled="isLoading || !timer">Stop</v-btn>
      </v-col>
      <v-col cols="2">
        <v-slider v-model.number="idx" min="0" :max="this.data.length" step="1" @change="sliderChange" />
      </v-col>
      <v-col cols="2">
        <v-checkbox v-model="leftFixed" label="고정단" class="ma-0" />
      </v-col>

      <v-col cols="2" class="pa-1">
        <v-text-field label="시간" v-model="current_time" read-only hide-details />
      </v-col>

      <v-col cols="1" class="pa-1">
        <v-text-field label="X" v-model="x" read-only hide-details />
      </v-col>
      <v-col cols="1" class="pa-1">
        <v-text-field label="Y" v-model="y" read-only hide-details />
      </v-col>
      <v-col cols="1" class="pa-1">
        <v-text-field label="Z" v-model="z" read-only hide-details />
      </v-col>
      <v-col cols="1" class="pa-1">
        <v-text-field label="θ" v-model="a" read-only hide-details />
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

    <br />

    <div style="width: 800px; height: 600px;" @mousedown="dragStart" @mouseup="dragStop" @mousemove="move" @mousewheel="wheel">
      <vgl-renderer antialias style="width: 800px; height: 600px;">
          <vgl-scene>

            <vgl-ambient-light color="#bbbbbb" intensity="1" />

            <vgl-mesh-lambert-material name="mat_left" color="#000055" />
            <vgl-box-geometry name="slab_left" width=50 height=2 depth=20 />
            <vgl-mesh geometry="slab_left" material="mat_left" :position="`${left_x} ${left_z} ${left_y}`" />

            <vgl-mesh-lambert-material name="mat_right" color="#005500" />
            <vgl-box-geometry name="slab_right" width=50 height=2 depth=20 />
            <vgl-mesh geometry="slab_right" material="mat_right" :position="`${right_x} ${right_z} ${right_y}`" />

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
      selected_device: null,
      devices: [],
      start_date: null,
      end_date: null,
      dates: [],
      dates2: [],
      isLoading: false,
      progress: 0,
      current_time: null,
      data: [],
      idx: 0,
      isDrag: false,
      timer: null,
      prev_mouse_x: 0,
      prev_mouse_y: 0,
      r: 50,
      pi: 1,
      theta: 0,
      // For display
      x: 0,
      y: 0,
      z: 0,
      a: 0,
      leftFixed: false,
      // For left slab
      left_x: -30,
      left_y: 0,
      left_z: 2,
      left_a: 0,
      // For right slab
      right_x: 30,
      right_y: 0,
      right_z: 2,
      right_a: 0,
    }
  },

  watch: {
    selected_device: function() {
      this.start_date = null
      this.end_date = null
      this.dates = []
      this.dates2 = []
      this.data = []

      axios
        .get(`/api/measurement_dates/?device_id=${this.selected_device.device_id}`)
        .then((response) => {
          this.dates = response.data
        })
    },

    start_date: function() {
      this.end_date = null
      this.dates2 = this.dates.filter((date) => date >= this.start_date)
    }
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
      this.stop()
      this.data = []
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
        this.data = this.data.concat(response.data.results)
        this.progress = this.data.length / total_count * 100

        let nextLink = new URL(response.data.next)
        nextLink = nextLink.pathname + nextLink.search

        response = await axios.get(nextLink)
      }

      this.data = this.data.concat(response.data.results)
      this.progress = this.data.length / total_count * 100
      this.isLoading = false
    },

    sliderChange() {
      if(!this.data) return;

      // FIXME(sjkim): for 백제큰다리, x-y axis are changed
      this.current_time = this.data[this.idx].datetime
      this.y = this.data[this.idx].diff_x.toFixed(2)
      this.x = this.data[this.idx].diff_y.toFixed(2)
      this.z = this.data[this.idx].diff_z.toFixed(2)
      this.a = this.data[this.idx].diff_a.toFixed(2)

      if(this.leftFixed) {
        this.left_x = -30
        this.left_y = 0
        this.left_z = +2

        this.right_x = this.x/1 + 30
        this.right_y = this.y/1
        this.right_z = this.z/1 + 2
      } else {
        this.left_x = -this.x/2 - 30
        this.left_y = -this.y/2
        this.left_z = -this.z/2 + 2

        this.right_x = this.x/2 + 30
        this.right_y = this.y/2
        this.right_z = this.z/2 + 2
      }
    },

    update() {
      this.sliderChange()

      if(this.idx >= this.data.length-1) {
        this.stop()
        this.idx = 0
        this.sliderChange()
      }

      this.idx += 1
    },

    start() {
      if(this.timer != null) return 

      this.timer = setInterval(this.update, 50)
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
    },

    dragStop() {
      this.isDrag = false
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
    }, 
    onChangeDevice() {
      this.stop();
      this.dates = []

      axios
        .get('/api/measurement_dates/', {params: {device_id: this.selected_device}})
        .then(function(response) {
          this.dates = response.data
        })
    },
  },

  mounted() {
    axios
      .get('/api/device/')
      .then((response) => {
        this.devices = response.data
      })
  },

  beforeDestroy() {
    this.stop();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
