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
            <div class="d-sm-flex">
              <h4>{post.title}</h4>
              <div class="d-sm-flex ms-auto">
                <h4 class="bi bi-pen" @click.once="update_post"></h4>
                <h4 class="bi bi-trash mx-3" @click.once="delete_post"></h4>
              </div>
            </div>
            <div class="py-2">
              <img :src="post.image" class="img-fluid mx-auto d-block w-50" style="border-radius: 10px;">
            </div>
            <hr>
            <span>{post.caption}</span>
          </div>
        </div>
      </div>
    </div>
    `,
  methods: {
    delete_post: async function(){
      if (confirm("Do you want to delete this post ?")){
        const response = await fetch('/' + this.post.username + '/post/'+ this.post.id + '/delete_post',{
          method:'DELETE',
          headers:{
            'Content-Type':'application/json',
            'Authentication-Token': localStorage.getItem("auth_token")
          }
        })
        if(response.status === 200){
          console.log("Post Deleted")
          window.location = '/'+ this.post.username +'/profile'
        }else if(response.status === 401){
          window.location = '/access_failure'
        }else{
          console.log("Delete Failed")
          window.location = '/'+ this.post.username +'/profile'
        }
      }else{
        window.location = '/'+ this.post.username +'/profile'
      }
    },
    update_post: async function(){
      sessionStorage.setItem("current_post",this.post.id)
      window.location = '/'+ this.post.username + '/post/' + this.post.id + '/update_post'
    }
  }
})

var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: function () {
        return {
            image_location: '',
            username: '',
            blog_count: 0,
            follower_count: 0,
            following_count: 0,
            post_list: ''
        };
    },
    mounted : async function(){
      this.username = sessionStorage.getItem("current_user")
      const response = await fetch('/' + this.username + '/get_profile',{
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
      followers: function(){
         window.location = '/'+this.username+'/followers'
      },
      following: function(){
        window.location = '/'+this.username+'/following'
      },
      dashboard : function() {
        window.location = '/'+ this.username +'/dashboard'
      },
      search : function() {
        window.location = '/'+ this.username +'/search'
      },
      make_post : function(){
        window.location = '/'+ this.username +'/make_blog'
      }
    }
})