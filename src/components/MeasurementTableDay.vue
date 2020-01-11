<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="4">
        <v-select label="계측기 선택" :items="devices" item-text="name" item-value="device_id" v-model="selected_device" />
      </v-col>

      <v-col cols="4">
        <v-select label="시작 날짜 선택" :items="dates" v-model="start_date" />
      </v-col>

      <v-col cols="4">
        <v-select label="종료 날짜 선택" :items="dates2" v-model="end_date" />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="tableData"
      :items-per-page="20"
      :loading="isLoading"
      :footer-props="{
        'items-per-page-options': [10, 20, 50],
        'showFirstLastPage': true,
      }"
      height="600"
      class="elevation-1"
      fixed-header
    >
      <template v-slot:item.min_x="{ item }">{{item.min_x.toFixed(2)}}</template>
      <template v-slot:item.min_y="{ item }">{{item.min_y.toFixed(2)}}</template>
      <template v-slot:item.min_z="{ item }">{{item.min_z.toFixed(2)}}</template>
      <template v-slot:item.min_a="{ item }">{{item.min_a.toFixed(2)}}</template>
      <template v-slot:item.max_x="{ item }">{{item.max_x.toFixed(2)}}</template>
      <template v-slot:item.max_y="{ item }">{{item.max_y.toFixed(2)}}</template>
      <template v-slot:item.max_z="{ item }">{{item.max_z.toFixed(2)}}</template>
      <template v-slot:item.max_a="{ item }">{{item.max_a.toFixed(2)}}</template>
      <template v-slot:item.diff_x="{ item }">{{item.diff_x.toFixed(2)}}</template>
      <template v-slot:item.diff_y="{ item }">{{item.diff_y.toFixed(2)}}</template>
      <template v-slot:item.diff_z="{ item }">{{item.diff_z.toFixed(2)}}</template>
      <template v-slot:item.diff_a="{ item }">{{item.diff_a.toFixed(2)}}</template>
    </v-data-table>
  </div>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  data() {
    return {
      selected_device: null,
      devices: [],
      start_date: null,
      end_date: null,
      dates: [],
      dates2: [],
      tableData: [],
      isLoading: false,
      headers: [
        {
          text: '날짜',
          align: 'center',
          value: 'date',
          width: 150
        },
        {
          text: 'min(X)',
          align: 'center',
          value: 'min_x',
        },
        {
          text: 'max(X)',
          align: 'center',
          value: 'max_x',
        },
        {
          text: 'diff(X)',
          align: 'center',
          value: 'diff_x',
        },
        {
          text: 'min(y)',
          align: 'center',
          value: 'min_y',
        },
        {
          text: 'max(y)',
          align: 'center',
          value: 'max_y',
        },
        {
          text: 'diff(y)',
          align: 'center',
          value: 'diff_y',
        },
        {
          text: 'min(Z)',
          align: 'center',
          value: 'min_z',
        },
        {
          text: 'max(Z)',
          align: 'center',
          value: 'max_z',
        },
        {
          text: 'diff(Z)',
          align: 'center',
          value: 'diff_z',
        },
        {
          text: 'min(θ)',
          align: 'center',
          value: 'min_a',
        },
        {
          text: 'max(θ)',
          align: 'center',
          value: 'max_a',
        },
        {
          text: 'diff(θ)',
          align: 'center',
          value: 'diff_a',
        },
      ],
      }
  },

  watch: {
    selected_device: function() {
      this.start_date = null
      this.end_date = null
      this.dates = []
      this.dates2 = []
      this.tableData = []

      axios
        .get(`/api/measurement_dates/?device_id=${this.selected_device}`)
        .then((response) => {
          this.dates = response.data
        })
    },

    start_date: function() {
      this.end_date = null
      this.dates2 = this.dates.filter((date) => date >= this.start_date)
    },

    end_date: function() {
      if(!this.end_date) return

      this.fetchData()
    }
  },

  methods: {
    fetchData() {
      this.tableData = []
      this.isLoading = true

      axios
        .get('/api/measurement_aggr/', { params: {
          device_id: this.selected_device, 
          start_date: this.start_date,
          end_date: this.end_date,
        }}).then((response) => {
          this.tableData = response.data
          this.isLoading = false
        })
    },

    measurement_formatter(row, column, value) {
      return value.toFixed(1);
    },
    onChangeStartDate() {
      var vm = this;
      vm.tableData = [];
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
      vm.tableData = [];

      axios
        .get('/api/measurement_aggr/?device_id=' + vm.selected_device.device_id + '&start_date=' + vm.start_date + '&end_date=' + vm.end_date)
        .then(function(response) {
          vm.tableData = response.data;
        });
    }, 

    onChangeDevice() {
      var vm = this;
      vm.tableData = [];
      vm.start_date =  '--'
      vm.end_date = '--'
      vm.dates = ['--']
      vm.dates2 = ['--']

      vm.selected_device = this.devices.find(function(d) { return d.name == vm.device});

      axios
        .get('/api/measurement_dates/?device_id=' + vm.selected_device.device_id)
        .then(function(response) {
          vm.dates = ['--'].concat(response.data);
        });
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
