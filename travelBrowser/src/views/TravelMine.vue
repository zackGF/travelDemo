<template>
  <div>
    我的
    <div v-if="isLogin">
      我的信息
      <p>
        当前用户：{{user_}}
      </p>
      <div>
        <button @click="OnOrder">我的订单</button>
      </div>
      <p>
        <button @click="OnComm">我的评论</button>
      </p>
      <p>
        <a href="/changepwd">更改密码</a>
      </p>

      <button @click="DoOut">退出</button>
    </div>
    <div v-else>
      <div>
        <router-link :to="{name: 'UserLogin'}">登录</router-link>
        <router-link :to="{name: 'UserRegister'}">注册</router-link>
      </div>
      <div>
        <router-view></router-view>
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: "TravelMine",
    data() {
      return {
        isLogin: false,
        user_:""
      }
    },
    mounted(){
      this.OnShow()
    },
    methods: {
      OnShow() {
        this.$ajax.get(this.globalURL + "/center").then(res => {
          if (res.data.code == 102) {
            this.isLogin = true;
            this.user_ = res.data.result;
          } else {
            this.isLogin = false;
            console.log(res.data.msg);
            return;
          }
        }).catch(err=>{
          console.log("UNAUTHORIZED");
        })
      },
      DoOut(){
        this.$store.commit('delLogin');
        location.reload();
        return;
      },
      OnOrder(){
        this.$router.push({
          path:'/userorder',
          query:{
            user_uuid:this.user_
          }
        })
      },
      OnComm(){
        this.$router.push({
          path:'/usercomm',
          query:{
            user_uuid:this.user_
          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
