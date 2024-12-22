<template>
  <div class="text-center">
    <h2 style="color: whitesmoke;">Совпадения</h2>
  </div>
  <div class="checkmark-container">
    <q-icon name="check" color="green" size="6em" />
    <!-- <q-icon name="close" color="red" size="6em"/> -->
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
    <div class="carousel-buttons">
      <q-btn @click="prevProfile" icon="chevron_left" outline rounded color="primary" style="margin-right: 200px;"/>
      <q-btn @click="nextProfile" icon="chevron_right" outline rounded color="primary" />
    </div>
  </div>
  <br>
  <div class="text-container">
    <p>Поздравляем, у вас есть совпадение!</p>
    <p>контакты для связи: </p>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import axios from "axios";
import { ref, onMounted, computed } from "vue";

export default {
  setup() {

    const router = useRouter();
    const slide = ref(1);
    const profiles = ref([]);

    const currentProfile = computed(() => {
      const found = profiles.value.find(p => p.id === slide.value);
      return found || { text: '' };
    });

    const getProfiles = async () => {
      try {
        const response = await axios.get("/api/profiles");
        profiles.value = response.data;
        if (profiles.value.length > 0) {
          slide.value = profiles.value[0].id;
        }
      } catch (error) {
        console.error("Failed to fetch profiles", error);
      }
    };

    onMounted(getProfiles);

    const prevProfile = () => {
      if (profiles.value.length === 0) return;
      const currentIndex = profiles.value.findIndex(p => p.id === slide.value);
      if (currentIndex > 0) {
        slide.value = profiles.value[currentIndex - 1].id;
      } else {
        slide.value = profiles.value[profiles.value.length - 1].id;
      }
    };

    const nextProfile = () => {
      if (profiles.value.length === 0) return;
      const currentIndex = profiles.value.findIndex(p => p.id === slide.value);
      if (currentIndex < profiles.value.length - 1) {
        slide.value = profiles.value[currentIndex + 1].id;
      } else {
        slide.value = profiles.value[0].id;
      }
    };

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push("/auth");
        }
        return Promise.reject(error);
      }
    );

    // проверОчка, если нет подходящих кандидатов
    // время сеанса истекло, авторизуемся заново

    return {
      slide,
      profiles,
      currentProfile,
      prevProfile,
      nextProfile,
    };
  },
}

</script>

<style scoped>
.q-pa-md {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.q-col-gutter-md {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-top: 50px;
}

.checkmark-container {
  position: absolute;
  top: 5%;
  right: 7%;
}

.carousel-buttons {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.carousel-buttons .q-btn {
  margin: 0 5px;
}

.text-container {
  color: whitesmoke;
  font-size: x-large;
  margin-top: 20px;
  text-align: center;
}

.profile-card {
  width: 450px;
  height: 450px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.profile-text {
  padding: 16px;
}
</style>
