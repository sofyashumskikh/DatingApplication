<template>
  <div class="text-center">
    <h2 style="color: whitesmoke;">Просмотр претендентов</h2>
  </div>
  <div class="checkmark-container">
    <q-icon name="check" color="green" size="6em" />
    <!-- <q-icon name="close" color="red" size="6em"/> -->
  </div>
  <!-- <div class="sort-container">
    <q-select v-model="selectedSort" :options="sortOptions" label="Сортировать по" style="width: 200px; right: 0%;"
      class="sort-menu" />
  </div> -->
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
    // const selectedSort = ref(null);
    // const sortOptions = ref([
    //   { label: "По умолчанию", value: "default" },
    //   { label: "По возрасту", value: "age" },
    //   { label: "По стране", value: "country" }
    // ]);

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("/auth");
        }
        return Promise.reject(error);
      }
    );

    const like = () => { };
    const dislike = () => { };
    const complaint = () => { };

    return {
      slide: ref(1),
      like,
      dislike,
      complaint,
      //selectedSort,
      //sortOptions,
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
/*
.sort-container {
  position: relative;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-right: 5%;
}

.sort-menu {
  margin-top: 20px;
}
*/
</style>

<!-- TODO :
добавить всплывающие уведомления  -->
