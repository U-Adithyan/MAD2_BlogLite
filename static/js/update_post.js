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
    mounted : async function(){
      this.username = sessionStorage.getItem("current_user")
      this.post_id = sessionStorage.getItem("current_post")
      const response = await fetch('/'+this.username+'/post/'+this.post_id, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if(response.status===200){
        const data = await response.json()
        this.title = data.title
        this.caption = data.caption
        console.log(this.title)
        console.log(this.caption)
      }else if (response.status===401){
        window.location = '/access_failure'
      }else{
        window.location = '/'+ this.username +'/dashboard'
      }
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
        update_post: async function () {
          const formData = new FormData()
          if(this.file_present){
            const input = document.getElementsByName("file")["0"].files
            formData.append('file', input["0"])
          }
          formData.append('title', this.title)
          formData.append('caption', this.caption)
          const response = await fetch('/'+this.username+'/post/'+this.post_id+'/update',{
            method: 'POST',
            headers: {
              'Authentication-Token': localStorage.getItem("auth_token")
            },
            body: formData
          })
          window.location = '/'+ this.username +'/dashboard'
        }
    }
})