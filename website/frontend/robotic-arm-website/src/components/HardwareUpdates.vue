<template>
  <div class="hardware-updates">
    <h2>Hardware Updates</h2>
    <div class="links">
      <router-link to="/progress">All Progress</router-link>
      
      <router-link to="/ai-progress">AI models progress
      </router-link>
      <router-link to="/printing-progress">3D Printing Progress</router-link>
    </div> 
      <div class="update-content" v-for="update in hardwareUpdates" :key="update.title">
      <h4>{{update.title}}</h4>
      <p v-html="update.content"></p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['hardwareUpdates']) // Access software updates from the Vuex store
  }
};
</script>
<style >

.links{
  
  display:flex;
  justify-content:space-between;
}
.hardware-updates{
  max-width:800px;
  width:90%;
  margin: 0 auto;
  padding:20px;
  font-family: Arial, sans-serif;
}

.update-content img.soldering-img{
  max-width: 100%;
  height: 300px;
  border:2px solid #ccc;
  border-radius: 8px;
}
.update-content div.sold-img{
  margin-top:20px;
  display:flex;
  justify-content:center;
}
.update-content{
  border: 1px solid #ddd;
  border-radius:5px;
  padding:10px;
  margin:10px 0;
  margin-top:20px;
}

@media(max-width:768px){
  .hardware-updates,
  .links,
  .update-content{
    max-width:90%;
    text-align:center;
    margin:0 auto;
  }
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
