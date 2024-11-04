
<template>
  <div class="ai-updates">
    <div class="title">
    <h3>AI Updates</h3>
    </div>
<div class="links">
      <router-link to="/progress">All Progress</router-link>
      
      <router-link to="/hardware-progress">Hardware Progress
      </router-link>
      <router-link to="/printing-progress">3D Printing Progress</router-link>
    </div> 
      <div class="update-content" v-for="update in aiUpdates" :key="update.title">
      <h4>{{update.title}}</h4>
      <p v-html="update.content"></p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['aiUpdates'])
  }
};
</script>

<style >

.github-link{
  display:flex;
  justify-content:center;
}
.title{
  display:flex;
  justify-content:center;
  font-size:1.2rem;
}

.links{
  
  display:flex;
  justify-content:space-between;
}
.container{
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

.ai-updates{
  max-width:800px;
  width:90%;
  margin: 0 auto;
  padding:20px;
  font-family:Arail, sans-serif;
}
@media(max-width:768px){
  .ai-updates,
  .links,
  .update-content{
    max-width:90%;
    text-align:center;
  }
}

</style>
