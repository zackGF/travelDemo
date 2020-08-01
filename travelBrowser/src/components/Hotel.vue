<template>
  <div>
    酒店
    <div v-for="(hotel_item,index) in hotel_list" :key="index">
      <div @click="HotelInfo(hotel_item.id)" style="border: 1px solid #000;margin-bottom: 10px">
        <p><img :src="hotel_item.picture" alt=""></p>
        <p>{{hotel_item.name}} <span style="color: red;">${{hotel_item.price}}(美元)</span></p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Hotel",
    data(){
      return{
        hotel_list:[],
      }
    },
    mounted() {
      this.OnShow()
    },
    methods: {
      OnShow() {
        this.$ajax.get(this.globalURL + "/hotel").then(res => {
          // console.log(res.data);
          this.hotel_list = res.data
        })
      },
      HotelInfo(hotel){
        this.$router.push({
          path:'/hotelinfo',
          query:{
            hotel:hotel
          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
