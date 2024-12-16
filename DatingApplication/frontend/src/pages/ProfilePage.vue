<template>
  <div class="profile-page">
    <div class="text-center">
      <h2>Редактирование профиля</h2>
    </div>
    <div class="form-conteiner">
      <q-card class="my-card" style="width: 450px;">
        <q-card-section>
          <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="width: 450px; height: 450px"></q-img>
          <br>
          <div class="buttons-container">
            <q-btn outlined rounded color="primary" label="изменить фото" @click="change" style="margin-right: 300px" />
            <q-btn outlined rounded color="primary" label="добавить фото" @click="add" />
          </div>
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
          <br>
          <q-checkbox left-label v-model="left" label="удалить аккаунт"/>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>

import { ref } from "vue";

const Name = ref("");
const Surname = ref("");
const Country = ref("");
const Town = ref("");
const Sex = ref("");
const Age = ref("");
const TgNick = ref("");
const Description = ref("")

const change = () => { };
const add = () => { };
const ok = () => { };
const del = () => { };

export default {
  setup() {
    return {
      Name,
      Surname,
      Country,
      Town,
      Sex,
      Age,
      TgNick,
      Description,
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
</style>
