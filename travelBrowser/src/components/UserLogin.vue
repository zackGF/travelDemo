<template>
  <div>
    用户登录
    <div>
      <p>
        手机号码：<input type="text" v-model="user_phone">
      </p>
      <p>
        密码：<input type="password" v-model="userpwd">
      </p>
      <p>
        <button @click="DoLogin">登录</button>
      </p>
    </div>
  </div>
</template>

<script>
  import {mapMutations} from 'vuex'
  export default {
    name: "UserLogin",
    data() {
      return {
        user_phone: "",
        userpwd: "",
        userToken:""
      }
    },
    methods: {
      ...mapMutations(['changeLogin']),
      DoLogin() {
        let _this = this;
        this.$ajax.post(this.globalURL + "/login", {
          phone: this.user_phone,
          password: this.userpwd,
        }).then(res => {
          if (res.data.code == 102) {
            console.log("Bearer "+res.data.user_token);
            _this.userToken = 'Bearer '+res.data.user_token;
            _this.changeLogin({Authorization:_this.userToken});
            location.reload()
            alert(res.data.msg)
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
