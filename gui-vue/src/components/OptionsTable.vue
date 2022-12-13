<template>
  <el-table
      :data="data"
      border
      :cell-style="{padding:'3px 5px'}"
      stripe style="width: 100%; font-size: 10px"
  >
    <el-table-column prop="name" label="名称" width="150"></el-table-column>
    <el-table-column prop="value" label="值">
      <template slot-scope="scope">
        <el-input v-model="scope.row.value" style="width: 100%"></el-input>
      </template>
    </el-table-column>
    <el-table-column prop="require" label="必填项" width="100">
      <template slot-scope="scope">
        <div slot="reference" class="name-wrapper">
          <el-tag size="medium" v-if="!scope.row.require">可选</el-tag>
          <el-tag size="medium" type="danger" v-else>必填</el-tag>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="type" label="类型" width="100"></el-table-column>
    <el-table-column prop="description" label="描述"></el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "OptionsTable",
  props: {
    data: Array
  }
}
</script>

<style scoped>

</style>