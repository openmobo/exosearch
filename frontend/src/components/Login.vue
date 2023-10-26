<template>
    <div class="login-container">
      <div class="login-form">
        <h2>{{ tab === 'login' ? 'Login' : 'Register' }}</h2>
        <form @submit.prevent="submitForm">
          <div v-if="tab === 'register'">
            <input
              v-model="formData.name"
              type="text"
              placeholder="Username"
              required
            />
          </div>
          <input
            v-model="formData.email"
            type="email"
            placeholder="Email"
            required
          />
          <input
            v-model="formData.password"
            type="password"
            placeholder="Password"
            required
          />
          <button @click="authAction" type="submit">{{ tab === 'login' ? 'Login' : 'Register' }}</button>
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
        },
        
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
    background-color: #f5f5f5; /* Background color */
  }
  
  .login-form {
    text-align: center;
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    max-width: 400px; /* Limit the width of the form */
  }
  
  input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 12px;
    background: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 4px;
    transition: background 0.3s;
  }
  
  button:hover {
    background: #0056b3;
  }
  
  .tab-toggle {
    background: transparent;
    border: none;
    cursor: pointer;
    color: #007bff;
    text-decoration: underline;
  }
  </style>
  