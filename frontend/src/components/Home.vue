<template>


    <!-- The main container for the component -->
    <div class="home">
      <v-toolbar flat>
        <v-toolbar-title>
          <span class="caption">Overview Dashboard</span><br>
          
          <!-- testing -->
          <h5>{{ message }}</h5>

         
        </v-toolbar-title>

        <v-toolbar-items>
        <!-- Conditional rendering based on authentication status -->
        <template v-if="!authStore.authenticated">
          <v-btn @click="login">Login</v-btn>
        </template>
        <template v-else>
          <v-btn @click="logout">Logout</v-btn>
        </template>
      </v-toolbar-items>
  
        <!-- logo -->
        
          <v-avatar class="logo-pos" size="120">
            <v-img src="../assets/exosearch-high-resolution-logo-transparent.png"></v-img>
          </v-avatar>
      </v-toolbar>
      <v-divider></v-divider>
      <v-container class="mt-5">
        <v-row>
          <v-col cols="12" sm="4">
            <!-- Card 1 -->
            <v-hover v-slot="{ hover }" open-delay="200">
              <v-card id="grad1" :elevation="hover ? 16 : 2">
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-list-item three-line>
                      <v-list-item-content>
                        <div class="mb-4">
                        
                        </div>
                        <!-- Title and subtitle -->
                        <v-list-item-title class="headline mb-1 white--text">
                          12 searches left only! 
                        </v-list-item-title>
                        <v-list-item-subtitle class="white--text">switch to premium now!</v-list-item-subtitle>
  
                        <div class="buton">
                          <!-- Button to upload log file -->
                          <v-btn
                            class="text-none text-subtitle-1 v-button"
                            color="#17ffee"
                            size="small"
                            variant="flat"
                            href="/upload"
                          >
                            Upload log file
                          </v-btn>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-card>
            </v-hover>
          </v-col>
          <v-col cols="12" sm="4">
            <!-- Card 2 -->
            <v-hover v-slot="{hover }" open-delay="200">
              <v-card id="grad2" :elevation="hover ? 16 : 2">
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-list-item three-line>
                      <v-list-item-content>
                        <div class="mb-4">
                         
                        </div>
                        <!-- Title and subtitle -->
                        <v-list-item-title class="headline mb-1 white--text">
                          72 uploaded
                        </v-list-item-title>
                        <v-list-item-subtitle class="white--text">Check your previous results</v-list-item-subtitle>
                        <div class="buton">
                          <!-- Button to check results -->
                          <v-btn
                            class="text-none text-subtitle-1 v-button"
                            color="#17ffee"
                            size="small"
                            variant="flat"
                            href="/result"
                          >
                            Previous results
                          </v-btn>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-card>
            </v-hover>
          </v-col>
          <v-col cols="12" sm="4">
            <!-- Card 3 -->
            <v-hover v-slot="{ hover }" open-delay="200">
              <v-card id="grad3" :elevation="hover ? 16 :2">
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-list-item three-line>
                      <v-list-item-content>
                        <div class="mb-4">
                         
                        </div>
                        <!-- Title and subtitle -->
                        <v-list-item-title class="headline mb-1 white--text">
                          13 most common errors
                        </v-list-item-title>
                        <v-list-item-subtitle class="white--text">Graphs and Analysis</v-list-item-subtitle>
                        <div class="buton">
                          <!-- Button check it out -->
                          <v-btn
                            class="text-none text-subtitle-1 v-button"
                            color="#17ffee"
                            size="small"
                            variant="flat"
                          >
                            check it out!
                          </v-btn>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                 
                </v-row>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </template>
  
  
  <script>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '../stores/auth'; // Import the Pinia store

export default {
  name: 'Home',
  setup() {
    const message = ref('You are not logged in!');
    const authStore = useAuthStore(); // Use the Pinia store

    onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/user', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    });

    if (response.status === 200) {
      console.log("Success");
      const content = await response.json();
      message.value = `Hi ${content.name}`;
      authStore.setAuth(true);
    } else {
      authStore.setAuth(false);
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
    authStore.setAuth(false);
  }
});

    return {
      message, authStore
    };
  },

  methods: {

    login(){

this.$router.push('/login');

    },

async logout(){

try {

      const authStore = useAuthStore();
      // Send a logout request to your backend API
      const response = await fetch('http://127.0.0.1:8000/logout', {
        method: 'POST',
        credentials: 'include', // Include cookies in the request
      });

      if (response.status === 200) {
        
        authStore.setAuth(false); 

        console.log("heya i am logged out");
        this.$router.push('/login');
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }

  }
  }
};
</script>


 
  <style scoped>


  .border {
    border-right: 1px solid grey
  }
  
  .buton {
    padding-top: 1.5rem;
    color: white;
    
  }
  
  
  #grad1 {
    background-image: linear-gradient(#D333FF, #CC17FF ,#Ca0aff);
    color:white;
  }
  
  #grad2 {
    background-image: linear-gradient(#7B23e7, #6917d0 ,#6716CA);
    color:white;
  }
  
  #grad3 {
  background-image: linear-gradient(#FF33a0, #FF1791 ,#FF0a8D);
  color: white;
  
  }
  
  .v-button {
    color: black;
    background: #17ffee;
  }

  .logo-pos {
    margin-right: 10px;
  }
  </style>