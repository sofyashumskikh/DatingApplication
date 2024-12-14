<template>
    <div class="login-page">
      <div class="text-center">
        <h2>Авторизация</h2>
      </div>
      <div class="fixed-center" style="width: 450px;">
        <q-card class="my-card">
          <q-card-section>
            <q-input outlined label="Email" v-model="email" />
            <br>
            <q-input outlined label="Password" v-model="password" type="password"/>
            <br>
            <q-btn outline rounded color="primary" label="Login" @click="login"/>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </template>
  
  <script>
    export default {
        setup() {
            return {
                email: '',
                password: '',
            };
        },
        methods: {
            login() {
            },
        },  
    };
  </script>
  
  <style lang="sass">
  .my-card
    width: 100%
    max-width: 500px 
  </style>