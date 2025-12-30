<script setup>
import { ref } from 'vue'

// Demo counter to demonstrate Vue reactivity is working
const count = ref(0)
</script>

<template>
  <div class="container">
    <div class="header">
      <h1>🎵 Quantumelodic MVP</h1>
      <p class="tagline">Astronomical Music Generation</p>
    </div>

    <div class="content">
      <div class="card">
        <h2>Welcome to Quantumelodic</h2>
        <p>
          This is a music generation system that translates astronomical 
          phenomena into musical compositions using quantum-inspired algorithms.
        </p>
        
        <div class="features">
          <div class="feature">
            <h3>🌙 Ephemeris Engine</h3>
            <p>Calculate astronomical positions and events</p>
          </div>
          <div class="feature">
            <h3>🎼 Harmonic Engine</h3>
            <p>Map celestial data to musical harmony</p>
          </div>
          <div class="feature">
            <h3>🎹 MIDI Engine</h3>
            <p>Generate playable MIDI compositions</p>
          </div>
          <div class="feature">
            <h3>🤖 AI Music Engine</h3>
            <p>Intelligent music pattern generation</p>
          </div>
        </div>

        <div class="demo">
          <button @click="count++">
            Count is {{ count }}
          </button>
          <p class="note">
            Frontend is running! Connect this to the Python backend API.
          </p>
        </div>
      </div>
    </div>

    <div class="footer">
      <p>Built with Vue.js + Vite</p>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.header {
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 3rem;
  color: #42b883;
  margin-bottom: 0.5rem;
}

.tagline {
  font-size: 1.2rem;
  color: #666;
}

.content {
  margin-bottom: 3rem;
}

.card {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card h2 {
  color: #333;
  margin-bottom: 1rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.feature h3 {
  color: #42b883;
  margin-bottom: 0.5rem;
}

.feature p {
  color: #666;
  font-size: 0.9rem;
}

.demo {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #ddd;
}

button {
  background: #42b883;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #35495e;
}

.note {
  margin-top: 1rem;
  color: #666;
  font-style: italic;
}

.footer {
  color: #999;
  font-size: 0.9rem;
}
</style>
