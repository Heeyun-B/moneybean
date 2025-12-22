<template>
  <div 
    class="skeleton-loader" 
    :style="{ width: width, height: height, borderRadius: radius }"
  ></div>
</template>

<script setup>
defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '20px' },
  radius: { type: String, default: '4px' }
})
</script>

<style scoped>
.skeleton-loader {
  background-color: #eee;
  background-image: linear-gradient(
    90deg,
    #eee 0px,
    #f9f9f9 50%,
    #eee 100%
  );
  background-size: 200px 100%;
  background-repeat: no-repeat;
  display: inline-block;
  animation: shimmer 1.5s infinite linear;
}

@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}
</style>