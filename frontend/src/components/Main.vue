<template>
  <v-row align-center justify-center>
    <v-col>
      <v-card color="#abb6bf" class="text-center justify-center">
        <v-card-title class="text-center justify-center py-6">
          <h1 class="font-weight-bold display-3 basil--text">Vence Garage</h1>
        </v-card-title>

        <v-tabs v-model="tab" background-color="transparent" color="basil" grow>
          <v-tab :key="'checkin'"> CheckIn </v-tab>

          <v-tab :key="'checkout'"> Checkout </v-tab>

          <v-tab :key="'status'"> Status </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item :key="'checkin'">
            <CheckIn></CheckIn>
          </v-tab-item>

          <v-tab-item :key="'checkout'">
            <Checkout></Checkout>
          </v-tab-item>

          <v-tab-item :key="'status'">
            <Status></Status>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-col>
  </v-row>
</template> 

<script>
import CheckIn from "./Checkin.vue";
import Status from "./Status.vue";
import Checkout from "./Checkout.vue";
export default {
  name: "VenceGarage",
  components: {
    CheckIn,
    Status,
    Checkout,
  },
  props: {
    msg: String,
  },
  data() {
    return {
      tab: null,
    };
  },
};
</script>

<style>
/* Helper classes */
.basil {
  background-color: #fffbe6 !important;
}
.basil--text {
  color: #356859 !important;
}
</style>