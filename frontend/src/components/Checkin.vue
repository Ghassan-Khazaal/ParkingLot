<template>
  <v-form style="max-width: 300px" ref="form" >
    <v-text-field
      v-model="vehicleId"
      label="Vehicle Id"
      required
    ></v-text-field>
    <v-select
      v-model="vehicleType"
      :items="vehicleTypes"
      item-text="name"
      label="VehicleType"
      return-object
    ></v-select>
    <v-btn @click="submit">Submit</v-btn>
    {{ msg }}
  </v-form>
</template>

<script>
export default {
  name: "CheckIn",
  data() {
    return {
      vehicleId: "",
      vehicleType: "",
      msg: "",
      vehicleTypes: [],
    };
  },
  created() {
    this.$axios
      .get(this.$api + "/vtypes/")
      .then((res) => {
        this.vehicleTypes = res.data.data;
      })
      .catch((err) => console.log(err));
  },
  methods: {
    submit() {
      var formData = new FormData();
      formData.append("vehicleType", this.vehicleType.id);
      formData.append("vehicleId", this.vehicleId);
      this.$axios
        .post(this.$api + "reserve/", formData)
        .then((res) => {
          if (res.data.data.constructor == Object){
              this.msg = "Level " + res.data.data.level + " - " + res.data.data.label + " Reserved";
          } else {
              this.msg = res.data.data
          }
        })
        .catch((err) => {
          this.msg = "error!";
          console.log(err);
        });
    },
  },
};
</script>