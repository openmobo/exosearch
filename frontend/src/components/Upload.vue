<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h2>Upload Log File</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent> <!-- Handle form submission here -->
          <div class="mb-3">
            <label for="logFile" class="form-label">Log File</label>
            <input type="file" name="file" class="form-control" id="logFile" @change="handleFileUpload" required />
          </div>
          <div class="mb-3">
            <label for="logDescription" class="form-label">Log Description</label>
            <textarea class="form-control" v-model="LogUpload.body" required></textarea>
          </div>
          <div class="mb-3">
            <label for="logDate" class="form-label">Today's Date</label>
            <input type="text" class="form-control" id="logDate" v-model="LogUpload.created_at" required>
          </div>
          <v-btn href="/result" @click = "saveLogUpload" type="submit" class="custom-button">Upload</v-btn>
        </form>
      </div>
    </div>
    <div class="log-upload-details"></div>
  </div>
</template>

<script>
import $ from 'jquery';
import 'bootstrap-datepicker/dist/css/bootstrap-datepicker.css';
import 'bootstrap-datepicker';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useAuthStore } from '../stores/auth'; // Import the Pinia store
import LoginVue from './Login.vue';

let email;

export default {
  data() {
    return {
      result: {},
      LogUpload: {
        uploadedFile: '',
        body: '',
        created_at: '',
        email: '',
      },
      selectedLogUpload: [],
    };
  },

  mounted() {
    $(this.$el)
      .find('#logDate')
      .datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
      })
      .on('changeDate', (e) => {
        this.LogUpload.created_at = e.target.value;
      });
  },

  methods: {
    handleFileUpload(event) {
      // Handle file upload and set the file name
      this.LogUpload.uploadedFile = event.target.files[0] || null; // Store the File object

    },

    saveLogUpload() {
      this.LogUpload.email = email; 
      const formData = new FormData();
      formData.append('logFile', this.LogUpload.uploadedFile); // Change this line to use the file input value
      formData.append('logDescription', this.LogUpload.body);
      formData.append('logDate', this.LogUpload.created_at);
      formData.append('email', this.LogUpload.email);

      axios
        .post('http://127.0.0.1:8000/upload-log/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        })
        .then(({ data }) => {
          alert('Log File Upload saved!');
          this.LogUpload.uploadedFile = null;
          this.LogUpload.body = '';
          this.LogUpload.created_at = '';
        });
    },
  },


  setup() {
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
      console.log(content);
      email = content.email;
      console.log(email);
      
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
       authStore
    };
  },

};
</script>

<style>
.log-upload-details {
  margin-top: 20px;
}
</style>
