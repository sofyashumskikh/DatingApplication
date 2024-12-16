<template>
  <div class="text-center">
    <h2>... кандидаты ...</h2>
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
    <div class="buttons-container">
      <q-btn outlined rounded color="primary" label="LIKE" @click="like" style="margin-right: 300px" />
      <q-btn outlined rounded color="primary" label="DISLIKE" @click="dislike" />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

const like = () => { }
const dislike = () => { }

export default {
  setup() {
    return {
      slide: ref(1),
      like,
      dislike,
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
  transform: translate(-50%, -50%)
}

.buttons-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
