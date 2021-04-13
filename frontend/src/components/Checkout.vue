<template>
  <v-card style="padding: 20px; margin: 1px">
    <v-form style="max-width: 300px" ref="form">
      <v-autocomplete
        v-model="vehicleId"
        :items="vehicleIds"
        label="VehicleID"
      ></v-autocomplete>
      <v-btn @click="submit" :disabled="!vehicleId">Submit</v-btn>
    </v-form>
  </v-card>
</template>

<script>
import { EventBus } from "../main";

export default {
  name: "Checkin",
  data() {
    return {
      vehicleId: "",
      vehicleIds: [],
    };
  },
  created() {
    EventBus.$on('refresh', e => {
        this.getCurrent()
        console.log(e)
    })
    this.getCurrent();
  },
  methods: {
    getCurrent() {
      this.$axios
        .get(this.$api + "/current/")
        .then((res) => {
          console.log(res.data.data);
          this.vehicleIds = res.data.data;
        })
        .catch((err) => console.log(err));
    },
    submit() {
      var formData = new FormData();
      formData.append("vehicleId", this.vehicleId);
      this.$axios
        .post(this.$api + "/checkout/", formData)
        .then((res) => {
          console.log(res);
          this.getCurrent();
          EventBus.$emit('refresh')
        })
        .catch((err) => {
          console.log(err);
          this.getCurrent();
        });

    },
  },
};
</script>