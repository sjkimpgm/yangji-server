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
        <v-slider v-model.number="idx" min="0" :max="this.data.length" step="1" />
      </v-col>
      <v-col cols="2">
        <v-checkbox v-model="leftFixed" label="고정단" class="ma-0" />
      </v-col>

      <v-col cols="2" class="pa-1">
        <v-text-field label="시간" v-model="current_time" read-only hide-details />
      </v-col>

      <v-col cols="1" class="pa-1">
        <v-text-field label="X" v-model="x" readonly hide-details />
      </v-col>
      <v-col cols="1" class="pa-1">
        <v-text-field label="Y" v-model="y" readonly hide-details />
      </v-col>
      <v-col cols="1" class="pa-1">
        <v-text-field label="Z" v-model="z" readonly hide-details />
      </v-col>
      <v-col cols="1" class="pa-1">
        <v-text-field label="θ" v-model="a" readonly hide-details />
      </v-col>
    </v-row>

    <v-row justify="end">
      <v-col cols="2" v-if="isLoading">
        <p>데이터 로딩: </p>
      </v-col>
      <v-col cols="4" v-if="isLoading">
        <v-progress-linear :value="progress"></v-progress-linear>
      </v-col>
      
      <v-col cols="2" class="pa-1" v-if="selected_device">
        <p>유격 기본값:</p>
      </v-col>

      <v-col cols="1" class="pa-1" v-if="selected_device">
        <v-text-field label="X" v-model.number="selected_device.params.default_offset[0]" hide-details />
      </v-col>
      <v-col cols="1" class="pa-1" v-if="selected_device">
        <v-text-field label="Y" v-model.number="selected_device.params.default_offset[1]" hide-details />
      </v-col>
      <v-col cols="1" class="pa-1" v-if="selected_device">
        <v-text-field label="Z" v-model.number="selected_device.params.default_offset[2]" hide-details />
      </v-col>
      <v-col cols="1" class="pa-1" v-if="selected_device">
        <v-text-field label="θ" v-model.number="selected_device.params.default_offset[3]" hide-details />
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
      renderer: new THREE.WebGLRenderer({antialias: true}),
      scene: new THREE.Scene(),
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
      this.y = this.data[this.idx].diff_x + this.selected_device.params.default_offset[1]
      this.x = this.data[this.idx].diff_y + this.selected_device.params.default_offset[0]
      this.z = this.data[this.idx].diff_z + this.selected_device.params.default_offset[2]
      this.a = this.data[this.idx].diff_a + this.selected_device.params.default_offset[3]

      this.x = this.x.toFixed(2)
      this.y = this.y.toFixed(2)
      this.z = this.z.toFixed(2)
      this.a = this.a.toFixed(2)

      // prevent overlapping slabs
      this.calc_x = Math.max(0, this.x)

      if(this.leftFixed) {
        this.left_x = -25
        this.left_y = 0
        this.left_z = +2

        this.right_x = this.calc_x/1 + 25
        this.right_y = this.y/1
        this.right_z = this.z/1 + 2
      } else {
        this.left_x = -this.calc_x/2 - 25
        this.left_y = -this.y/2
        this.left_z = -this.z/2 + 2

        this.right_x = this.calc_x/2 + 25
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
      this.idx = 0
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

    // Scene
    this.scene.background = new THREE.Color( 0xe0e0e0 );
		this.scene.fog = new THREE.Fog( 0xe0e0e0, 200, 300 );

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      50,
      el.clientWidth / el.clientHeight,
      0.1,
      300
    )
    this.camera.position.y = 100
    this.camera.position.z = 100
    this.camera.lookAt(new THREE.Vector3(0, 0, 0))

    // Orbit controls
    let controls = new OrbitControls(this.camera, this.renderer.domElement)
		controls.minDistance = 20;
		controls.maxDistance = 200;
		controls.maxPolarAngle = Math.PI / 2;

    // Light
    let light = new THREE.HemisphereLight( 0xffffff, 0x444444 )
		light.position.set( 0, 20, 0 )
		this.scene.add( light )

		light = new THREE.DirectionalLight( 0xffffff )
		light.position.set( 0, 20, 10 )
    this.scene.add( light )
    
    // ground
		let mesh = new THREE.Mesh( new THREE.PlaneBufferGeometry( 2000, 2000 ), new THREE.MeshPhongMaterial( { color: 0x999999, depthWrite: false } ) )
		mesh.rotation.x = - Math.PI / 2
		this.scene.add( mesh )

		let grid = new THREE.GridHelper( 1000, 200, 0x000000, 0x000000 )
		grid.material.opacity = 0.2
    grid.material.transparent = true
    grid.position.y = -3
		this.scene.add( grid )

    // Slabs
    function createSlab(color) {
      const slab = new THREE.Group()

      const mat = new THREE.MeshLambertMaterial({ color })

      const boardGeo = new THREE.BoxGeometry(50, 2, 20)
      const sideGeo = new THREE.BoxGeometry(50, 0.5, 1)
      const sidePillarGeo = new THREE.CylinderGeometry(0.3, 0.3, 2, 10)
      const pillarGeo = new THREE.CylinderGeometry(4, 4, 5, 20)

      let mesh = new THREE.Mesh(boardGeo, mat)
      slab.add(mesh)

      mesh = new THREE.Mesh(sideGeo, mat)
      mesh.position.y = 3


      for(let i = -1; i <= 1; i += 2) {
        mesh = mesh.clone()
        mesh.position.z = i * 9
        slab.add(mesh)

        let mesh2 = new THREE.Mesh(sidePillarGeo, mat)
        mesh2.position.y = 2
        mesh2.position.z = i * 9
        for(let j = -5; j <= 5; ++j) {
          mesh2 = mesh2.clone()
          mesh2.position.x = j * 4.8
          slab.add(mesh2)
        }
      }

      // pillar
      mesh = new THREE.Mesh(pillarGeo, mat)
      mesh.position.y = -3

      for(let i = -1; i <= 1; i += 2) {
        mesh = mesh.clone()
        mesh.position.x = i * 20
        slab.add(mesh)
      }

      return slab
    }
    const leftSlab = createSlab(0x202027)
    const rightSlab = createSlab(0x202720)

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