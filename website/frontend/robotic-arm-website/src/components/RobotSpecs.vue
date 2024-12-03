<template>
  <div class="ai-features">
    <h3>What does AI Powered mean?</h3>
    <p class="caption">
      This section outlines the AI capabilities of the robotic arm, showcasing
      the technologies used to enhance interaction and functionality, which is
      the main goal of the project.
      <br />
      <br />
      The models, developed from scratch using the TensorFlow library, aim to
      explore and learn about the power of machine learning.
    </p>
    <p class="caption">We'll start with the three models that are the foundation of the entire project, which are:</p>

    <ul>
      <li
        v-for="(feature, index) in features"
        :key="index"
        class="feature-item"
      >
        <strong>{{ feature.title }}</strong>
        <p>{{ feature.description }}</p>
      </li>
    </ul>
  </div>
  <div class="hardware-specs">
    <h3>What about the Hardware?</h3>
    <p class="caption">
      This section details the essential hardware components of the robotic arm,
      showcasing the technology that enables its functionality and interaction.
    </p>
    <p class="caption">
      This are the main components I used, if you would like to see everything I used, check this link
    </p>
      <div class="progress-link">
          <router-link to="/components" class="progress-link">View Components List</router-link>

      </div>
    <ul>
      <li v-for="(spec, index) in hardwareSpecs" :key="index" class="spec-item">
        <strong>{{ spec.title }}</strong>
        <p>{{ spec.description }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      features: [
        {
          title: "Speech-to-Text Model:",
          description:
            "Developed from scratch using TensorFlow, this model converts spoken language into text commands for the robotic arm, enabling more intuitive interaction.",
        },
        {
          title: "Wake Word Detection:",
          description:
            "Implemented a custom wake word detection system from scratch that listens for a specific phrase to activate the robotic arm, ensuring it only responds when needed.",
        },
        {
          title: "Object Detection:",
          description:
            "Utilizing the Raspberry Pi Camera Module 2, the robotic arm can identify and interact with objects in its environment. This capability enhances its functionality for various tasks.",
        },
      ],
      hardwareSpecs: [
        {
          title: "Raspberry Pi 5:",
          description:
            "The Raspberry Pi will be responsible for the AI support.Combined with the Camera Pi it will sustain all the three models.",
        },
        {
          title: "Raspberry Pi Official Camera Module V2:",
          description:
            "Used for object detection and visual feedback, allowing the arm to identify and interact with its environment.",
        },
        {
          title: "Adafruit Microphone:",
          description:
            "Captures voice commands for speech-to-text processing, enabling user interaction.",
        },
        {
          title: "NEMA 17 Stepper Motors:",
          description:
            "Provide precise control and movement for the robotic arm's joints.",
        },
        {
          title: "MG996R Servo Motors:",
          description:
            "Used for tasks requiring precise positioning and movement.",
        },
        {
          title: "Arduino Mega 2560:",
          description:
            "Controls the motors, providing an interface for precise movement and task execution.",
        },
      ],
    };
  },
};
</script>

<style scoped>

.progress-link{
  display:flex;
  justify-content:center;
}
.ai-features {
  border-top: 1px dashed black;
  max-width: 50%;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h3 {
  color: black; 
  font-weight: bold;
  text-align: center;
  margin-bottom: 15px;
}

.caption {
  font-style: italic;
  color: #666;
  text-align: center;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

ul li {
  margin-bottom: 15px; 
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px; 
  transition: transform 0.2s, box-shadow 0.2s;
}

ul li:hover {
  transform: translateY(-2px); 
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

strong {
  color: black; 
}

p {
  margin: 5px 0; 
}
/* Dark mode styles */
body.dark h2 {
  color: #e0e0e0; /* Light color for h2 */
}

body.dark .caption{
  color: #cccccc; /* Softer light color for general text */
}

body.dark .ai-features,
body.dark .hardware-specs{
  border-top: 1px dashed #ddd; /* Subtle border for dark mode */
}

body.dark .progress-link a {
  color: #bb86fc; /* Softer, lighter link color in dark mode */
}
.hardware-specs {
  border-top: 1px dashed black;
  max-width: 50%;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}
@media (max-width: 768px) {
  .caption,
  .hardware-specs,
  .ai-features
 {
     max-width: 90%;
    text-align:center;
  }
  h2 {
    font-size: 1.5em;
  }
  .caption {
    padding: 0 20px; 
    text-align: center;
  }
}
</style>
