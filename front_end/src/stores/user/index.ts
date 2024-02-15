// cSpell:ignore pinia
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('userStore', ()=> {
    let loginState = ref(false);
    if (localStorage.getItem('loginState')) {
        loginState.value = eval(localStorage.getItem('loginState') as string);
    }
    let userName = ref(localStorage.getItem('userName') || '');

    let setLoginState = function(value: boolean){
        loginState.value = value;
        localStorage.setItem('loginState', String(value));
    }
    let setUserName = function(value: string){
        userName.value = value;
        localStorage.setItem('userName', value);
    }
    
    return {
        loginState, userName,
        setLoginState, setUserName
    }
})

