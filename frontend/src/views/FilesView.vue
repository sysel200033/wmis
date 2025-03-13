<template>
  <div class="container">
    <div class="my-3" v-if="currentFolder">
      <router-link
        :to="
          currentFolder.head_folder_id
            ? `/files/${currentFolder.head_folder_id}`
            : '/files'
        "
        >&lt; Back</router-link
      >
    </div>
    <div
      class="card mt-4"
      v-if="currentFolder && currentFolder.files.at(0)?.content"
    >
      <div class="card-header">
        <h5 class="mb-0">
          <button class="btn btn-link">File</button>
        </h5>
      </div>

      <div class="collapse show">
        <div class="card-body">
          <textarea
            disabled="true"
            v-model="currentFolder.files.at(0).content"
            class="form-control"
            style="resize: none"
            rows="10"
            placeholder="Content of your File"
          ></textarea>
        </div>
      </div>
    </div>
    <h5 class="mt-5 mb-2">Folders:</h5>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Link</th>
            <th scope="col">Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in folders" :key="idx">
            <th
              v-if="item.users.some((user) => user.user_mail === ownMail)"
              scope="row"
            >
              {{ idx + 1 }}
            </th>
            <td v-if="item.users.some((user) => user.user_mail === ownMail)">
              {{ item.name }}
            </td>
            <td v-if="item.users.some((user) => user.user_mail === ownMail)">
              <router-link :to="'/files/' + item.id">Link</router-link>
            </td>
            <td
              v-if="
                item.users.find((user) => user.user_mail === ownMail)
                  ?.status === 'creator'
              "
            >
              <button @click="removeFolder(item.id)" class="btn btn-danger">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mb-5">
      <div
        class="card mt-4"
        v-if="
          (currentFolder &&
            (currentFolder.users.find((user) => user.user_mail === ownMail)
              ?.status === 'creator' ||
              currentFolder.users.find((user) => user.user_mail === ownMail)
                ?.status === 'admin')) ||
          !currentFolder
        "
      >
        <div class="card-header">
          <h5 class="mb-0">
            <button class="btn btn-link">Create New Folder</button>
          </h5>
        </div>

        <div class="collapse show">
          <div class="card-body">
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
              <div class="mb-3" v-if="users.length > 1">
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
                      @change="
                        updatePermission(user.email, $event.target.value)
                      "
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
          </div>
        </div>
      </div>

      <div
        class="card mt-3"
        v-if="
          currentFolder &&
          (currentFolder.users.find((user) => user.user_mail === ownMail)
            ?.status === 'creator' ||
            currentFolder.users.find((user) => user.user_mail === ownMail)
              ?.status === 'admin' ||
            currentFolder.users.find((user) => user.user_mail === ownMail)
              ?.status === 'write')
        "
      >
        <div class="card-header">
          <h5 class="mb-0">
            <button class="btn btn-link">Update File</button>
          </h5>
        </div>

        <div class="collapse show">
          <div class="card-body">
            <div>
              <form @submit.prevent="updateFile()">
                <div class="mb-3">
                  <label for="foldername" class="form-label">Content</label>
                  <textarea
                    v-model="updateData.content"
                    class="form-control"
                    style="resize: none"
                    rows="10"
                    placeholder="Content of your File"
                  ></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Update</button>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div
        class="card mt-3"
        v-if="
          currentFolder &&
          (currentFolder.users.find((user) => user.user_mail === ownMail)
            ?.status === 'creator' ||
            currentFolder.users.find((user) => user.user_mail === ownMail)
              ?.status === 'admin')
        "
      >
        <div class="card-header">
          <h5 class="mb-0">
            <button class="btn btn-link">Update Folder</button>
          </h5>
        </div>

        <div class="collapse show">
          <div class="card-body">
            <div>
              <h5 class="mt-3">Update Folder:</h5>
              <form @submit.prevent="updateFolder()">
                <div class="mb-3">
                  <label for="foldername" class="form-label">Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="foldername"
                    v-model="updateData.name"
                    placeholder="Foldername"
                    required
                  />
                </div>
                <div class="mb-3" v-if="users.length > 1">
                  <label for="foldername" class="form-label"
                    >Participants</label
                  >
                  <div
                    v-for="user in users.filter(
                      (user) => user.email !== ownMail
                    )"
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
                          :checked="isUserSelectedUpdate(user.email)"
                          @change="handleCheckboxChangeUpdate(user)"
                        />
                        <p>{{ user.email }}</p>
                      </div>

                      <!-- Select dropdown, binds to the user's permission or defaults to selectedPermission -->
                      <select
                        class="form-select"
                        aria-label="Permission select"
                        :v-model="
                          selectedUsersUpdate?.find(
                            (user) => user.mail === user.email
                          )?.permission || selectedPermission
                        "
                        @change="
                          updatePermissionUpdate(
                            user.email,
                            $event.target.value
                          )
                        "
                      >
                        <option value="read">Read</option>
                        <option value="write">Write</option>
                        <option value="admin">Admin</option>
                      </select>
                    </div>
                  </div>
                </div>
                <button type="submit" class="btn btn-primary">Update</button>
              </form>
            </div>
          </div>
        </div>
      </div>
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
  deleteFolder,
  deleteFolderUser,
  getFolderId,
  getFoldersByHead,
  getFoldersByHeadId,
  updateFileContent,
  updateFolderName,
  updateFolderUser,
} from "../api/files";

