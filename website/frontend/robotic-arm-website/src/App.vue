<template>
  <div id="app">
    <div class="nav-bar">
    <button @click="toggleDarkMode">
      {{ isDarkMode ? "Light Mode" : "Dark Mode" }}
    </button> 
    </div>
    <router-view></router-view>
        <!-- This is where the content will change -->
  </div>
</template>


<script>
export default {
  name: "App",
  data(){
    return{
      isDarkMode:false,
    };
  },
 methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem("darkMode", this.isDarkMode);
      this.applyDarkModeClass();
    },
    applyDarkModeClass() {
      document.body.classList.toggle("dark", this.isDarkMode);
    },
  },
  watch: {
    // Watch for route changes to reapply dark mode
    $route() {
      this.applyDarkModeClass();
    },
  },
  mounted() {
    // Load dark mode preference from localStorage
    this.isDarkMode = localStorage.getItem("darkMode") === "true";
    this.applyDarkModeClass();
  },};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}


a{
  text-decoration: none;
  transition: color 0.3s ease;
}

body{
  background-color:#ffffff;
  color:#000000
}

body.dark {
  background-color: #121212;
  color:#ffffff
}
body.dark h1,
body.dark h2,
body.dark h3,
body.dark h4,
body.dark h5,
body.dark h6,
body.dark strong,
body.dark p{
  color: #ffffff;
}

.nav-bar{
  display:flex;
  justify-content:right;
}

.dark a {
  color: #4aa3ff;
  text-decoration: none;
  transition: color 0.3s ease;
}


.dark a:hover {
  color: #82cfff; 
}


.dark a:visited {
  color: #a381ff; 
}
button {
  background-color: #333;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 7px 16px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 300;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
}

button:hover {
  background-color: #555;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

button:active {
  transform: scale(0.98);
}

body.dark button {
  background-color: #ccc;
  color: #333;
}

body.dark button:hover {
  background-color: #bbb;
}</style>
