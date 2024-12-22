<template>
    <div class="profile-page">
      <div class="text-center">
        <h2>Редактирование профиля</h2>
      </div>
        <div class="form-conteiner">
        <q-card class="my-card" style="width: 450px;">
          <q-card-section>
            <q-input outlined label="Имя" v-model="Name"/>
            <br>
            <q-input outlined label="Фамилия" v-model="Surname"/>
            <br>
            <q-input outlined label="Страна" v-model="Country"/>
            <br>
            <q-input outlined label="Город" v-model="Town"/>
            <br>
            <q-input outlined label="Пол" v-model="Sex"/>
            <br>
            <q-input outlined label="Возраст" v-model="Age"/>
            <br>
            <q-input outlined label="Контакты" v-model="TgNick"/>
            <br>
            <q-btn outline rounded color="primary" label="OK" @click="ok"/>
          </q-card-section>
        </q-card>
      </div>
      </div>
  </template>
  
  <script>
    export default {
        setup() {
            return {
              Name: '',
              Surname: '',
              Country: '',
              Town: '',
              Sex: '',
              Age: '',
              TgNick: ''
            };
        },
        methods: {
            ok() {
            },
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
  </style>