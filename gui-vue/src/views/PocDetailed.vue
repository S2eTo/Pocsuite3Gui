<template>
  <div class="poc-detailed">
    <div>
      <h1>PAYLOAD 设置</h1>
      <div class="settings">
        <span>只看EXP与必填项：<el-switch v-model="only_require" @change="filter_require"></el-switch></span>
      </div>
      <el-table
          :data="show_options"
          border
          :cell-style="{padding:'3px 5px'}"
          stripe style="width: 100%; font-size: 10px"
      >
        <el-table-column prop="name" label="名称" width="150"></el-table-column>
        <el-table-column prop="value" label="值">
          <template slot-scope="scope">
            <el-input v-model="scope.row.value" style="width: 100%" v-if="scope.row.type != 'Dict'"></el-input>
            <el-select v-model="scope.row.value" placeholder="请选择" v-else style="width: 100%">
              <el-option
                  v-for="(k, v) in scope.row.default"
                  :key="v"
                  :value="v">
              </el-option>
            </el-select>
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

      <h1>执行</h1>
      <div class="tools">
        <el-button type="primary" icon="el-icon-lightning" size="small" @click="run('shell')">SHELL</el-button>
        <el-button type="primary" icon="el-icon-sunset" size="small" @click="run('verify')">VERIFY</el-button>
        <el-button type="primary" icon="el-icon-sunny" size="small" @click="run('attack')">ATTACK</el-button>
      </div>

    </div>
  </div>
</template>

<script>
import {Loading} from "element-ui";
import axios from "axios";

export default {
  name: "PocDetailed",
  data() {
    return {
      name: null,
      data: {
        name: ""
      },
      show_options: [],
      only_require: true
    }
  },
  created() {
    this.name = this.$route.query.name
    let loading = Loading.service({
      fullscreen: true,
      text: '拼命加载中',
      background: 'rgba(0, 0, 0, 0.8)',
      spinner: 'el-icon-loading',
    });
    axios.get(`http://127.0.0.1:8888/poc_detailed?poc=${this.name}`).then((res) => {
      loading.close()
      this.data = res.data
      this.filter_require()
      this.channels.$emit("switch_page", this.data.name, true)
    }).catch((res) => {
      loading.close()
      this.$message.error('请求失败');
    });
  },
  methods: {
    filter_require() {
      if (this.only_require) {
        this.show_options = []
        for (let i in this.data.options) {
          if (this.data.options[i].require) {
            this.show_options.push(this.data.options[i])
          }
        }
      } else {
        this.show_options = this.data.options
      }
    },
    run(m) {
      let optlist = []
      for (let i in this.data.options) {
        let item = this.data.options[i];
        if (item.name == "content_type") {
          console.log(item)
        }
        optlist.push(`${item.name} ${item.value}`)
      }
      this.channels.$emit("show_console")
      axios.post("http://127.0.0.1:8888/run", {mode: m, poc: this.name, options: optlist}, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        }
      }).then((res) => {
        console.log(res)
      }).catch((res) => {
        console.log(res)
        this.$message.error('请求失败');
      })
    }
  }
}
</script>

<style scoped>
.poc-detailed {
  background: #ffffff;
  padding: 20px;
}

.information div {
  padding-bottom: 5px;
}

.settings {
  margin: 15px 0;
}

h1 {
  margin: 15px 0;
}
</style>