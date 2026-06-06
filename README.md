<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CampusOS AI</title>
<script src="https://js.puter.com/v2/"></script>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #06080f;--bg2: #0d1017;--bg3: #141820;--bg4: #1c2130;
  --border: #1f2840;--border2: #2d3a5a;
  --text: #dde4f5;--text2: #8a96b8;--text3: #445070;
  --accent: #3d7fff;--accent2: #6e44ff;
  --green: #18e0a0;--amber: #f0a030;--red: #ef4545;--pink: #e060c0;
  --glow: rgba(61,127,255,0.12);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");opacity:0.025;pointer-events:none;z-index:9999}

/* HEADER */
header{padding:0 36px;height:60px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;background:rgba(6,8,15,0.9);position:sticky;top:0;z-index:100;backdrop-filter:blur(20px)}
.logo{display:flex;align-items:center;gap:12px}
.logo-icon{width:34px;height:34px;background:linear-gradient(135deg,var(--accent),var(--accent2));border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 0 20px rgba(61,127,255,0.3)}
.logo-text{font-family:'Syne',sans-serif;font-size:17px;font-weight:800;letter-spacing:-0.5px}
.logo-text span{color:var(--accent)}
.header-right{display:flex;align-items:center;gap:12px}
.live-dot{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--green);font-weight:600;letter-spacing:0.5px}
.live-dot::before{content:'';width:6px;height:6px;background:var(--green);border-radius:50%;animation:livepulse 1.5s ease infinite}
@keyframes livepulse{0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(24,224,160,0.4)}50%{opacity:0.7;box-shadow:0 0 0 5px rgba(24,224,160,0)}}
.model-tag{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text3);background:var(--bg3);border:1px solid var(--border);padding:4px 10px;border-radius:4px}
.free-badge{font-size:10px;font-weight:700;padding:3px 8px;border-radius:4px;background:rgba(24,224,160,0.12);color:var(--green);border:1px solid rgba(24,224,160,0.25);letter-spacing:.4px}

/* NAV */
.nav{padding:0 36px;background:var(--bg2);border-bottom:1px solid var(--border);display:flex;gap:0;overflow-x:auto}
.nav::-webkit-scrollbar{height:0}
.nav-tab{padding:0 18px;height:44px;font-size:12px;font-weight:600;color:var(--text3);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap;transition:all .2s;display:flex;align-items:center;gap:7px;letter-spacing:0.3px;text-transform:uppercase}
.nav-tab:hover{color:var(--text2)}
.nav-tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.nav-count{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:4px;font-size:9px;font-weight:700;background:rgba(61,127,255,0.2);color:var(--accent)}

/* MAIN */
main{max-width:1240px;margin:0 auto;padding:32px 36px}
.view{display:none}
.view.active{display:block;animation:fadeIn .25s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

/* CARDS */
.card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:24px}
.card-title{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:20px;display:flex;align-items:center;gap:8px}
.card-title-accent{width:3px;height:12px;background:linear-gradient(to bottom,var(--accent),var(--accent2));border-radius:2px}

/* FORM */
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.form-group{display:flex;flex-direction:column;gap:6px}
.form-group.full{grid-column:1/-1}
label{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.8px}
input,select,textarea{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:11px 14px;color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;transition:all .2s;width:100%}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--glow)}
textarea{resize:vertical;min-height:110px;line-height:1.6}
select option{background:var(--bg3)}

/* PILLS */
.pill{font-size:11px;padding:5px 11px;background:var(--bg3);border:1px solid var(--border);border-radius:20px;cursor:pointer;color:var(--text2);transition:all .15s;display:inline-flex;align-items:center;gap:4px}
.pill:hover{border-color:var(--accent);color:var(--accent);background:var(--glow)}

/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:7px;padding:11px 22px;border-radius:8px;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s;border:none;letter-spacing:0.2px}
.btn-primary{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;box-shadow:0 4px 20px rgba(61,127,255,0.25)}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 8px 30px rgba(61,127,255,0.35)}
.btn-primary:active{transform:translateY(0)}
.btn-primary:disabled{opacity:0.45;transform:none;cursor:not-allowed}
.btn-secondary{background:var(--bg3);color:var(--text2);border:1px solid var(--border)}
.btn-secondary:hover{border-color:var(--border2);color:var(--text)}
.btn-sm{padding:7px 14px;font-size:11px;border-radius:6px}
.btn-success{background:rgba(24,224,160,0.12);color:var(--green);border:1px solid rgba(24,224,160,0.25)}
.btn-success:hover{background:rgba(24,224,160,0.22)}
.btn-warn{background:rgba(240,160,48,0.12);color:var(--amber);border:1px solid rgba(240,160,48,0.25)}
.btn-warn:hover{background:rgba(240,160,48,0.22)}
.btn-danger{background:rgba(239,69,69,0.12);color:var(--red);border:1px solid rgba(239,69,69,0.25)}
.btn-danger:hover{background:rgba(239,69,69,0.22)}

/* BADGES */
.badge{display:inline-flex;align-items:center;padding:3px 9px;border-radius:20px;font-size:10px;font-weight:700;letter-spacing:0.4px}
.badge-high{background:rgba(239,69,69,0.1);color:var(--red);border:1px solid rgba(239,69,69,0.2)}
.badge-medium{background:rgba(240,160,48,0.1);color:var(--amber);border:1px solid rgba(240,160,48,0.2)}
.badge-low{background:rgba(24,224,160,0.1);color:var(--green);border:1px solid rgba(24,224,160,0.2)}
.badge-pending{background:rgba(61,127,255,0.1);color:var(--accent);border:1px solid rgba(61,127,255,0.2)}
.badge-resolved{background:rgba(24,224,160,0.1);color:var(--green);border:1px solid rgba(24,224,160,0.2)}
.badge-in-progress{background:rgba(110,68,255,0.1);color:var(--accent2);border:1px solid rgba(110,68,255,0.2)}

/* AI RESULT */
.ai-result{display:none;margin-top:20px;border:1px solid var(--border);border-radius:14px;overflow:hidden}
.ai-result.show{display:block;animation:slideUp .35s ease}
@keyframes slideUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.ai-header{background:linear-gradient(135deg,rgba(61,127,255,0.1),rgba(110,68,255,0.07));border-bottom:1px solid var(--border);padding:14px 18px;display:flex;align-items:center;gap:10px}
.ai-fields{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--border)}
.ai-field{background:var(--bg3);padding:14px 18px}
.ai-label{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:0.6px;margin-bottom:5px;font-weight:700}
.ai-value{font-size:15px;font-weight:600;color:var(--text)}
.priority-high{color:var(--red)}
.priority-medium{color:var(--amber)}
.priority-low{color:var(--green)}
.ai-summary{padding:14px 18px;border-top:1px solid var(--border);background:var(--bg2)}

/* TICKET BOX */
.ticket-box{display:none;margin-top:20px;background:linear-gradient(135deg,rgba(61,127,255,0.07),rgba(110,68,255,0.05));border:1px solid var(--border2);border-radius:14px;padding:28px;text-align:center}
.ticket-box.show{display:block;animation:popIn .5s cubic-bezier(0.34,1.56,0.64,1)}
@keyframes popIn{from{opacity:0;transform:scale(0.85)}to{opacity:1;transform:scale(1)}}
.ticket-id{font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:600;color:var(--accent);letter-spacing:3px;margin:8px 0}
.ticket-status{display:inline-flex;align-items:center;gap:7px;background:rgba(24,224,160,0.1);color:var(--green);border:1px solid rgba(24,224,160,0.25);padding:6px 14px;border-radius:20px;font-size:12px;font-weight:700}

