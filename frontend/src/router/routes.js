const routes = [
  {
    path: '/',
    component: () => import('layouts/EmptyLayout.vue'),
    children: [{ path: '', component: () => import('pages/HomePage.vue') },
      { path: 'auth', component: () => import('pages/AuthPage.vue') },
      { path: 'moderate', component: () => import('pages/ModerPage.vue') }],
  },
  {
    path: '/app',
    component: () => import('layouts/MainLayout.vue'),
    children: [

      { path: 'profile', component: () => import('pages/ProfilePage.vue') },
      { path: 'search', component: () => import('pages/SearchPage.vue') },
      { path: 'match', component: () => import('pages/MatchPage.vue') }
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
