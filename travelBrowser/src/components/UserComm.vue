<template>
  <div>
    <div v-if="isLogin">
      <h2>我的评论</h2>
<!--      <p>{{user_obj}}</p>-->
      <div>
        景点
        <div v-for="attr_item in attrList">
          <div @click="AttrInfo(attr_item.attr_)">
            <div style="border: brown 1px solid;margin-bottom: 10px">{{attr_item.text}}====={{attr_item.attrname}}</div>
          </div>
        </div>
      </div>
      <div>
        酒店
        <div v-for="hotel_item in hotelList">
          <div @click="HotelInfo(hotel_item.hotel_)">
            <div style="border: aquamarine 1px solid;margin-bottom: 10px">{{hotel_item.text}}====={{hotel_item.hotelname}}</div>
          </div>
        </div>
      </div>

    </div>
    <div v-else>
      <p>
        无权限访问
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "UserComm",
    data() {
      return {
        user_obj: "",
        isLogin: false,
        uphone: '',

        attrList:[],
        hotelList:[]
      }
    },
    created() {
      this.OnShow()
      var uuid = this.$route.query.user_uuid
      this.uphone = uuid
    },
    mounted() {
      this.ShowAttr()
      this.ShowHotel()
    },
    methods: {
      OnShow() {
        this.$ajax.get(this.globalURL + "/center").then(res => {
          if (res.data.code == 102) {
            this.isLogin = true
            this.user_obj = res.data.result
            return;
          } else {
            this.isLogin = false
            alert(res.data.msg)
            return;
          }
        }).catch(err => {
          // console.log("失败");
          this.isLogin = false
          this.$router.push('/mine/');
          alert("访问失败");
          return;
        })
      },
      ShowAttr() {
        this.$ajax.get(this.globalURL + '/showattr', {
          params: {
            "userphone": this.uphone
          }
        }).then(res => {
          // console.log(res.data);
          this.attrList = res.data
        })
      },
      ShowHotel() {
        this.$ajax.get(this.globalURL + '/showhotel', {
          params: {
            "userphone": this.uphone
          }
        }).then(res => {
          // console.log(res.data);
          this.hotelList = res.data
        })
      },
      AttrInfo(attr){
        this.$router.push({
          path:'/attrinfo',
          query:{
            attraction:attr
          }
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
