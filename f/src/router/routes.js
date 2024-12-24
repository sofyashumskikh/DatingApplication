import AuthPage from 'pages/AuthPage.vue'
import MainLayout from 'layouts/MainLayout.vue';
import EmptyLayout from 'layouts/EmptyLayout.vue'; // Для страниц, которые не требуют общего макета

const routes = [
  {
    path: '/',
    component: EmptyLayout, // Используем EmptyLayout для главной страницы
    children: [
      {
        path: '',
        component: () => import('pages/HomePage.vue'), // Главная страница
      },
      {
        path: 'auth',
        component: AuthPage, // Страница авторизации
      },
      {
        path: 'moderate',
        component: () => import('pages/ModerPage.vue'), // Страница модерации
      }
    ]
  },
  {
    path: '/app',
    component: MainLayout, // Используем MainLayout для страниц после авторизации
    children: [
      {
        path: 'profile',
        component: () => import('pages/ProfilePage.vue'),
      },
      {
        path: 'search',
        component: () => import('pages/SearchPage.vue'),
      },
      {
        path: 'match',
        component: () => import('pages/MatchPage.vue'),
      }
    ]
  }
];


export default routes
