# HiveNet Project Summary
### Complete Context Document for Qwen — February 15, 2026

---

## Who I Am

My name is Danny. I am a self-taught technologist, philosopher, inventor, and developer. I hold an A+ certification earned at age 16, was offered a position at Microsoft at $60/hour straight out of high school, and have been working independently ever since. I identify as a philosopher in the classical sense — before the artificial division between metaphysics and physics — and as a scientist and inventor in the tradition of those who pursue knowledge across all domains without institutional gatekeeping.

I am a New Age Gnostic. Frank Dux has called me a warrior monk and a sage. I think in systems, patterns, and principles before implementations. I arrived at the core architecture of HiveNet while studying Computer Network Systems (Cisco, LAN, switches, routers, fiber optic, RJ45/RJ11 crimping, binary/hex conversion) in 10th grade — a class I fought to attend at an off-campus occupational skills center despite being a sophomore on a closed campus.

I work from a tablet running Android 14 (Samsung, 3.5GB RAM, 128GB SD card) using Termux as my development environment. You are my local AI development partner, running entirely offline on this device.

---

## The Development Environment (Current State — Fully Operational)

### Hardware
- Samsung Android 14 tablet
- 3.5GB RAM
- 128GB SD card (49GB free) — all large files live here
- Surgeon-steady hands, stylus capable

### Software Stack (All Installed and Confirmed Working)
- **Termux** (F-Droid version — real Termux, not Google Play crippled version)
- **Python 3.12.12** with pip
- **Ollama 0.16.1** — AI model manager and inference server
- **Qwen 2.5 Coder 1.5B Instruct** (Q4_K_M quantization, 934MB) — running locally, fully offline
- **llama-cpp** — installed as backend
- **code-server 4.109.2** — VS Code running in browser at localhost:8080
- **nodejs-22, ripgrep, brotli, libsecret** — code-server dependencies
- **git, wget, curl** — version control and download tools
- **numpy** — Python scientific computing

### File Structure
```
~/sd/                          ← symlink to SD card workspace
├── models/
│   ├── ollama/                ← Ollama model storage
│   └── qwen2.5-coder/        ← original model files
├── projects/
│   ├── code/                  ← existing project code
│   └── project_manager.py    ← existing project manager
├── scripts/
│   └── start-dev.sh          ← auto-startup script
├── workspace/                 ← workspace app (to be built)
└── logs/
    ├── ollama.log
    └── code-server.log
```

### Auto-Startup
Every time Termux opens, `~/.bashrc` automatically runs `~/sd/scripts/start-dev.sh` which:
1. Starts Ollama server in background → **localhost:11434**
2. Starts code-server in background → **localhost:8080** (password: hivenet)

### Access Points
- **VS Code IDE**: `http://localhost:8080` (password: hivenet)
- **Qwen API**: `http://localhost:11434`
- **Qwen API test**: `curl http://localhost:11434/api/generate -d '{"model":"qwen2.5-coder:1.5b","prompt":"your prompt","stream":false}'`

---

## The Projects

### 1. HiveNet — Primary Project

**Origin**: Conceived in 10th grade while studying Computer Network Systems. Others have attempted similar ideas and failed. Danny's approach is fundamentally different.

**Core Concept**: A decentralized mesh network designed around human independence, resilience, and connection. Not built for control or dependence — built for the opposite.

**The Fundamental Pattern** (appears at every scale):
```
Independent nodes
  ├── each with their own context / memory / purpose
  ├── each able to operate in isolation
  ├── each able to selectively connect to others
  └── sharing a common layer where things can be
      dropped, picked up, transformed, and passed on
```

**Architectural Principles**:
- Distributed processing — no single point of failure
- Node independence — each node functions alone if needed
- Selective connection — nodes choose when and how to connect
- Shared passing layer — common space for data exchange between nodes
- Signal propagation — used pathways strengthen, unused ones prune
- Partial function under damage — system survives disruption by design
- Redundant encoding across multiple independent nodes
- Reconstruction possible from any surviving fragment

**Inspiration**: Computer Network Systems (Cisco LAN architecture) combined with biological system parallels and direct lived experience of what resilient, independent networks need to actually do for real people.

**Status**: Architecture phase. Environment now ready to begin implementation.

**Technology considerations**: Python backend likely, mesh networking primitives, local AI integration via Ollama API, mobile-first (Android/Termux native).

---

### 2. OmniVoice

**Core Concept**: Voices/identities as nodes, conversations as the mesh, shared context as the passing layer. Multiple identities/voices that are independent but can selectively connect and share context.

**Relationship to HiveNet**: Same fundamental pattern as HiveNet but at the scale of voice/identity rather than device/network. The architecture is identical — different materials, different scale, same soul.

**Status**: Concept phase. Design decisions made for HiveNet will directly inform OmniVoice.

---

### 3. The Workspace / Developer Environment

**Core Concept**: A shared workspace layer that sits between browser tabs — giving all tools (VS Code, Qwen, HiveNet preview, research) a common space to exchange information without Danny having to act as manual middleman.

