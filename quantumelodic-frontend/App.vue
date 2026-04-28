<script setup>
import { ref, reactive } from 'vue'

// ── App state ──────────────────────────────────────────────────────────────
const STEP = { FORM: 'form', LOADING: 'loading', REPORT: 'report', UPGRADE: 'upgrade' }
const step = ref(STEP.FORM)
const errorMsg = ref('')

// ── Form data ──────────────────────────────────────────────────────────────
const form = reactive({
  date: '',
  time: '',
  lat: '',
  lon: '',
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC',
})

// ── Report data (returned from /api/report) ────────────────────────────────
const reportData = ref(null)

// ── Premium upsell state ───────────────────────────────────────────────────
const PRICE_USD = '9.99'
const premiumLoading = ref(false)
const premiumError = ref('')

// ── Helpers ────────────────────────────────────────────────────────────────
const ELEMENT_EMOJI = { Fire: '🔥', Water: '💧', Air: '🌬️', Earth: '🌿' }
const ELEMENT_COLOR = {
  Fire:  '#e25822',
  Water: '#1a73e8',
  Air:   '#7cb9e8',
  Earth: '#4caf50',
}

function elementEmoji(el) { return ELEMENT_EMOJI[el] || '✨' }
function elementColor(el) { return ELEMENT_COLOR[el] || '#7c5cbf' }

// ── Submit birth-data form → free report ──────────────────────────────────
async function generateReport() {
  errorMsg.value = ''
  if (!form.date || !form.time || !form.lat || !form.lon || !form.timezone) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }
  step.value = STEP.LOADING
  try {
    const res = await fetch('/api/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: form.date,
        time: form.time,
        lat: parseFloat(form.lat),
        lon: parseFloat(form.lon),
        timezone: form.timezone,
      }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Report generation failed')
    reportData.value = data
    step.value = STEP.REPORT
  } catch (err) {
    errorMsg.value = err.message
    step.value = STEP.FORM
  }
}

// ── Reset to form ──────────────────────────────────────────────────────────
function resetForm() {
  reportData.value = null
  premiumError.value = ''
  step.value = STEP.FORM
}

// ── Premium checkout (opens Stripe-style payment link) ────────────────────
async function startPremiumCheckout() {
  premiumLoading.value = true
  premiumError.value = ''
  // In production: call your backend to create a Stripe Checkout Session and
  // redirect to session.url.  For the MVP we show a placeholder alert.
  await new Promise(r => setTimeout(r, 600))
  premiumLoading.value = false
  step.value = STEP.UPGRADE
}

function closePremiumModal() {
  step.value = STEP.REPORT
}
</script>

