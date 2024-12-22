<template>
  <div class="login-page">
    <div class="text-center">
      <h2 style="color: whitesmoke;">Авторизация</h2>
    </div>
    <div class="exit-container">
      <q-btn outline rounded color="lime-2" label="Назад" @click="logout" />
    </div>
    <div class="fixed-center" style="width: 450px;">
      <q-card class="my-card">
        <q-card-section>
          <q-input outlined label="Email" v-model="email" />
          <br>
          <q-input outlined label="Password" v-model="password" type="password" />
          <br>
          <q-btn v-if="from === 'login'"  outline rounded color="primary" label="Login" @click="login" />
          <q-btn v-if="from === 'register'" outline rounded color="primary" label="Register" @click="register" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { ref } from "vue";
export default {
  setup() {
    const router = useRouter();
    const email = ref("");
    const password = ref("");
    const route = useRoute()
    const from = route.query.from // Получаем параметр from из URL
    const baseURL = 'http://localhost:7000'
    // Перехватчик axios
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("/auth");
        }
        return Promise.reject(error);
      }
    );

    const login = () => {
      if (!email.value || !password.value) {
        alert("Пожалуйста, заполните все поля.");
        return;
      }

      axios
        .post(`${baseURL}/api/login`, {
          email: email.value,
          password: password.value,
        })
        .then((response) => {
          alert('Успешно вошли!')
          const token = response.data.token
          const active = response.headers['x-active']
          const moderated = response.headers['x-moderated']
          const role = response.headers['x-role']

          localStorage.setItem('moderated', moderated)
          localStorage.setItem('token', token)
          localStorage.setItem('role', role)
          localStorage.setItem('active', active)
          console.log('Active:', active)
          console.log('Moderated:', moderated)
          console.log('Role:', role)
          router.push('/app/search')
        })
        .catch((error) => {
          const statusCode = error.response.status
          // Обработка разных типов ошибок
          if (statusCode === 400) {
            alert('Пользователя нет.')
          } else {
            alert('Ошибка при регистрации. Попробуйте позже.')
          }
        })
    };
    const register = () => {
      if (!email.value || !password.value) {
        alert('Пожалуйста, заполните все поля.')
        return
      }

      axios
        .post(`${baseURL}/api/register`, {
          email: email.value,
          password: password.value,
        })
        .then((response) => {
          alert('Успешно вошли!')
          const token = response.data.token
          //const active = response.headers['x-active'];
          const role = response.headers['X-Role']
          sessionStorage.setItem('token', token)
          sessionStorage.setItem('role', role) // Сохраняем роль в localStorage
          if (role == 'user') {
            router.push('/app/profile')
          } else {
            router.push('/app/search')
          }
        })
        .catch((error) => {
          const statusCode = error.response.status
          // Обработка разных типов ошибок
          if (statusCode === 400) {
            alert('Пользователь с таким email уже существует.')
          } else {
            alert('Ошибка при регистрации. Попробуйте позже.')
          }
        })
    }
    const logout = () => {
      localStorage.removeItem('token')
      router.push("/");
    };

    return {
      email,
      password,
      login,
      logout,
      from,
      register
    };
  },
};
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.exit-container {
  position: absolute;
  top: 5%;
  right: 5%;
}
</style>
