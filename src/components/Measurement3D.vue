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
        <v-btn color="primary" @click="start()" :disabled="isLoading || Boolean(timer) || !data.length">Play</v-btn>
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

    <div class="scene" ref="scene" style="height: 600px; width: 800px;" />
  </div>
</template>

<script>
import axios from 'axios'
import { setInterval, clearInterval } from 'timers';

import * as THREE from "three"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"

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
      timer: null,

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

      // For three.js
      camera: null,
      renderer: new THREE.WebGLRenderer(),
      scene: new THREE.Scene(),
      debug: false,
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
    },

    idx: function() {
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

    update() {
      if(this.idx >= this.data.length-1) {
        this.stop()
        this.idx = 0
        return
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
  },

  mounted() {
    const el = this.$refs.scene

    this.renderer.setSize(el.clientWidth, el.clientHeight)
    el.appendChild(this.renderer.domElement)

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      50,
      el.clientWidth / el.clientHeight,
      0.1,
      300
    )
    this.camera.position.y = 100 * Math.sin(Math.PI/6)
    this.camera.position.z = 100 * Math.cos(Math.PI/6)

    // Orbit controls
    function render() {
      this.renderer.render( this.scene, this.camera );
    }

    let controls = new OrbitControls(this.camera, this.renderer.domElement)
    controls.addEventListener( 'change', render);
		controls.minDistance = 20;
		controls.maxDistance = 150;
		controls.maxPolarAngle = Math.PI / 2;

    // Light
    const light1 = new THREE.AmbientLight(0xbbbbbb, 1)
    this.scene.add(light1)

    const light2 = new THREE.DirectionalLight(0xffffff, 2)
    this.scene.add(light2)

    // Grid helper
    const grid = new THREE.GridHelper(100, 20)
    this.scene.add(grid)

    // Slabs
    const boxGeo = new THREE.BoxGeometry(50, 2, 20)
    const matLeft = new THREE.MeshLambertMaterial({ color: 0x000055 })
    const leftSlab = new THREE.Mesh(boxGeo, matLeft)

    const matRight = new THREE.MeshLambertMaterial({ color: 0x005500 })
    const rightSlab = new THREE.Mesh(boxGeo, matRight)

    this.scene.add(leftSlab)
    this.scene.add(rightSlab)
    
    const animate = () => {
      requestAnimationFrame(animate)

      leftSlab.position.set(this.left_x, this.left_z, this.left_y)
      rightSlab.position.set(this.right_x, this.right_z, this.right_y)

      this.renderer.render(this.scene, this.camera)
    };

    animate()

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