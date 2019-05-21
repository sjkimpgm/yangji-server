<template>
  <el-table height="600" :data="tableData">

    <el-table-column prop="datetime" label="DateTime" width="360" sortable />
    <el-table-column prop="measure_a" label="A" width="180" :formatter="measurement_formatter" /> 
    <el-table-column prop="measure_b" label="B" width="180" :formatter="measurement_formatter" /> 
    <el-table-column prop="measure_c" label="C" width="180" :formatter="measurement_formatter" /> 
    <el-table-column prop="measure_d" label="D" width="180" :formatter="measurement_formatter" />

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
      return value.toFixed(2);
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
