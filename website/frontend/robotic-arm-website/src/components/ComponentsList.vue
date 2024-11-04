
<template>
  <div class="container">
    <h2>Components Overview</h2>
    <div class="home-link">
      <router-link to="/">Home</router-link>
    </div>
    <table>
      <thead>
        <tr>
          <th>Component Name</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(component, index) in components" :key="index">
          <td>{{ component.name }}</td>
          <td>{{ component.description }}</td>
        </tr>
      </tbody>
    </table>
    <div class="other-components">
      <p>Additional minor components required:</p>
      <ul>
        <li>Power supply for the Raspberry Pi</li>
        <li>SD card for Raspberry Pi OS and storage</li>
        <li>3D printer (if you plan to print components yourself)</li>
        <li>Various types of jumper wires: male-male, female-female, and female-male</li>
        <li>Plenty of patience</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      components: [
        { name: 'Raspberry Pi 5 4GB', description: 'Handles all AI models necessary to achieve project goals.' },
        { name: 'Arduino Mega 2560', description: 'Controls all motors, including both steppers and servos.' },
        { name: '4x NEMA17', description: 'Stepper motors selected for their precision and reliability.' },
        { name: '2x MG996R', description: 'High-precision servo motors with decent torque.' },
        { name: '4x DRV8825', description: 'Motor drivers for simultaneous stepper motor control.' },
        { name: 'PCA9685 PWM', description: 'Driver for controlling servo motors.' },
        { name: 'Raspberry Pi Camera Module V2 8MP', description: 'Camera for object detection.' },
        { name: 'Adafruit I2S MEMS Microphone - SPH0645LM4H', description: 'Microphone for wake word detection and speech-to-text processing.' },
        { name: '24V Power Supply', description: 'Power source for stepper motors.' },
        { name: '6V Power Supply', description: 'Power source for servo motors.' },
      ],
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  color: #333;
}

.home-link {
  margin-bottom: 20px;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.other-components {
  margin-top: 30px;
}

.other-components p {
  font-weight: bold;
}

.other-components ul {
  margin-top: 10px;
  padding-left: 20px;
}

/* Responsive styling for smaller screens */
@media (max-width: 768px) {
  .container {
    max-width: 90%;
  }

  h2,
  .home-link,
  .other-components p {
    text-align: center;
  }

  table {
    font-size: 0.9em;
  }

  th, td {
    padding: 8px;
  }

  .other-components ul {
    padding-left: 10px;
  }
}
</style>
``
/style>
