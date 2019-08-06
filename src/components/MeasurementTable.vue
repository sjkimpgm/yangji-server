<template>
  <el-table height="600" :data="tableData">

    <el-table-column prop="datetime" label="DateTime" width="200" sortable />
    <el-table-column prop="diff[0]" label="X" width="90" :formatter="measurement_formatter" /> 
    <el-table-column prop="diff[1]" label="Y" width="90" :formatter="measurement_formatter" /> 
    <el-table-column prop="diff[2]" label="Z" width="90" :formatter="measurement_formatter" /> 
    <el-table-column prop="diff[3]" label="theta" width="90" :formatter="measurement_formatter" />
    <el-table-column prop="measure_a" label="A" width="90" :formatter="measurement_formatter" /> 
    <el-table-column prop="measure_b" label="B" width="90" :formatter="measurement_formatter" /> 
    <el-table-column prop="measure_c" label="C" width="90" :formatter="measurement_formatter" /> 
    <el-table-column prop="measure_d" label="D" width="90" :formatter="measurement_formatter" />

  </el-table>
</template>

<script>
//import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  data() {
    return {
      tableData: null    
      }
  },
  methods: {
    measurement_formatter(row, column, value) {
      return value.toFixed(3);
    }
  },
  mounted() {
    var vm = this;

    axios
      .get('/api/measurement/')
      .then(function(response) {
        vm.tableData = response.data;
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