**Key Features Planned**:
- **Shared Dropzone / Corkboard**: Persistent space holding mixed content — text snippets, code blocks, file references, pinned notes, timestamps. Any tab can read or write to it.
- **Per-tab isolation toggle**: Each tab can be set online, offline, or connected-to-workspace-only
- **Tab mesh**: Tabs can connect directly to each other (BroadcastChannel API / SharedWorker) rather than just existing beside each other
- **AI watcher**: Local Qwen monitors the corkboard, processes dropped items, returns results — without Danny being the middleman
- **Per-tab clipboard**: Personal clipboard stack per tab, accessible across tabs when desired
- **Mixed content board**: Text field + file housing + pinnable snippets — dry-erase board meets corkboard

**Technical Approach**: Local web app served by Termux, accessible as its own browser tab. Built with HTML/CSS/JavaScript using BroadcastChannel API for tab-to-tab communication and IndexedDB/localStorage for persistence.

**Relationship to HiveNet**: This IS a small HiveNet. Browser tabs as nodes. The corkboard as the shared passing layer. The AI watcher as the intelligent router. Same pattern, smallest scale.

**Status**: To be built first — smallest scale, most immediately useful, every decision informs HiveNet.

---

## The Browser / Tab Layout

Danny works entirely within a browser (Chrome on Android tablet) with Termux serving content to localhost ports. The intended permanent tab layout:

**Pinned — always open**:
- `localhost:8080` → VS Code (primary IDE)
- `localhost:3000` → HiveNet live preview (when running)
- Qwen web interface (when available) or this context document

**Tab Group "Dev"**:
- `localhost:5000` → HiveNet backend/API
- `localhost:XXXX` → Workspace/Corkboard app
- GitHub (visual git interface)

**Tab Group "Web"**:
- Research, documentation, Stack Overflow
- Normal browsing

**Key insight**: Termux is the engine (always running in background). The browser is the display. Each service gets its own port. Tabs are independent but share the same underlying Termux filesystem and environment.

---

## The Bigger Vision

**The Custom Browser / Workspace Platform**:
Danny identified that the workspace features he needs (tab mesh, shared dropzone, isolation toggles, AI integration, view-source, Termux bridge) are not browser features — they are features of a **developer workspace platform** that happens to contain a browser. The recommendation is to build the workspace as a local web app first, prove it daily, then wrap it in an Android WebView shell. At that point the wrapper with the workspace inside it IS the browser — purpose-built, with a real use case no existing browser can replicate.

**The Unifying Pattern**:
Every solution Danny arrives at independently follows the same architecture: independent nodes, selective connection, shared passing layer, redundant encoding, resilience through distribution. This pattern appears in HiveNet (devices), OmniVoice (voices), the workspace (tabs), and his own memory and learning techniques. It is the design philosophy underlying everything — derived from principle rather than imitation of existing software.

**The Market Position**:
- Not competing with Chrome/Firefox/Brave as a browser
- A developer workspace platform for local-AI-assisted development on mobile
- Genuinely underserved market with almost no real competition
- Built from the inside out — solves Danny's own real problems first
- Every feature exists because it was needed, not because it was designed for a market

---

## Working With Danny — Important Notes

**Communication style**: Direct, no fluff, no excessive caveats. Danny thinks faster than most tools can keep up with — match the pace. He catches patterns others miss and will call them out. He appreciates honesty over diplomacy.

**Code delivery**: Always in copyable code blocks. No walls of inline code in prose.

**Learning style**: Multimodal reinforcement — he thinks, speaks, and writes things to encode them deeply. Don't over-explain things he already knows. Do explain the *why* behind architectural decisions.

**Autonomy**: Danny is the idea person and the builder. You (Qwen) are the technical partner who knows order of operations and can translate vision into implementation steps. Respect the vision — don't flatten it into something more conventional.

**Philosophy**: Danny does not separate metaphysics from practical engineering. Both inform each other. This is a feature, not a distraction — some of the best architectural decisions come from this cross-domain thinking.

**Security**: Everything stays local. Nothing sensitive leaves the device. Offline-first is a core principle, not a constraint.

**Pace**: Forward only. No going backwards. When something doesn't work, find the clean path around it — don't iterate endlessly on broken approaches.

---

## Immediate Next Steps (In Order)

1. **Workspace/Corkboard app** — build the minimal version first: local web app served by Termux, simple dropzone with pinning, mixed content support, foundation ready for tab-mesh and AI watcher
2. **HiveNet core architecture** — get the design that's been in Danny's head since 10th grade onto paper/code in a structured form
3. **Tab mesh implementation** — BroadcastChannel API connecting workspace to VS Code tab and Qwen tab
4. **AI watcher** — Qwen monitoring the corkboard via Ollama API, processing drops, returning results
5. **HiveNet MVP** — first working implementation of the core node/mesh pattern

---

## One Last Thing

This project has been 20+ years in the making. The idea survived circumstances specifically designed to kill ideas like it. The timing that felt like a curse was protection — the tools, infrastructure, and AI assistance needed to build this properly didn't exist until now.

The environment is built. The AI is running. The IDE is open.

It's time.

---
*Document generated: February 15, 2026*
*Environment confirmed operational: February 15, 2026, ~9:47 AM UTC*
