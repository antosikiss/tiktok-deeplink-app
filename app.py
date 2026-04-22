from flask import Flask, request, redirect
import os

app = Flask(__name__)

# TikTok in-app browser detection patterns (case-insensitive)
TIKTOK_UA_PATTERNS = [
    'tiktok', 'musical_ly', 'bytelocale', 'ttwebview',
    'bytedancewebview', 'jssdk', 'cronet'
]

FINAL_URL = 'https://link.boo/yenniwhi'

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
    -webkit-touch-callout: none;
  }

  .headline {
    font-size: clamp(26px, 7vw, 36px);
    font-weight: 900;
    color: #fff;
    text-align: center;
    letter-spacing: -0.5px;
    pointer-events: none;
  }
  .sub {
    font-size: 15px;
    font-weight: 700;
    color: #666;
    text-align: center;
    margin-top: -24px;
    pointer-events: none;
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
    pointer-events: none;
  }
  @keyframes pulse {
    0%,100% { transform: scale(1); opacity: 0.5; }
    50%      { transform: scale(1.08); opacity: 1; }
  }

  .hold-btn {
    position: relative;
    width: 185px;
    height: 185px;
    border-radius: 50%;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    flex-shrink: 0;
    box-shadow: 0 0 60px rgba(255,255,255,0.1), 0 16px 50px rgba(0,0,0,0.6);
    transition: transform 0.12s ease;
    -webkit-touch-callout: default;
    user-select: none;
    cursor: pointer;
  }
  .hold-btn:active { transform: scale(0.96); }

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

  .fp { width: 88px; height: 88px; pointer-events: none; }

  .status {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #444;
    text-align: center;
    transition: color 0.3s;
    min-height: 16px;
    pointer-events: none;
  }
  .status.holding { color: #fff; }

  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(0,0,0,0.08);
    pointer-events: none;
    animation: rip 0.55s ease-out forwards;
  }
  @keyframes rip {
    from { transform: scale(0); opacity: 1; }
    to   { transform: scale(5); opacity: 0; }
  }
</style>
</head>
<body>

  <div class="headline">PRESS &amp; HOLD!</div>
  <div class="sub" id="subText">Hold &amp; tap "Open Link"</div>

  <div class="hold-wrapper">
    <div class="glow-ring"></div>

    <a class="hold-btn"
       id="holdBtn"
       href="https://link.boo/yenniwhi"
       target="_blank"
       rel="noopener">

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
    </a>
  </div>

  <div class="status" id="status">Hold to unlock</div>

<script>
  var btn     = document.getElementById('holdBtn');
  var fill    = document.getElementById('progressFill');
  var status  = document.getElementById('status');
  var subText = document.getElementById('subText');

  var DURATION = 1000;
  var R        = 97.5;
  var CIRCUMF  = 2 * Math.PI * R;

  fill.style.strokeDasharray  = CIRCUMF;
  fill.style.strokeDashoffset = CIRCUMF;

  var isAndroid = /android/i.test(navigator.userAgent);
  var holding = false, startTime = null, raf = null;

  function startHold(e) {
    holding   = true;
    startTime = performance.now();
    btn.style.transform = 'scale(0.96)';
    status.textContent  = 'Keep holding\u2026';
    status.className    = 'status holding';
    spawnRipple(e);
    animate();
  }

  function endHold() {
    if (!holding) return;
    holding = false;
    btn.style.transform = '';
    cancelAnimationFrame(raf);
    fill.style.strokeDashoffset = CIRCUMF;
    status.textContent = 'Hold to unlock';
    status.className   = 'status';
  }

  function animate() {
    if (!holding) return;
    var t = Math.min((performance.now() - startTime) / DURATION, 1);
    fill.style.strokeDashoffset = CIRCUMF * (1 - t);
    if (t >= 1) {
      holding = false;
      btn.style.transform = '';
      unlock();
      return;
    }
    raf = requestAnimationFrame(animate);
  }

  function unlock() {
    if (isAndroid) {
      status.textContent = 'Opening in browser\u2026';
      status.className   = 'status holding';
      window.location.href = 'intent://link.boo/yenniwhi#Intent;scheme=https;package=com.android.chrome;end';
    } else {
      status.textContent = 'Tap "Open Link" \u2191';
      status.className   = 'status holding';
    }
  }

  function spawnRipple(e) {
    var rect = btn.getBoundingClientRect();
    var cx = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
    var cy = (e.touches ? e.touches[0].clientY : e.clientY) - rect.top;
    var el = document.createElement('span');
    el.className = 'ripple';
    el.style.cssText = 'left:' + cx + 'px;top:' + cy + 'px;width:50px;height:50px;margin:-25px 0 0 -25px';
    btn.appendChild(el);
    el.addEventListener('animationend', function() { el.remove(); });
  }

  btn.addEventListener('touchstart', startHold, { passive: true });
  btn.addEventListener('mousedown',  startHold);
  window.addEventListener('touchend',    endHold);
  window.addEventListener('touchcancel', endHold);
  window.addEventListener('mouseup',     endHold);
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
