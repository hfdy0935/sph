<template>
<div class="register-container">
    <!-- 注册内容 -->
    <div class="register">
    <h3>注册新用户
        <span class="go">我有账号，去 <RouterLink to="/login">登录</RouterLink>
        </span>
    </h3>
    <div class="content">
        <label>手机号:</label>
        <input type="text" placeholder="请输入你的手机号" v-model="tel" @input="telInputCheck">
        <span class="error-msg" v-show="isTelTipShow">请输入正确格式的手机号</span>
    </div>
    <div class="content">
        <label>验证码:</label>
        <input type="text" placeholder="请输入验证码" v-model="idCode" @input="idCodeInputCheck">
        <button class="getCode" @click="getIdCode">获取验证码</button>
        <!-- <img ref="code" src="http://182.92.128.115/api/user/passport/code" alt="code"> -->
        <span class="error-msg" v-show="isIdCodeTipShow">验证码错误</span>
    </div>
    <div class="content">
        <label>登录密码:</label>
        <input type="text" placeholder="请输入你的登录密码" v-model="password" @input="passwordInputCheck">
        <span class="error-msg" v-show="isPasswordTipShow">密码应由【数字、字母/下划线/$】组成，且至少8位、至多14位 </span>
    </div>
    <div class="content">
        <label>确认密码:</label>
        <input type="text" placeholder="请输入确认密码" v-model="confirmPassword" @input="confirmPasswordInputCheck">
        <span class="error-msg" v-show="isConfirmPasswordTipShow">两次密码输入不一致</span>
    </div>
    <div class="controls">
        <input name="m1" type="checkbox" v-model="isAlreadyRead">
        <span>我已阅读<a @click="isMaskShow = true">《尚品汇用户协议》</a></span>
        <span class="error-msg" v-show="!isAlreadyRead">请阅读《尚品汇用户协议》</span>
        <Teleport to="body">
            <div class="mask" v-show="isMaskShow">
                <div class="dialog">
                    <h1>尚品汇用户协议</h1>
                    <p class="p1">&emsp;&emsp;欢迎使用我们的服务！在使用我们的服务前，请务必仔细阅读以下用户协议。通过访问或使用我们的服务，即表示您同意遵守以下条款和条件：</p><br>
                    <p><strong>&emsp;&emsp;1.服务描述：</strong> 我们的服务提供……（在此描述您的服务提供的内容、功能和特点）。</p>
                    <p><strong>&emsp;&emsp;2.用户责任：</strong> 用户应当对其在使用我们的服务过程中产生的行为负责。用户不得利用我们的服务进行任何违法或违反道德的活动，包括但不限于……（在此列举禁止的行为）。</p>
                    <p><strong>&emsp;&emsp;3.隐私保护：</strong> 我们尊重并保护用户的隐私权。我们将采取一切合理措施保护用户的个人信息，并仅在法律允许或用户授权的情况下使用或披露用户的个人信息。</p>
                    <p><strong>&emsp;&emsp;4.知识产权：</strong> 我们的服务包含的所有内容，包括但不限于文字、图片、音频、视频等，均受到知识产权法律的保护。未经授权，用户不得擅自复制、传播、修改、出售或利用我们的服务中的任何内容。</p>
                    <p><strong>&emsp;&emsp;5.免责声明：</strong> 我们不对用户因使用我们的服务而产生的任何直接或间接损失负责，包括但不限于利润损失、数据丢失等。用户应当自行承担使用我们服务的风险。</p>
                    <p><strong>&emsp;&emsp;6.服务变更与终止：</strong> 我们有权随时根据实际情况对服务内容进行变更、暂停或终止，并无需事先通知用户。在服务终止后，我们将不再对用户承担任何义务。</p>
                    <p><strong>&emsp;&emsp;7.法律适用与争议解决：</strong> 本用户协议受中华人民共和国法律管辖。因本用户协议引起的或与之相关的任何争议，双方应通过友好协商解决；如协商不成，任何一方均可向有管辖权的法院提起诉讼。</p>
                    <p><strong>&emsp;&emsp;8.其他条款：</strong> 本用户协议构成双方之间的完整协议，取代双方之前就本协议主题达成的任何口头或书面协议。任何对本协议的修改必须以书面形式进行，并由双方签字确认。</p>
                    <p><strong>&emsp;&emsp;9.协议更新：</strong> 我们保留随时更新本用户协议的权利，更新后的协议将在我们的网站上公布。用户应定期查阅最新的用户协议，并自觉遵守。</p>
                    <p>&emsp;&emsp;感谢您阅读我们的用户协议。如果您有任何疑问或意见，请随时联系我们。</p>
                    <div @click="isMaskShow = false">我已阅读</div>
                </div>
            </div>
        </Teleport>
    </div>
    <div class="btn" @click="submitRegister">
        <button>完成注册</button>
    </div>
    </div>

    <!-- 底部 -->
    <div class="copyright">
        <ul>
            <li>关于我们</li>
            <li>联系我们</li>
            <li>联系客服</li>
            <li>商家入驻</li>
            <li>营销中心</li>
            <li>手机尚品汇</li>
            <li>销售联盟</li>
            <li>尚品汇社区</li>
        </ul>
        <div class="address">地址：北京市昌平区宏福科技园综合楼6层</div>
        <div class="beian">京ICP备19006430号</div>
    </div>
