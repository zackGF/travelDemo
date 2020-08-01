<template>
  <div>
    景点
    <div v-for="(attr_item,index) in attr_list" :key="index">
      <div @click="AttrInfo(attr_item.id)" style="border: 1px solid #000;margin-bottom: 10px">
        <p><img :src="attr_item.picture" alt="" style="width: 324px;height: 200px;"></p>
        <p>{{attr_item.name}} <span style="color: red;">${{attr_item.price}}(美元)</span></p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Attractions",
    data(){
      return{
        attr_list:[],
      }
    },
    mounted() {
      this.OnShow()
    },
    methods: {
      OnShow() {
        this.$ajax.get(this.globalURL + "/").then(res => {
          // console.log(res.data);
          this.attr_list = res.data
        })
      },
      AttrInfo(attr){
        this.$router.push({
          path:'/attrinfo',
          query:{
            attraction:attr
          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
