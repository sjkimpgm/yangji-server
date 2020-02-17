<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="3">
        <v-select label="계측기 선택" :items="devices" item-text="name" return-object v-model="selected_device" />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="tableData"
      :items-per-page="300"
      height="600"
      class="elevation-1"
      fixed-header
      sort-by="datetime"
      sort-desc
    >
      <template v-slot:item.diff_x="{ item }">
        {{item.diff_x.toFixed(2)}}
      </template>
      <template v-slot:item.diff_y="{ item }">
        {{item.diff_y.toFixed(2)}}
      </template>
      <template v-slot:item.diff_z="{ item }">
        {{item.diff_z.toFixed(2)}}
      </template>
      <template v-slot:item.diff_a="{ item }">
        {{item.diff_a.toFixed(2)}}
      </template>
      <template v-slot:item.measure_a="{ item }">
        {{item.measure_a.toFixed(2)}}
      </template>
      <template v-slot:item.measure_b="{ item }">
        {{item.measure_b.toFixed(2)}}
      </template>
      <template v-slot:item.measure_c="{ item }">
        {{item.measure_c.toFixed(2)}}
      </template>
      <template v-slot:item.measure_d="{ item }">
        {{item.measure_d.toFixed(2)}}
      </template>
    </v-data-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      selected_device: null,
      devices: [],
      tableData: [],
      headers: [
        {
          text: '시간',
          align: 'center',
          value: 'datetime',
          sortable: false,
        },
        {
          text: 'X',
          align: 'center',
          value: 'diff_x',
          sortable: false,
        },
        {
          text: 'Y',
          align: 'center',
          value: 'diff_y',
          sortable: false,
        },
        {
          text: 'Z',
          align: 'center',
          value: 'diff_z',
          sortable: false,
        },
        {
          text: 'θ',
          align: 'center',
          value: 'diff_a',
          sortable: false,
        },
        {
          text: 'A',
          align: 'center',
          value: 'measure_a',
          sortable: false,
        },
        {
          text: 'B',
          align: 'center',
          value: 'measure_b',
          sortable: false,
        },
        {
          text: 'C',
          align: 'center',
          value: 'measure_c',
          sortable: false,
        },
        {
          text: 'D',
          align: 'center',
          value: 'measure_d',
          sortable: false,
        },
      ],
    }
  },

  watch: {
    selected_device: function() {
      this.stop();

      var now = new Date();
      now.setMinutes(now.getMinutes() - 3);
      var now_str = this.date_format(now);

      this.tableData = []
      axios
        .get('/api/measurement_recent/?device_id=' + this.selected_device.device_id + '&last_time=' + now_str)
        .then((response) => {
          this.tableData = response.data

          this.start();
        });
    }
  },

  methods: {
    update() {
      var last_time = this.tableData[this.tableData.length-1].datetime;

      axios
        .get('/api/measurement_recent/?device_id=' + this.selected_device.device_id + '&last_time=' + last_time)
        .then((response) => {
          this.tableData = this.tableData.concat(response.data)
          this.tableData = this.tableData.slice(this.tableData.length - 300)
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
    }
  },

  mounted() {
    axios
      .get('/api/device/')
      .then((response) => {
        this.devices = response.data;
      });
  },

  beforeDestroy() {
    this.stop();
  }
};
</script>
