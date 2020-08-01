import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TravelIndex from '@/views/TravelIndex'
import TravelMine from '@/views/TravelMine'

import UserLogin from '@/components/UserLogin'
import UserRegister from "@/components/UserRegister"

import Hotel from '@/components/Hotel'
import Attractions from '@/components/Attractions'
import UserChange from '@/components/UserChange'
import AttrInfo from '@/components/AttrInfo'
import HotelInfo from '@/components/HotelInfo'
import UserOrder from '@/components/UserOrder'
import UserComm from '@/components/UserComm'



Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'TravelIndex',
      component: TravelIndex,
      children:[
        {
          path:'/',
          name:'Attractions',
          component:Attractions
        },
        {
          path:'/hotel',
          name:'Hotel',
          component:Hotel
        }
      ]
    },
    {
      path:'/mine',
      name:'TravelMine',
      component:TravelMine,
      children:[
        {
          path:'/',
          name:"UserLogin",
          component:UserLogin
        },
        {
          path:"/register",
          name:"UserRegister",
          component:UserRegister
        }
      ]
    },
    {
      path:'/changepwd',
      name:'UserChange',
      component:UserChange
    },
    {
      path:'/usercomm',
      name:'UserComm',
      component:UserComm
    },
    {
      path:'/attrinfo',
      name:'AttrInfo',
      component:AttrInfo
    },
    {
      path:'/hotelinfo',
      name:'HotelInfo',
      component:HotelInfo
    },
    {
      path:'/userorder',
      name:'UserOrder',
      component:UserOrder
    }
  ]
})
