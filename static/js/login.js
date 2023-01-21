var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: function () {
        return {
            username: '',
            password: ''
        };
    },
    created : function(){
      
    },
    methods: {
        login: async function () {
            const response = await fetch('/login?include_auth_token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "username": this.username, "password": this.password })
            })
            console.log(response.status)
            if (response.status == 200) {
                const data = await response.json()
                const token = data.response.user.authentication_token
                const id = data.response.user.id
                localStorage.setItem("auth_token", token);
                sessionStorage.setItem("current_user", this.username);
                window.location = '/'+ this.username + '/dashboard' 
            } else {
                const data = await response.json()
                if (data.response.errors[0] == "Invalid password") {
                    console.log("hello 401")
                    window.location = '/login_failed/401'
                } else if (data.response.errors[0] == "Specified user does not exist") {
                    console.log("hello 404")
                    window.location = '/login_failed/404'
                } else {
                    window.location = '/login_failed/' + response.status
                }
            }
        }
    }
})