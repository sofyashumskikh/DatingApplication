<template>
  <div id="app" class="background">
  <router-view />
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App'
});
</script>

<style>
.background {
    background-image: url("https://t4.ftcdn.net/jpg/07/28/65/59/360_F_728655984_sRoDyIVYPWW1cScnWBExeAMyzBorJBnX.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
</style>
