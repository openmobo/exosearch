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
        <div class="mb-3">
            <label for="From Date" class="form-label">From Date</label>
            <input type="text" class="form-control" id="fromDate" v-model="fromDate" required>
          </div>

        <div class="mb-3">
            <label for="From Date" class="form-label">To Date</label>
            <input type="text" class="form-control" id="toDate" v-model="toDate" required>
          </div>

        <v-btn @click="searchLogs" class="custom-button">Search</v-btn>
      </div>

  
    </div>

    <div class="search-results">
      <h3>Search Results</h3>
     
      <select v-model="selectedFile" class="input-field" @change="filenameSelected">
        <option value="" disabled selected>Please select a file</option>
      <option v-for="item in items" :key="item" :value="item">{{ item.file_name }}</option>
       </select>






      <table class="table table-bordered">
        
        <thead>
          <tr>
            <th>File Name</th>
            <th>Date</th>
            <th>Time</th>
            <th>Log Data</th>
          </tr>
        </thead>


      


        <tbody>
            <tr v-for="(log, logIndex) in paginatedItems" :key="logIndex">
             
              <td>{{ selectedFile.file_name }}</td>
              <td>
               
                  {{ formatDate(log.log_datetime) }}
             
              </td>
              <td>
               
                  {{ formatTime(log.log_datetime) }}
                
              </td>
              <td>
               
                  {{ log.log_data }}
             
              </td>
            </tr>
          </tbody>
       
       
      </table>

      <pagination v-model="page" :records="totalItems" :per-page="perPage" @paginate="pageChanged"/>
      
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import 'bootstrap-datepicker/dist/css/bootstrap-datepicker.css';
import 'bootstrap-datepicker';
import axios from 'axios';
import Pagination from 'v-pagination-3';
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

  components: {
    Pagination,
  },

  data() {
    return {
      fromDate: '',
      toDate: '',
      searchQuery: '',
      items: [],
      paginatedItems: [],
      page: 1,
      perPage: 5,
      totalItems: 0,
      pageCount: 0,
      selectedFile:'',
      totalItemData:[],
    };
  },

  mounted() {
    $(this.$el)
      .find('#fromDate')
      .datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
      })
      .on('changeDate', (e) => {
        this.fromDate = e.target.value;
      });

      $(this.$el)
      .find('#toDate')
      .datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
      })
      .on('changeDate', (e) => {
        this.toDate = e.target.value;
      });
  },

  methods: {

    formatDate(datetime) {
      if (datetime) {
        const date = new Date(datetime);
        return date.toDateString();
      }
    },
    formatTime(datetime) {
      if (datetime) {
        const date = new Date(datetime);
        return date.toLocaleTimeString();
      }
    },


    searchLogs() {
      email = this.authStore.email;

      axios
        .get(`http://127.0.0.1:8000/forwarder-data/?query=${this.searchQuery}&email=${email}&from=${this.fromDate}&to=${this.toDate}`)
        .then((response) => {
          this.items = response.data;
          console.log(this.items);
          
          
        })
        .catch((error) => {
          console.error('Error searching logs', error);
        });
    },

    filenameSelected(){

     console.log(this.selectedFile);
     this.totalItems = this.selectedFile.log_data.length;

     this.pageCount = Math.ceil(this.totalItems / this.perPage);
          this.page = 1;
          this.paginateItems();


    },

    paginateItems() {
      const startIndex = (this.page - 1) * this.perPage;
      console.log(this.selectedFile)
      this.paginatedItems = this.selectedFile.log_data.slice(startIndex, startIndex + this.perPage);
      
    },

    pageChanged(page) {
      this.page = page;
      this.paginateItems();
    },
  },

  
};
</script>

<style>
.search-results {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.input-field {
  width: 30%;
  padding: 12px;
  margin: 10px, 0px ;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
