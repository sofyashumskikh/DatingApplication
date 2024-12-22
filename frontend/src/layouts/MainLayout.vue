<template>
  <q-layout view="lHh Lpr lFf">
        <!-- Header с кнопкой выхода для админа -->

    <q-drawer
      :model-value="true"
      show-if-above
      :mini="miniOpen"
      bordered
      class="menu-item"
      :width="240"
      behavior="desktop"
    >
      <q-list>
        <q-item>
          <q-item-section>
            <q-item-label class="label">Dating</q-item-label>
          </q-item-section>
        </q-item>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { useRouter } from "vue-router";

const linksList = [
  {
    title: 'Поиск',
    icon: 'search',
    to: '/app/search', // Для внутреннего маршрута
  },
  {
    title: 'Мэтчи',
    icon: 'favorite',
    to: '/app/matches', // Для внутреннего маршрута
  },
  {
    title: 'Профиль',
    icon: 'settings',
    to: '/app/profile', // Для внутреннего маршрута
  },
  {
    title: 'Выход',
    icon: 'exit_to_app',
    action: () => {
      //userStore.clearAll() example
    },
    to: '/', // Перенаправление на главную страницу после выхода
  },
]

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink,
  },

  setup() {
        // Получаем роль из localStorage
    const role = sessionStorage.getItem('role');
    const router = useRouter();

    // Функция выхода
    const logout = () => {
      // Очистить токен и роль из localStorage
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('role');

      router.push('/');
    };
    return {  role,
      linksList,
      logout
    }
  },
})
</script>

<style scoped>
.label {
  font-size: 40px;  /* Увеличиваем размер шрифта */
  font-weight: bold;  /* Делаем текст жирным */
}</style>
