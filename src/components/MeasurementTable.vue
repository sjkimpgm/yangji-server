<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="4">
        <v-select label="계측기 선택" :items="devices" item-text="name" item-value="device_id" v-model="selected_device" />
      </v-col>

      <v-col cols="4">
        <v-select label="날짜 선택" :items="dates" v-model="selected_date" />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="tableData"
      :items-per-page="100"
      :loading="isLoading"
      :options.sync="options"
      :server-items-length="items_total_count"
      :footer-props="{
        'items-per-page-options': [50, 100, 200],
        'showFirstLastPage': true,
      }"
      height="600"
      class="elevation-1"
      fixed-header
    >
      <template v-slot:footer.page-text="{pageStart, pageStop, itemsLength}">
        <v-row>
          <v-col align-self="center">
            <span>{{ pageStart }}-{{ pageStop }} of {{ itemsLength }}</span>
          </v-col>
          <v-col align-self="center">
            <v-text-field
              v-model.number="options.page"
              type="number"
              hide-details
              single-line
              dense
              class="my-0 py-0 caption"
            />
          </v-col>
        </v-row>
      </template> 
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
//import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  data() {
    return {
      selected_device: null,
      devices: [],
      selected_date: null,
      dates: [],
      tableData: [],
      isLoading: false,
      options: {},
      items_total_count: null,
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
  mounted() {
    axios
      .get('/api/device/')
      .then((response) => {
        this.devices = response.data
      })
  },

  watch: {
    selected_device: function() {
      this.selected_date = null
      this.dates = []
      this.tableData = []

      axios
        .get(`/api/measurement_dates/?device_id=${this.selected_device}`)
        .then((response) => {
          this.dates = response.data
        })
    },

    selected_date: function() {
      if(!this.selected_date) return

      this.fetchData()
    },

    options: {
      handler () {
        if(!this.selected_device || !this.selected_date) return

        this.fetchData()
      },
      deep: true
    }
  },
  methods: {
    fetchData() {
      this.tableData = []
      this.isLoading = true

      axios
        .get('/api/measurement/', { params: {
          device_id: this.selected_device, 
          target_date: this.selected_date,
          page: this.options.page,
          page_size: this.options.itemsPerPage
        }}).then((response) => {
          this.items_total_count = response.data.count
          this.tableData = response.data.results
          this.isLoading = false
        })
    }
  },
}
</script>
