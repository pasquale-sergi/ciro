<template>
  <div class="progress-page">
    <h2>Project Progress</h2>
    <div class="home-link">
      <a href="/">Home</a>
    </div>
    <section class="updates">
      <div class="links-section">
        <div class="other-links">
          <p class="caption">
              Below, you’ll find all progress updates in chronological order.<br> 
              Alternatively, you can check specific sections by following these links:
          </p>
        </div>
        <div class="progress-links">

          <router-link to="/hardware-progress">Hardware Progress</router-link>
          <router-link to="/ai-progress">AI models Progress</router-link>
          <router-link to="/printing-progress">3D Printing Progress</router-link>
        </div>
      </div>
      <div v-for="(update, index) in allUpdates" :key="index" class="update">
        <h4>{{ update.title }}</h4>
      <p v-html="update.content"></p>
      </div>
        
   </section>
  </div>
</template>
  
  <script>
import {mapGetters} from 'vuex';

export default {
      computed:{
        ...mapGetters(['allUpdates'])
      }
    };
</script>
  
  <style >

.github-link{
  display:flex;
  justify-content:center;
}
.other-links{
  display:flex;
  justify-content:center;
}

.links-section{
  border:2px dashed #ddd;
  padding:9px;
  margin-top:10px;
}

.progress-links{
  display:flex;
  justify-content:space-between;
}

.update div.sold-img {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.update img.soldering-img {
  max-width: 100%; 
  height: 300px; 
  border: 2px solid #ccc;
  border-radius: 8px; 
}

.progress-page {
  max-width: 800px;
  width:90%;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  color: #333;
}

h3 {
  margin-top: 20px;
}

.update {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  margin: 10px 0;
  margin-top:20px;
}

.image-gallery {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin: 10px 0;
}

.image-gallery img {
  width: 45%;
  border-radius: 5px;
}

.video-gallery {
  text-align: center;
  margin: 20px 0;
}

video {
  width: 100%;
  border-radius: 5px;
}
.procedure {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9; 
}

.procedure p {
  font-weight: bold;
  margin-bottom: 10px;
}

.procedure-step {
  font-family: "Courier New", Courier, monospace; 
  margin: 5px 0;
  position: relative;
  padding-left: 20px; 
}

.home-link{
  display:flex;
  justify-content:center;
}
  .code-images{
  display:flex;
  align-items:center;
  flex-direction:column;
  margin:0 auto;
}
  .code-img{
  max-width:800px;
  width:95%;
  margin-top:20px;
}
@media(max-width:768px){
  .caption,
  .progress-page,
  .updates{
    max-width:100%;
    text-align:center;
    margin:0 auto;
  }
  .progress-links {
    flex-direction: column;
    align-items: center; 
    padding: 12px;
  }

  .progress-links a {
    margin: 5px 0;
  }

  .links-section{
    border:2px dashed #ddd;
    padding:9px;
    margin-top:10px;
  }

  .code-img{
    margin-top:10px;
    margin-bottom:10px;
  }
}
</style>
  
