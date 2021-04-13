<template>
  <v-data-table
    :headers="headers"
    :items="status"
    :items-per-page="5"
    class="elevation-1"
  ></v-data-table>
</template>

<script>
import { EventBus } from "../main";

export default {
  name: "Status",
  created() {
    this.getStatus();
    EventBus.$on("refresh", (e) => {
      this.getStatus();
      console.log(e);
    });
  },
  data() {
    return {
      headers: [
        { text: "Level", value: "Level" },
        { text: "Vehicle Type", value: "VehicleType" },
        { text: "Total Spot", value: "TotalSpots" },
        { text: "Reserved Spots", value: "ReservedSpots" },
        { text: "Free Spots", value: "FreeSpots" },
      ],
      status: [],
    };
  },
  methods: {
    getStatus() {
      let self = this;
      this.$axios.get(this.$api + "status/").then((res) => {
        let data = res.data.data;
        this.status = [];
        Object.keys(data).forEach(function (l) {
          Object.keys(data[l]).forEach(function (t) {
            self.status.push({
              Level: l,
              VehicleType: t,
              TotalSpots: data[l][t]["all"],
              ReservedSpots: data[l][t]["taken"],
              FreeSpots: data[l][t]["free"],
            });
          });
        });
      });
    },
  },
};
</script>