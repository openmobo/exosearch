<template>
  <v-app>
    <sideBar />
    <v-main>
      <router-link to="/"></router-link><br />
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

import SideBar from './components/SideBar.vue'


export default {
  name: 'App',

  components: {
    
    SideBar,
 
  },

  data: () => ({
  
  }),
}
</script>
