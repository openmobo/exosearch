import { defineStore } from 'pinia';

// Define your store
export const useAuthStore = defineStore('auth', {
  state: () => ({
    authenticated: false,
  }),
  actions: {
    // Define your setAuth action
    setAuth(auth) {
      this.authenticated = auth;
    },
  },
});