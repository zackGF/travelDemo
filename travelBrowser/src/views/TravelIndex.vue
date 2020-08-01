<template>
  <div>
    首页
    <div>
      <router-link :to="{name:'Attractions'}">景点</router-link>
      <router-link :to="{name:'Hotel'}">酒店</router-link>
    </div>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  export default {
    name: "TravelIndex",
    data(){
      return{
        attr_list:[]
      }
    }
  }
</script>

<style scoped>

</style>
