<template>
  <div class="update">
    <h4>{{ title }}</h4>
    <p>{{ content }}</p>
  </div>
  
</template>

<script>

export default {
  props: {
    title: String,
    content: String,
    steps: Array,
    image: String
  },
  components: {
  }
};
</script>

<style scoped>
/* Your styles */
</style>

