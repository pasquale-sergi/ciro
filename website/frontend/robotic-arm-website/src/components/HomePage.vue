<template>
  <div class="home-page">
    <h2>
Ciro: The AI-Powered Robotic Arm
</h2>
    <div class="caption">
      <p>

Welcome to Ciro's development journey! Ciro is an intelligent robotic arm designed to recognize objects, respond to voice commands, and perform tasks with precision. This project combines robotics with AI for an exciting hands-on exploration into machine intelligence. Follow along as Ciro grows in capability and skill.       <br>       <br>One of the goals of this project is to have a buddy with whom I can play physical chess and communicate.


      </p>
      <p>
  <strong>Disclaimer</strong>: I know this project is easily achievable with some AI APIs, but I wanted to experience firsthand what it means to build and train a model. So enjoy my struggles in the progress section.
</p>
    </div>
    <div class="progress-link">
      <router-link to="/progress" class="progress-link"
        >View Project Progress</router-link
      >
    </div>
    <div class="robot-specs">
      <robot-specs></robot-specs>
    </div>
    <div class="about-me">
      <h3>About Me</h3>
      <p>
        Hi! I'm a Computer and Electrical Engineering student. I love to program and build things. After spending most of my time developing web applications, I was curious to create something physical. I'm also new to the world of machine learning and eager to test its potential. This project gives me the chance to combine everything and challenge myself. 
        <br><br>
        If you have any suggestions, feel free to reach out to me at <a href="mailto:[email]">pasquale.s3rgi@gmail.com</a> or check my GitHub: <a href="https://www.github.com/pasquale-sergi">pasquale-sergi</a>.
      </p>
    </div>
  </div>
</template>

<script>
import RobotSpecs from "./RobotSpecs.vue";
export default {
  components: { RobotSpecs },
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h2 {
  text-align: center;
}

.caption {
  max-width:800px;
  width: 90%;
  text-align: center;
  margin: 0 auto;
}

.progress-link {
  text-align: center;
}

.robot-specs {
  margin-top: 20px;
}
.about-me {
  border-top: 1px dashed black;
  max-width:800px;
  width: 90%;
  text-align: center;
  margin: 20px auto;
}
@media (max-width: 768px) {
  .caption,
  .about-me {
    width: 90%;
  }
  h2 {
    font-size: 1.5em;
  }
  .home-page,
  .progress-link {
    text-align: center;
  }
}
</style>
