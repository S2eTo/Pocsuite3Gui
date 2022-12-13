<template>
  <div class="home">
    <PocLists/>
  </div>
</template>

<script>
// @ is an alias to /src
import PocLists from '@/components/PocLists.vue'

export default {
  name: 'HomeView',
  components: {
    PocLists
  }
}
</script>

<style scoped>
.home {
  background: #ffffff;
  padding: 20px;
}
</style>
