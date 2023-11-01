<template>
  

  
    <div class="login-container">
      <div class="login-form">
       
        <v-avatar class="logo-pos" size="120">
              <v-img src="../assets/exosearch-high-resolution-logo-transparent.png"></v-img>
            </v-avatar>
 
     
        <form @submit.prevent="submitForm">
          
            <input
              v-model="currentPassword"
              type="password"
              placeholder="Current Paaword"
              required
              class="input-field"
            />
         
          <input
            v-model="newPassword"
            placeholder="New Password"
            required
            class="input-field"
          />
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirm Password"
            required
            class="input-field"
          />

          <v-btn type="submit">Sumbit</v-btn>
  
  
        </form>
       
      </div>
    </div>
  </template>
    
    <script>
    import { useAuthSetup } from '../recall function/authsetup'
let email;

export default {
 

  setup() {
    const { authStore, fetchData } = useAuthSetup();

    // Call fetchData to fetch and set authentication data
    fetchData();

    

    return {
      authStore,
    };
  },
      data() {
        
        return {
          
            currentPassword: '',

            newPassword: '',

            confirmPassword: '',
          
        };
      },
      methods: {
       
        async submitForm() {

          email = this.authStore.email;
           
            

            const changePassData = {
                email: email,
               currentPassword: this.currentPassword,
               password: this.confirmPassword,
                };

                console.log(changePassData);
                console.log(email);

                if(this.newPassword == this.confirmPassword){
  
                try {
            const response = await fetch('http://127.0.0.1:8000/changepass', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             credentials: 'include',
            body: JSON.stringify(changePassData),         
              });

              console.log(response)

              this.$router.push('/')
 
        } catch (error) {
       console.error('An error occurred during password change', error);
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
  
  
  
  </style>
    