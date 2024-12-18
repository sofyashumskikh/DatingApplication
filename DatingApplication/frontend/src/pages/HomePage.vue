<template>
  <p>Добро пожаловать в наше приложения для знакомств, располагайтесь поудобнее и начинайте искать!</p>
  <div class="home">
    <q-btn outline rounded color="lime-1" label="Войти" @click="goToAuthPage" style="width: 200px; height: 20px;" />
    <br>
    <q-btn outline rounded color="lime-1" label="Зарегистрироваться" @click="goToAuthPage"
      style="margin-top: 20px; width: 200px; height: 20px;" />
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
  left: 59%;
  margin-right: -50%;
  transform: translate(-50%, -50%);
}

p {
  text-align: center;
  font-size: xx-large;
  color: whitesmoke;
  margin-left: 20px;
  margin-right: 20px;
}
</style>
