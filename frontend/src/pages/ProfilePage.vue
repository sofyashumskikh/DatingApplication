<template>
  <div class="profile-page">
    <div class="text-center">
      <h2 style="color: whitesmoke">Редактирование профиля</h2>
    </div>
    <div class="form-conteiner">
      <q-card class="my-card" style="width: 450px">
        <q-card-section>
          <q-carousel
            v-if="profileImages.length > 0"
            animated
            v-model="slide"
            arrows
            navigation
            infinite
            style="width: 400px; height: 400px"
          >
            <q-carousel-slide
              v-for="(image, index) in profileImages"
              :key="index"
              :name="index"
              :img-src="image"
            />
          </q-carousel>
          <div v-else style="width: 400px; height: 400px; background-color: #f0f0f0"></div>
          <br />
          <div class="buttons-container">
            <q-btn
              outline
              rounded
              color="primary"
              label="изменить фото"
              @click="change"
              style="margin-right: 100px"
            />
            <q-btn outline rounded color="primary" label="добавить фото" @click="add" />
          </div>
          <input type="file" ref="fileInput" style="display: none" @change="changeFile" />
          <br />
          <q-input outlined label="Имя" v-model="Name" />
          <br />
          <q-input outlined label="Фамилия" v-model="Surname" />
          <br />
          <q-input outlined label="Страна" v-model="Country" />
          <br />
          <q-input outlined label="Город" v-model="Town" />
          <br />
          <q-checkbox v-model="Sex" val="male" label="Мужской" />
          <q-checkbox v-model="Sex" val="female" label="Женский" />
          <br />
          <q-input outlined label="Возраст" v-model="Age" />
          <br />
          <q-input outlined label="Контакты" v-model="TgNick" />
          <br />
          <q-input uutlined label="Обо мне" v-model="Description" />
          <br />
          <q-btn
            outline
            rounded
            color="primary"
            label="OK"
            @click="ok"
            style="margin-right: 200px"
          />
          <q-btn outline rounded color="primary" label="Удалить аккаунт" @click="show" />
          <q-dialog v-model="showDialog">
            <q-card style="width: 300px">
              <q-card-section>
                <div class="text-h6">Вы уверены?</div>
                <div>Вы действительно хотите удалить свой аккаунт?</div>
              </q-card-section>
              <q-card-actions>
                <q-btn
                  label="Отмена"
                  outline
                  rounded
                  color="primary"
                  v-close-popup
                  style="margin-left: 50px"
                />
                <q-btn
                  label="Удалить"
                  outline
                  rounded
                  color="negative"
                  @click="deleteProfile"
                  style="margin-left: 25px"
                />
              </q-card-actions>
            </q-card>
          </q-dialog>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
