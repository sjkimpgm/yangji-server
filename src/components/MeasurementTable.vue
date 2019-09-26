<template>
  <div>
      <span>계측기 선택: </span>
      <select v-model="device" @change="onChangeDevice()">
        <option v-for="option in devices">
          {{ option.name }}
        </option>
      </select>

      &nbsp;
      &nbsp;
      &nbsp;

    <span>날짜 선택: </span>
    <select v-model="selected_date" @change="onChangeDate($event)">
      <option v-for="option in dates">
        {{ option }}
      </option>
    </select>

    <el-table height="600" :data="tableData">

      <el-table-column prop="datetime" label="DateTime" width="200" sortable />
      <el-table-column prop="diff_x" label="X" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="diff_y" label="Y" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="diff_z" label="Z" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="diff_a" label="theta" width="90" :formatter="measurement_formatter" />
      <el-table-column prop="measure_a" label="A" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="measure_b" label="B" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="measure_c" label="C" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="measure_d" label="D" width="90" :formatter="measurement_formatter" />

    </el-table>
  </div>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  data() {
    return {
      device: '--',
      selected_device: null,
      devices: ['--'],
      selected_date: '--',
      dates: ['--'],
      tableData: null    
      }
  },
  methods: {
    measurement_formatter(row, column, value) {
      return value.toFixed(3);
    },
    onChangeDate(event) {
      var vm = this;
      vm.tableData = null;

      axios
        .get('/api/measurement/?device_id=' + vm.selected_device.device_id + '&target_date=' + vm.selected_date)
        .then(function(response) {
          vm.tableData = response.data;
        });
    },

    onChangeDevice() {
      var vm = this;
      vm.dates = ['--'];
      vm.selected_date = '--';

      vm.selected_device = this.devices.find(function(d) { return d.name == vm.device});

      axios
        .get('/api/measurement_dates/?device_id=' + vm.selected_device.device_id)
        .then(function(response) {
          vm.dates = ['--'].concat(response.data);
        });
    },
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
