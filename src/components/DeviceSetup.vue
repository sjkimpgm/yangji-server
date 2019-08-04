<template>
  <div>
    <form class="form" v-on:submit="sendPost">
      <button type="submit" class="btn btn-primary">저장 및 계산</button>
      <table>
        <tr> <td> f_A0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.f_Aa"> &times; <input class="border rounded" type="number" step="0.0001" v-model="device.V_A0"> &#43; <input class="border rounded" type="number" step="0.0001" v-model="device.f_Ab"> = {{f_A0.toFixed(4)}} </td> </tr>
        <tr> <td> f_B0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.f_Ba"> &times; <input class="border rounded" type="number" step="0.0001" v-model="device.V_B0"> &#43; <input class="border rounded" type="number" step="0.0001" v-model="device.f_Bb"> = {{f_B0.toFixed(4)}} </td> </tr>
        <tr> <td> f_C0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.f_Ca"> &times; <input class="border rounded" type="number" step="0.0001" v-model="device.V_C0"> &#43; <input class="border rounded" type="number" step="0.0001" v-model="device.f_Cb"> = {{f_C0.toFixed(4)}} </td> </tr>
        <tr> <td> f_D0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.f_Da"> &times; <input class="border rounded" type="number" step="0.0001" v-model="device.V_D0"> &#43; <input class="border rounded" type="number" step="0.0001" v-model="device.f_Db"> = {{f_D0.toFixed(4)}} </td> </tr>
        <tr>&nbsp;</tr>
        <tr> <td> L_A0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.L_Ak"> &#43; {{f_A0.toFixed(4)}} = {{L_A0.toFixed(4)}} </td> </tr>
        <tr> <td> L_B0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.L_Bk"> &#43; {{f_B0.toFixed(4)}} = {{L_B0.toFixed(4)}} </td> </tr>
        <tr> <td> L_C0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.L_Ck"> &#43; {{f_C0.toFixed(4)}} = {{L_C0.toFixed(4)}} </td> </tr>
        <tr> <td> L_D0 = <input class="border rounded" type="number" step="0.0001" style="text-align: right;" v-model="device.L_Dk"> &#43; {{f_D0.toFixed(4)}} = {{L_D0.toFixed(4)}} </td> </tr>
        <tr>&nbsp;</tr>
        <tr> <td> G_bar = <input class="border rounded" type="number" step="0.0001" v-model="device.G_bar"> </td> </tr>
        <tr> <td> Q_bar = <input class="border rounded" type="number" step="0.0001" v-model="device.Q_bar"> </td> </tr>
        <tr> <td> F_bar = <input class="border rounded" type="number" step="0.0001" v-model="device.F_bar"> </td> </tr>
        <tr>&nbsp;</tr>
        <tr> <td> theta_x = <input class="border rounded" type="number" step="0.0001" v-model="device.theta_x"> </td> </tr>
        <tr> <td> theta_y = <input class="border rounded" type="number" step="0.0001" v-model="device.theta_y"> </td> </tr>
        <tr> <td> theta_z = <input class="border rounded" type="number" step="0.0001" v-model="device.theta_z"> </td> </tr>
        <tr>&nbsp;</tr>
        <tr> <td> D =  <input class="border rounded" type="number" step="0.0001" v-model="device.D"> </td> </tr>
        <tr> <td> w1 = <input class="border rounded" type="number" step="0.0001" v-model="device.w1"> </td> </tr>
        <tr> <td> w2 = <input class="border rounded" type="number" step="0.0001" v-model="device.w2"> </td> </tr>
        <tr> <td> d =  <input class="border rounded" type="number" step="0.0001" v-model="device.dsmall"> </td> </tr>
        <tr>&nbsp;</tr>
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
    }
  },
  methods: {
    sendPost: function() {
      var vm = this;

      axios.post('/api/calc_device/', vm.device)
      .then(function(res) {
        console.log(res.data)
        vm.updateDevice();
      }, function() {
      	console.log('failed')
      })
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
    f_A0: function() { return this.device.f_Aa * this.device.V_A0  + this.device.f_Ab },
    f_B0: function() { return this.device.f_Ba * this.device.V_B0  + this.device.f_Bb },
    f_C0: function() { return this.device.f_Ca * this.device.V_C0  + this.device.f_Cb },
    f_D0: function() { return this.device.f_Da * this.device.V_D0  + this.device.f_Db },
    L_A0: function() { return this.device.L_Ak  + this.f_A0 },
    L_B0: function() { return this.device.L_Bk  + this.f_B0 },
    L_C0: function() { return this.device.L_Ck  + this.f_C0 },
    L_D0: function() { return this.device.L_Dk  + this.f_D0 },
  },
  mounted() {
    this.updateDevice();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