//import { useQuasar } from "quasar"
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    //const $q = useQuasar();
    const router = useRouter()
    const Name = ref('')
    const Surname = ref('')
    const Country = ref('')
    const Town = ref('')
    const Sex = ref([])
    const Age = ref('')
    const TgNick = ref('')
    const Description = ref('')
    const fileInput = ref(null)
    const profileImages = ref([])
    const slide = ref(0)
    const baseURL = 'http://localhost:7000'
    const showDialog = ref(false)
    const show = () => {
      showDialog.value = true
    }

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          router.push('/auth')
        }
        return Promise.reject(error)
      },
    )

    const selectedFile = ref(null) // Хранит выбранный файл
    const previewImage = ref(null) // Для предварительного просмотра изображения
    /*// Обработка выбора файла
    const changeFile = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file

        // Создание превью изображения
        const reader = new FileReader()
        reader.onload = (e) => {
          previewImage.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }*/
    // Функция для обработки изменения файла
    const changeFile = async (event) => {
      const file = event.target.files[0] // Получаем выбранный файл

      if (file) {
        selectedFile.value = file

        // Создание превью изображения
        const reader = new FileReader()
        reader.onload = (e) => {
          previewImage.value = e.target.result // Превью изображения
        }
        reader.readAsDataURL(file)
      }

      if (!selectedFile.value) {
        alert('Выберите файл для загрузки.')
        return
      }

      const formData = new FormData()
      formData.append('photo', selectedFile.value) // Добавляем файл в объект FormData

      try {
        const response = await axios.post(`${baseURL}/api/photo`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data', // Указание типа данных
          },
        })

        console.log('Фото успешно загружено:', response.data)
        profileImages.value.unshift(response.data.photoUrl || previewImage.value)
        alert('Фото успешно загружено!')
      } catch (error) {
        console.error('Ошибка при загрузке фото:', error)
        alert('Произошла ошибка при загрузке фото.')
      }
    }

    const change = () => {
      fileInput.value.click()
    }

    const add = async () => {
      fileInput.value.click()
      console.log('add ', fileInput.value)
    }

    const ok = async () => {
      const profileData = {
        id: 0, // Укажите здесь реальный ID, если он существует
        user_id: 0, // Укажите ID пользователя, если это требуется
        name: Name.value,
        surname: Surname.value,
        country_name: Country.value,
        city_name: Town.value,
        gender: Sex.value === 'female', // Преобразуем в булевое значение
        age: Age.value,
        active: true, // Укажите реальное значение, если требуется
        about_me: Description.value,
        nickname_tg: TgNick.value,
        complaints_count: 0, // Задайте актуальное значение
      }

      console.log('Данные профиля для сохранения:', profileData)

      try {
        const token = localStorage.getItem('token') // Получаем токен из sessionStorage
        console.log(`Bearer ${token}`)
        const response = await axios.post(
          `${baseURL}/api/profile`,
          profileData, // Передаём данные профиля
          {
            headers: {
              Authorization: `Bearer ${token}`, // Передаём токен с приставкой "Bearer"
              'Content-Type': 'application/json',
            },
          },
        )

        // Обработка успешного ответа
        console.log('Успешный ответ:', response.data)
        console.log('Заголовки ответа:', {
          XActive: response.headers['x-active'],
          XModerated: response.headers['x-moderated'],
          XRole: response.headers['x-role'],
        })
        alert('Профиль успешно сохранён!')
      } catch (error) {
        // Обработка ошибок
        if (error.response) {
          console.error('Ошибка сервера:', error.response.data)
          alert(
            `Ошибка: ${error.response.status} - ${error.response.data.detail || 'Не удалось сохранить профиль'}`,
          )
        } else {
          console.error('Ошибка сети или другая ошибка:', error.message)
          alert('Ошибка: Не удалось подключиться к серверу.')
        }
      }
      if (fileInput.value) {
        try {
          const token = localStorage.getItem('token') // Получаем токен из sessionStorage
          console.log(`Bearer ${token}`, fileInput, fileInput.value)
          const response = await axios.post(
            `${baseURL}/api/photo`,
            fileInput.value, // Передаём данные профиля
            {
              headers: {
                Authorization: `Bearer ${token}`, // Передаём токен с приставкой "Bearer"
              },
            },
          )

          // Обработка успешного ответа
          console.log('Успешный ответ:', response.data)
          console.log('Заголовки ответа:', {
            XActive: response.headers['x-active'],
            XModerated: response.headers['x-moderated'],
            XRole: response.headers['x-role'],
          })
          alert('Профиль успешно сохранён!')
        } catch (error) {
          // Обработка ошибок
          if (error.response) {
            console.error('Ошибка сервера:', error.response.data)
            alert(
              `Ошибка: ${error.response.status} - ${error.response.data.detail || 'Не удалось сохранить профиль'}`,
            )
          } else {
            console.error('Ошибка сети или другая ошибка:', error.message)
            alert('Ошибка: Не удалось подключиться к серверу.')
          }
        }
      }
    }

    const deleteProfile = async () => {
      try {
        const response = await axios.delete(`${baseURL}/api/user`)
        if (response.status === 200) {
          // Удаление профиля прошло успешно
          router.push('/')
        } else {
          console.error('Failed to delete profile, server returned:', response.status)
          // Обработайте ошибку (например, покажите сообщение об ошибке)
        }
      } catch (error) {
        console.error('Error during profile deletion:', error)
        // Обработайте ошибку (например, покажите сообщение об ошибке)
      }
      showDialog.value = false
    }

    onMounted(async () => {
      try {
        const token = localStorage.getItem('token') // Получаем токен из sessionStorage

        let responce = await axios.get(`${baseURL}/api/profile`, {
          headers: {
            Authorization: `Bearer ${token}`, // Передаём токен с приставкой "Bearer"
          },
        })
        const profile = responce.data
        Name.value = profile.name
        Surname.value = profile.surname
        Country.value = profile.country_name
        Town.value = profile.city_name
        Sex.value = profile.gender
        Age.value = profile.age
        TgNick.value = profile.nickname_tg
        Description.value = profile.about_me
        responce = await axios.get(`${baseURL}/api/profile_photo`, {
          headers: {
            Authorization: `Bearer ${token}`, // Передаём токен с приставкой "Bearer"
          },
        })
        profileImages.value = responce.data
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error)
      }
    })

    return {
      Name,
      Surname,
      Country,
      Town,
      Sex,
      Age,
      TgNick,
      Description,
      fileInput,
      profileImages,
      slide,
      changeFile,
      change,
      add,
      ok,
      show,
      showDialog,
      deleteProfile,
    }
  },
}
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.form-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.buttons-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.my-card {
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
</style>
