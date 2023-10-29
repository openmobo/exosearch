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

    <!-- Display Search Results -->
    <!-- <div class="search-results">
      <h3>Search Results</h3>
      <ul>
        <li v-for="log in items" :key="log.id">
          <b>{{ log.file_name }}</b> - {{ log.log_data }}
        </li>
      </ul>
    </div> -->
    </div>

    <div class="search-results">
      <h3>Search Results</h3>
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
              <td>{{ log.file_name }}</td>
              <td>
                <div class="table-margin" v-for="(logEntry, entryIndex) in log.log_data" :key="entryIndex">
                  {{ formatDate(logEntry.log_datetime) }}
                </div>
              </td>
              <td>
                <div class="table-margin" v-for="(logEntry, entryIndex) in log.log_data" :key="entryIndex">
                  {{ formatTime(logEntry.log_datetime) }}
                </div>
              </td>
              <td>
                <div class="table-margin" v-for="(logEntry, entryIndex) in log.log_data" :key="entryIndex">
                  {{ logEntry.log_data }}
                </div>
              </td>
            </tr>
          </tbody>
      </table>

      <pagination :data="items" @pagination-change-page="pageChanged" :limit="perPage" :pagination="pagination"></pagination>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import 'bootstrap-datepicker/dist/css/bootstrap-datepicker.css';
import 'bootstrap-datepicker';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import VuejsPaginate from 'vuejs-paginate';

let email;

export default {
  components: {
    VuejsPaginate,
  },

  data() {
    return {
      fromDate: '',
      toDate: '',
      searchQuery: '',
      items: [],
      paginatedItems: [],
      page: 1,
      perPage: 100,
      totalItems: 0,
      pageCount: 0,
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
      axios
        .get(`http://127.0.0.1:8000/forwarder-data/?query=${this.searchQuery}&email=${email}&from=${this.fromDate}&to=${this.toDate}`)
        .then((response) => {
          this.items = response.data;
          console.log(this.items);
          this.totalItems = this.items.length;
          this.pageCount = Math.ceil(this.totalItems / this.perPage);
          this.page = 1;
          this.paginateItems();
        })
        .catch((error) => {
          console.error('Error searching logs', error);
        });
    },

    paginateItems() {
      const startIndex = (this.page - 1) * this.perPage;
      this.paginatedItems = this.items.slice(startIndex, startIndex + this.perPage);
    },

    pageChanged(page) {
      this.page = page;
      this.paginateItems();
    },
  },

  setup() {
    const authStore = useAuthStore();

    onMounted(async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/user', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
        });

        if (response.status === 200) {
          const content = await response.json();
          email = content.email;
          authStore.setAuth(true);
        } else {
          authStore.setAuth(false);
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        authStore.setAuth(false);
      }
    });
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
.table-margin{
  margin-bottom: 30px;
}
</style>
