import axios from "axios";


axios.interceptors.request.use(config => {
    config.headers["Content-Type"] = "application/json";
})

const api = axios.create({
    baseURL : process.env.VUE_APP_BACKEND_URL
});


export default api;
