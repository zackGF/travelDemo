<template>
    <div>

      <div v-if="isLogin">
        <h3>我的订单</h3>
        <div>
          <div v-if="isAttr">
            <p>景点</p>
            <table border="1">
              <th>订单编号</th>
              <th>名称</th>
              <tr v-for="(item,index) in attrlist" :key="index">
                <td>{{item.id}}</td>
                <td>{{item.info}}</td>
              </tr>
            </table>
          </div>

        </div>
        <div>

          <div v-if="isHotel">
            <p>酒店</p>
            <table border="1">
              <th>订单编号</th>
              <th>名称</th>
              <tr v-for="(item,index) in hotellist" :key="index">
                <td>{{item.id}}</td>
                <td>{{item.info}}</td>
              </tr>
            </table>
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
        name: "UserOrder",
      data(){
          return{
            isAttr:false,
            isHotel:false,
            user_obj:"",
            isLogin:false,
            uphone:'',
            attrlist:[],
            hotellist:[]
          }
      },
      mounted() {
        this.$ajax.get(this.globalURL+"/center").then(res=>{
          if (res.data.code == 102) {
            this.isLogin = true
            this.user_obj = res.data.result
            return;
          }else {
            this.isLogin = false
            alert(res.data.msg)
            return;
          }
        }).catch(err=>{
          // console.log("失败");
          this.isLogin = false
          this.$router.push('/mine/');
          alert("访问失败");
          return;
        })
          this.OnShowAttr()
        this.OnShowHotel()
      },
      created(){
        var uuid = this.$route.query.user_uuid
        this.uphone = uuid
      },
      methods:{
          OnShowAttr(){
            this.$ajax.get(this.globalURL+'/attrorder',{
              params:{
                phone:this.uphone
              }
            }).then(res=>{
              if (res.data.code == 107) {
                this.isAttr = false
              }else if (res.data.code == 104) {
                this.isAttr = false
              } else {
                this.isAttr = true
                this.attrlist = res.data
              }
            })
          },
        OnShowHotel(){
            this.$ajax.get(this.globalURL+'/hotelorder',{
              params:{
                phone:this.uphone
              }
            }).then(res=>{
              if (res.data.code == 107) {
                this.isHotel = false
              }else if (res.data.code == 104) {
                this.isHotel = false
              } else {
                this.isHotel = true
                this.hotellist = res.data
              }
            })
        }
      }
    }
</script>

<style scoped>

</style>
