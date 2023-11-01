<template>
    <div>
      <!-- The main container for the component -->
      <!-- The app bar at the top -->
      <v-app-bar style="background: linear-gradient(to right ,#ff1791,#9c5Aed,#c8a3f5) ;">
        <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <v-avatar size="120">
          <v-img src="../assets/exosearch-high-resolution-logo-transparent.png"></v-img>
        </v-avatar>
      </v-app-bar>
  
      <!-- The navigation drawer on the side -->
      <v-navigation-drawer v-model="drawer" permanent color="#F4F5F9" app>
        <v-list-item class="px-2 py-5">
          <v-list-item-title class="text-capitalize" align="center">
           Exosearch
          </v-list-item-title>
        </v-list-item>
  
        <!-- The list of navigation items -->
        <v-list nav dense>
          <v-list-item-group v-model="selectedItem" color="deep-purple">
            <v-list-item v-for="(item, i) in items" :key="i">
              <v-list-item-content class="d-flex align-center">
                <a class="navbar-brand" :href="item.route">
                  <v-list-item-title class="sidetext" v-text="item.text"></v-list-item-title>
                </a>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
  
        <!-- The user profile section -->
        <template v-slot:append>
          <div class="pa-2 padding-profile">
            <v-card align="center" class="pa-3">
              <v-badge bordered bottom color="green" dot offset-x="10" offset-y="10" class="mb-8">
                <v-avatar size="120">
                  <v-img src="https://cdn-icons-png.flaticon.com/512/8214/8214212.png"></v-img>
                </v-avatar>
              </v-badge>

              <h4  v-if="authStore.authenticated" class="green--text">Hi {{ authStore.name }}</h4>
              <h4 v-else class="green--text">Please Log in</h4>
              
              <v-btn @click="logout" v-if="authStore.authenticated" depressed color="primary">Log Out</v-btn>
              <v-btn href='/login' v-else depressed color="primary">Log in</v-btn>
            </v-card>
          </div>
        </template>
      </v-navigation-drawer>
    </div>
  </template>
  
  
<script>

import { useAuthSetup } from '../recall function/authsetup'

export default {
 

  setup() {
    const { authStore, fetchData } = useAuthSetup();

    // Call fetchData to fetch and set authentication data
    fetchData();

    return {
      authStore,
    };
  },


    data: () => ({
        selectedItem: 0,
        drawer: false,
        items: [
            {text: 'Dashboard', route: '/'},
            { text: 'Upload File', route: '/upload'},
            { text: 'Result', route: '/result'},
            { text: 'Change Password', route: '/changepass'},

        ]
        }),

      

        methods: {

async logout(){

try {
  // Send a logout request to your backend API
  const response = await fetch('http://127.0.0.1:8000/logout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include', // Include cookies in the request
  });

  if (response.status === 200) {

    console.log(response);
    
    this.$router.push('/login');
  }
} catch (error) {
  console.error('Logout failed:', error);
}

}
}

        
}
</script>
<style scoped>


.bar {

    color: blue;

}


.sidetext{
  margin-left: 15px;
}

.padding-profile{

  margin-bottom: 250px;
}


</style>