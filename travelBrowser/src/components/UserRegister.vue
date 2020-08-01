<template>
  <div>
    用户注册
    <div>
      <p>
        手机号：<input type="number" v-model="userphone">
      </p>
      <p>
        密码：<input type="password" v-model="userpwd1">
      </p>
      <p>
        确认密码：<input type="password" v-model="userpwd2">
      </p>
      <p>
        <button @click="DoReg">注册</button>
      </p>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: "UserRegister",
    data() {
      return {
        userphone: "",
        userpwd1: "",
        userpwd2: ""
      }
    },
    methods: {
      DoReg() {
        axios.post(this.globalURL + "/register", {
          phone: this.userphone,
          password1: this.userpwd1,
          password2: this.userpwd2
        }).then(res=>{
          if (res.data.code == 102){
            this.$router.push("/mine");
            alert(res.data.msg+"!注册手机号:"+res.data.result)
          }else {
            alert(res.data.msg)
          }
        })
      }
    }

  }
</script>

<style scoped>

</style>