/* DASHBOARD STATS */
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px}
.stat-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:20px;position:relative;overflow:hidden}
.stat-glow{position:absolute;inset:0;opacity:0.04;pointer-events:none}
.stat-num{font-family:'Syne',sans-serif;font-size:36px;font-weight:800;line-height:1;margin:8px 0 4px}
.stat-label{font-size:11px;color:var(--text3);font-weight:600;text-transform:uppercase;letter-spacing:0.5px}

/* TABLE */
.table-wrap{overflow-x:auto;border-radius:10px;border:1px solid var(--border)}
table{width:100%;border-collapse:collapse;font-size:12px}
th{padding:10px 14px;text-align:left;font-size:9px;text-transform:uppercase;letter-spacing:0.8px;color:var(--text3);background:var(--bg3);font-weight:700;border-bottom:1px solid var(--border)}
td{padding:12px 14px;border-bottom:1px solid var(--border);color:var(--text2)}
tr:last-child td{border-bottom:none}
tr:hover td{background:rgba(61,127,255,0.03)}

/* CHARTS */
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.chart-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:20px}
.chart-title{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:16px}
.bar-chart{display:flex;flex-direction:column;gap:10px}
.bar-row{display:flex;align-items:center;gap:10px}
.bar-label{font-size:11px;color:var(--text3);width:110px;text-align:right;flex-shrink:0}
.bar-track{flex:1;height:6px;background:var(--bg4);border-radius:3px;overflow:hidden}
.bar-fill{height:100%;border-radius:3px;transition:width 1s ease}
.bar-val{font-size:11px;font-weight:700;color:var(--text2);width:24px;text-align:right;flex-shrink:0}
.pie-visual{display:flex;align-items:center;gap:24px}
.pie-svg{width:110px;height:110px;flex-shrink:0}
.pie-legend{display:flex;flex-direction:column;gap:8px}
.pie-item{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text2)}
.pie-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}

/* POLICY CHAT */
.chat-container{display:flex;flex-direction:column;gap:14px;margin-bottom:16px;max-height:400px;overflow-y:auto;padding-right:4px}
.chat-container::-webkit-scrollbar{width:3px}
.chat-container::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}
.chat-msg{display:flex;gap:10px;align-items:flex-start}
.chat-msg.user{flex-direction:row-reverse}
.chat-avatar{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0}
.chat-avatar.ai{background:linear-gradient(135deg,var(--accent),var(--accent2))}
.chat-avatar.user{background:var(--bg4);border:1px solid var(--border2)}
.chat-bubble{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:12px 15px;font-size:13px;line-height:1.65;max-width:500px;color:var(--text)}
.chat-msg.user .chat-bubble{background:linear-gradient(135deg,rgba(61,127,255,0.12),rgba(110,68,255,0.08));border-color:rgba(61,127,255,0.25)}
.chat-input-row{display:flex;gap:10px}
.chat-input-row input{flex:1}

/* TRACKER */
.tracker-hero{text-align:center;padding:48px 20px;margin-bottom:24px;background:linear-gradient(135deg,rgba(61,127,255,0.05),rgba(110,68,255,0.03));border:1px solid var(--border);border-radius:14px}
.tracker-hero h2{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;margin-bottom:8px}
.tracker-hero p{font-size:13px;color:var(--text3);margin-bottom:24px}
.tracker-input-row{display:flex;gap:10px;max-width:420px;margin:0 auto}

/* TIMELINE */
.timeline{display:flex;flex-direction:column;gap:0}
.timeline-item{display:flex;gap:14px;position:relative}
.timeline-item:not(:last-child)::after{content:'';position:absolute;left:14px;top:30px;width:1px;bottom:-8px;background:var(--border)}
.timeline-dot{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;position:relative;z-index:1}
.timeline-dot.done{background:rgba(24,224,160,0.12);border:2px solid var(--green)}
.timeline-dot.active{background:rgba(61,127,255,0.12);border:2px solid var(--accent);animation:ringPulse 2s infinite}
.timeline-dot.pending{background:var(--bg3);border:1px solid var(--border)}
@keyframes ringPulse{0%,100%{box-shadow:0 0 0 0 rgba(61,127,255,0.4)}50%{box-shadow:0 0 0 7px rgba(61,127,255,0)}}
.timeline-content{padding:4px 0 20px}
.timeline-title{font-size:13px;font-weight:600;margin-bottom:2px}
.timeline-note{font-size:12px;color:var(--text3);line-height:1.5}

/* TICKET DETAIL */
.ticket-detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);border-radius:10px;overflow:hidden;margin-bottom:18px}
.ticket-detail-field{background:var(--bg3);padding:14px 18px}
.ticket-detail-label{font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:0.7px;margin-bottom:5px;font-weight:700}
.ticket-detail-value{font-size:14px;font-weight:600}