<template>
  <div class="app">
    <!-- ════════════════ HEADER ════════════════ -->
    <header class="site-header">
      <div class="header-inner">
        <span class="logo">🎵 Quantumelodic</span>
        <span class="tagline">Astronomical Music Generation</span>
      </div>
    </header>

    <!-- ════════════════ HERO / FORM ════════════════ -->
    <main class="main">
      <!-- ── Birth-data form ── -->
      <section v-if="step === 'form'" class="card form-card">
        <h1 class="card-title">Generate Your Quantumelodic Report</h1>
        <p class="card-subtitle">
          Enter your birth details below — <strong>no account required.</strong>
          Your personal astronomical chart and harmonic analysis are&nbsp;<em>free</em>.
        </p>

        <form class="birth-form" @submit.prevent="generateReport">
          <div class="form-row">
            <label class="field">
              <span>Birth Date</span>
              <input v-model="form.date" type="date" required />
            </label>
            <label class="field">
              <span>Birth Time <small>(24h)</small></span>
              <input v-model="form.time" type="time" required />
            </label>
          </div>

          <div class="form-row">
            <label class="field">
              <span>Latitude</span>
              <input v-model="form.lat" type="number" step="0.0001" placeholder="e.g. 34.0522" required />
            </label>
            <label class="field">
              <span>Longitude</span>
              <input v-model="form.lon" type="number" step="0.0001" placeholder="e.g. -118.2437" required />
            </label>
          </div>

          <label class="field full-width">
            <span>Timezone</span>
            <input v-model="form.timezone" type="text" placeholder="e.g. America/Los_Angeles" required />
          </label>

          <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

          <button class="btn btn-primary" type="submit">
            🌟 Generate My Free Report
          </button>
        </form>

        <!-- How it works -->
        <div class="features">
          <div class="feature-item">
            <span class="feat-icon">🌙</span>
            <strong>Ephemeris Engine</strong>
            <p>Precise planetary positions for your birth moment</p>
          </div>
          <div class="feature-item">
            <span class="feat-icon">🎼</span>
            <strong>Harmonic Analysis</strong>
            <p>Map celestial patterns to musical modes</p>
          </div>
          <div class="feature-item">
            <span class="feat-icon">🎹</span>
            <strong>Premium: Song Generation</strong>
            <p>AI-composed audio uniquely tuned to your chart</p>
          </div>
        </div>
      </section>

      <!-- ── Loading spinner ── -->
      <section v-else-if="step === 'loading'" class="card loading-card">
        <div class="spinner"></div>
        <p>Calculating your celestial chart…</p>
      </section>

      <!-- ── Free Report ── -->
      <section v-else-if="step === 'report'" class="report-wrapper">

        <!-- Big sign headline -->
        <div class="report-headline">
          <span class="big-element-badge"
            :style="{ background: elementColor(reportData.harmonic?.dominant_element) }">
            {{ elementEmoji(reportData.harmonic?.dominant_element) }}
            {{ reportData.harmonic?.dominant_element }}
          </span>
          <div class="big-signs">
            <div class="sign-pill">☀️ Sun · {{ reportData.sun_sign }}</div>
            <div class="sign-pill">🌙 Moon · {{ reportData.moon_sign }}</div>
            <div class="sign-pill">⬆️ Rising · {{ reportData.rising_sign }}</div>
          </div>
        </div>

        <div class="report-grid">

          <!-- Planets -->
          <div class="card report-card">
            <h2>🪐 Planets</h2>
            <ul class="planet-list">
              <li v-for="p in reportData.report?.planets" :key="p.name">
                <span class="planet-name">{{ p.name }}</span>
                <span class="planet-detail">{{ p.sign }} · House {{ p.house || '—' }}</span>
              </li>
            </ul>
          </div>

          <!-- Aspects -->
          <div class="card report-card">
            <h2>🔗 Aspects</h2>
            <ul class="aspect-list" v-if="reportData.report?.aspects?.length">
              <li v-for="a in reportData.report.aspects" :key="a.p1+a.p2">
                <span class="aspect-body">{{ a.p1 }} <em>{{ a.aspect }}</em> {{ a.p2 }}</span>
                <span class="aspect-orb">{{ a.angle }}°</span>
              </li>
            </ul>
            <p v-else class="muted">No major aspects detected.</p>
          </div>

          <!-- Harmonic analysis -->
          <div class="card report-card harmonic-card">
            <h2>🎵 Harmonic Analysis</h2>
            <div class="harmonic-grid">
              <div class="h-item">
                <span class="h-label">Pentatonic Mode</span>
                <span class="h-value">{{ reportData.harmonic?.primary_pentatonic_mode }}</span>
              </div>
              <div class="h-item">
                <span class="h-label">Quadratonic Mode</span>
                <span class="h-value">{{ reportData.harmonic?.primary_quadratonic_mode }}</span>
              </div>
              <div class="h-item">
                <span class="h-label">Tension Index</span>
                <span class="h-value">{{ reportData.harmonic?.harmonic_tension_index }}&thinsp;/&thinsp;100</span>
              </div>
              <div class="h-item">
                <span class="h-label">Suggested Tempo</span>
                <span class="h-value">{{ reportData.harmonic?.sonic_payload?.recommended_tempo_bpm }}&thinsp;BPM</span>
              </div>
              <div class="h-item">
                <span class="h-label">Waveform</span>
                <span class="h-value">{{ reportData.harmonic?.sonic_payload?.waveform }}</span>
              </div>
              <div class="h-item">
                <span class="h-label">Timbres</span>
                <span class="h-value">{{ (reportData.harmonic?.sonic_payload?.timbres || []).join(', ') }}</span>
              </div>
            </div>
          </div>

          <!-- Insights -->
          <div class="card report-card">
            <h2>🔍 Insights</h2>
            <div class="insights">
              <p><strong>Dominant element:</strong> {{ reportData.report?.insights?.dominant_element }}</p>
              <p><strong>Dominant sign:</strong> {{ reportData.report?.insights?.dominant_sign }}</p>
              <template v-if="reportData.report?.insights?.grand_trines?.length">
                <p v-for="gt in reportData.report.insights.grand_trines" :key="gt">
                  ✨ Grand Trine: {{ Array.isArray(gt) ? gt.join(', ') : gt }}
                </p>
              </template>
              <template v-if="reportData.report?.insights?.t_squares?.length">
                <p v-for="ts in reportData.report.insights.t_squares" :key="ts.apex">
                  ⚡ T-Square apex {{ ts.apex }}
                </p>
              </template>
            </div>
          </div>
        </div>

        <!-- ── Premium upsell banner ── -->
        <div class="upsell-banner">
          <div class="upsell-text">
            <h2>🎶 Turn Your Chart into Music</h2>
            <p>
              Unlock a fully personalized AI-generated composition scored directly
              from your natal chart — unique tempo, mode, instrumentation, and a
              Suno-ready prompt tuned to your {{ reportData.harmonic?.dominant_element }} energy.
            </p>
            <ul class="upsell-features">
              <li>🎼 Suno AI-ready music prompt</li>
              <li>🎹 Stable Audio structured payload</li>
              <li>🎧 Instrument recommendations</li>
              <li>📄 Full arrangement blueprint</li>
            </ul>
          </div>
          <div class="upsell-cta">
            <div class="price-tag">${{ PRICE_USD }}<span> one-time</span></div>
            <button class="btn btn-upgrade" @click="startPremiumCheckout" :disabled="premiumLoading">
              {{ premiumLoading ? '⏳ Loading…' : '🎵 Get My Song' }}
            </button>
            <p class="upsell-note">No account needed · Instant delivery</p>
          </div>
        </div>

        <div class="report-actions">
          <button class="btn btn-secondary" @click="resetForm">← New Report</button>
        </div>
      </section>

      <!-- ── Premium / Upgrade modal placeholder ── -->
      <section v-else-if="step === 'upgrade'" class="card upgrade-card">
        <h2>🎉 Premium Song Generation</h2>
        <p class="upgrade-sub">
          In production this page completes your Stripe checkout and delivers
          your personalized music prompt and composition blueprint.
        </p>
        <div class="upgrade-preview">
          <h3>Your AI Music Prompt (preview)</h3>
          <p class="muted upgrade-preview-note">
            Complete payment to unlock the full prompt and all composition assets.
          </p>
          <div class="prompt-preview-box">
            <p>Title: <em>{{ reportData?.harmonic?.primary_pentatonic_mode }} — {{ reportData?.harmonic?.dominant_element }} Piece</em></p>
            <p>Tempo: <em>{{ reportData?.harmonic?.sonic_payload?.recommended_tempo_bpm }} BPM</em></p>
            <p>Waveform: <em>{{ reportData?.harmonic?.sonic_payload?.waveform }}</em></p>
            <p class="blurred">The rest of your prompt is revealed after payment…</p>
          </div>
        </div>
        <div class="upgrade-actions">
          <a class="btn btn-upgrade"
             href="https://buy.stripe.com/placeholder"
             target="_blank" rel="noopener noreferrer">
            💳 Complete Payment on Stripe
          </a>
          <button class="btn btn-secondary" @click="closePremiumModal">← Back to Report</button>
        </div>
      </section>
    </main>

    <!-- ════════════════ FOOTER ════════════════ -->
    <footer class="site-footer">
      <p>© 2026 Quantumelodic · No account required · Powered by Vue&nbsp;+&nbsp;Python</p>
    </footer>
  </div>
