<template>
  <div class="printing-updates">
    <div class="title">
      <h4>3D Printing Updates</h4>
    </div>
    <div class="links">
      <router-link to="/progress">All Progress</router-link>
      
      <router-link to="/ai-progress">AI models progress
      </router-link>
      <router-link to="/hardware-progress">Hardware Progress</router-link>
    </div> 
      <div class="update-content" v-for="update in printingUpdates" :key="update.title">
      <h4>{{update.title}}</h4>
      <p v-html="update.content"></p>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex';
export default {
  computed:{
    ...mapGetters(['printingUpdates'])
  }
};
</script>

<style >

.title{
  display:flex;
  justify-content:center;
}
.update-content .link{
  display:flex;
  justify-content:center;
} 

.model-link{
  margin-left:3px;
}
.links{
  
  display:flex;
  justify-content:space-between;
}
.printing-updates{
 max-width:800px;
  width:90%;
  margin: 0 auto;
  padding:20px;
  font-family: Arial, sans-serif;
}
.update-content{
  border: 1px solid #ddd;
  border-radius:5px;
  padding:10px;
  margin:10px 0;
  margin-top:20px;
}
@media(max-width:760px){

  .printing-updates,
  .links,
  .update-content{
    max-width:90%;
    text-align:center;
    margin:0 auto;
  }
}
  .update-content{
  margin-top:20px;
}
  .links {
    flex-direction: column; /* Change to vertical layout */
    align-items: center; /* Center the items */
    padding: 12px;
  }

  .links a {
    margin: 5px 0; /* Add vertical spacing between links */
  }
</style>

