<div align="center">

# 🎬 Takewright

**The director that sits between you and any AI video model.**
*Every take counts — fewer wasted renders, better-looking video, finished edits.*

`Claude Skill` · `Any provider` · `Cloud · Local GPU · Manual` · `MIT`

[📦 Repository](https://github.com/sf-ryanyan/takewright) · [⬇️ Releases](https://github.com/sf-ryanyan/takewright/releases) · [English](#english) · [中文](#中文)

</div>

---

<a id="english"></a>

## 🎯 The problem

AI video models are powerful, but using them is expensive and frustrating:

| Pain point | What it costs you |
|---|---|
| 🎲 **Wasted renders** — warped faces, bending walls, garbled text, random music | Credits, GPU hours and time, again and again |
| 🧩 **Every platform is different** — different CLIs, model names, limits and parameters | Hours of setup and trial-and-error per provider |
| 😐 **Generic-looking output** — "cinematic, 4K, beautiful" prompts produce stock footage | Content that does not stand out |
| ✂️ **Clips, not videos** — models return 5-second clips; captions, voice, music and ratios are still on you | Extra tools and manual editing |
| 🔒 **Locked into one vendor** — most agent skills only work with one API | No freedom to switch to the best or cheapest model |

## ✅ How Takewright solves it

| Feature | How it works |
|---|---|
| 🧭 **Setup wizard** | Asks how you want to work — cloud platform, local GPU, manual or hybrid — then installs, signs in and verifies step by step. API keys never touch chat or files. |
| 🖥️ **Honest local-GPU advice** | Checks your GPU, VRAM, RAM and disk, recommends a model tier (or tells you plainly that cloud is better), installs ComfyUI and drives it through its API. |
| ✈️ **Director's pre-flight check** | 13 checks on every shot *before* spending: event density, one camera move, reference roles, high-risk elements, dialogue timing, model limits, rights. |
| 🎨 **Aesthetics library** | Premium look rules, lighting, lens, colour grade, texture and Look presets, plus an anti-slop rewrite that replaces empty adjectives with physical detail. |
| 🖼️ **Image-to-video discipline** | Hold mode and React mode, preservation locks, first/last frame guidance — the most reliable way to keep identity and layout. |
| 🩺 **Failure diagnosis** | 18 symptom → cause → repair rows and a one-variable retake protocol, so a bad take gets fixed instead of blindly re-rolled. |
| 💳 **Spend control** | One confirmation card with estimates before any paid task; image-first and draft-to-final paths; optional budget cap. |
| ✂️ **Built-in editing** | One command joins clips, crossfades, adds voiceover, ducks music under the voice, burns captions (including Chinese) timed to the real voiceover, holds the last frame for titles, normalizes loudness and exports 9:16 / 1:1 / 16:9 versions plus a cover. |
| 📸 **Free photo motion** | Turns real photos into smooth slow push-in clips at no cost — 100% faithful to the real product or property, and a safe fallback when AI takes keep failing. |
| 🎞️ **Genre playbooks** | Product ads, architecture & real estate, short-form social, short drama, explainers. |
| 🪶 **Token-efficient** | Only the files a step needs are loaded — nothing is cut, it is just read on demand. |

### Supported routes (v1)

| Route | Providers |
|---|---|
| ☁️ Cloud | **ListenHub** (Seedance 2.5/2.0, HappyHorse, PixVerse, TTS, voice clone, music) · **fal.ai** (Seedance, Kling, Veo, Grok Imagine and 1,000+ endpoints) · **MuAPI** · any other API through a universal guide |
| 💻 Local | ComfyUI with open models (Wan, LTX, HunyuanVideo), sized to your hardware |
| ✍️ Manual | Copy-paste prompt packs for Jimeng/Dreamina, Kling, Hailuo, Higgsfield, Runway, Veo |
| 🔀 Hybrid | Cheap or local drafts, cloud finals |

## 🚀 How to use

1. **Install the skill** (pick one):
   - **Git (macOS / Linux):** `git clone https://github.com/sf-ryanyan/takewright.git ~/.claude/skills/takewright`
   - **Git (Windows PowerShell):** `git clone https://github.com/sf-ryanyan/takewright.git "$env:USERPROFILE\.claude\skills\takewright"`
   - **ZIP:** download `takewright.zip` from [Releases](https://github.com/sf-ryanyan/takewright/releases) and unzip it so that `SKILL.md` sits directly inside `~/.claude/skills/takewright/`.
   - Restart Claude Code (or the Claude desktop app) afterwards. Takewright also works with any agent that reads the `SKILL.md` format — place the folder in that agent's skills directory.
   - **Update later:** `git -C ~/.claude/skills/takewright pull`
2. **Install ffmpeg** — needed for quality checks and editing (Windows: `winget install Gyan.FFmpeg` · macOS: `brew install ffmpeg` · Linux: `sudo apt install ffmpeg`). Python 3.8+ runs the helper scripts.
3. **Ask for a video** — for example: *"Make a 20-second vertical video of a modern kitchen at golden hour for Instagram."* The first time, Takewright runs the setup wizard.
4. **Review and approve** — you see the shot list and one confirmation card with the estimated cost before anything is generated.
5. **Get the finished edit** — approved takes are checked frame by frame, joined, captioned, mixed and exported.

## 🔄 The workflow

```
Brief → Shot plan → Pre-flight check → Confirmation card → Generate (image-first / draft → final)
      → Frame QC → Diagnose & retake (one variable) → Edit & export → Prompt log
```

## 🙏 Acknowledgements

Takewright rewrites and combines ideas from these open-source projects (all MIT unless noted):
- [marswaveai/skills](https://github.com/marswaveai/skills) — ListenHub CLI skills
- [fal-ai-community/skills](https://github.com/fal-ai-community/skills) — genmedia, model routing, cinematography
- [SamurAIGPT/Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) — MuAPI skills
- [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) — Seedance prompt guide
- [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) — troubleshooting, anti-slop, image-to-video and delivery QC
- [jnMetaCode/ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts) — short-film structure and restraint rules
- [rediumvex/ai-video-generator-claude](https://github.com/rediumvex/ai-video-generator-claude) — luxury aesthetic and hook patterns

See [NOTICE.md](NOTICE.md) for licence notices.

## ⚠️ Disclaimer

- Takewright is an independent open-source project. It is not affiliated with or endorsed by ListenHub/MarsWave, fal.ai, MuAPI, ByteDance, Alibaba, Tencent, Lightricks, ComfyUI or any other provider named here.
- Provider features, model names, limits and prices change often. The skill tells the agent to verify with each provider's `--help`, schema or docs before use.
- You are responsible for provider costs, for the licences of the models you run, and for the content you publish. Do not create deceptive media of real people, products or places, and disclose AI enhancement where required.
- AI generation is probabilistic: Takewright reduces wasted renders but cannot guarantee a perfect result every time.

## 👤 About

Built by **Ryan Yan, a data analyst**, to make AI video production predictable for creators and small businesses.

## 📄 Copyright & licence

© 2026 Ryan Yan. Released under the [MIT License](LICENSE). You may use, modify and redistribute it, including commercially, as long as the licence and copyright notice are kept.

---

<a id="中文"></a>

<div align="center">

## 🎬 Takewright · 镜头匠人

**站在你和任何 AI 视频模型之间的"导演"。**
*每一条都算数——少出废片、画面更好看、直接出成片。*

</div>

## 🎯 解决什么问题

| 痛点 | 代价 |
|---|---|
| 🎲 **废片太多**——人脸变形、墙壁弯曲、文字乱码、乱加音乐 | 反复浪费 credit、显卡时间和精力 |
| 🧩 **每个平台都不一样**——命令、模型名、限制、参数各不相同 | 每换一个平台都要花几个小时摸索 |
| 😐 **画面很普通**——"电影感、4K、唯美"这类提示词只能生成素材库一样的画面 | 内容没有辨识度 |
| ✂️ **只有片段，没有成片**——模型只给 5 秒的片段，字幕、配音、配乐、比例还得自己弄 | 要再学其他工具、手动剪辑 |
| 🔒 **被一个平台绑死**——大多数 skill 只支持一家 API | 没办法自由切换到最好或最便宜的模型 |

## ✅ 怎么解决

| 功能 | 说明 |
|---|---|
| 🧭 **设置向导** | 先问你想用哪种方式：云端平台、本地显卡、手动或混合，然后一步一步带你安装、登录、测试连通。API key 绝不出现在对话或文件里 |
| 🖥️ **诚实的本地部署建议** | 检测显卡、显存、内存、硬盘，推荐适合的模型档位（不适合就直接告诉你用云端更好），安装 ComfyUI 并通过接口自动调用 |
| ✈️ **导演自检** | 每个镜头在花钱**之前**做 13 项检查：内容密度、单一运镜、素材用途、高风险元素、台词时长、模型限制、版权 |
| 🎨 **审美库** | 高端审美原则、光线、焦段、调色、质感和风格预设，并且会把空洞的形容词改写成具体的画面描述 |
| 🖼️ **图转视频规范** | 静态型 / 反应型两种模式、"保持不变"锁定词、首尾帧指南，这是保持人物和场景一致最可靠的方法 |
| 🩺 **废片诊断** | 18 种"症状 → 原因 → 修法"，加上"一次只改一个变量"的重做规则，不再盲目重新抽卡 |
| 💳 **花费控制** | 生成前给出一张确认单，列明预估费用；先出图再转视频、先出草稿再出成片；可以设置预算上限 |
| ✂️ **内置剪辑** | 一条命令完成：拼接镜头、转场、配音、背景音乐自动避让人声、烧录字幕（支持中文，并自动对齐真实配音）、结尾定格留出标题位置、统一音量，并导出 9:16 / 1:1 / 16:9 版本和封面 |
| 📸 **免费照片动态化** | 把真实照片做成平滑的缓慢推进镜头，完全免费，100% 忠于真实产品或房子；AI 镜头一直失败时，也可以用它来兜底 |
| 🎞️ **场景模板** | 产品广告、建筑与房地产、短视频、短剧、讲解视频 |
| 🪶 **省 token** | 每一步只读取需要的文件，内容一条不删，只是用到才读 |

## 🚀 怎么用

1. **安装 skill**（任选一种）：
   - **Git（macOS / Linux）：**`git clone https://github.com/sf-ryanyan/takewright.git ~/.claude/skills/takewright`
   - **Git（Windows PowerShell）：**`git clone https://github.com/sf-ryanyan/takewright.git "$env:USERPROFILE\.claude\skills\takewright"`
   - **ZIP 下载：**到 [Releases](https://github.com/sf-ryanyan/takewright/releases) 下载 `takewright.zip`，解压后确保 `SKILL.md` 直接位于 `~/.claude/skills/takewright/` 文件夹里
   - 安装后重启 Claude Code（或 Claude 桌面版）。也支持其他能读取 `SKILL.md` 格式的 agent，放到对应的 skills 文件夹即可
   - **以后更新：**`git -C ~/.claude/skills/takewright pull`
2. **安装 ffmpeg**：质检和剪辑需要用到（Windows：`winget install Gyan.FFmpeg`，macOS：`brew install ffmpeg`，Linux：`sudo apt install ffmpeg`）。辅助脚本需要 Python 3.8 以上。
3. **直接说你要什么视频**，比如："帮我做一个 20 秒的竖屏视频，现代风格厨房，黄金时段光线，发 Instagram。"第一次使用时会自动运行设置向导。
4. **确认方案**：生成之前，你会先看到分镜和一张写明预估费用的确认单。
5. **拿到成片**：通过的镜头会逐帧质检，然后自动拼接、加字幕、混音、导出。

## ⚠️ 免责声明

- Takewright 是独立的开源项目，与文中提到的 ListenHub/MarsWave、fal.ai、MuAPI、字节跳动、阿里巴巴、腾讯、Lightricks、ComfyUI 等任何平台都没有关联，也没有获得它们的背书。
- 各平台的功能、模型名称、限制和价格经常变化。skill 会要求 agent 在使用前通过各平台的 `--help`、参数说明或官方文档进行核实。
- 平台费用、所用模型的授权、发布的内容，由使用者自行负责。请勿制作对真实人物、产品或地点的误导性内容；按要求标注 AI 生成或 AI 增强。
- AI 生成本身有随机性：Takewright 能大幅减少废片，但无法保证每次都完美。

## 👤 关于作者

由 **Ryan Yan（数据分析师）** 开发，目标是让创作者和小企业做 AI 视频更可控、更省钱。

## 📄 版权与协议

© 2026 Ryan Yan。基于 [MIT 协议](LICENSE) 开源：可以自由使用、修改和再发布（包括商业用途），只需保留协议和版权声明。