const route = useRoute();
const folders = ref([]);
const users = ref([]);
const selectedUsers = ref([]);
const selectedPermission = ref("read");
const ownMail = ref("");
const currentFolder = ref(null);

import { useDialogStore } from "../store/dialog";
import { apiGetUserList } from "../api/user";

const folderData = ref({
  name: "",
});

const updateData = ref({
  name: "",
  content: "",
  selectedUsers: [],
});

const dialogStore = useDialogStore();

function isUserSelected(email) {
  return selectedUsers.value.some((user) => user.mail === email);
}

function isUserSelectedUpdate(email) {
  return updateData.value.selectedUsers.some((user) => user.mail === email);
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

function handleCheckboxChangeUpdate(user) {
  if (this.isUserSelectedUpdate(user.email)) {
    updateData.value.selectedUsers = updateData.value.selectedUsers.filter(
      (u) => u.mail !== user.email
    );
  } else {
    const userPermission = selectedPermission.value;
    updateData.value.selectedUsers.value.push({
      email: user.email,
      permission: userPermission,
    });
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

function updatePermissionUpdate(email, permission) {
  const userIndex = updateData.value.selectedUsers.findIndex(
    (u) => u.email === email
  );
  if (userIndex !== -1) {
    updateData.value.selectedUsers[userIndex].permission = permission;
  } else {
    updateData.value.selectedUsers.push({ mail: email, permission });
  }
}

const submitFolder = async (data) => {
  try {
    const data = await createFolder({
      name: folderData.value.name,
      head_folder_id: route.params.id || undefined,
    });
    console.log(data);

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

    await fetchFolders();

    dialogStore.setSuccess({
      title: "Folder Created",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  } catch (error) {
    console.error("Error: ", error);
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

const updateFolder = async () => {
  try {
    await updateFolderName(currentFolder.value.id, updateData.value.name);
    for (const user of updateData.value.selectedUsers) {
      if (
        currentFolder.value.users.some((item) => item.user_mail === user.mail)
      ) {
        if (
          currentFolder.value.users.find((item) => item.user_mail === user.mail)
            ?.status !== user.permission
        ) {
          // update user permission
          await updateFolderUser(
            currentFolder.value.id,
            user.mail,
            user.permission
          );
        }
      } else {
        // create user
        await createFolderUser({
          user_mail: user.mail,
          folder_id: currentFolder.value.id,
          status: user.permission,
        });
      }
    }

    for (const user of currentFolder.value.users) {
      if (
        !updateData.value.selectedUsers.some(
          (item) => item.mail === user.user_mail
        )
      ) {
        // delete folder user
        await deleteFolderUser(currentFolder.value.id, user.user_mail);
      }
    }

    await fetchFolder();

    dialogStore.setSuccess({
      title: "Folder Updated",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  } catch (error) {
    dialogStore.setError({
      title: "Error updating folder",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const updateFile = async () => {
  try {
    await updateFileContent(currentFolder.value.id, updateData.value.content);

    await fetchFolder();
    dialogStore.setSuccess({
      title: "File Updated",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  } catch (error) {
    dialogStore.setError({
      title: "Error updating file",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const removeFolder = async (folderId) => {
  try {
    await deleteFolder(folderId);
    folders.value = folders.value.filter((folder) => folder.id !== folderId);
    dialogStore.setSuccess({
      title: "Folder Removed",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  } catch (error) {
    dialogStore.setError({
      title: "Error removing folder",
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

async function fetchFolder() {
  const id = route.params.id;
  if (id) {
    const response = await getFolderId(id);
    if (response.data) {
      currentFolder.value = response.data;
      updateData.value.name = response.data.name;
      updateData.value.content = response.data.files.at(0).content;
      response.data.users.map((user) => {
        updateData.value.selectedUsers.push({
          mail: user.user_mail,
          permission: user?.status,
        });
      });
    } else {
      currentFolder.value = null;
    }
  } else {
    currentFolder.value = null;
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
    console.log(route.params);
    fetchFolders();
    fetchFolder();
  },
  { deep: true }
);

onMounted(() => {
  fetchFolders();
  fetchUsers();
  getOwnData();
});
</script>
