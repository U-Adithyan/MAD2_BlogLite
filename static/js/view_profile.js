const Post = Vue.component('blog_post',{
  delimiters: ['{', '}'],
  props: {
    post: {
      type: Object,
      required: true
    },
  },
  template:
    `
    <div class="container py-1">
      <div class="justify-content-center align-items-center">
        <div class="card" style="border-radius: 15px;">
          <div class="card-body p-4">
            <h4>{post.title}</h4>
            <div class="py-2">
              <img :src="post.image" class="img-fluid mx-auto d-block w-50" style="border-radius: 10px;">
            </div>
            <hr>
            <span>{post.caption}</span>
          </div>
        </div>
      </div>
    </div>
    `
})

var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    components:{
      'blog_post': Post
    },
    data: function () {
        return {
            image_location: '',
            view_user: '',
            username: '',
            blog_count: 0,
            follower_count: 0,
            following_count: 0,
            status: false,
            post_list: ''
        };
    },
    mounted : async function(){
      this.username = sessionStorage.getItem("current_user")
      this.view_user = sessionStorage.getItem("view_user")
      console.log(this.view_user)
      const response = await fetch('/' + this.view_user + '/get_profile',{
        method:'GET',
        headers:{
          'Content-Type':'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if(response.status === 200){
        const data = await response.json()
        this.image_location = data.image_location
        this.blog_count = data.blog_count
        this.follower_count = data.follower_count
        this.following_count =  data.following_count
        this.post_list = data.post_list
        const response2 = await fetch('/'+this.username+'/check/follow/'+this.view_user,{
          method:'GET',
          headers:{
            'Content-Type':'application/json',
            'Authentication-Token': localStorage.getItem("auth_token")
          }
        })
        if(response2.status === 200){
          const data2 = await response2.json()
          this.status = data2.status
        }
      }else if(response.status === 401){
        window.location = '/access_failure'
      }
    },
    methods: {
      logout : function(){
        localStorage.removeItem("auth_token")
        sessionStorage.removeItem("current_user")
        window.location = '/logout'
      },
      follow: async function(){
        const response = await fetch('/'+this.username+'/follows/'+this.view_user, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem("auth_token")
          }
        })
        if (response.status == 200) {
          this.status = true
        }else{
          window.location.reload()
        }
      },
      unfollow: async function(){
        const response = await fetch('/'+this.username+'/unfollows/'+this.view_user, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem("auth_token")
          }
        })
        if (response.status == 200) {
          this.status = false
        }else{
          window.location.reload()
        }
      },
      dashboard : function() {
        window.location = '/'+ this.username +'/dashboard'
      },
      search : function() {
        window.location = '/'+ this.username +'/search'
      },
      profile : function() {
        window.location = '/'+ this.username +'/profile'
      }
    }
})