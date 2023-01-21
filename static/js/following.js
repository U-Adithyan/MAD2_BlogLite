const User = Vue.component('user_card',{
  delimiters: ['{', '}'],
  data: function () {
    return {
      following: '',
      };
  },
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  template:`
    <div class="card">
      <div class="card-body">
        <div class="d-sm-flex">
          <div @click = "view_profile">
            <h5 class="card-text">{user.username}</h5>
          </div>
          <div class="ms-auto">          
            <div v-if="following">
              <button class="btn btn-primary" @click="unfollow">Unfollow</button>
            </div>
            <div v-else>
              <button class="btn btn-primary" @click="follow">Follow</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  created: function(){
    this.following = this.user.followed
  },
  methods:{
    follow: async function(){
      const response = await fetch('/'+this.$parent.username+'/follows/'+this.user.username, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if (response.status == 200) {
        this.following = true
      }else{
        window.location.reload()
      }
    },
    unfollow: async function(){
      const response = await fetch('/'+this.$parent.username+'/unfollows/'+this.user.username, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if (response.status == 200) {
        this.following = false
        window.location.reload()
      }else{
        window.location.reload()
      }
      
    },
    view_profile: function(){
      sessionStorage.setItem("view_user",this.user.username)
      let location = '/' + this.user.username + '/view/profile'
      this.$parent.change_location(location)
    }
  }
})

var app = new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: function () {
        return {
            username: '',
            search_query:'',
            user_list: '',
            filtered_list: ''
        };
    },
    components:{
      'user_card': User
    },
    created : async function(){
      this.username = sessionStorage.getItem("current_user")
      const response = await fetch('/'+ this.username +'/get_following',{
        method:'GET',
        headers:{
          'Content-Type':'application/json',
          'Authentication-Token': localStorage.getItem("auth_token")
        }
      })
      if(response.status === 200){
        const data = await response.json()
        this.user_list = data.user_list
      }else if(response.status === 401){
        window.location = '/access_failure'
      }
    },
  methods :{
    filtered : function(){
      console.log(this.search_query)
      this.filtered_list = this.user_list.filter(this.search_bar)
    },
    search_bar: function(user){
      return user.username.toLowerCase().startsWith(this.search_query.toLowerCase())
    },
    logout : function(){
        localStorage.removeItem("auth_token")
        sessionStorage.removeItem("current_user")
        window.location = '/logout'
    },
    change_location: function(location){
      window.location = location
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