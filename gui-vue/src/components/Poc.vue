<template>
  <div class="poc" @click="detailed">
    <div class="name border-bottom">{{ data.name }}</div>

    <el-popover
        placement="top-start"
        width="500"
        trigger="hover"
        :content="data.desc"
        v-if="data.desc.trim()">
      <div class="desc border-bottom" slot="reference">{{ data.desc }}</div>
    </el-popover>
    <div class="desc border-bottom" v-else>暂无描述...</div>

    <div class="info border-bottom">
      <el-tag size="mini" type="danger" style="font-size: 10px">{{ data.vulType }}</el-tag>
    </div>

    <div class="info border-bottom">影响版本： {{data.appVersion}} </div>
  </div>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Poc",
  props: {
    data: Object,
    i: Number
  },
  methods: {
    detailed: function () {
      this.$router.push({
        name: 'poc-detailed',
        query: {
          name: this.data.path,
        },
      })
    }
  }
}
</script>

<style scoped>
.border-bottom {
  margin-bottom: 25px;
}
.poc {
  vertical-align: top;
  display: inline-block;
  width: calc(50% - 40px);
  margin: 15px 20px;
  padding: 30px 20px 15px 20px;
  border: 1px solid #EBEEF5;
  border-radius: 3px;
  cursor: pointer;
}

.poc:hover {
  background: #fbfbfb;
}

.name {
  margin-bottom: 15px;
  font-weight: bold;
}

.desc {
  overflow: hidden;

  text-overflow: ellipsis;
  white-space: nowrap;
}

</style>