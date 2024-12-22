<template>

    <div class="home">
        <q-btn outline rounded color="primary" label="Войти"
        @click="goToAuthPage('login')" style="width: 200px; height: 20px;" />
        <br>
        <q-btn outline rounded color="primary" label="Зарегистрироваться"
        @click="goToAuthPage('register')" style="margin-top: 20px; width: 200px; height: 20px;" />
    </div>
    <div>
        <p>СПБГУ Винчик</p>
    </div>
  </template>

  <script>
    import { useRouter } from 'vue-router';

    export default {
      setup() {
        const router = useRouter();

        const goToAuthPage = (page) => {
          console.log("Go to autarisation page", page);
          router.push( {path: '/auth', query: { from: page }
        });

        };



        return { goToAuthPage};
      },
    };
  </script>

  <style scoped>
  .home {
    margin: 0;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-right: -50%;
    transform: translate(-50%, -50%);
  }

  p {
    text-align: center;
    font-size: xx-large;
    color: grey;
  }
  </style>
