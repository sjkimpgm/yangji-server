<template>
  <div>
    <div>
      <span>계측기 선택: </span>
      <select v-model="device" @change="onChangeDevice()">
        <option v-for="option in devices" :key="option.name">
          {{ option.name }}
        </option>
      </select>
    </div>

    <el-table height="600" :data="tableData" :default-sort = "{prop: 'datetime', order: 'descending'}" >

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
      return value.toFixed(1);
    },

    update() {
      var vm = this;
      var last_time = this.tableData[this.tableData.length-1].datetime;

      axios
        .get('/api/measurement_recent/?device_id=' + vm.selected_device.device_id + '&last_time=' + last_time)
        .then(function(response) {
          vm.tableData = vm.tableData.concat(response.data)
          vm.tableData = vm.tableData.slice(vm.tableData.length - 300)
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
          vm.tableData = response.data

          vm.start();
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
  },

  beforeDestroy() {
    this.stop();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