</div>
</template>

<script setup lang="ts" name="Register">
    import { ref } from 'vue'
    import { useRouter,RouterLink } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import { reqIdCode,reqRegister } from '@/api'
    import { useUserStore } from '@/stores/user'

    let router = useRouter();
    // 手机号
    let tel = ref('');
    let isTelTipShow = ref(false);
    function telInputCheck(){
        tel.value = tel.value.replace(/[^0-9]/, '');
        tel.value = tel.value.length > 11? tel.value.slice(0,11) : tel.value;
        isTelTipShow.value = /^1[0-9]{10}$/.test(tel.value)? false : true;
        if (tel.value.length === 0){
            isTelTipShow.value = false;
        }
    }

    // 验证码
    let idCode = ref('');
    let isIdCodeTipShow = ref(false);
    function idCodeInputCheck(){
        idCode.value = idCode.value.replace(/[^0-9]/, '');
        idCode.value = idCode.value.length > 6? idCode.value.slice(0,6) : idCode.value;
        isIdCodeTipShow.value = [0,6].includes(idCode.value.length)? false : true;
    }
    // 点击获取验证码
    async function getIdCode(){
        if (isTelTipShow.value || tel.value.length === 0) return
        let result:any = await reqIdCode({'tel': tel.value});
        if (result.message === 'OK'){
            alert(`我是手机，验证码是${result.idCode}`);
        } else alert(result.message);
    }

    // 密码
    let password = ref('');
    let isPasswordTipShow = ref(false);
    function passwordInputCheck(){
        password.value = password.value.replace(/[^0-9a-zA-Z_$]/,'');
        password.value = password.value.length > 14? password.value.slice(0,14) : password.value;
        // 8-14位数字字母下划线$
        if (!/[0-9 | a-z | A-Z | $ | _]{8,14}/.test(password.value)) {
            isPasswordTipShow.value = true;
        } else if (/^[0-9]+$/.test(password.value)) {
            // 纯数字
            isPasswordTipShow.value = true;
        } else {
            isPasswordTipShow.value = false;
        }
        isPasswordTipShow.value = password.value.length === 0? false : isPasswordTipShow.value;
    }
    // 确认密码
    let confirmPassword = ref('');
    let isConfirmPasswordTipShow = ref(false);
    function confirmPasswordInputCheck(){
        confirmPassword.value = confirmPassword.value.replace(/[^0-9a-zA-Z_$]/,'');
        confirmPassword.value = confirmPassword.value.length > 14? confirmPassword.value.slice(0,14) : confirmPassword.value;
        isConfirmPasswordTipShow.value = confirmPassword.value === password.value || confirmPassword.value.length === 0? false : true;
    }
    // 阅读协议
    let isAlreadyRead = ref(false);
    let isMaskShow = ref(false);

    let { setLoginState,setUserName } = useUserStore();
    // 提交注册
    async function submitRegister(){
        let sign = 0;
        if (!tel.value) { isTelTipShow.value = true; sign+=1; }
        if (!idCode.value) { isIdCodeTipShow.value = true; sign+=1; }
        if (!password.value) { isPasswordTipShow.value = true; sign+=1; }
        if (!confirmPassword.value) { isConfirmPasswordTipShow.value = true; sign+=1;}
        if (sign) return
        let data = {
            'tel': tel.value,
            'idCode': idCode.value,
            'password': password.value,
            'registerTime': Date.now()
        }
        let result:any = await reqRegister(data);
        if (result.message === '注册成功') {
            setLoginState(true);
            setUserName(tel.value);
            router.push('/home');
            ElMessage({
                message: '注册成功',
                type: 'success'
            });
        }
    }
    

