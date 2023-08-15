import axios from "axios";
import store from "../store";
import router from "../router";

const errorHandler = (state, msg) => {
  switch (state) {
    case 400:
      console.log("login fail" + msg);
      break;
    case 401:
      console.log("axios errorHandler : 401 Auth Fail");
      router.push({ name: "Refresh" });
      break;
    case 403:
      console.log("unauthorized");
      break;
    case 404:
      console.log("not found");
      break;
    default:
      console.log("undefined error" + msg);
  }
};


var instance = axios.create({
  baseURL:
    (import.meta.env.API_URL || "http://localhost:5001/api") ,
});


instance.interceptors.request.use(
  (config) => {
    const access_token = store.getters["auth/access_token"];
    access_token && (config.headers.Authorization = "Bearer " + access_token);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const { response } = error;
    if (response) {
      errorHandler(response.status, response.data.error);
      return Promise.reject(error);
    } else {
      if (!window.navigator.onLine) {
        console.log("offline");
      } else {
        return Promise.reject(error);
      }
    }
  }
);

export default function (method, url, data = null , headers = null) {
  method = method.toUpperCase();
  let composeUrl = `${url}${data && Object.values(data)[0] ? "/" + Object.values(data)[0] : ""}`;

  if( headers ){
    instance.defaults.headers.common = headers;
  }

  switch (method) {
    case "GET":
      let params = {};
      if (data && Object.keys(data).length > 1) {
        let i = 0;
        for (let j in data) if (i++ > 0) params[j] = data[j];
      } else {
        params = null;
      }
      return instance.get(composeUrl, { ...params });
    case "POST":
      return instance.post(url, data);
    case "PUT":
      return instance.put(url, data);
    case "DELETE":
      return instance.delete(composeUrl, { ...params });
    case "PATCH":
      return instance.patch(composeUrl, { ...params });
    default:
      console.log("unknow methods" + method);
      return false;
  }
}
