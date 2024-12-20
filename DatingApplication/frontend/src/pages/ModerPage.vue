<template>
  <div class="text-center">
    <h2 style="color: whitesmoke;">Модерация профилей</h2>
  </div>
  <div class="exit-container">
    <q-btn outline rounded color="lime-2" label="Выход" @click="logout" />
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
      <q-btn outline rounded color="primary" label="просмотр жалоб" @click="view" style="margin-right: 300px" />
      <q-btn outline rounded color="primary" label="редактирование профиля" @click="edit" />
    </div>
  </div>
  <q-dialog v-model="isDialogVisible" @hide="isDialogVisible = false">
    <q-card style="width: 700px; max-width: 80vw;">
      <q-card-section>
        <div class="text-h6">Жалобы</div>
      </q-card-section>
      <q-card-section class="scroll">
        <q-list>
          <q-item v-for="(complaint, index) in complaints" :key="index">
            <q-item-section>
              <q-item-label>
                дата и время: {{ complaint.date_time }}
                <br> Текст жалобы: {{ complaint.text }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="просмотрено" outline rounded color="primary" @click="isDialogVisible = false" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useRouter } from "vue-router";
import axios from "axios";
import { ref } from "vue";

export default {
  setup() {

    const router = useRouter();
    const isDialogVisible = ref(false);
    const complaints = ref([
      {
        id: 1,
        date_time: "10:00",
        text: "Этот пользователь плохо себя ведет",
      },
      {
        id: 2,
        date_time: "11:00",
        text: "Нарушает правила сообщества",
      },
      {
        id: 3,
        date_time: "12:00",
        text: "Оскорбляет других пользователей",
      },
    ]);

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("/auth");
        }
        return Promise.reject(error);
      }
    );

    const view = () => {
      isDialogVisible.value = true;
    };

    const edit = () => {
      router.push("/profile");
    };

    const logout = () => {
      localStorage.removeItem('token')
      router.push("/");
    };

    return {
      slide: ref(1),
      complaints,
      isDialogVisible,
      view,
      edit,
      logout,
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

.buttons-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.exit-container {
  position: absolute;
  top: 5%;
  right: 5%;
}

.scroll {
  max-height: 500px;
  overflow-y: auto;
}
</style>

<!-- TODO :
добавить всплывающее окно -->
