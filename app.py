from flask import Flask, request, redirect
import os

app = Flask(__name__)

# TikTok in-app browser detection patterns (case-insensitive)
TIKTOK_UA_PATTERNS = [
    'tiktok', 'musical_ly', 'bytelocale', 'ttwebview',
    'bytedancewebview', 'jssdk', 'cronet'
]

INSTRUCTIONAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Continue to profile</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #ffffff;
            margin: 0;
            padding: 0;
            color: #000;
            text-align: center;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }
        .top-circle {
            position: absolute;
            top: -8px;
            right: 2px;
            width: 72px;
            height: 72px;
            background: #ff69b4;
            border-radius: 50%;
            z-index: 10;
            box-shadow: 0 1px 6px rgba(0,0,0,0.18);
            animation: pulse-circle 2.8s ease-in-out infinite;
        }
        @keyframes pulse-circle {
            0%, 100% { transform: scale(1); opacity: 0.94; }
            50%      { transform: scale(1.09); opacity: 1; }
        }
        .arrow-wrapper {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 11;
            animation: subtle-nudge 2.4s ease-in-out infinite alternate;
        }
        @keyframes subtle-nudge {
            0%   { transform: translate(0, 0) scale(1); }
            100% { transform: translate(5px, -5px) scale(1.05); }
        }
        .arrow {
            font-size: 44px;
            color: #000000;
            font-weight: bold;
            line-height: 1;
            transform: rotate(-69deg);
        }
        .content {
            position: relative;
            z-index: 3;
            padding: 96px 24px 40px;
            flex: 1;
        }
        h1 {
            font-size: 26px;
            font-weight: 700;
            margin: 0 0 30px;
            line-height: 1.32;
        }
        .steps {
            max-width: 380px;
            margin: 0 auto;
        }
        .step {
            display: flex;
            align-items: center;
            background: #fff0f5;
            border-radius: 999px;
            padding: 16px 20px;
            margin-bottom: 16px;
            text-align: left;
            font-size: 17px;
            font-weight: 600;
            box-shadow: 0 1px 6px rgba(0,0,0,0.07);
        }
        .step-icon {
            width: 48px;
            height: 48px;
            background: #ff69b4;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            margin-right: 16px;
            flex-shrink: 0;
        }
        .footer {
            padding: 20px 0 40px;
            color: #777;
            font-size: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .footer-logo {
            width: 18px;
            height: 18px;
            background: #6b46c1;
            color: white;
            font-size: 11px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="top-circle">
        <div class="arrow-wrapper">
            <div class="arrow">→</div>
        </div>
    </div>

    <div class="content">
        <h1>To access the link,<br>follow these 2 simple<br>steps:</h1>

        <div class="steps">
            <div class="step">
                <div class="step-icon">👆</div>
                Click the ... menu in the top right
            </div>
            <div class="step">
                <div class="step-icon">↗️</div>
                Select "Open in browser"
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="footer-logo">□</div>
        Powered by GetAllMyLinks
    </div>
</body>
</html>
"""

def is_tiktok_inapp(user_agent):
    if not user_agent:
        return False
    ua_lower = user_agent.lower()
    return any(pattern in ua_lower for pattern in TIKTOK_UA_PATTERNS)


# Root route - this is what people hit when they visit www.ffionamorgan.com directly
@app.route('/')
def root():
    user_agent = request.headers.get('User-Agent')
    if is_tiktok_inapp(user_agent):
        return INSTRUCTIONAL_HTML
    else:
        return redirect('https://link.me/ffionamorgan0')


# Keep the dynamic route in case you ever use other usernames
@app.route('/<username>')
def handle_request(username):
    user_agent = request.headers.get('User-Agent')
    if is_tiktok_inapp(user_agent):
        return INSTRUCTIONAL_HTML
    else:
        return redirect('https://link.me/ffionamorgan0')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
