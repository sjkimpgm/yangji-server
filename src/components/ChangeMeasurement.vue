<template>
  <div>
    <form class="form" v-on:submit="sendPost">
      <button type="submit" class="btn btn-primary">저장 및 계산</button>
      <table>
        <tr> <td> V_A = <input class="border rounded" type="number" step="0.0001" v-model.number="V_A"> </td> </tr>
        <tr> <td> V_B = <input class="border rounded" type="number" step="0.0001" v-model.number="V_B"> </td> </tr>
        <tr> <td> V_C = <input class="border rounded" type="number" step="0.0001" v-model.number="V_C"> </td> </tr>
        <tr> <td> V_D = <input class="border rounded" type="number" step="0.0001" v-model.number="V_D"> </td> </tr>

        <tr>&nbsp;</tr>

        <tr> <td> &Delta;x = {{delta_x.toFixed(4)}} </td> </tr>
        <tr> <td> &Delta;y = {{delta_y.toFixed(4)}} </td> </tr>
        <tr> <td> &Delta;z = {{delta_z.toFixed(4)}} </td> </tr>
        <tr> <td> &Delta;&theta;y = {{delta_theta_y.toFixed(4)}} </td> </tr>

        <tr>&nbsp;</tr>

        <tr> <td> &Delta;L_A = {{delta_L_A.toFixed(4)}} </td> </tr>
        <tr> <td> &Delta;L_B = {{delta_L_B.toFixed(4)}} </td> </tr>
        <tr> <td> &Delta;L_C = {{delta_L_C.toFixed(4)}} </td> </tr>
        <tr> <td> &Delta;L_D = {{delta_L_D.toFixed(4)}} </td> </tr>

        <tr>&nbsp;</tr>

        <tr> <td> L_A = {{L_A.toFixed(4)}} </td> </tr>
        <tr> <td> L_B = {{L_B.toFixed(4)}} </td> </tr>
        <tr> <td> L_C = {{L_C.toFixed(4)}} </td> </tr>
        <tr> <td> L_D = {{L_D.toFixed(4)}} </td> </tr>

        <tr>&nbsp;</tr>

        <tr> <td> L_A0 = {{L_A0.toFixed(4)}} </td> </tr>
        <tr> <td> L_B0 = {{L_B0.toFixed(4)}} </td> </tr>
        <tr> <td> L_C0 = {{L_C0.toFixed(4)}} </td> </tr>
        <tr> <td> L_D0 = {{L_D0.toFixed(4)}} </td> </tr>

        <tr>&nbsp;</tr>

        <tr> <td> f_A = {{f_A.toFixed(4)}} = {{device.f_Aa.toFixed(4)}} &times; {{V_A.toFixed(4)}} &#43; {{device.f_Ab.toFixed(4)}} </td> </tr>
        <tr> <td> f_B = {{f_B.toFixed(4)}} = {{device.f_Ba.toFixed(4)}} &times; {{V_B.toFixed(4)}} &#43; {{device.f_Bb.toFixed(4)}} </td> </tr>
        <tr> <td> f_C = {{f_C.toFixed(4)}} = {{device.f_Ca.toFixed(4)}} &times; {{V_C.toFixed(4)}} &#43; {{device.f_Cb.toFixed(4)}} </td> </tr>
        <tr> <td> f_D = {{f_D.toFixed(4)}} = {{device.f_Da.toFixed(4)}} &times; {{V_D.toFixed(4)}} &#43; {{device.f_Db.toFixed(4)}} </td> </tr>

      </table>

      <div class="row">
        <h3>Matrix</h3>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.M00.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M01.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M02.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M03.toFixed(4)}}</div>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.M10.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M11.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M12.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M13.toFixed(4)}}</div>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.M20.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M21.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M22.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M23.toFixed(4)}}</div>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.M30.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M31.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M32.toFixed(4)}}</div>
        <div class="col-1 border">{{device.M33.toFixed(4)}}</div>
      </div>

      <div class="row">
        <h3>Inverse matrix</h3>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.inv00.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv01.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv02.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv03.toFixed(4)}}</div>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.inv10.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv11.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv12.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv13.toFixed(4)}}</div>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.inv20.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv21.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv22.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv23.toFixed(4)}}</div>
      </div>
      <div class="row">
        <div class="col-1 border">{{device.inv30.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv31.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv32.toFixed(4)}}</div>
        <div class="col-1 border">{{device.inv33.toFixed(4)}}</div>
      </div>

    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      device: {
        'f_Aa': 0,
        'f_Ba': 0,
        'f_Ca': 0,
        'f_Da': 0,
        'f_Ab': 0,
        'f_Bb': 0,
        'f_Cb': 0,
        'f_Db': 0,
        'L_Ak': 0,
        'L_Bk': 0,
        'L_Ck': 0,
        'L_Dk': 0,
        'V_A0': 0,
        'V_B0': 0,
        'V_C0': 0,
        'V_D0': 0,
        'M00': 0,
        'M01': 0,
        'M02': 0,
        'M03': 0,
        'M10': 0,
        'M11': 0,
        'M12': 0,
        'M13': 0,
        'M20': 0,
        'M21': 0,
        'M22': 0,
        'M23': 0,
        'M30': 0,
        'M31': 0,
        'M32': 0,
        'M33': 0,
        'inv00': 0,
        'inv01': 0,
        'inv02': 0,
        'inv03': 0,
        'inv10': 0,
        'inv11': 0,
        'inv12': 0,
        'inv13': 0,
        'inv20': 0,
        'inv21': 0,
        'inv22': 0,
        'inv23': 0,
        'inv30': 0,
        'inv31': 0,
        'inv32': 0,
        'inv33': 0,
      },
      V_A: 0.0,
      V_B: 0.0,
      V_C: 0.0,
      V_D: 0.0,
      }
  },
  methods: {
    sendPost: function() {
      var vm = this;

      // axios.post('/api/calc_device/', vm.device)
      // .then(function(res) {
      //   console.log(res.data)
      //   vm.updateDevice();
      // }, function() {
      // 	console.log('failed')
      // })
    },
    updateDevice: function() {
      var vm = this;

      axios
        .get('/api/device/')
        .then(function(response) {
          vm.device = response.data[0];
        });
    }
  },
  computed: {
    f_A: function() { return this.device.f_Aa * this.V_A  + this.device.f_Ab },
    f_B: function() { return this.device.f_Ba * this.V_B  + this.device.f_Bb },
    f_C: function() { return this.device.f_Ca * this.V_C  + this.device.f_Cb },
    f_D: function() { return this.device.f_Da * this.V_D  + this.device.f_Db },

    L_A: function() { return this.device.L_Ak + this.f_A },
    L_B: function() { return this.device.L_Bk + this.f_B },
    L_C: function() { return this.device.L_Ck + this.f_C },
    L_D: function() { return this.device.L_Dk + this.f_D },

    L_A0: function() { return this.device.L_Ak + this.device.f_Aa * this.device.V_A0  + this.device.f_Ab },
    L_B0: function() { return this.device.L_Bk + this.device.f_Ba * this.device.V_B0  + this.device.f_Bb },
    L_C0: function() { return this.device.L_Ck + this.device.f_Ca * this.device.V_C0  + this.device.f_Cb },
    L_D0: function() { return this.device.L_Dk + this.device.f_Da * this.device.V_D0  + this.device.f_Db },

    delta_L_A: function() { return this.L_A - this.L_A0 },
    delta_L_B: function() { return this.L_B - this.L_B0 },
    delta_L_C: function() { return this.L_C - this.L_C0 },
    delta_L_D: function() { return this.L_D - this.L_D0 },

    delta_x: function() { return this.device.inv00 * this.delta_L_A + this.device.inv01 * this.delta_L_B + this.device.inv02 * this.delta_L_C + this.device.inv03 * this.delta_L_D },
    delta_y: function() { return this.device.inv10 * this.delta_L_A + this.device.inv11 * this.delta_L_B + this.device.inv12 * this.delta_L_C + this.device.inv13 * this.delta_L_D },
    delta_z: function() { return this.device.inv20 * this.delta_L_A + this.device.inv21 * this.delta_L_B + this.device.inv22 * this.delta_L_C + this.device.inv23 * this.delta_L_D },
    delta_theta_y: function() { return this.device.inv30 * this.delta_L_A + this.device.inv31 * this.delta_L_B + this.device.inv32 * this.delta_L_C + this.device.inv33 * this.delta_L_D },
  },
  mounted() {
    this.updateDevice();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
