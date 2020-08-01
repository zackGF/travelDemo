<template>
  <div>
    <div v-if="isLogin">
      <p>
        当前用户：{{user_obj}} <br>
        新密码：<input type="password" v-model="newpassword">
      </p>
      <p>
        <button @click="ChangePwd">更换密码</button>
      </p>
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
    name: "UserChange",
    data() {
      return {
        user_obj: "",
        isLogin: false,
        newpassword: ""
      }
    },
    created() {
      this.OnShow()
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
      ChangePwd() {
        this.$ajax.post(this.globalURL + "/changepwd", {
          userphone: this.user_obj,
          newpassword: this.newpassword
        }).then(res => {
          if (res.data.code == 102) {
            this.$store.commit('delLogin');
            this.$router.push("/mine/");
            alert(res.data.msg + "，请重新登录！")
          } else {
            alert(res.data.msg)
          }
        }).catch(err => {
          alert("发生未知错误！！")
        })
      }
    }
  }
</script>

<style scoped>

</style>
