<template>
    <div class="text-center">
      <h2>... кандидаты ...</h2>
    </div>
    <div class="q-pa-md">
      <div class="q-col-gutter-md row items-start">
        <div class="col-6">
          <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="width: 450px; height: 450px">
            <div class="absolute-bottom text-subtitle1 text-center">
              Caption
            </div>
          </q-img>
        </div>
        <div class="col-6">
          <q-card style="width: 450px; height: 450px">
            <div class="text-center">text text text</div> 
          </q-card>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
    .q-pa-md {
      margin: 0;
      position: absolute;
      top: 50%;
      left: 50%;
      margin-right: -50%;
      transform: translate(-50%, -50%)
    }
  </style>