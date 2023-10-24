<template>
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h2>Search Log Files</h2>
        </div>
        <div class="card-body">
          <div class="mb-3">
            <label for="searchQuery" class="form-label">Search Query</label>
            <input
              type="text"
              class="form-control"
              id="searchQuery"
              v-model="searchQuery"
            />
          </div>
          <v-btn @click="searchLogs" class="custom-button">Search</v-btn>
        </div>
      </div>
  
      <!-- Display Search Results -->
      <div class="search-results">
        <h3>Search Results</h3>
        <ul>
          <li v-for="log in searchResults" :key="log.id">
            <b>{{ log.file_name }}</b> - {{ log.log_data }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchQuery: '',
        searchResults: [],
      };
    },
    methods: {
      searchLogs() {
        // Send a request to your Django backend to search for log files based on the searchQuery
        axios
          .get(`http://127.0.0.1:8000/forwarder-data/?query=${this.searchQuery}`)

          .then((response) => {
            this.searchResults = response.data;
            console.log(this.searchResults);
          })
          .catch((error) => {
            console.error('Error searching logs', error);
          });
      },
    },
  };
  </script>
  
  <style>
  .search-results {
    margin-top: 20px;
  }
  </style>
  