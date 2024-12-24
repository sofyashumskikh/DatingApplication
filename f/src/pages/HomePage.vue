<template>
  <div class="text-container">
  <p>Добро пожаловать в наше приложение для знакомств! Здесь вы сможете найти новых друзей, единомышленников и, возможно, свою вторую половинку.
    Просто зарегистрируйтесь и начните искать! Мы предлагаем удобный интерфейс и множество возможностей для общения. Независимо от того, какие
    у вас интересы или цели, у нас вы найдете то, что ищете. Присоединяйтесь к нам и откройте для себя новые горизонты!</p>
  </div>
  <div class="home">
    <q-btn outline rounded color="lime-1" label="Войти" @click="goToAuthPage('login')" style="width: 200px; height: 20px;" />
    <br>
    <q-btn outline rounded color="lime-1" label="Зарегистрироваться" @click="goToAuthPage('register')"
      style="margin-top: 20px; width: 200px; height: 20px;" />
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const goToAuthPage = (page) => {
      console.log("Go to autarisation page");
      router.push({ path: '/auth', query: { from: page } })

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

.text-container {
  padding-top: 5px;
  padding-bottom: 5px;
  border-radius: 50px;
  margin-top: 5%;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}

p {
  text-align: center;
  font-size: x-large;
  color: whitesmoke;
  margin-left: 20px;
  margin-right: 20px;
}
</style>
