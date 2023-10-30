import { createWebHistory, createRouter } from "vue-router"
import Home from './components/Home.vue'
import Result from './components/Result.vue'
import SideBar from './components/SideBar.vue'
import Upload from './components/Upload.vue'
import Login from './components/Login.vue'
import changePass from './components/changePass.vue'


const routes =[{

    name: 'Home',
    path: '/',
    component: Home

},
 {   name: 'Result',
    path: '/result',
    component: Result

},
 {   name: 'SideBar',
    path: '/sidebar',
    component: SideBar

},
{
    name: 'Upload',
    path: '/upload',
    component: Upload

},

{
    name: 'Login',
    path: '/login',
    component: Login
},
{
    name: 'changePass',
    path: '/changePass',
    component: changePass
},



];



const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;