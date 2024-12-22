<template>
  <div class="profile-page">
    <div class="text-center">
      <h2 style="color: whitesmoke;">Редактирование профиля</h2>
    </div>
    <div class="form-conteiner">
      <q-card class="my-card" style="width: 450px;">
        <q-card-section>
          <q-carousel v-if="profileImages.length > 0" animated v-model="slide" arrows navigation infinite
            style="width: 400px; height: 400px;">
            <q-carousel-slide v-for="(image, index) in profileImages" :key="index" :name="index" :img-src="image" />
          </q-carousel>
          <div v-else style="width: 400px; height: 400px; background-color: #f0f0f0;"></div>
          <br>
          <div class="buttons-container">
            <q-btn outline rounded color="primary" label="изменить фото" @click="change" style="margin-right: 100px" />
            <q-btn outline rounded color="primary" label="добавить фото" @click="add" />
          </div>
          <input type="file" ref="fileInput" style="display: none" @change="changeFile">
          <br>
          <q-input outlined label="Имя" v-model="Name" />
          <br>
          <q-input outlined label="Фамилия" v-model="Surname" />
          <br>
          <q-input outlined label="Страна" v-model="Country" />
          <br>
          <q-input outlined label="Город" v-model="Town" />
          <br>
          <q-input outlined label="Пол" v-model="Sex" />
          <br>
          <q-input outlined label="Возраст" v-model="Age" />
          <br>
          <q-input outlined label="Контакты" v-model="TgNick" />
          <br>
          <q-input uutlined label="Обо мне" v-model="Description" />
          <br>
          <q-btn outline rounded color="primary" label="OK" @click="ok" style="margin-right: 200px;" />
          <q-btn outline rounded color="primary" label="Удалить аккаунт" @click="show" />
          <q-dialog v-model="showDialog">
            <q-card style="width: 300px;">
              <q-card-section>
                <div class="text-h6">Вы уверены?</div>
                <div>Вы действительно хотите удалить свой аккаунт?</div>
              </q-card-section>
              <q-card-actions>
                <q-btn label="Отмена" outline rounded color="primary" v-close-popup style="margin-left: 50px;"/>
                <q-btn label="Удалить" outline rounded color="negative" @click="deleteProfile" style="margin-left: 25px;"/>
              </q-card-actions>
            </q-card>
          </q-dialog>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>

import { useRouter } from "vue-router"
//import { useQuasar } from "quasar"
import { ref } from "vue";
import axios from "axios";

export default {
  setup() {

    //const $q = useQuasar();
    const router = useRouter();
    const Name = ref("");
    const Surname = ref("");
    const Country = ref("");
    const Town = ref("");
    const Sex = ref("");
    const Age = ref("");
    const TgNick = ref("");
    const Description = ref("")
    const fileInput = ref(null);
    const profileImages = ref([]);
    const slide = ref(0);

    const showDialog = ref(false);
    const show = () => {
      showDialog.value = true;
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

    const changeFile = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          profileImages.value.push(e.target.result); // Добавляем новое изображение в массив
        };
        reader.readAsDataURL(file);
      }
    };

    const change = () => {
      fileInput.value.click();
    };

    const add = async () => {
      fileInput.value.click();
    };

    const ok = () => {
      const profileData = {
        Name: Name.value,
        Surname: Surname.value,
        Country: Country.value,
        Town: Town.value,
        Sex: Sex.value,
        Age: Age.value,
        TgNick: TgNick.value,
        Description: Description.value,
        profileImages: profileImages.value,
      };
      console.log("Данные профиля для сохранения:", profileData);
      // Здесь должна быть отправка данных на сервер
    };

    const deleteProfile = async () => {
      try {
        const response = await axios.delete("/api/profile");
        if (response.status === 200) {
          // Удаление профиля прошло успешно
          router.push("/auth");
        } else {
          console.error(
            "Failed to delete profile, server returned:",
            response.status
          );
          // Обработайте ошибку (например, покажите сообщение об ошибке)
        }
      } catch (error) {
        console.error("Error during profile deletion:", error);
        // Обработайте ошибку (например, покажите сообщение об ошибке)
      }
      showDialog.value = false;
    };

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
    };
  },
};
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
