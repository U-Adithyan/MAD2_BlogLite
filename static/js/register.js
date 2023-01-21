var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: function () {
        return {
            username: '',
            email: '',
            password: '',
            file_present: false
        };
    },
    methods: {
        checking: function () {
            var Extensions = [".jpg", ".jpeg", ".bmp", ".png"];
            const file = this.$refs.file.files[0]
            var imageName = file.name
            if (imageName.length > 0) {
                var checker = false;
                for (var j = 0; j < Extensions.length; j++) {
                    var ext = Extensions[j];
                    if (imageName.substr(imageName.length - ext.length, ext.length).toLowerCase() == ext.toLowerCase()) {
                        checker = true;
                        break;
                    }
                }
                if (!checker) {
                    alert("Sorry, " + imageName + " is invalid, allowed extensions are: " + Extensions.join(", "));
                    imageName = "";
                }
            }
            if (imageName != "") {
                this.file_present = true
            } else {
                this.file_present = false
            }
        },
        register: async function () {
            const response = await fetch('/register?include_auth_token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "username": this.username, "email": this.email, "password": this.password })
            })
            const data = await response.json()
            if (response.status == 200) {
                const token = data.response.user.authentication_token
                const id = data.response.user.id
                localStorage.setItem("auth_token", token);
                sessionStorage.setItem("current_user", this.username);

                const input = document.getElementsByName("file")["0"].files
                const formData = new FormData()
                formData.append('file', input["0"])
                const response = await fetch('/user/' + this.username + '/add_dp', {
                    method: 'POST',
                    headers: {
                        'Authentication-Token': localStorage.getItem("auth_token")
                    },
                    body: formData
                })
                if (response.status == 200) {
                    window.location = '/'+ this.username +'/dashboard'
                } else {
                    window.location = '/' + this.username + '/register_failed/' + response.status
                }

            } else {
                window.location = '/register_failed/' + response.status
            }
        }
    }
})