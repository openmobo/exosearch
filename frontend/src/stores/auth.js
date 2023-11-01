import { defineStore } from 'pinia';

// Define your store
export const useAuthStore = defineStore('auth', {
  state: () => ({
    authenticated: false,
    name: '',
    email: '',
  }),
  actions: {
    // Define your setAuth action
    setAuth(auth) {
      this.authenticated = auth;
    },
    setName(name) {
      this.name = name;
    },
    setEmail(email) {
      this.email = email;
    },
  },
});