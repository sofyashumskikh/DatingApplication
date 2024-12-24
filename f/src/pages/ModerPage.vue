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
          <q-carousel-slide v-for="profile in profiles" :key="profile.id" :name="profile.id" :img-src="profile.image" />
        </q-carousel>
      </div>
      <div class="col-6">
        <q-card class="profile-card">
          <div class="text-center profile-text">
            <p style="font-size: xx-large;">{{ currentProfile.text }}</p>
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
import { useRouter} from "vue-router";
import axios from "axios";
import { ref, onMounted } from "vue";

export default {
  setup() {

    const router = useRouter();
    const slide = ref();
    const isDialogVisible = ref(false);
    const complaints = ref([]);
    const baseURL = 'http://localhost:7000';

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("app/auth");
        }
        return Promise.reject(error);
      }
    );

    const view = () => {
      isDialogVisible.value = true;
    };

    // загрузить профиль
    // заблокировать пользователя
    const profiles = ref();
    const getProfiles = async () => {
      try {
        const response = await axios.get(`${baseURL}/api/profiles`)
        profiles.value = response.data
        if (profiles.value.length > 0) {
          slide.value = profiles.value[0].id
        }
      } catch (error) {
        console.error('Failed to fetch profiles', error)
      }
    }

    onMounted(getProfiles)

    const edit = () => {
      const user_id = sessionStorage.getItem('user_id');
      if (user_id) {
        router.push({ path: "app/profile", query: { user_id: user_id }, });
      }
      else {
        console.error("Не удалось получить ID пользователя")
      }
    };

    const logout = () => {
      sessionStorage.removeItem('token')
      router.push("app");
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
