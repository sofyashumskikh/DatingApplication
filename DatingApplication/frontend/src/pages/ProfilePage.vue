<template>
  <div class="profile-page">
    <div class="text-center">
      <h2 style="color: whitesmoke;">Редактирование профиля</h2>
    </div>
    <div class="form-conteiner">
      <q-card class="my-card" style="width: 450px;">
        <q-card-section>
          <q-img :src="profileImage" style="width: 400px; height: 400px"></q-img>
          <br>
          <div class="buttons-container">
            <q-btn outline rounded color="primary" label="изменить фото" @click="change" style="margin-right: 100px" />
            <q-btn outline rounded color="primary" label="добавить фото" @click="add" />
          </div>
          <input type="file" ref="fileInput" style="display: none" @change="changeFile">
          <br>
          <q-input outlined label="Имя" v-model="Name" />
          <br>
          <q-input outlined label="Фамилия" v-model="Surname" />
          <br>
          <q-input outlined label="Страна" v-model="Country" />
          <br>
          <q-input outlined label="Город" v-model="Town" />
          <br>
          <q-input outlined label="Пол" v-model="Sex" />
          <br>
          <q-input outlined label="Возраст" v-model="Age" />
          <br>
          <q-input outlined label="Контакты" v-model="TgNick" />
          <br>
          <q-input uutlined label="Обо мне" v-model="Description" />
          <br>
          <q-btn outline rounded color="primary" label="OK" @click="ok" style="margin-right: 200px;" />
          <q-btn outline rounded color="primary" label="Удалить аккаунт" @click="del" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>

import { useRouter } from "vue-router"
import { useQuasar } from "quasar"
import { ref } from "vue";
import axios from "axios";

export default {
  setup() {

    const $q = useQuasar();
    const router = useRouter();
    const Name = ref("");
    const Surname = ref("");
    const Country = ref("");
    const Town = ref("");
    const Sex = ref("");
    const Age = ref("");
    const TgNick = ref("");
    const Description = ref("")
    const fileInput = ref(null);
    const profileImage = ref("https://cdn.quasar.dev/img/parallax2.jpg");

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("/auth");
        }
        return Promise.reject(error);
      }
    );

    const changeFile = (event) => {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
              profileImage.value = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      };

    const change = () => {
      fileInput.value.click();
    };

    const add = () => {};
    const ok = () => { };
    const del = () => {
      $q.dialog({
        dark: true,
        message: "Вы уверены, что хотите удалить аккаунт?",
        cancel: true,
        persistent: true
      }).onOk(() => {
        // удаляем аккаунт
      }).onCancel(() => {
        // ниче не делаем
      })
    };

    return {
      Name,
      Surname,
      Country,
      Town,
      Sex,
      Age,
      TgNick,
      Description,
      fileInput,
      profileImage,
      changeFile,
      change,
      add,
      ok,
      del,
    };
  },
};
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.form-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.buttons-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.my-card {
    background-color: rgba(255, 255, 255, 0.8);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
</style>