/* ADMIN */
.admin-login{max-width:420px;margin:56px auto 0}
.admin-ticket-card{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:10px;transition:border-color .2s}
.admin-ticket-card:hover{border-color:var(--border2)}
.admin-ticket-top{display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.admin-ticket-complaint{font-size:13px;color:var(--text2);line-height:1.5;margin-bottom:10px}
.admin-ticket-actions{display:flex;gap:7px;flex-wrap:wrap}
.admin-stat-bar{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}
.admin-stat-mini{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center}
.admin-stat-mini-num{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;margin-bottom:2px}
.admin-stat-mini-label{font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:0.6px;font-weight:700}

/* POLICY CARDS */
.policy-card{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:14px;margin-bottom:10px}
.policy-card-title{font-size:12px;font-weight:700;color:var(--text);margin-bottom:6px}
.policy-card-body{font-size:12px;color:var(--text3);line-height:1.6}

/* LOADING */
.dot-pulse{display:inline-flex;gap:4px;align-items:center}
.dot-pulse span{width:5px;height:5px;background:var(--accent);border-radius:50%;animation:dp 1.2s ease-in-out infinite}
.dot-pulse span:nth-child(2){animation-delay:.2s}
.dot-pulse span:nth-child(3){animation-delay:.4s}
@keyframes dp{0%,80%,100%{transform:scale(.5);opacity:.3}40%{transform:scale(1);opacity:1}}

/* ARCH */
.arch{display:flex;flex-direction:column;align-items:center;gap:0;padding:16px 0}
.arch-node{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:9px 20px;font-size:12px;font-weight:600;color:var(--text2);text-align:center;min-width:150px}
.arch-node.hl{border-color:var(--accent);color:var(--accent);background:rgba(61,127,255,0.07)}
.arch-arrow{width:1px;height:24px;background:var(--border2);margin:0 auto;position:relative}
.arch-arrow::after{content:'▼';position:absolute;bottom:-9px;left:50%;transform:translateX(-50%);font-size:7px;color:var(--text3)}
.arch-branches{display:flex;gap:12px;justify-content:center}
.arch-branch-wrap{display:flex;flex-direction:column;align-items:center}

/* MISC */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.section-sub{font-size:13px;color:var(--text3);margin-bottom:18px;line-height:1.6}
.empty-state{text-align:center;padding:56px 24px;color:var(--text3)}
.empty-state-icon{font-size:44px;margin-bottom:14px;opacity:0.5}
.empty-state h3{font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:var(--text2);margin-bottom:6px}
.empty-state p{font-size:13px;line-height:1.6}
.lang-tag{font-size:10px;padding:2px 8px;border-radius:4px;background:rgba(224,96,192,0.1);color:var(--pink);border:1px solid rgba(224,96,192,0.2);font-weight:700;letter-spacing:0.4px}
.update-log{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:8px 12px;font-size:11px;color:var(--green);margin-top:8px;display:none;font-family:'JetBrains Mono',monospace}
.ai-badge-tag{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;padding:3px 8px;border-radius:4px;letter-spacing:0.5px}

/* Puter login overlay */
#puter-overlay{position:fixed;inset:0;background:rgba(6,8,15,0.95);z-index:1000;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:20px;backdrop-filter:blur(10px)}
#puter-overlay h2{font-family:'Syne',sans-serif;font-size:22px;font-weight:800}
#puter-overlay p{font-size:13px;color:var(--text3);text-align:center;max-width:340px;line-height:1.7}

@media(max-width:768px){
  .stat-grid{grid-template-columns:1fr 1fr}
  .form-grid{grid-template-columns:1fr}
  .chart-grid{grid-template-columns:1fr}
  .two-col{grid-template-columns:1fr}
  main{padding:16px}
  .nav{padding:0 12px}
  header{padding:0 16px}
  .ticket-detail-grid{grid-template-columns:1fr}
  .admin-stat-bar{grid-template-columns:1fr}
  .tracker-input-row{flex-direction:column}
}
</style>
</head>
<body>

<!-- Puter sign-in overlay (shows only if not signed in) -->
<div id="puter-overlay" style="display:none">
  <div style="font-size:48px">🏫</div>
  <h2>CampusOS AI</h2>
  <p>This app uses <strong style="color:var(--accent)">Puter.js</strong> for free AI — no API key needed.<br>Sign in with a free Puter account to get started.</p>
  <button class="btn btn-primary" id="puter-signin-btn" onclick="puterSignIn()">Sign in with Puter (Free) →</button>
  <p style="font-size:11px;color:var(--text3)">puter.com — free account, no credit card required</p>
</div>

<header>
  <div class="logo">
    <div class="logo-icon">🏫</div>
    <div class="logo-text">Campus<span>OS</span></div>
  </div>
  <div class="header-right">
    <div class="live-dot">AI LIVE</div>
    <div class="free-badge">FREE · No API Key</div>
    <div class="model-tag">gpt-4o-mini · puter.js</div>
  </div>
</header>

<nav class="nav">
  <div class="nav-tab active" data-view="complaint" onclick="switchView('complaint',this)">Submit</div>
  <div class="nav-tab" data-view="dashboard" onclick="switchView('dashboard',this)">Dashboard <span class="nav-count" id="nav-count">0</span></div>
  <div class="nav-tab" data-view="tracker" onclick="switchView('tracker',this)">Track Ticket</div>
  <div class="nav-tab" data-view="admin" onclick="switchView('admin',this)">Dept. Admin</div>
  <div class="nav-tab" data-view="policy" onclick="switchView('policy',this)">Policy AI</div>
  <div class="nav-tab" data-view="architecture" onclick="switchView('architecture',this)">Architecture</div>
</nav>

<main>

<!-- SUBMIT -->
<div id="view-complaint" class="view active">
  <div class="two-col">
    <div>
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>New Complaint</div>
        <p class="section-sub">Submit in Hindi, English, or Hinglish — AI will classify and route it automatically. <strong style="color:var(--green)">Completely free via Puter.js!</strong></p>
        <div class="form-grid">
          <div class="form-group">
            <label>Your Name</label>
            <input type="text" id="f-name" placeholder="e.g. Priya Sharma">
          </div>
          <div class="form-group">
            <label>Your Department</label>
            <select id="f-dept">
              <option value="CSE">CSE</option>
              <option value="ECE">ECE</option>
              <option value="ME">ME</option>
              <option value="Civil">Civil</option>
              <option value="MBA">MBA</option>
              <option value="IT">IT</option>
            </select>
          </div>
          <div class="form-group full">
            <label>Describe Your Problem <span class="lang-tag">🌐 Multilingual</span></label>
            <textarea id="f-complaint" placeholder="Type in Hindi, English, or Hinglish…&#10;e.g. Mera hostel ka fan 3 din se kharab hai / WiFi not working in lab"></textarea>
          </div>
          <div class="form-group full">
            <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center">
              <span style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.5px">Try: </span>
              <div class="pill" onclick="setC('Mera hostel fan 3 din se kharab hai, please jaldi fix karo')">🔧 Fan kharab</div>
              <div class="pill" onclick="setC('WiFi not working in library for 2 days, can\'t study')">📶 WiFi issue</div>
              <div class="pill" onclick="setC('Mess ka khana bahut kharab hai, quality bilkul thik nahi')">🍽 Mess quality</div>
              <div class="pill" onclick="setC('Scholarship form submit nahi ho raha, portal error aa raha hai')">📝 Scholarship</div>
              <div class="pill" onclick="setC('Classroom B-204 mein AC kharab hai, bahut garmi ho rahi hai')">❄️ AC issue</div>
            </div>
          </div>
        </div>
        <div style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap">
          <button class="btn btn-primary" id="submit-btn" onclick="submitComplaint()">🚀 Analyse & Submit</button>
          <button class="btn btn-secondary" onclick="clearForm()">Clear</button>
        </div>
      </div>

      <div class="ai-result" id="ai-result"></div>

      <div class="ticket-box" id="ticket-box">
        <div style="font-size:36px;margin-bottom:8px">🎫</div>
        <div style="font-size:11px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:1px">Ticket Generated</div>
        <div class="ticket-id" id="ticket-id">—</div>
        <div style="font-size:12px;color:var(--text3);margin-bottom:14px" id="ticket-meta">—</div>
        <div class="ticket-status">✓ Routed to Department</div>
        <div style="margin-top:14px;font-size:12px;color:var(--text3)">Track in <strong style="color:var(--accent);cursor:pointer" onclick="goTracker()">Track Ticket</strong> tab</div>
      </div>
    </div>

    <div style="display:flex;flex-direction:column;gap:16px">
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>Recent Submissions</div>
        <div id="recent-tickets">
          <div class="empty-state" style="padding:32px 16px">
            <div class="empty-state-icon">📋</div>
            <h3>No complaints yet</h3>
            <p>Submit your first complaint to see it here.</p>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>How It Works</div>
        <div style="display:flex;flex-direction:column;gap:10px">
          <div style="display:flex;gap:12px;align-items:flex-start;padding:12px;background:var(--bg3);border-radius:8px;border:1px solid var(--border)">
            <div style="font-size:18px;flex-shrink:0">1️⃣</div>
            <div><div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:3px">Write in any language</div><div style="font-size:12px;color:var(--text3)">Hindi, English, Hinglish — AI understands all</div></div>
          </div>
          <div style="display:flex;gap:12px;align-items:flex-start;padding:12px;background:var(--bg3);border-radius:8px;border:1px solid var(--border)">
            <div style="font-size:18px;flex-shrink:0">2️⃣</div>
            <div><div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:3px">AI Analysis (Free via Puter.js)</div><div style="font-size:12px;color:var(--text3)">Classifies, prioritizes, and routes automatically — no API key</div></div>
          </div>
          <div style="display:flex;gap:12px;align-items:flex-start;padding:12px;background:rgba(24,224,160,0.05);border-radius:8px;border:1px solid rgba(24,224,160,0.15)">
            <div style="font-size:18px;flex-shrink:0">3️⃣</div>
            <div><div style="font-size:12px;font-weight:700;color:var(--green);margin-bottom:3px">Ticket Generated</div><div style="font-size:12px;color:var(--text3)">Track real-time status in the tracker</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- DASHBOARD -->
<div id="view-dashboard" class="view"><div id="dash-content"></div></div>

<!-- TRACKER -->
<div id="view-tracker" class="view">
  <div class="tracker-hero">
    <h2>🎫 Track Your Ticket</h2>
    <p>Enter your ticket ID to see real-time status and timeline</p>
    <div class="tracker-input-row">
      <input type="text" id="track-input" placeholder="e.g. CMP-001" style="font-family:'JetBrains Mono',monospace;font-size:15px;letter-spacing:1px" onkeypress="if(event.key==='Enter')trackTicket()">
      <button class="btn btn-primary" onclick="trackTicket()">Track →</button>
    </div>
    <div style="margin-top:14px;display:flex;gap:7px;justify-content:center;flex-wrap:wrap" id="demo-ids"></div>
  </div>
  <div id="tracker-not-found" style="display:none;text-align:center;padding:40px;color:var(--text3)">
    <div style="font-size:44px;margin-bottom:12px">🔍</div>
    <div style="font-size:15px;font-weight:600;color:var(--text2);margin-bottom:6px">Ticket not found</div>
    <div style="font-size:13px">Submit a complaint first to get a ticket ID</div>
  </div>
  <div id="tracker-result" style="display:none"></div>
</div>

<!-- ADMIN -->
<div id="view-admin" class="view">
  <div id="admin-login-screen" class="admin-login">
    <div class="card">
      <div style="text-align:center;margin-bottom:24px">
        <div style="font-size:40px;margin-bottom:10px">🏢</div>
        <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;margin-bottom:4px">Department Admin</div>
        <div style="font-size:12px;color:var(--text3)">Login to manage your department's tickets</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px">
        <div class="form-group">
          <label>Select Department</label>
          <select id="admin-dept-select">
            <option value="">-- Choose Department --</option>
            <option value="Hostel Office">Hostel Office</option>
            <option value="IT Dept">IT Dept</option>
            <option value="Mess Committee">Mess Committee</option>
            <option value="Academic Office">Academic Office</option>
            <option value="Facilities">Facilities</option>
          </select>
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" id="admin-password" placeholder="admin123">
        </div>
      </div>
      <button class="btn btn-primary" style="width:100%;margin-top:16px;justify-content:center" onclick="adminLogin()">Login →</button>
      <div style="margin-top:10px;font-size:11px;color:var(--text3);text-align:center">Demo password: <span style="font-family:'JetBrains Mono',monospace;color:var(--accent)">admin123</span></div>
    </div>
  </div>
  <div id="admin-dashboard-screen" style="display:none">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:10px">
      <div>
        <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800" id="admin-dept-title">Dashboard</div>
        <div style="font-size:12px;color:var(--text3);margin-top:2px">Manage and resolve your department's complaints</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <div style="font-size:11px;color:var(--green);background:rgba(24,224,160,0.08);border:1px solid rgba(24,224,160,0.2);padding:5px 12px;border-radius:20px;font-weight:700">🟢 Logged in</div>
        <button class="btn btn-secondary btn-sm" onclick="adminLogout()">Logout</button>
      </div>
    </div>
    <div class="admin-stat-bar" id="admin-stats-bar"></div>
    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px">
        <div class="card-title" style="margin-bottom:0"><div class="card-title-accent"></div>Assigned Tickets</div>
        <select id="admin-filter" onchange="renderAdminTickets()" style="padding:7px 12px;font-size:12px;border-radius:7px;width:auto">
          <option value="all">All Status</option>
          <option value="Pending">Pending</option>
          <option value="In Progress">In Progress</option>
          <option value="Resolved">Resolved</option>
        </select>
      </div>
      <div id="admin-tickets-list"></div>
    </div>
  </div>
</div>

<!-- POLICY -->
<div id="view-policy" class="view">
  <div class="two-col">
    <div>
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>AI Policy Assistant</div>
        <p class="section-sub">Ask anything about college rules, hostel timings, attendance, fees — Hindi, English, Hinglish supported.</p>
        <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;align-items:center">
          <span style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase">Quick Ask: </span>
          <div class="pill" onclick="askPolicy('What is the hostel curfew timing?')">Hostel curfew</div>
          <div class="pill" onclick="askPolicy('Attendance kitni percentage chahiye pass hone ke liye?')">Attendance</div>
          <div class="pill" onclick="askPolicy('How to apply for merit scholarship?')">Scholarship</div>
          <div class="pill" onclick="askPolicy('Library closing time kya hai?')">Library hours</div>
          <div class="pill" onclick="askPolicy('Backlog exam ke liye kya process hai?')">Backlogs</div>
        </div>
        <div class="chat-container" id="chat-container">
          <div class="chat-msg">
            <div class="chat-avatar ai">✦</div>
            <div class="chat-bubble">Namaste! I'm CampusOS Policy AI. Ask me anything about campus rules, hostel timings, fees, attendance, or procedures — in Hindi, English, or Hinglish! 😊</div>
          </div>
        </div>
        <div class="chat-input-row">
          <input type="text" id="policy-input" placeholder="Hostel timing kya hai? / What are exam rules?" onkeypress="if(event.key==='Enter')sendPolicy()">
          <button class="btn btn-primary" onclick="sendPolicy()">Send ↗</button>
        </div>
      </div>
    </div>
    <div>
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>Policy Reference</div>
        <div class="policy-card"><div class="policy-card-title">🏠 Hostel Rules</div><div class="policy-card-body">Curfew: 10 PM weekdays, 11 PM weekends. Guests must register at reception. Violations result in fine or suspension.</div></div>
        <div class="policy-card"><div class="policy-card-title">📚 Attendance</div><div class="policy-card-body">Minimum 75% attendance required. Below 60% = exam debarment. Medical leaves need official doctor's certificate within 3 days.</div></div>
        <div class="policy-card"><div class="policy-card-title">💰 Scholarships</div><div class="policy-card-body">Merit scholarship: Top 10% students. Need-based: Apply by 30th Sept. Documents: income certificate, marksheets, bank details.</div></div>
        <div class="policy-card"><div class="policy-card-title">📖 Library</div><div class="policy-card-body">Mon–Sat: 8 AM–10 PM. Sunday: 10 AM–6 PM. No food/beverages. Max 5 books issued per student.</div></div>
        <div class="policy-card"><div class="policy-card-title">📝 Exams</div><div class="policy-card-body">No electronic devices allowed. Late entry after 30 min not permitted. Malpractice results in cancellation + disciplinary action.</div></div>
      </div>
    </div>
  </div>
</div>

<!-- ARCHITECTURE -->
<div id="view-architecture" class="view">
  <div class="two-col">
    <div class="card">
      <div class="card-title"><div class="card-title-accent"></div>System Architecture</div>
      <div class="arch">
        <div class="arch-node hl">👨‍🎓 Student Input (Any Language)</div>
        <div class="arch-arrow"></div>
        <div class="arch-node">🌐 CampusOS Frontend (HTML)</div>
        <div class="arch-arrow"></div>
        <div class="arch-node hl">🆓 Puter.js — Free AI, No API Key</div>
        <div class="arch-arrow"></div>
        <div class="arch-node hl">🤖 GPT-4o-mini via Puter</div>
        <div class="arch-arrow"></div>
        <div class="arch-branches">
          <div class="arch-branch-wrap"><div style="height:22px;width:1px;background:var(--border2)"></div><div class="arch-node" style="min-width:90px;font-size:11px">📂 Category</div></div>
          <div class="arch-branch-wrap"><div style="height:22px;width:1px;background:var(--border2)"></div><div class="arch-node" style="min-width:90px;font-size:11px">🔴 Priority</div></div>
          <div class="arch-branch-wrap"><div style="height:22px;width:1px;background:var(--border2)"></div><div class="arch-node" style="min-width:90px;font-size:11px">🏢 Routing</div></div>
        </div>
        <div class="arch-arrow" style="margin-top:10px"></div>
        <div class="arch-node">🎫 Ticket Generator</div>
        <div class="arch-arrow"></div>
        <div class="arch-node">💾 In-Memory Store</div>
        <div class="arch-arrow"></div>
        <div class="arch-branches">
          <div class="arch-branch-wrap"><div style="height:22px;width:1px;background:var(--border2)"></div><div class="arch-node hl" style="min-width:110px;font-size:11px">📊 Dashboard</div></div>
          <div class="arch-branch-wrap"><div style="height:22px;width:1px;background:var(--border2)"></div><div class="arch-node hl" style="min-width:110px;font-size:11px">🔍 Tracker</div></div>
          <div class="arch-branch-wrap"><div style="height:22px;width:1px;background:var(--border2)"></div><div class="arch-node hl" style="min-width:110px;font-size:11px">🏢 Admin</div></div>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:16px">
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>Tech Stack</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div style="background:var(--bg3);border-radius:8px;padding:12px;border:1px solid var(--border)"><div style="font-size:9px;color:var(--text3);margin-bottom:4px;text-transform:uppercase;font-weight:700">Frontend</div><div style="font-size:12px;color:var(--text2)">HTML · CSS · Vanilla JS</div></div>
          <div style="background:rgba(24,224,160,0.05);border-radius:8px;padding:12px;border:1px solid rgba(24,224,160,0.2)"><div style="font-size:9px;color:var(--green);margin-bottom:4px;text-transform:uppercase;font-weight:700">AI Engine</div><div style="font-size:12px;color:var(--green)">Puter.js · GPT-4o-mini · FREE</div></div>
          <div style="background:var(--bg3);border-radius:8px;padding:12px;border:1px solid var(--border)"><div style="font-size:9px;color:var(--text3);margin-bottom:4px;text-transform:uppercase;font-weight:700">Data Store</div><div style="font-size:12px;color:var(--text2)">In-Memory (JS Array)</div></div>
          <div style="background:var(--bg3);border-radius:8px;padding:12px;border:1px solid var(--border)"><div style="font-size:9px;color:var(--text3);margin-bottom:4px;text-transform:uppercase;font-weight:700">Languages</div><div style="font-size:12px;color:var(--text2)">Hindi · English · Hinglish</div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title"><div class="card-title-accent"></div>AI Features</div>
        <div style="display:flex;flex-direction:column;gap:8px">
          <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:var(--text2)"><span style="color:var(--green)">✓</span> Auto complaint classification (GPT-4o-mini)</div>
          <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:var(--text2)"><span style="color:var(--green)">✓</span> Smart priority assessment</div>
          <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:var(--text2)"><span style="color:var(--green)">✓</span> Automatic department routing</div>
          <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:var(--text2)"><span style="color:var(--green)">✓</span> Multilingual NLP — Hindi, Hinglish, English</div>
          <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:var(--text2)"><span style="color:var(--green)">✓</span> Policy Q&A chatbot</div>
          <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:var(--green)"><span>★</span> <strong>100% Free — No API key, no backend</strong></div>
        </div>
      </div>
    </div>
  </div>
</div>

</main>

<script>
// ======= STATE =======
let allComplaints = [];
let currentAdminDept = null;
let policyHistory = [];

// ======= PUTER.JS AI =======
// Uses puter.ai.chat() — free, no API key, works in any browser
const AI_MODEL = 'gpt-4o-mini'; // Free model via Puter.js

async function aiGenerate(systemPrompt, userText) {
  // Puter.js doesn't have a separate system param, so we prepend it
  const fullPrompt = `${systemPrompt}\n\n---\n${userText}`;
  const response = await puter.ai.chat(fullPrompt, { model: AI_MODEL });
  // Response can be string or object
  if (typeof response === 'string') return response.trim();
  if (response && response.message) return (response.message.content?.[0]?.text || response.message.content || '').trim();
  if (response && response.text) return response.text.trim();
  return String(response).trim();
}

async function aiChat(systemPrompt, history) {
  // Build a context string from history
  let ctx = systemPrompt + '\n\n---\nConversation so far:\n';
  history.forEach(m => { ctx += `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}\n`; });
  ctx += 'Assistant:';
  const response = await puter.ai.chat(ctx, { model: AI_MODEL });
  if (typeof response === 'string') return response.trim();
  if (response && response.message) return (response.message.content?.[0]?.text || response.message.content || '').trim();
  if (response && response.text) return response.text.trim();
  return String(response).trim();
}

// ======= PUTER AUTH =======
async function initPuter() {
  // puter.js auto-handles auth; show overlay if sign-in is needed
  try {
    // Try a lightweight call to see if we're authed
    await puter.auth.getUser();
    // If we reach here, we're signed in — hide overlay
    document.getElementById('puter-overlay').style.display = 'none';
  } catch(e) {
    // Not signed in — show overlay
    document.getElementById('puter-overlay').style.display = 'flex';
  }
}

async function puterSignIn() {
  try {
    document.getElementById('puter-signin-btn').textContent = 'Signing in…';
    await puter.auth.signIn();
    document.getElementById('puter-overlay').style.display = 'none';
  } catch(e) {
    document.getElementById('puter-signin-btn').textContent = 'Sign in with Puter (Free) →';
    alert('Sign-in failed or cancelled. Please try again.');
  }
}

// ======= UTIL =======
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}

