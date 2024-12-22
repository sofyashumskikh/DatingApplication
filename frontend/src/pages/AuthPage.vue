<template>
  <div class="login-page">
    <div class="text-center">
      <h2>Авторизация</h2>
    </div>
    <div class="fixed-center" style="width: 450px">
      <q-card class="my-card">
        <q-card-section>
          <q-input outlined label="Email" v-model="email" />
          <br />
          <q-input outlined label="Password" v-model="password" type="password" />
          <br />
          <q-btn
            v-if="from === 'login'"
            outline
            rounded
            color="primary"
            label="Login"
            @click="login"
          />
          <q-btn
            v-if="from === 'register'"
            outline
            rounded
            color="primary"
            label="Register"
            @click="register"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
export default {
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const route = useRoute()
    const from = route.query.from // Получаем параметр from из URL
    const baseURL = 'http://localhost:7000'
    onMounted(() => {
      console.log('Компонент был смонтирован')
      // Например, здесь можно получить роль пользователя из localStorage
      console.log(route.query.from)
    })

    // Перехватчик axios
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push({ path: '/auth', query: 'login' })
        }
        return Promise.reject(error)
      },
    )

    const login = () => {
      if (!email.value || !password.value) {
        alert('Пожалуйста, заполните все поля.')
        return
      }

      axios
        .post(`${baseURL}/api/login`, {
          email: email.value,
          password: password.value,
        })
        .then((response) => {
          alert('Успешно вошли!')
          const token = response.data.token
          /*const active = response.headers['X-Active'];
          const moderated = response.headers['X-Moderated'];

          const role = response.headers['X-Role'];
          console.log(response);
          console.log(response.headers);
          console.log(response.headers['X-Role']);
          console.log(response.headers['x-role']);
          */ // Сохраняем роль в localStorage
          const active = response.headers['x-active']
          const moderated = response.headers['x-moderated']
          const role = response.headers['x-role']

          sessionStorage.setItem('moderated', moderated)
          sessionStorage.setItem('token', token)
          sessionStorage.setItem('role', role)
          sessionStorage.setItem('active', active)
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
    }

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

    return {
      email,
      password,
      login,
      from,
      register,
    }
  },
}
</script>

<style lang="sass">
.my-card
  width: 100%
  max-width: 500px
</style>
