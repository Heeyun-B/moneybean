<template>
  <div class="video-card" @click="$emit('click', video)">
    <div class="thumbnail-wrapper">
      <img :src="video.snippet.thumbnails.medium.url" :alt="video.snippet.title" class="thumbnail">
    </div>
    <div class="video-info">
      <h3 class="video-title">{{ video.snippet.title }}</h3>
      <p class="channel-name">{{ video.snippet.channelTitle }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoCard',
  props: {
    video: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.video-card {
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  background: white;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
  background: #000;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-info {
  padding: 12px;
}

.video-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.channel-name {
  font-size: 12px;
  color: #666;
  margin: 0;
}
</style>