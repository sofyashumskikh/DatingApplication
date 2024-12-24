<template>
  <div class="text-center">
    <h2 style="color: whitesmoke">Просмотр претендентов</h2>
  </div>
  <div class="checkmark-container">
    <q-icon name="check" color="green" size="6em" />
  </div>
  <div class="q-pa-md">
    <div class="q-col-gutter-md row items-start">
      <div class="col-6">
        <q-carousel animated v-model="slide" arrows navigation infinite style="width: 450px; height: 450px">
          <q-carousel-slide v-for="profile in profiles" :key="profile.id" :name="profile.id" :img-src="profile.image" />
        </q-carousel>
      </div>
      <div class="col-6">
        <q-card class="profile-card">
          <div class="text-center profile-text">
            <p style="font-size: xx-large">{{ currentProfile.text }}</p>
          </div>
        </q-card>
      </div>
    </div>
    <div class="buttons-container">
      <q-btn outline rounded color="primary" label="LIKE" @click="like" style="margin-right: 300px" />
      <q-btn outline rounded color="primary" label="DISLIKE" @click="dislike" />
    </div>
    <br />
    <q-btn outline rounded color="primary" label="ПОЖАЛОВАТЬСЯ" @click="openComplaintDialog" style="left: 42%" />
  </div>
  <q-dialog v-model="showComplaintDialog">
    <q-card style="width: 300px">
      <q-card-section>
        <div class="text-h6">Опишите вашу жалобу</div>
        <q-input outlined v-model="complaintText" type="textarea" />
      </q-card-section>
      <q-card-actions>
        <q-btn label="Отмена" outline rounded color="primary" v-close-popup style="margin-left: 50px" />
        <q-btn label="Отправить" outline rounded color="negative" @click="sendComplaint" style="margin-left: 25px" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

export default {
  setup() {
    const router = useRouter()
    const slide = ref()
    const showComplaintDialog = ref(false)
    const complaintText = ref('')
    const userId = 1
    const profiles = ref([])
    const baseURL = 'http://localhost:7000'
    const currentProfile = computed(() => {
      const found = profiles.value.find((p) => p.id === slide.value)
      return found || { text: '' }
    })

    const getProfiles = async () => {
      try {
        const token = sessionStorage.getItem('token');
        console.log(token);
        const response = await axios.get(`${baseURL}/api/profiles`,
          {headers: { Authorization: `Bearer ${token}`},}
        )
        const role = response.headers['x-role'];
        console.log("role ",role);
        sessionStorage.setItem('role', role); // Сохраняем роль в localStorage
        console.log(response.data);
        profiles.value = response.data
        if (profiles.value.length > 0) {
          slide.value = profiles.value[0].id
        }

      } catch (error) {
        console.error('Failed to fetch profiles', error)
      }
    }


    // Код, который будет выполнен при монтировании компонента
    onMounted(() => {
      console.log('Компонент был смонтирован!');
      // Например, можно сделать API-запрос здесь
      getProfiles();

    });

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push('/auth')
        }
        return Promise.reject(error)
      },
    )

    const openComplaintDialog = () => {
      showComplaintDialog.value = true
      complaintText.value = ''
    }

    const like = async () => {
      try {
        const response = await axios.post('/api/like', {
          userId: userId,
        })
        if (response.status === 200) {
          console.log('Like was successful')
        } else {
          console.error('Like failed, server returned:', response.status)
        }
      } catch (error) {
        console.error('Error during like action:', error)
      }
    }

    const dislike = async () => {
      try {
        const response = await axios.post('/api/dislike', {
          userId: userId,
        })
        if (response.status === 200) {
          console.log('Dislike was successful')
        } else {
          console.error('Dislike failed, server returned:', response.status)
        }
      } catch (error) {
        console.error('Error during dislike action:', error)
      }
    }

    const sendComplaint = async () => {
      try {
        const response = await axios.post('/api/complaint', {
          userId: userId,
          text: complaintText.value,
        })
        if (response.status === 200) {
          console.log('Complaint was successful')
          showComplaintDialog.value = false
        } else {
          console.error('Complaint failed, server returned:', response.status)
        }
      } catch (error) {
        console.error('Error during complaint action:', error)
      }
    }

    return {
      slide,
      like,
      dislike,
      profiles,
      currentProfile,
      complaintText,
      showComplaintDialog,
      openComplaintDialog,
      sendComplaint,
    }
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
