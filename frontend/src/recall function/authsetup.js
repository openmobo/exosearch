import { useAuthStore } from '../stores/auth';
let email

export function useAuthSetup() {
  const authStore = useAuthStore();

  async function fetchData() {
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
        authStore.setName(content.name);
        authStore.setEmail(content.email);
      } else {
        authStore.setAuth(false);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      authStore.setAuth(false);
    }
  }

  return {
    authStore,
    fetchData,
  };
}
