<template>
  <q-layout view="lHh Lpr lFf">
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

const linksList = [
  {
    title: 'Поиск',
    icon: 'school',
    to: '/search', // Для внутреннего маршрута
  },
  {
    title: 'Мэтчи',
    icon: 'code',
    to: '/matches', // Для внутреннего маршрута
  },
  {
    title: 'Выход',
    icon: 'chat',
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
    return {
      linksList,
    }
  },
})
</script>

<style scoped></style>
