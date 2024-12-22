const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/HomePage.vue') },
      { path: 'profile', component: () => import('pages/ProfilePage.vue') },
      { path: 'search', component: () => import('pages/SearchPage.vue') },
      { path: 'match', component: () => import('pages/MatchPage.vue') }
    ],
  },
  {
    path: '/auth',
    component: () => import('src/layouts/EmptyLayout.vue'),
    children: [{ path: '', component: () => import('pages/AuthPage.vue') }],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
