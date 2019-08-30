<template>
  <div>
    <div>
      <span>시작 날짜 선택: </span>
      <select v-model="start_date" @change="onChangeStartDate()">
        <option v-for="option in dates">
          {{ option }}
        </option>
      </select>

      &nbsp;
      &nbsp;
      &nbsp;

      <span>종료 날짜 선택: </span>
      <select v-model="end_date" @change="onChangeEndDate()">
        <option v-for="option in dates2">
          {{ option }}
        </option>
      </select>
    </div>

    <el-table height="600" :data="tableData">

      <el-table-column prop="date" label="DateTime" width="200" sortable />
      <el-table-column prop="min_x" label="min(X)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="max_x" label="max(X)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="diff_x" label="diff(X)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="min_y" label="min(Y)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="max_y" label="max(Y)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="diff_y" label="diff(Y)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="min_z" label="min(Z)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="max_z" label="max(Z)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="diff_z" label="diff(Z)" width="90" :formatter="measurement_formatter" /> 
      <el-table-column prop="min_a" label="min(θ)" width="90" :formatter="measurement_formatter" />
      <el-table-column prop="max_a" label="max(θ)" width="90" :formatter="measurement_formatter" />
      <el-table-column prop="diff_a" label="diff(θ)" width="90" :formatter="measurement_formatter" /> 

    </el-table>
  </div>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  data() {
    return {
      start_date: '--',
      end_date: '--',
      dates: ['--'],
      dates2: ['--'],
      tableData: null    
      }
  },
  methods: {
    measurement_formatter(row, column, value) {
      return value.toFixed(3);
    },
    onChangeStartDate() {
      var vm = this;
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
        .get('/api/measurement_aggr/?start_date=' + vm.start_date + '&end_date=' + vm.end_date)
        .then(function(response) {
          vm.tableData = response.data;
        });
    }
  },
  mounted() {
    var vm = this;

    axios
      .get('/api/measurement_dates/')
      .then(function(response) {
        vm.dates = ['--'].concat(response.data);
      });

  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