function detectLang(t){
  if(/[\u0900-\u097F]/.test(t)) return '🇮🇳 Hindi';
  if(/\b(mera|meri|mein|hai|nahi|kya|tha|bahut|kharab|din|karein|raha|bilkul|aur|ki|ka|ko|se|pe|wala)\b/i.test(t)) return '🌐 Hinglish';
  return '🇬🇧 English';
}

function genId(){
  const nums = allComplaints.map(c=>parseInt(c.id.replace('CMP-',''),10)).filter(n=>!isNaN(n));
  const next = nums.length ? Math.max(...nums)+1 : 1;
  return 'CMP-'+String(next).padStart(3,'0');
}

function nowStr(){
  return new Date().toLocaleString('en-IN',{day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'});
}

function updateNavCount(){
  document.getElementById('nav-count').textContent = allComplaints.length;
}

// ======= VIEWS =======
function switchView(name,el){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('view-'+name).classList.add('active');
  if(el) el.classList.add('active');
  if(name==='dashboard') renderDashboard();
  if(name==='tracker') renderDemoIds();
  if(name==='admin'&&currentAdminDept) renderAdminTickets();
}

function goTracker(){
  const tab=document.querySelector('.nav-tab[data-view="tracker"]');
  switchView('tracker',tab);
}

// ======= COMPLAINT FORM =======
function setC(t){document.getElementById('f-complaint').value=t}
function clearForm(){
  document.getElementById('f-name').value='';
  document.getElementById('f-complaint').value='';
  document.getElementById('ai-result').classList.remove('show');
  document.getElementById('ai-result').innerHTML='';
  document.getElementById('ticket-box').classList.remove('show');
}

async function submitComplaint(){
  const name=(document.getElementById('f-name').value.trim())||'Anonymous';
  const dept=document.getElementById('f-dept').value;
  const complaint=document.getElementById('f-complaint').value.trim();
  if(!complaint){alert('Please describe your complaint');return;}

  const btn=document.getElementById('submit-btn');
  btn.disabled=true;
  btn.innerHTML='<div class="dot-pulse"><span></span><span></span><span></span></div> Analysing with AI...';
  document.getElementById('ai-result').classList.remove('show');
  document.getElementById('ai-result').innerHTML='';
  document.getElementById('ticket-box').classList.remove('show');

  const lang=detectLang(complaint);
  const reset=()=>{btn.disabled=false;btn.innerHTML='🚀 Analyse & Submit'};

  const systemPrompt=`You are CampusOS AI, a campus complaint classifier for an Indian university. Analyze the complaint (may be in Hindi, Hinglish, or English) and return ONLY a valid JSON object — no markdown, no backticks, no explanation, nothing else:
{"category":"one of [Maintenance, IT / Network, Food, Academic, Infrastructure, Transport, Medical, Safety, Other]","priority":"one of [High, Medium, Low]","assigned_department":"most appropriate department e.g. Hostel Office, IT Dept, Mess Committee, Academic Office, Facilities","summary":"one clear English sentence summarizing the complaint","estimated_resolution":"e.g. Same day, 1-2 days, 2-3 days, 3-5 days"}`;

  try {
    let raw = await aiGenerate(systemPrompt, `Student: ${name} | Department: ${dept}\nComplaint: ${complaint}`);
    raw = raw.replace(/```[a-z]*\n?/gi,'').replace(/```/g,'').trim();
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if(jsonMatch) raw=jsonMatch[0];
    const parsed=JSON.parse(raw);

    fillAIResult(parsed,lang);

    setTimeout(()=>{
      const id=genId();
      const now=nowStr();
      document.getElementById('ticket-id').textContent=id;
      document.getElementById('ticket-meta').textContent='Submitted '+now+' · '+parsed.priority+' Priority';
      document.getElementById('ticket-box').classList.add('show');
      allComplaints.unshift({
        id,student:name,dept,category:parsed.category,priority:parsed.priority,
        assigned:parsed.assigned_department,status:'Pending',complaint:parsed.summary,
        submittedAt:now,eta:parsed.estimated_resolution,
        updates:['Complaint received','AI analysed: '+parsed.category+', '+parsed.priority+' priority','Routed to '+parsed.assigned_department]
      });
      updateNavCount();renderRecent();renderDemoIds();reset();
    },400);

  } catch(e) {
    console.error('AI error:',e);
    btn.innerHTML='⚠ Error — Retry';btn.disabled=false;
    const errBox=document.getElementById('ai-result');
    errBox.classList.add('show');
    errBox.innerHTML=`<div class="ai-header"><span class="ai-badge-tag" style="background:var(--red)">ERROR</span><span style="font-size:13px;font-weight:600;color:var(--red);margin-left:8px">Analysis Failed</span></div><div class="ai-summary" style="color:var(--text2)">${esc(e.message||'AI unavailable. Make sure you are signed in to Puter and try again.')}</div>`;
  }
}

function fillAIResult(p,lang){
  const box=document.getElementById('ai-result');
  box.innerHTML=`<div class="ai-header"><span class="ai-badge-tag">PUTER AI</span><span style="font-size:13px;font-weight:600;color:var(--text);margin-left:8px">Analysis Complete</span><span style="margin-left:auto" class="lang-tag">${esc(lang||'')}</span></div><div class="ai-fields"><div class="ai-field"><div class="ai-label">Category</div><div class="ai-value">${esc(p.category||'—')}</div></div><div class="ai-field"><div class="ai-label">Priority</div><div class="ai-value priority-${(p.priority||'').toLowerCase()}">${esc(p.priority||'—')}</div></div><div class="ai-field"><div class="ai-label">Assigned To</div><div class="ai-value">${esc(p.assigned_department||'—')}</div></div><div class="ai-field"><div class="ai-label">Est. Resolution</div><div class="ai-value">${esc(p.estimated_resolution||'2-3 days')}</div></div></div><div class="ai-summary"><div class="ai-label" style="margin-bottom:5px">AI Summary</div><div style="font-size:13px;line-height:1.65;color:var(--text2)">${esc(p.summary||'—')}</div></div>`;
  box.classList.add('show');
}

function renderRecent(){
  const el=document.getElementById('recent-tickets');if(!el)return;
  if(!allComplaints.length){el.innerHTML=`<div class="empty-state" style="padding:32px 16px"><div class="empty-state-icon">📋</div><h3>No complaints yet</h3><p>Submit your first complaint to see it here.</p></div>`;return;}
  el.innerHTML=allComplaints.slice(0,6).map(c=>`<div style="background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:12px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;margin-bottom:8px;transition:border-color .15s" onmouseover="this.style.borderColor='var(--border2)'" onmouseout="this.style.borderColor='var(--border)'" onclick="qTrack('${esc(c.id)}')"><div><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent);font-weight:600;margin-bottom:3px">${esc(c.id)}</div><div style="font-size:12px;color:var(--text2)">${esc(c.complaint.slice(0,50))}${c.complaint.length>50?'…':''}</div></div><span class="badge badge-${c.priority.toLowerCase()}">${esc(c.priority)}</span></div>`).join('');
}

function qTrack(id){
  const el=document.getElementById('track-input');if(el)el.value=id;
  const tab=document.querySelector('.nav-tab[data-view="tracker"]');
  switchView('tracker',tab);trackTicket();
}

// ======= DASHBOARD =======
function renderDashboard(){
  const el=document.getElementById('dash-content');
  if(!allComplaints.length){el.innerHTML=`<div class="empty-state"><div class="empty-state-icon">📊</div><h3>No data yet</h3><p>Submit complaints to see dashboard analytics here.</p></div>`;return;}
  const total=allComplaints.length,pending=allComplaints.filter(c=>c.status!=='Resolved').length,high=allComplaints.filter(c=>c.priority==='High').length,resolved=allComplaints.filter(c=>c.status==='Resolved').length;
  const tableRows=allComplaints.map(c=>`<tr style="cursor:pointer" onclick="qTrack('${esc(c.id)}')"><td><span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent)">${esc(c.id)}</span></td><td style="color:var(--text)">${esc(c.student)}</td><td><span class="badge badge-pending" style="background:rgba(61,127,255,0.08);color:var(--accent2);border-color:rgba(110,68,255,0.2)">${esc(c.dept)}</span></td><td>${esc(c.category)}</td><td><span class="badge badge-${c.priority.toLowerCase()}">${esc(c.priority)}</span></td><td>${esc(c.assigned)}</td><td><span class="badge badge-${c.status.toLowerCase().replace(/ /g,'-')}">${esc(c.status)}</span></td></tr>`).join('');
  const cats={};allComplaints.forEach(c=>{cats[c.category]=(cats[c.category]||0)+1});
  const maxCat=Math.max(...Object.values(cats),1);
  const catColors={'Maintenance':'#3d7fff','IT / Network':'#6e44ff','Food':'#f0a030','Academic':'#18e0a0','Infrastructure':'#e060c0','Transport':'#ef4545','Medical':'#30d8f0','Safety':'#f0e030','Other':'#8a96b8'};
  const barChart=Object.entries(cats).sort((a,b)=>b[1]-a[1]).map(([cat,n])=>`<div class="bar-row"><div class="bar-label">${esc(cat)}</div><div class="bar-track"><div class="bar-fill" style="width:${Math.round(n/maxCat*100)}%;background:${catColors[cat]||'#3d7fff'}"></div></div><div class="bar-val">${n}</div></div>`).join('');
  const pCols={High:'#ef4545',Medium:'#f0a030',Low:'#18e0a0'};
  const pris={High:0,Medium:0,Low:0};allComplaints.forEach(c=>{if(pris[c.priority]!==undefined)pris[c.priority]++});
  const pTotal=Object.values(pris).reduce((a,b)=>a+b,0);
  let angle=0;
  const paths=Object.entries(pris).map(([p,n])=>{if(!n)return'';if(n===pTotal)return`<circle cx="50" cy="50" r="38" fill="${pCols[p]}"/>`;const slice=n/pTotal*360,s=polar(50,50,38,angle),end=polar(50,50,38,angle+slice),lg=slice>180?1:0,d=`<path d="M50 50 L${s.x} ${s.y} A38 38 0 ${lg} 1 ${end.x} ${end.y} Z" fill="${pCols[p]}"/>`;angle+=slice;return d;}).join('');
  const legend=Object.entries(pris).map(([p,n])=>`<div class="pie-item"><div class="pie-dot" style="background:${pCols[p]}"></div>${esc(p)}: <b>${n}</b></div>`).join('');
  el.innerHTML=`<div class="stat-grid"><div class="stat-card"><div style="font-size:18px;margin-bottom:4px">📋</div><div class="stat-num" style="color:var(--accent)">${total}</div><div class="stat-label">Total Complaints</div></div><div class="stat-card"><div style="font-size:18px;margin-bottom:4px">⏳</div><div class="stat-num" style="color:var(--accent2)">${pending}</div><div class="stat-label">Pending</div></div><div class="stat-card"><div style="font-size:18px;margin-bottom:4px">🔴</div><div class="stat-num" style="color:var(--red)">${high}</div><div class="stat-label">High Priority</div></div><div class="stat-card"><div style="font-size:18px;margin-bottom:4px">✅</div><div class="stat-num" style="color:var(--green)">${resolved}</div><div class="stat-label">Resolved</div></div></div><div class="card" style="margin-bottom:20px"><div class="card-title"><div class="card-title-accent"></div>All Complaints</div><div class="table-wrap"><table><thead><tr><th>Ticket ID</th><th>Student</th><th>Dept</th><th>Category</th><th>Priority</th><th>Assigned To</th><th>Status</th></tr></thead><tbody>${tableRows}</tbody></table></div></div><div class="chart-grid"><div class="chart-card"><div class="chart-title">Complaints by Category</div><div class="bar-chart">${barChart}</div></div><div class="chart-card"><div class="chart-title">Priority Distribution</div><div class="pie-visual"><svg class="pie-svg" viewBox="0 0 100 100">${paths}</svg><div class="pie-legend">${legend}</div></div></div></div>`;
}

function polar(cx,cy,r,deg){const rad=(deg-90)*Math.PI/180;return{x:parseFloat((cx+r*Math.cos(rad)).toFixed(3)),y:parseFloat((cy+r*Math.sin(rad)).toFixed(3))};}

// ======= TRACKER =======
function renderDemoIds(){
  const el=document.getElementById('demo-ids');if(!el)return;
  if(!allComplaints.length){el.innerHTML='<span style="font-size:11px;color:var(--text3)">Submit a complaint to get a ticket ID</span>';return;}
  el.innerHTML='<span style="font-size:10px;color:var(--text3);font-weight:700;align-self:center">Try: </span>'+allComplaints.slice(0,6).map(c=>`<div class="pill" onclick="document.getElementById('track-input').value='${esc(c.id)}';trackTicket()">${esc(c.id)}</div>`).join('');
}

function trackTicket(){
  const input=(document.getElementById('track-input').value||'').trim().toUpperCase();
  if(!input)return;
  const ticket=allComplaints.find(c=>c.id===input);
  document.getElementById('tracker-not-found').style.display='none';
  document.getElementById('tracker-result').style.display='none';
  if(!ticket){document.getElementById('tracker-not-found').style.display='block';return;}
  const statusClass={'Pending':'badge-pending','In Progress':'badge-in-progress','Resolved':'badge-resolved'}[ticket.status]||'badge-pending';
  const priClass={'High':'priority-high','Medium':'priority-medium','Low':'priority-low'}[ticket.priority]||'';
  const steps=[{label:'Submitted',icon:'📝',desc:'Complaint received by CampusOS'},{label:'AI Analysed',icon:'🤖',desc:`Classified as ${ticket.category} · ${ticket.priority} priority`},{label:'Assigned',icon:'🏢',desc:`Routed to ${ticket.assigned}`},{label:'In Progress',icon:'🔧',desc:'Department working on resolution'},{label:'Resolved',icon:'✅',desc:'Issue resolved successfully'}];
  const sOrder=['Pending','In Progress','Resolved'];
  const si=sOrder.indexOf(ticket.status),doneCount=si===0?3:si===1?4:5,isRes=ticket.status==='Resolved';
  const timeline=steps.map((s,i)=>{const isDone=isRes?true:(i<doneCount-1),isActive=!isRes&&(i===doneCount-1),isPend=!isRes&&(i>doneCount-1),dotCls=isDone?'done':isActive?'active':'pending',note=(ticket.updates&&ticket.updates[i])?ticket.updates[i]:(isPend?'Waiting…':s.desc);return`<div class="timeline-item"><div class="timeline-dot ${dotCls}">${isDone?'✓':isActive?s.icon:'○'}</div><div class="timeline-content"><div class="timeline-title" style="${isPend?'color:var(--text3)':''}">${esc(s.label)}</div><div class="timeline-note">${esc(note)}</div></div></div>`;}).join('');
  document.getElementById('tracker-result').innerHTML=`<div class="two-col"><div><div class="card" style="margin-bottom:16px"><div class="card-title"><div class="card-title-accent"></div>Ticket Details</div><div class="ticket-detail-grid"><div class="ticket-detail-field"><div class="ticket-detail-label">Ticket ID</div><div class="ticket-detail-value" style="font-family:'JetBrains Mono',monospace;color:var(--accent)">${esc(ticket.id)}</div></div><div class="ticket-detail-field"><div class="ticket-detail-label">Status</div><div class="ticket-detail-value"><span class="badge ${statusClass}" style="font-size:12px;padding:4px 12px">${esc(ticket.status)}</span></div></div><div class="ticket-detail-field"><div class="ticket-detail-label">Priority</div><div class="ticket-detail-value"><span class="${priClass}">${esc(ticket.priority)}</span></div></div><div class="ticket-detail-field"><div class="ticket-detail-label">Category</div><div class="ticket-detail-value">${esc(ticket.category)}</div></div><div class="ticket-detail-field"><div class="ticket-detail-label">Student</div><div class="ticket-detail-value">${esc(ticket.student)} (${esc(ticket.dept)})</div></div><div class="ticket-detail-field"><div class="ticket-detail-label">Assigned To</div><div class="ticket-detail-value">${esc(ticket.assigned)}</div></div></div><div style="background:var(--bg3);border-radius:8px;padding:13px;border:1px solid var(--border)"><div style="font-size:9px;color:var(--text3);margin-bottom:5px;font-weight:700;text-transform:uppercase;letter-spacing:.6px">AI Summary</div><div style="font-size:13px;color:var(--text2);line-height:1.6">${esc(ticket.complaint)}</div></div></div><div class="card"><div class="card-title"><div class="card-title-accent"></div>Estimated Resolution</div><div style="display:flex;align-items:center;gap:16px"><div style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;color:var(--accent)">${esc(ticket.eta||'2-3 days')}</div><div style="font-size:12px;color:var(--text3);line-height:1.6">Based on AI priority assessment and category type</div></div></div></div><div class="card"><div class="card-title"><div class="card-title-accent"></div>Status Timeline</div><div class="timeline">${timeline}</div></div></div>`;
  document.getElementById('tracker-result').style.display='block';
}

// ======= ADMIN =======
function adminLogin(){
  const dept=document.getElementById('admin-dept-select').value;
  const pass=document.getElementById('admin-password').value;
  if(!dept){alert('Please select a department');return;}
  if(pass!=='admin123'){alert('Wrong password. Demo: admin123');return;}
  currentAdminDept=dept;
  document.getElementById('admin-login-screen').style.display='none';
  document.getElementById('admin-dashboard-screen').style.display='block';
  document.getElementById('admin-dept-title').textContent=dept+' Admin';
  renderAdminTickets();
}

function adminLogout(){
  currentAdminDept=null;
  document.getElementById('admin-login-screen').style.display='block';
  document.getElementById('admin-dashboard-screen').style.display='none';
  document.getElementById('admin-dept-select').value='';
}

function renderAdminTickets(){
  if(!currentAdminDept)return;
  const filter=(document.getElementById('admin-filter')||{}).value||'all';
  let mine=allComplaints.filter(c=>c.assigned===currentAdminDept);
  const total=mine.length,pend=mine.filter(c=>c.status!=='Resolved').length,res=mine.filter(c=>c.status==='Resolved').length;
  document.getElementById('admin-stats-bar').innerHTML=`<div class="admin-stat-mini"><div class="admin-stat-mini-num" style="color:var(--accent)">${total}</div><div class="admin-stat-mini-label">Total Assigned</div></div><div class="admin-stat-mini"><div class="admin-stat-mini-num" style="color:var(--amber)">${pend}</div><div class="admin-stat-mini-label">Pending</div></div><div class="admin-stat-mini"><div class="admin-stat-mini-num" style="color:var(--green)">${res}</div><div class="admin-stat-mini-label">Resolved</div></div>`;
  if(filter!=='all') mine=mine.filter(c=>c.status===filter);
  const list=document.getElementById('admin-tickets-list');
  if(!mine.length){list.innerHTML=`<div style="text-align:center;padding:52px 24px;color:var(--text3)"><div style="font-size:44px;margin-bottom:12px">🎉</div><div style="font-size:14px;font-weight:600;color:var(--text2);margin-bottom:6px">${total?'No tickets match this filter':'No tickets assigned yet'}</div></div>`;return;}
  list.innerHTML=mine.map(c=>{
    const pCls={'High':'badge-high','Medium':'badge-medium','Low':'badge-low'}[c.priority]||'';
    const sCls={'Pending':'badge-pending','In Progress':'badge-in-progress','Resolved':'badge-resolved'}[c.status]||'';
    return`<div class="admin-ticket-card"><div class="admin-ticket-top"><span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent);font-weight:700">${esc(c.id)}</span><span class="badge ${pCls}">${esc(c.priority)}</span><span class="badge ${sCls}">${esc(c.status)}</span><span style="font-size:11px;color:var(--text3);margin-left:auto">${esc(c.student)} · ${esc(c.dept)}</span></div><div class="admin-ticket-complaint">${esc(c.complaint)}</div><div style="font-size:11px;color:var(--text3);margin-bottom:10px">📅 ${esc(c.submittedAt||'Recently')} · ⏱ ETA: ${esc(c.eta||'2-3 days')}</div><div class="admin-ticket-actions">${c.status!=='In Progress'&&c.status!=='Resolved'?`<button class="btn btn-warn btn-sm" onclick="setStatus('${esc(c.id)}','In Progress')">🔧 In Progress</button>`:''} ${c.status!=='Resolved'?`<button class="btn btn-success btn-sm" onclick="setStatus('${esc(c.id)}','Resolved')">✅ Resolve</button>`:''} ${c.status==='Resolved'?`<button class="btn btn-secondary btn-sm" onclick="setStatus('${esc(c.id)}','Pending')">↩ Reopen</button>`:''}<button class="btn btn-danger btn-sm" onclick="escalate('${esc(c.id)}')">🚨 Escalate</button></div><div class="update-log" id="log-${esc(c.id)}"></div></div>`;
  }).join('');
}

function setStatus(id,newStatus){
  const c=allComplaints.find(t=>t.id===id);if(!c)return;
  c.status=newStatus;if(!c.updates)c.updates=[];
  if(newStatus==='In Progress')c.updates.push('Technician assigned, work in progress');
  else if(newStatus==='Resolved')c.updates.push('Issue resolved by '+currentAdminDept);
  else c.updates.push('Ticket reopened for review');
  renderAdminTickets();
  setTimeout(()=>{const log=document.getElementById('log-'+id);if(log){log.style.display='block';log.textContent='✓ Status → "'+newStatus+'" at '+new Date().toLocaleTimeString('en-IN');setTimeout(()=>{if(log)log.style.display='none'},4000);}},50);
}

function escalate(id){
  const c=allComplaints.find(t=>t.id===id);if(!c)return;
  c.priority='High';if(!c.updates)c.updates=[];
  c.updates.push('⚠ Escalated to High priority by admin');
  renderAdminTickets();
  setTimeout(()=>{const log=document.getElementById('log-'+id);if(log){log.style.display='block';log.textContent='⚠ Escalated to High priority';setTimeout(()=>{if(log)log.style.display='none'},4000);}},50);
}

// ======= POLICY CHAT =======
const POLICY_SYSTEM=`You are CampusOS Policy Assistant for an Indian university. Answer questions about campus policies concisely (2-4 sentences). Support Hindi, English, and Hinglish.
Campus Policy:
- Hostel curfew: 10 PM weekdays, 11 PM weekends. Guests must register at reception.
- Attendance: Minimum 75% required. Below 60% = debarred from exams. Medical leave needs doctor certificate within 3 days.
- Library: Mon-Sat 8 AM-10 PM, Sunday 10 AM-6 PM. Max 5 books per student. No food allowed.
- Scholarships: Merit (top 10%), Need-based (apply by 30th Sept). Documents: income cert, marksheets, bank details.
- Backlogs: Fill backlog form at Academic Office within 7 days of results. Fee: Rs.500 per subject.
- Exams: No electronics. No entry after 30 min. Malpractice = cancellation + disciplinary committee.
- Mess: Breakfast 7-9 AM, Lunch 12-2 PM, Dinner 7-9 PM.
- Fees: Semester fee due by 15th of first month. Late fee: Rs.100/day.`;

async function sendPolicy(){
  const inp=document.getElementById('policy-input');
  const q=inp.value.trim();if(!q)return;inp.value='';
  const chat=document.getElementById('chat-container');
  chat.innerHTML+=`<div class="chat-msg user"><div class="chat-avatar user">👤</div><div class="chat-bubble">${esc(q)}</div></div>`;
  chat.innerHTML+=`<div class="chat-msg" id="thinking"><div class="chat-avatar ai">✦</div><div class="chat-bubble"><div class="dot-pulse"><span></span><span></span><span></span></div></div></div>`;
  chat.scrollTop=chat.scrollHeight;
  policyHistory.push({role:'user',content:q});
  try{
    const reply=await aiChat(POLICY_SYSTEM,policyHistory);
    policyHistory.push({role:'assistant',content:reply});
    document.getElementById('thinking').remove();
    chat.innerHTML+=`<div class="chat-msg"><div class="chat-avatar ai">✦</div><div class="chat-bubble">${esc(reply)}</div></div>`;
    chat.scrollTop=chat.scrollHeight;
  }catch(e){
    document.getElementById('thinking').remove();
    chat.innerHTML+=`<div class="chat-msg"><div class="chat-avatar ai">✦</div><div class="chat-bubble" style="color:var(--red)">Sorry, AI is unavailable. ${esc(e.message||'Please try again.')}</div></div>`;
    policyHistory.pop();chat.scrollTop=chat.scrollHeight;
  }
}

function askPolicy(q){document.getElementById('policy-input').value=q;sendPolicy();}

// ======= INIT =======
renderRecent();updateNavCount();
// Check Puter auth status on load
window.addEventListener('load', () => {
  // Small delay to let puter.js initialise
  setTimeout(initPuter, 800);
});
</script>
</body>
</html>
