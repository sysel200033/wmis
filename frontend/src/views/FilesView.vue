<template>
  <div class="container">
    <router-link
      v-if="folders.at(0)?.head_folder_id"
      :to="'/files/' + folders.at(0).head_folder_id"
      >&lt; Back</router-link
    >

    <h5 class="mt-3">Create Folder:</h5>
    <form @submit.prevent="submitFolder(folderData)">
      <div class="mb-3">
        <label for="foldername" class="form-label">Name</label>
        <input
          type="text"
          class="form-control"
          id="foldername"
          v-model="folderData.name"
          placeholder="Foldername"
          required
        />
      </div>
      <div class="mb-3">
        <label for="foldername" class="form-label">Participants</label>
        <div
          v-for="user in users.filter((user) => user.email !== ownMail)"
          :key="user.id"
        >
          <div
            class="form-check"
            style="
              display: flex;
              position: relative;
              justify-content: space-between;
              border-bottom: 1px solid #dcdcdc;
              align-items: center;
            "
          >
            <div style="display: flex; align-items: center">
              <!-- Checkbox binds to whether the user's email is included in selectedUsers -->
              <input
                class="form-check-input"
                type="checkbox"
                :checked="isUserSelected(user.email)"
                @change="handleCheckboxChange(user)"
              />
              <p>{{ user.email }}</p>
            </div>

            <!-- Select dropdown, binds to the user's permission or defaults to selectedPermission -->
            <select
              class="form-select"
              aria-label="Permission select"
              :v-model="
                selectedUsers.find((user) => user.mail === user.email)
                  ?.permission || selectedPermission
              "
              @change="updatePermission(user.email, $event.target.value)"
            >
              <option value="read">Read</option>
              <option value="write">Write</option>
              <option value="admin">Admin</option>
            </select>
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <h5 class="mt-5 mb-2">Folders:</h5>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">id</th>
            <th scope="col">Name</th>
            <th scope="col">Link</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in folders" :key="idx">
            <th scope="row">{{ idx + 1 }}</th>
            <td>{{ item.id }}</td>
            <td>
              <input
                class="form-control"
                type="text"
                v-model="item.name"
                @input="updateFolder(item.name, item.head_folder_id)"
              />
            </td>
            <td><router-link :to="'/files/' + item.id">Link</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { apiGetMyself } from "../api/me";
import {
  createFolder,
  createFolderUser,
  getFoldersByHead,
  getFoldersByHeadId,
} from "../api/files";

const route = useRoute();
const folders = ref([]);
const users = ref([]);
const selectedUsers = ref([]);
const selectedPermission = ref("read");
const ownMail = ref("");

import { useDialogStore } from "../store/dialog";
import { apiGetUserList } from "../api/user";

const folderData = ref({
  name: "",
});
const dialogStore = useDialogStore();

function isUserSelected(email) {
  return selectedUsers.value.some((user) => user.mail === email);
}

function handleCheckboxChange(user) {
  if (this.isUserSelected(user.email)) {
    selectedUsers.value = selectedUsers.value.filter(
      (u) => u.mail !== user.email
    );
  } else {
    const userPermission = selectedPermission.value;
    selectedUsers.value.push({ email: user.email, permission: userPermission });
  }
}

function updatePermission(email, permission) {
  const userIndex = selectedUsers.value.findIndex((u) => u.email === email);
  if (userIndex !== -1) {
    selectedUsers.value[userIndex].permission = permission;
  } else {
    selectedUsers.value.push({ mail: email, permission });
  }
}

const submitFolder = async (data) => {
  try {
    const data = await createFolder({
      name: folderData.value.name,
      head_folder_id: route.params.id || undefined,
    });

    folders.value.push({
      id: data.data,
      name: folderData.value.name,
      head_folder_id: route.params.id || undefined,
    });

    for (const selectedUser of selectedUsers.value) {
      await createFolderUser({
        user_mail: selectedUser.email,
        folder_id: data.data,
        status: selectedUser.permission,
      });
    }

    folderData.value.name = "";
    folderData.value.head_folder_id = undefined;
    selectedUsers.value = [];
    selectedUsers.value = [];
  } catch (error) {
    console.error(error);
    dialogStore.setError({
      title: "Error creating folder",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const updateFolder = async (newClass) => {
  try {
    await createClass({
      class_id: newClass.id,
      girl_count: newClass.girls,
      boy_count: newClass.boys,
    });
    classes.value.push({
      class_id: newClass.id,
      girl_count: newClass.girls,
      boy_count: newClass.boys,
    });
  } catch (error) {
    dialogStore.setError({
      title: "Error creating class",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const removeFolder = async (classId) => {
  try {
    await deleteClass(classId);
    classes.value = classes.value.filter(
      (schoolClass) => schoolClass.class_id !== classId
    );
  } catch (error) {
    dialogStore.setError({
      title: "Error removing class",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

async function fetchFolders() {
  const id = route.params.id;
  if (id) {
    const response = await getFoldersByHeadId(id);
    folders.value = response.data;
  } else {
    const response = await getFoldersByHead();
    folders.value = response.data;
  }
}

async function fetchUsers() {
  const response = await apiGetUserList();
  users.value = response.data;
}

async function getOwnData() {
  const response = await apiGetMyself();
  ownMail.value = response.data.email;
}

watch(
  () => route.params,
  () => {
    window.location.reload();
  },
  { deep: true }
);

onMounted(() => {
  fetchFolders();
  fetchUsers();
  getOwnData();
});
</script>
