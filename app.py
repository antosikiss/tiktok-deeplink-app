from flask import Flask, request, redirect
import os

app = Flask(__name__)

# TikTok in-app browser detection patterns (case-insensitive)
TIKTOK_UA_PATTERNS = [
    'tiktok', 'musical_ly', 'bytelocale', 'ttwebview',
    'bytedancewebview', 'jssdk', 'cronet'
]

FINAL_URL = 'https://link.me/ffionamorgan0'

INSTRUCTIONAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Exclusive Content</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;900&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Inter', sans-serif;
    background: #000;
    height: 100vh;
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 36px;
    overflow: hidden;
  }
  .headline {
    font-size: clamp(26px, 7vw, 36px);
    font-weight: 900;
    color: #fff;
    text-align: center;
    letter-spacing: -0.5px;
  }
  .sub {
    font-size: 15px;
    font-weight: 700;
    color: #666;
    text-align: center;
    margin-top: -24px;
  }
  .hold-wrapper {
    position: relative;
    width: 230px;
    height: 230px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .glow-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    animation: pulse 2.2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.08); opacity: 1; }
  }

  /* The real anchor — covers the entire button invisibly.
     TikTok sees a real <a target="_blank"> tap and shows "Open Link" */
  .real-link {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    z-index: 10;
    display: block;
    opacity: 0;
    pointer-events: none; /* disabled until hold completes */
  }

  .hold-btn {
    position: relative;
    width: 185px;
    height: 185px;
    border-radius: 50%;
    background: #fff;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
    touch-action: none;
    outline: none;
    box-shadow: 0 0 60px rgba(255,255,255,0.1), 0 16px 50px rgba(0,0,0,0.6);
    transition: transform 0.12s ease;
    flex-shrink: 0;
  }
  .hold-btn.pressing { transform: scale(0.96); }
  .progress-svg {
    position: absolute;
    inset: -10px;
    width: calc(100% + 20px);
    height: calc(100% + 20px);
    transform: rotate(-90deg);
    pointer-events: none;
  }
  .progress-track { fill: none; stroke: rgba(0,0,0,0.06); stroke-width: 5; }
  .progress-fill {
    fill: none;
    stroke: #000;
    stroke-width: 5;
    stroke-linecap: round;
    stroke-dasharray: 645;
    stroke-dashoffset: 645;
    transition: stroke-dashoffset 0.04s linear;
  }
  .fp { width: 88px; height: 88px; }
  .status {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #444;
    text-align: center;
    transition: color 0.3s;
    min-height: 16px;
  }
  .status.holding { color: #fff; }
  .status.done { color: #fff; }

  /* Big tap-here button that appears after hold completes */
  .tap-btn {
    display: none;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 18px 36px;
    background: #fff;
    color: #000;
    font-family: 'Inter', sans-serif;
    font-size: 17px;
    font-weight: 900;
    border-radius: 50px;
    text-decoration: none;
    letter-spacing: -0.3px;
    box-shadow: 0 0 40px rgba(255,255,255,0.15);
    animation: tapPulse 1s ease-in-out infinite;
  }
  .tap-btn.visible { display: flex; }
  @keyframes tapPulse {
    0%,100% { transform: scale(1); box-shadow: 0 0 30px rgba(255,255,255,0.15); }
    50%      { transform: scale(1.04); box-shadow: 0 0 50px rgba(255,255,255,0.3); }
  }

  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(0,0,0,0.08);
    pointer-events: none;
    animation: rip 0.55s ease-out forwards;
  }
  @keyframes rip {
    from { transform: scale(0); opacity: 1; }
    to { transform: scale(5); opacity: 0; }
  }
</style>
</head>
<body>
  <div class="headline">PRESS &amp; HOLD!</div>
  <div class="sub" id="subText">Hold to open the link</div>

  <div class="hold-wrapper" id="holdWrapper">
    <div class="glow-ring"></div>

    <!-- Hidden anchor that covers the button — TikTok treats this as a real tap -->
    <a id="realLink" class="real-link" href="https://link.me/ffionamorgan0" target="_blank" rel="noopener"></a>

    <button class="hold-btn" id="holdBtn">
      <svg class="progress-svg" viewBox="0 0 205 205">
        <circle class="progress-track" cx="102.5" cy="102.5" r="97.5"/>
        <circle class="progress-fill" id="progressFill" cx="102.5" cy="102.5" r="97.5"/>
      </svg>
      <svg class="fp" viewBox="0 0 80 80" fill="none">
        <path d="M40 6C24.54 6 12 18.54 12 34" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.22"/>
        <path d="M40 13C28.4 13 19 22.4 19 34c0 6.5 1.5 12.6 4.1 18" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.38"/>
        <path d="M40 20c-7.7 0-14 6.3-14 14 0 8.8 2.1 17.1 5.8 24.4" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.58"/>
        <path d="M40 27c-3.9 0-7 3.1-7 7 0 7.2 1.5 14 4.2 20.2" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.85"/>
        <path d="M40 27c3.9 0 7 3.1 7 7 0 7.2-1.5 14-4.2 20.2" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.85"/>
        <path d="M54 34c0-7.7-6.3-14-14-14" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.58"/>
        <path d="M61 34c0-11.6-9.4-21-21-21" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.38"/>
        <path d="M68 34C68 18.54 55.46 6 40 6" stroke="#111" stroke-width="4" stroke-linecap="round" opacity="0.22"/>
      </svg>
    </button>
  </div>

  <div class="status" id="status">Hold to unlock</div>

  <!-- Shown after hold — a real visible <a> tag they tap to trigger Open Link -->
  <a id="tapBtn" class="tap-btn" href="https://link.me/ffionamorgan0" target="_blank" rel="noopener">
    👆 Tap here to open
  </a>

<script>
  const holdBtn    = document.getElementById('holdBtn');
  const fill       = document.getElementById('progressFill');
  const status     = document.getElementById('status');
  const subText    = document.getElementById('subText');
  const realLink   = document.getElementById('realLink');
  const tapBtn     = document.getElementById('tapBtn');

  const DURATION = 1000;
  const R        = 97.5;
  const CIRCUMF  = 2 * Math.PI * R;

  fill.style.strokeDasharray  = CIRCUMF;
  fill.style.strokeDashoffset = CIRCUMF;

  let holding = false, startTime = null, raf = null, unlocked = false;

  function startHold(e) {
    e.preventDefault();
    if (unlocked) return;
    if (holding) return;
    holding   = true;
    startTime = performance.now();
    holdBtn.classList.add('pressing');
    status.textContent = 'Keep holding\u2026';
    status.className   = 'status holding';
    spawnRipple(e);
    animate();
  }

  function endHold() {
    if (!holding) return;
    holding = false;
    holdBtn.classList.remove('pressing');
    cancelAnimationFrame(raf);
    if (!unlocked) {
      fill.style.strokeDashoffset = CIRCUMF;
      status.textContent = 'Hold to unlock';
      status.className   = 'status';
    }
  }

  function animate() {
    if (!holding) return;
    const t = Math.min((performance.now() - startTime) / DURATION, 1);
    fill.style.strokeDashoffset = CIRCUMF * (1 - t);
    if (t >= 1) { unlock(); return; }
    raf = requestAnimationFrame(animate);
  }

  function unlock() {
    holding  = false;
    unlocked = true;
    holdBtn.classList.remove('pressing');

    // Update UI
    status.textContent = 'Now tap the button below \u2193';
    status.className   = 'status done';
    subText.textContent = 'Tap below to open in browser';

    // Show the big tap button — a real <a> tag TikTok will show "Open Link" for
    tapBtn.classList.add('visible');
  }

  function spawnRipple(e) {
    const rect = holdBtn.getBoundingClientRect();
    const cx = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
    const cy = (e.touches ? e.touches[0].clientY : e.clientY) - rect.top;
    const el = document.createElement('span');
    el.className = 'ripple';
    el.style.cssText = 'left:' + cx + 'px;top:' + cy + 'px;width:50px;height:50px;margin:-25px 0 0 -25px';
    holdBtn.appendChild(el);
    el.addEventListener('animationend', function() { el.remove(); });
  }

  holdBtn.addEventListener('mousedown',  startHold);
  holdBtn.addEventListener('touchstart', startHold, { passive: false });
  window.addEventListener('mouseup',    endHold);
  window.addEventListener('touchend',   endHold);
  window.addEventListener('touchcancel', endHold);
</script>
</body>
</html>
"""

def is_tiktok_inapp(user_agent):
    if not user_agent:
        return False
    ua_lower = user_agent.lower()
    return any(pattern in ua_lower for pattern in TIKTOK_UA_PATTERNS)


@app.route('/')
def root():
    user_agent = request.headers.get('User-Agent')
    if is_tiktok_inapp(user_agent):
        return INSTRUCTIONAL_HTML
    else:
        return redirect(FINAL_URL)


@app.route('/<username>')
def handle_request(username):
    user_agent = request.headers.get('User-Agent')
    if is_tiktok_inapp(user_agent):
        return INSTRUCTIONAL_HTML
    else:
        return redirect(FINAL_URL)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
