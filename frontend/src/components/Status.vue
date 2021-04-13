<template>
  <div>
    <v-container>
      <v-treeview :items="status" open-all activatable shaped></v-treeview>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "Status",
  created() {
    let self = this;
    this.$axios.get(this.$api + "status/").then((res) => {
      let data = res.data.data;
      this.status = [];
      let cnt = 0;
      Object.keys(data).forEach(function (l) {
        cnt += 1;
        let level = { id: cnt, name: "Level " + l, children: [] };
        Object.keys(data[l]).forEach(function (t) {
          cnt += 1;
          let ty = { id: cnt, name: t, children: [] };
          level["children"].push(ty);
          Object.keys(data[l][t]).forEach(function (s) {
            cnt += 1;
            let st = { id: cnt, name: s + data[l][t][s], children: ["1"] };
            ty["children"].push(st);
          });
        });
        self.status.push(level);
      });
      console.log(this.status);
    });
  },
  data() {
    return {
      status: [
        {
          id: 1,
          name: "Applications :",
          children: [
            { id: 2, name: "Calendar : app" },
            { id: 3, name: "Chrome : app" },
            { id: 4, name: "Webstorm : app" },
          ],
        },
      ],
    };
  },
};
</script>