</template>

<style scoped>
/* ── Reset / base ── */
*, *::before, *::after { box-sizing: border-box; }

/* ── Layout ── */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0d0d1a 0%, #1a1040 100%);
  color: #e8e0ff;
  font-family: 'Inter', system-ui, sans-serif;
}

/* ── Header ── */
.site-header {
  background: rgba(255,255,255,0.04);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  padding: 1rem 2rem;
}
.header-inner {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.logo {
  font-size: 1.4rem;
  font-weight: 700;
  color: #b89eff;
  letter-spacing: 0.02em;
}
.tagline {
  font-size: 0.9rem;
  color: #8a7ab8;
}

/* ── Main ── */
.main {
  flex: 1;
  padding: 2.5rem 1.5rem;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

/* ── Card ── */
.card {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 1.5rem;
}

/* ── Form ── */
.form-card { max-width: 700px; margin: 0 auto 1.5rem; }
.card-title { font-size: 1.8rem; font-weight: 700; color: #c9b8ff; margin-bottom: 0.5rem; text-align: center; }
.card-subtitle { color: #9d8ec7; margin-bottom: 2rem; text-align: center; line-height: 1.6; }

.birth-form { display: flex; flex-direction: column; gap: 1rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.field span {
  font-size: 0.85rem;
  color: #a094c8;
  font-weight: 500;
}
.field input {
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  padding: 0.65rem 0.9rem;
  color: #e8e0ff;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}
.field input:focus { border-color: #9b74f7; }
.field input::placeholder { color: #5a4f7a; }
.full-width { grid-column: 1 / -1; }

/* ── Buttons ── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.75rem 1.8rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}
.btn:active { transform: scale(0.97); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-primary {
  background: linear-gradient(135deg, #7c4dff, #b06cff);
  color: #fff;
  margin-top: 0.5rem;
  width: 100%;
  font-size: 1.05rem;
  padding: 0.9rem;
}
.btn-primary:hover:not(:disabled) { opacity: 0.88; }

.btn-upgrade {
  background: linear-gradient(135deg, #e25822, #ff8c42);
  color: #fff;
  min-width: 200px;
}
.btn-upgrade:hover:not(:disabled) { opacity: 0.88; }

.btn-secondary {
  background: rgba(255,255,255,0.08);
  color: #c9b8ff;
  border: 1px solid rgba(255,255,255,0.15);
}
.btn-secondary:hover { background: rgba(255,255,255,0.14); }

/* ── Error ── */
.error-msg {
  color: #ff7070;
  font-size: 0.9rem;
  margin: 0;
}

/* ── Features grid ── */
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-top: 2.5rem;
}
.feature-item {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 1.2rem;
  text-align: center;
}
.feat-icon { font-size: 1.8rem; display: block; margin-bottom: 0.4rem; }
.feature-item strong { font-size: 0.9rem; color: #c9b8ff; }
.feature-item p { font-size: 0.8rem; color: #8a7ab8; margin-top: 0.3rem; }

/* ── Loading ── */
.loading-card { text-align: center; padding: 4rem; max-width: 400px; margin: 0 auto; }
.spinner {
  width: 50px; height: 50px;
  border: 4px solid rgba(255,255,255,0.1);
  border-top-color: #9b74f7;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1.5rem;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Report headline ── */
.report-headline {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.big-element-badge {
  font-size: 1.3rem;
  font-weight: 700;
  padding: 0.5rem 1.2rem;
  border-radius: 50px;
  color: #fff;
}
.big-signs { display: flex; flex-wrap: wrap; gap: 0.6rem; }
.sign-pill {
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.13);
  border-radius: 50px;
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  color: #c9b8ff;
}

/* ── Report grid ── */
.report-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
@media (max-width: 640px) { .report-grid { grid-template-columns: 1fr; } }

.report-card { margin-bottom: 0; }
.report-card h2 { font-size: 1rem; color: #b89eff; margin-bottom: 1rem; }

/* Planet list */
.planet-list, .aspect-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.4rem; }
.planet-list li, .aspect-list li { display: flex; justify-content: space-between; align-items: center; font-size: 0.87rem; }
.planet-name { color: #c9b8ff; font-weight: 500; }
.planet-detail { color: #8a7ab8; }
.aspect-body { color: #c9b8ff; }
.aspect-body em { color: #b06cff; font-style: normal; }
.aspect-orb { color: #8a7ab8; font-size: 0.8rem; }

/* Harmonic card */
.harmonic-card { grid-column: 1 / -1; }
.harmonic-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.8rem; }
.h-item { background: rgba(255,255,255,0.04); border-radius: 10px; padding: 0.8rem; }
.h-label { display: block; font-size: 0.75rem; color: #8a7ab8; margin-bottom: 0.2rem; }
.h-value { display: block; font-size: 1rem; color: #c9b8ff; font-weight: 600; }

/* Insights */
.insights { display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.88rem; }
.muted { color: #7a6fa0; font-style: italic; }

/* ── Upsell banner ── */
.upsell-banner {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
  background: linear-gradient(135deg, rgba(226,88,34,0.15), rgba(255,140,66,0.10));
  border: 1px solid rgba(226,88,34,0.3);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 1.5rem;
}
.upsell-text { flex: 1; min-width: 260px; }
.upsell-text h2 { font-size: 1.4rem; color: #ffb380; margin-bottom: 0.6rem; }
.upsell-text p { color: #c9a880; line-height: 1.6; margin-bottom: 1rem; font-size: 0.95rem; }
.upsell-features { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.3rem; color: #d4b890; font-size: 0.9rem; }
.upsell-cta { display: flex; flex-direction: column; align-items: center; gap: 0.8rem; text-align: center; }
.price-tag { font-size: 2.5rem; font-weight: 800; color: #ffb380; }
.price-tag span { font-size: 1rem; font-weight: 400; color: #c9a880; }
.upsell-note { font-size: 0.78rem; color: #9d7a58; }

/* ── Report actions ── */
.report-actions { display: flex; justify-content: flex-start; margin-top: 1rem; }

/* ── Upgrade card ── */
.upgrade-card { max-width: 680px; margin: 0 auto; text-align: center; }
.upgrade-card h2 { font-size: 1.8rem; color: #c9b8ff; margin-bottom: 0.5rem; }
.upgrade-sub { color: #9d8ec7; margin-bottom: 2rem; }
.upgrade-preview { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; text-align: left; }
.upgrade-preview h3 { color: #b89eff; margin-bottom: 1rem; }
.upgrade-preview-note { color: #7a6fa0; font-size: 0.85rem; margin-bottom: 1rem; }
.prompt-preview-box { display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.9rem; }
.prompt-preview-box p { margin: 0; color: #c9b8ff; }
.prompt-preview-box em { color: #b06cff; font-style: normal; }
.blurred { filter: blur(4px); user-select: none; color: #8a7ab8; }
.upgrade-actions { display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; }

/* ── Footer ── */
.site-footer {
  text-align: center;
  padding: 1.5rem;
  color: #5a4f7a;
  font-size: 0.82rem;
  border-top: 1px solid rgba(255,255,255,0.05);
}
</style>
