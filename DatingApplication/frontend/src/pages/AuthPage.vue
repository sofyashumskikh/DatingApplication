<template>
  <div class="login-page">
    <div class="text-center">
      <h2 style="color: whitesmoke;">Авторизация</h2>
    </div>
    <div class="fixed-center" style="width: 450px;">
      <q-card class="my-card">
        <q-card-section>
          <q-input outlined label="Email" v-model="email" />
          <br>
          <q-input outlined label="Password" v-model="password" type="password" />
          <br>
          <q-btn outline rounded color="primary" label="Login" @click="login" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref } from "vue";
export default {
  setup() {
    const router = useRouter();
    const email = ref("");
    const password = ref("");

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
        .post("/api/login", {
          email: email.value,
          password: password.value,
        })
        .then(() => {
          alert("Успешно вошли!");
          router.push("/"); // Перенаправить на главную
        })
        .catch((error) => {
          console.error(error);
          alert("Ошибка при входе. Проверьте введённые данные.");
        });
    };

    return {
      email,
      password,
      login,
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
</style>
