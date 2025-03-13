import request from "./req";

export const getFoldersByHead = () => request("GET", "/folders");
export const getFoldersByHeadId = (id) =>
  request("GET", `folders?head_folder_id=${id}`);
export const getFolderId = (id) => request("GET", `folders/${id}`);
export const createFolder = (data) => request("POST", "/folders", data);
export const updateFolderName = (id, name) =>
  request("PUT", `/folders/${id}?new_folder_name=${name}`);
export const deleteFolder = (id) => request("DELETE", `/folders/${id}`)
export const createFolderUser = (data) =>
  request("POST", "/folder_users", data);
export const updateFolderUser = (folder_id, mail, status) =>
  request("PUT", `/folder_users/${folder_id}?mail=${mail}&status=${status}`);
export const deleteFolderUser = (folder_id, mail) =>
  request("DELETE", `/folder_users/${folder_id}?mail=${mail}`);
export const updateFileContent = (folder_id, content) => request("PUT", `/files/${folder_id}?content=${content}`);
