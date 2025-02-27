import request from "./req";

export const getFoldersByHead = () => request("GET", "/folders");
export const getFoldersByHeadId = (id) => request("GET", `folders/${id}`);
export const createFolder = (data) => request("POST", "/folders", data);
export const createFolderUser = (data) => request("POST", "/folder_users", data);