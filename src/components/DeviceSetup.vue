<template>
  <v-container fluid>
    <v-row>
      <v-select
        v-model="targetDevice"
        label="계측기 선택"
        :items="devices"
        item-text="name"
        return-object
        />
    </v-row>

    <v-row justify="space-around">
      <v-btn color="primary" width="200" @click="updateDevice">저장</v-btn>
    </v-row>

    <div v-if="targetDevice">
      <v-row>
        <v-col cols="4">
          <v-text-field label="이름" v-model="targetDevice.name" />
        </v-col>
        <v-col cols="4">
          <v-text-field label="기기 ID" v-model="targetDevice.device_id" />
        </v-col>
        <v-col cols="4">
          <v-text-field label="기기 타입" v-model="targetDevice.device_type" hint="후보: default, adv_v3" />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p class="text-right">경고 최대값</p>
        </v-col>
        <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`limit_max_${idx}`">
          <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.limit_max[idx]" type="number" hide-details />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p class="text-right">경고 최소값</p>
        </v-col>
        <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`limit_min_${idx}`">
          <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.limit_min[idx]" type="number" hide-details />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p class="text-right">유격 기본값</p>
        </v-col>
        <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`default_offset_${idx}`">
          <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.default_offset[idx]" type="number" hide-details />
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-10">
        <span class="red--text">아래 값들은 기기 측정 값에서 실제 유격을 계산하는데 사용되는 값입니다. 함부로 변경하지 말아주세요.</span>
      </v-row>

      <v-row justify="space-between">
        <v-col cols="5">
          <v-row>
            <span>Inverted matrix</span>
          </v-row>
          <v-row v-for="i in [0, 1, 2, 3]" :key="`inv_${i}`">
            <v-col v-for="j in [0, 1, 2, 3]" :key="`inv_${i}_${j}`" cols="3" class="py-0 px-1">
              <v-text-field v-model.number="targetDevice.params.inv_matrix[i][j]" type="number" hide-details />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="5">
          <v-row>
            <span>Matrix</span>
          </v-row>
          <v-row v-for="i in [0, 1, 2, 3]" :key="`inv_${i}`">
            <v-col v-for="j in [0, 1, 2, 3]" :key="`inv_${i}_${j}`" cols="3" class="py-0 px-1">
              <v-text-field v-model.number="targetDevice.params.matrix[i][j]" type="number" hide-details />
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <div v-if="targetDevice.device_type === 'default'">
        <v-row>
          <v-col>
            <p class="text-right">F_a</p>
          </v-col>
          <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`F_a_${idx}`">
            <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.F_a[idx]" type="number" hide-details />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <p class="text-right">F_b</p>
          </v-col>
          <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`F_b_${idx}`">
            <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.F_b[idx]" type="number" hide-details />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <p class="text-right">V_k</p>
          </v-col>
          <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`L_k_${idx}`">
            <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.L_k[idx]" type="number" hide-details />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <p class="text-right">V_0</p>
          </v-col>
          <v-col cols="2" v-for="idx in [0,1,2,3]" :key="`V_0_${idx}`">
            <v-text-field :label="diffLabel[idx]" v-model.number="targetDevice.params.V_0[idx]" type="number" hide-details />
          </v-col>
        </v-row>

      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'

// FIXME(sjkim): For axios update. Please find better way
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

export default {
  data() {
    return {
      devices: [],
      targetDevice: null,
      diffLabel: ['X', 'Y', 'Z', 'θ']
    }
  },
  methods: {
    updateDevice: function() {
      if(!this.targetDevice) {
        alert("먼저 계측기를 선택해주세요.")
        return
      }

      axios
        .patch(`/api/device/${this.targetDevice.id}/`, this.targetDevice)
        .then(() => {
          alert("변경 사항이 저장되었습니다.")
        });
    }
  },

  mounted() {
    axios.get('/api/device')
    .then((response) => {
      this.devices = response.data.map((device) => {
        if(!device.params.limit_max) {
          device.params.limit_max = [10, 10, 10, 10]
        }

        if(!device.params.limit_min) {
          device.params.limit_min = [-10, -10, -10, -10]
        }

        if(!device.params.default_offset) {
          device.params.default_offset = [0, 0, 0, 0]
        }

        return device
      })
    })
  }
};
</script>