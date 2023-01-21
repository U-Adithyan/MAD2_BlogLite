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
          <h6 @click="view_profile">{post.username}'s post</h6>
          <hr>
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
    `,
  methods: {
      view_profile : function(){
        sessionStorage.setItem("view_user",this.post.username)
        window.location = '/' + this.post.username + '/view/profile'
      }
    }
})

var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: function () {
        return {
            username: '',
            post_list: ''
        };
    },
    components:{
      'blog_post': Post
    },
    beforeCreate : async function(){
      const response = await fetch('/authenticate',{
        method:'GET',
        headers:{
          'Content-Type':'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if(response.status === 200){
        const data = await response.json()
      }else if(response.status === 401){
        window.location = '/access_failure'
      }
    },
    mounted : async function() {
      this.username = sessionStorage.getItem("current_user")
      const response = await fetch('/'+this.username+'/get_feed',{
        method:'GET',
        headers:{
          'Content-Type':'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if(response.status === 200){
        const data = await response.json()
        this.post_list = data.post_list
        console.log(this.post_list)
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
      search : function() {
        window.location = '/'+ this.username +'/search'
      },
      profile : function() {
        window.location = '/'+ this.username +'/profile'
      },
      make_post : function(){
        window.location = '/'+ this.username +'/make_blog'
      }
    }
})