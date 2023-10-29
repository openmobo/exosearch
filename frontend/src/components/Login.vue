<template>
  

  
  <div class="login-container">
    <div class="login-form">
     
      <v-avatar class="logo-pos" size="120">
            <v-img src="../assets/exosearch-high-resolution-logo-transparent.png"></v-img>
          </v-avatar>
      <h2 class="form-title">{{ tab === 'login' ? 'Login' : 'Register' }}</h2>

   
      <form @submit.prevent="submitForm">
        <div v-if="tab === 'register'">
          <input
            v-model="formData.name"
            type="text"
            placeholder="Username"
            required
            class="input-field"
          />
        </div>
        <input
          v-model="formData.email"
          type="email"
          placeholder="Email"
          required
          class="input-field"
        />
        <input
          v-model="formData.password"
          type="password"
          placeholder="Password"
          required
          class="input-field"
        />

        <div v-if="tab === 'register'">
  <select v-model="formData.role" class="input-field">
    <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
  </select>
</div>

        <button @click="authAction" type="submit" class="submit-button">
          {{ tab === 'login' ? 'Login' : 'Register' }}
        </button>
      </form>
      <button @click="toggleTab" class="tab-toggle">
        {{ tab === 'login' ? 'Switch to Register' : 'Switch to Login' }}
      </button>
    </div>
  </div>
</template>
  
  <script>
  
  
  export default {
    data() {
      
      return {
        tab: 'login',
        formData: {
          name: '',
          email: '',
          password: '',
          role: 'admin',
        },

        roles: ['admin', 'role1', 'role2'], // Available roles
        
      };
    },
    methods: {
      toggleTab() {
        this.tab = this.tab === 'login' ? 'register' : 'login';
      },
      async submitForm() {
        if (this.tab === 'register') {
           
           await fetch('http://127.0.0.1:8000/register', {
         method: 'POST',
         headers: {'Content-Type': 'application/json'},
         body: JSON.stringify(this.formData)
       });
 
        this.tab = 'login'
 
       
 
         }
 
         if (this.tab === 'login') { 

          const loginData = {
             email: this.formData.email,
             password: this.formData.password,
              };

              try {
          const response = await fetch('http://127.0.0.1:8000/login', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           credentials: 'include',
          body: JSON.stringify(loginData),

         
  });

  if (response.ok) {
   console.log("successful") // Successful login 
   this.$router.push('/')
  } else {
    // Handle login error
    console.error('Login failed:', response.status, response.statusText);
  }
} catch (error) {
  console.error('An error occurred during login:', error);
}
         }
 
      },



    },
  };
  </script>
  
 
<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
  margin-top: -30px;
}

.login-form {
  text-align: center;
  background: #ffffff;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  max-width: 400px;
}

.form-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #007bff;
}

.input-field {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.3s;
}

.submit-button:hover {
  background: #0056b3;
}

.tab-toggle {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #007bff;
  text-decoration: underline;
}

.logo-pos {
  margin-top: -60px;
  margin-bottom: -50px;
  margin-right: 500px;
}

</style>
  