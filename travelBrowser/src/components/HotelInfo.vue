<template>
  <div>
    <p>酒店详情</p>
    <p><img style="width: 400px" :src="picture" alt=""></p>
    <p>{{name}}</p>
    <p>{{create_time}}</p>
    <p><span style="color: red;">${{price}}</span></p>
    <p>{{info}}</p>
    <div v-if="isLogin">
      <button @click="DoOrder">预定酒店</button>
      <p>
        留言：<input type="text" v-model="text">
        <button @click="OnComm">发表言论</button>
      </p>
      <div>
        <hr>
        <p>共{{comms.length}}评论</p>
        <div v-for="item in comms">
          <div style="border: aqua 1px solid;margin-bottom: 10px">匿名用户 {{item.text}}</div>
        </div>
      </div>

    </div>
    <div v-else>
      <button disabled>预定酒店</button>
      <p>
        尚未登录，无法查看评论
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "AttrInfo",
    data() {
      return {
        isLogin: false,
        user_obj: "",

        id: 0,
        name: '',
        info: '',
        price: '',
        picture: '',
        create_time: '',

        text: '',
        comms: [
          {text: "默认评论"}
        ]
      }
    },
    created() {
      var hotel_id = this.$route.query.hotel;
      this.id = hotel_id
    },
    mounted() {
      this.ShowComm()
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
      })
      this.$ajax.get(this.globalURL + '/hotelinfo', {
        params: {
          hotel: this.id
        }
      }).then(res => {
        if (res.data.code == 102) {
          var obj = res.data.result
          this.name = obj.name
          this.info = obj.info
          this.price = obj.price
          this.picture = obj.picture
          this.create_time = obj.c_time
        }
      })
    },
    methods: {
      DoOrder() {
        this.$ajax.post(this.globalURL + '/hotelorder', {
          hotel: this.id,
          userphone: this.user_obj,
          info: this.name
        }).then(res => {
          if (res.data.code == 102) {
            location.reload();
            alert(res.data.msg + "预定用户:" + res.data.result)
          } else {
            alert(res.data.msg)
          }
        }).catch(err => {
          alert("发生未知错误")
        })
      },
      OnComm() {
        this.$ajax.post(this.globalURL + "/hotelcomm", {
          hotel: this.id,
          userphone: this.user_obj,
          textinfo: this.text,
          hotelname: this.name
        }).then(res => {
          if (res.data.code == 102) {
            this.comms.unshift({
              text: this.text
            })
            this.text = ''
          }
        })
      },
      ShowComm() {
        this.$ajax.get(this.globalURL + "/hotelcomm", {
          params: {
            id: this.id
          }
        }).then(res => {
          console.log(res.data);
          this.comms = res.data
        })
      }
    }
  }
</script>

<style scoped>

</style>