</script>

<style lang="less" scoped>
.register-container {
    .register {
    width: 1200px;
    height: 445px;
    border: 1px solid rgb(223, 223, 223);
    margin: 0 auto;

    h3 {
        background: #ececec;
        margin: 0;
        padding: 6px 15px;
        color: #333;
        border-bottom: 1px solid #dfdfdf;
        font-size: 20.04px;
        line-height: 30.06px;

        span {
            font-size: 14px;
            float: right;
            a {
                color: #e1251b;
            }
        }
        
    }

    div:nth-of-type(1) {
        margin-top: 40px;
    }

    .content {
        padding-left: 390px;
        margin-bottom: 18px;
        position: relative;

        label {
        font-size: 14px;
        width: 96px;
        text-align: right;
        display: inline-block;
        }

        input {
        width: 270px;
        height: 38px;
        padding-left: 8px;
        box-sizing: border-box;
        margin-left: 5px;
        outline: none;
        border: 1px solid #999;
        }

        .getCode {
            width: 80px;
            height: 38px;
            margin-left: 10px;

        }
        img {
        vertical-align: sub;
        }

        .error-msg {
        position: absolute;
        top: 100%;
        left: 495px;
        color: red;
        }
    }

    .controls {
        text-align: center;
        position: relative;
        

        input {
            vertical-align: middle;
            margin-left: -30px;
            margin-right: 20px;

        }

        span>a {
            color: deepskyblue;
            cursor: pointer;
            &:hover {
                color: red;
            }
        }
        

        .error-msg {
            position: absolute;
            top: 100%;
            left: 495px;
            color: red;
            margin-top: 10px;
        }
    }

    .btn {
        text-align: center;
        line-height: 36px;
        margin: 17px 0 0 55px;
        margin-top: 40px;

        button {
        outline: none;
        width: 270px;
        height: 36px;
        background: #e1251b;
        color: #fff !important;
        display: inline-block;
        font-size: 16px;
        }
    }
}

    .copyright {
        width: 1200px;
        margin: 0 auto;
        text-align: center;
        line-height: 24px;

        ul {
            li {
            display: inline-block;
            border-right: 1px solid #e4e4e4;
            padding: 0 20px;
            margin: 15px 0;
            }
        }
    }
}
.mask {
    position: absolute;
    background-color: rgba(0,0,0,0.5);
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    .dialog {
        width: 500px;
        height: 300px;
        background-color: #ccc;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
        padding: 60px;
        border-radius: 10px;
        overflow: auto;
        h1 {
            font-size: 30px;
            text-align: center;
        }
        p {
            font-size: 15px;
        }
        .p1 {
            font-size: 20px;
        }
        div {
            width: 80px;
            height: 20px;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            margin-top: 20px;
            border: 1px solid black;
            border-radius: 5px;
            text-align: center;
            line-height: 20px;
            cursor: pointer;
            &:hover {
                color: white;
                background-color: deepskyblue;
            }
            
        }
    }
}
</style>@/stores/user