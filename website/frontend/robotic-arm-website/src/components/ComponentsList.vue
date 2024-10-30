
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
    <p>You will also need some other minor components like:</p>
    <ul>
      <li>Power supply for the raspberry pi</li>
      <li>Sd card for the raspberry pi OS and storage</li>
      <li>3D printer if you decide to print it by yourself</li>
 <li>All types of pin wires, male-male, female-female, female-male</li>
      <li>A lot of patience</li>
    </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      components: [
        { name: 'Raspberry Pi 5 4Gb', description: 'The Raspberry Pi 5 will handle all the AI models needed to achieve the goal'},
        
        { name: 'Arduino Mega 2560', description: 'The arduino will handle all the motors, both the steppers and the servos one.'},
        { name: '4x NEMA17', description: 'The NEMA17 are the stepper motors I decided to go with.'},
        { name: '2x MG996R', description: 'These are the servo motors I chose. High precision and decent torque.'},
        { name: '4x DRV8825', description: 'The DRV8825 are motor drivers and will handle the stepper motors simultaneously.'},
        { name: 'PCA9685 PWM', description: 'Same as the DRV8825 but for the servo motors.'},
        {name:'RASPBERRY PI Official Camera Module V2 8Mp', description:'The camera I will use for object detection.'},
        {name:'Adafruit I2S MEMS - SPH0645LM4H', description:'Microphone I will use for the wake word model and the speech to text model.'},
        { name: 'Power Supply 24V', description: 'Power supply for the stepper motors'},
        { name: 'Power Supply 6V', description: 'Power supply for the servo motors'},
        
      ],
    };
  },
};
</script>

<style scoped>

.other-components{
  margin-top:45px;
}
h2{
  text-align:center;
}
.home-link{
  margin-bottom:20px;
}
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}
</style>
