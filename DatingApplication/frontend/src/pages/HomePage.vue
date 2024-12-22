<template>
    <div class="text-center">
        <p>some text about app</p>
    </div>
    <div class="home">
        <q-btn outline rounded color="primary" label="Войти" 
        @click="goToAuthPage" style="width: 200px; height: 20px;" />
        <br>
        <q-btn outline rounded color="primary" label="Зарегистрироваться" 
        @click="goToAuthPage" style="margin-top: 20px; width: 200px; height: 20px;" />
    </div>
  </template>
  
  <script>
    import { useRouter } from 'vue-router';
  
    export default {
      setup() {
        const router = useRouter();
  
        const goToAuthPage = () => {
          console.log("Go to autarisation page")
          router.push("/auth")
        };
  
        return { goToAuthPage };
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