var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: function () {
        return {
            username: '',
            title: '',
            caption: '',
            post_id: '',
            file_present: false
        };
    },
    mounted : function(){
      this.username = sessionStorage.getItem("current_user")
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
        post: async function () {
            const response = await fetch('/'+this.username+'/posting', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem("auth_token")
                },
                body: JSON.stringify({ 'title' : this.title,
                                      'caption': this.caption })
            })
            const data = await response.json()
            if (response.status == 200) {
                this.post_id = data.id
                const input = document.getElementsByName("file")["0"].files
                const formData = new FormData()
                formData.append('file', input["0"])
              
                const response = await fetch('/' + this.username + '/post/'+this.post_id+'/posting_image', {
                    method: 'POST',
                    headers: {
                        'Authentication-Token': localStorage.getItem("auth_token")
                    },
                    body: formData
                })
                if (response.status == 200) {
                    window.location = '/'+ this.username +'/dashboard'
                } else {
                    window.location = '/'+this.username+'/1/post_failure'
                }

            } else {
                window.location = '/'+this.username+'/0/post_failure'
            }
        }
    }
})