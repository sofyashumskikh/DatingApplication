<template>
  <div class="text-center">
    <h2 style="color: whitesmoke;">Просмотр претендентов</h2>
  </div>
  <div class="checkmark-container">
    <q-icon name="check" color="green" size="6em" />
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
          <div class="text-center">
            <p style="font-size: xx-large;">text<br>text</p>
          </div>
        </q-card>
      </div>
    </div>
    <div class="buttons-container">
      <q-btn outline rounded color="primary" label="LIKE" @click="like" style="margin-right: 300px" />
      <q-btn outline rounded color="primary" label="DISLIKE" @click="dislike" />
    </div>
    <br>
    <q-btn outline rounded color="primary" label="ПОЖАЛОВАТЬСЯ" @click="complaint" style="left: 42%;" />
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import axios from "axios";
import { ref } from "vue";

export default {
  setup() {

    const router = useRouter();
    const slide = ref(1);

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("/auth");
        }
        return Promise.reject(error);
      }
    );

    const like = () => {};
    const dislike = () => {};
    const complaint = () => {};

    return {
      slide,
      like,
      dislike,
      complaint,
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

.q-col-gutter-md {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-top: 50px;
}

.buttons-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.checkmark-container {
  position: absolute;
  top: 5%;
  right: 7%;
}
</style>

<!-- TODO :
добавить всплывающие уведомления  -->
