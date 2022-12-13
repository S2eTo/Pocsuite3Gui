<template>
  <div class="poc-lists">
    <el-form :rules="searchFormRules" ref="searchForm" :model="searchForm" @submit.native.prevent label-width="100px" style="width: 100%">
      <el-form-item label="Poc 名称:" prop="name">
        <el-input v-model="searchForm.name" style="font-size: 14px">
          <el-button slot="append" icon="el-icon-search" @click="submitForm()" native-type="submit"></el-button>
        </el-input>
      </el-form-item>
    </el-form>
    <div class="searched" v-if="searched">共有 {{ this.lists.length }} 条结果, 找到 {{ this.rlists.length }} 条,
      <el-link type="primary" @click="searchBack">返回</el-link>
    </div>
    <Poc class="poc-item" v-for="(data, index) in rlists" :key="index" :data="data" :i="index"/>
  </div>
</template>

<script>
import axios from "axios";
import Poc from '@/components/Poc.vue'
import {Loading} from "element-ui";

export default {
  name: "PocLists",
  components: {
    Poc,
  },
  data() {
    return {
      lists: [],
      rlists: [],
      searchForm: {
        name: '',
      },
      searched: false,
      searchFormRules: {
        name: [
          {required: true, message: '请输入名称', trigger: 'change'}
        ]
      }
    }
  },
  created() {
    let loading = Loading.service({
      fullscreen: true,
      text: '拼命加载中',
      background: 'rgba(0, 0, 0, 0.8)',
      spinner: 'el-icon-loading',
    });

    axios.get("http://127.0.0.1:8888/poc_list").then((res) => {
      loading.close()
      this.lists = res.data
      this.rlists = res.data
    }).catch((res) => {
      loading.close()
      this.$message.error('请求失败');
    });
  },
  methods: {
    searchBack() {
      this.rlists = this.lists;
      this.searched = false;
      this.$refs.searchForm.resetFields();
    },
    submitForm() {
      this.$refs.searchForm.validate((valid) => {
        if (valid) {
          this.searched = true
          this.rlists = []
          for (let i in this.lists) {
            let poc = this.lists[i];
            if (poc.name.toLowerCase().indexOf(this.searchForm.name.toLowerCase()) != -1) {
              this.rlists.push(poc)
            }
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
  }
}
</script>

<style scoped>

.searched {
  padding: 10px 0;
}

.searched .back {
  color: #4d79dc;
  cursor: pointer;
}
</style>