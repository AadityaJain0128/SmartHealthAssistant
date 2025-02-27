import axios from "axios";


axios.interceptors.request.use(config => {
    config.headers["Content-Type"] = "application/json";
})

const api = axios.create({
    baseURL : "https://closing-racer-repeatedly.ngrok-free.app"
});


export default api;