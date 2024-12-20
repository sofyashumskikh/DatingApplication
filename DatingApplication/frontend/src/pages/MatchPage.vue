<template>
  <div class="text-center">
    <h2 style="color: whitesmoke;">Совпадения</h2>
  </div>
  <div class="q-pa-md">
    <div class="q-col-gutter-md row items-start">
      <div class="col-6">
        <q-carousel animated v-model="slide" arrows navigation infinite style="width: 450px; height: 450px;">
          <q-carousel-slide :name="1" img-src="https://cdn.quasar.dev/img/parallax2.jpg" />
          <q-carousel-slide :name="2" img-src="https://cdn.quasar.dev/img/parallax1.jpg" />
          <q-carousel-slide :name="3" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
        </q-carousel>
      </div>
      <div class="col-6">
        <q-card style="width: 450px; height: 450px">
          <div class="text-center">text text text</div>
        </q-card>
      </div>
    </div>
    <div class="arrow-buttons">
      <q-btn icon="arrow_back_ios" round flat @click="prevPage" class="arrow-button" />
      <q-btn icon="arrow_forward_ios" round flat @click="nextPage" class="arrow-button" />
    </div>
  </div>
  <div class="text-center">
    <p>Поздравляем, у вас есть совпадение!</p>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    return {
      slide: ref(1),
    };
  },
}

</script>

<style scoped>
.q-pa-md {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%);
}
</style>

<!-- TODO :
добавить стрелочки  -->
