# 智慧选课与AI参考系统 (Smart Course Platform with AI Reference)

本项目是一个结合 **AI 辅助学习** 与 **教育引导设计** 的课程学习与作业管理平台。  
旨在帮助教师合理利用 AI 技术布置课程任务，并引导学生在参考 AI 答案的同时，保持自主学习与思考能力。  

---

## 项目背景 (Background)

随着大语言模型（LLM）等 AI 技术的快速普及，越来越多学生依赖 AI 生成答案来完成课业，  
这在一定程度上削弱了他们独立思考与问题解决的能力。  

因此本项目设计了一套**人机共学系统**：
- 教师可以发布课程内容、作业与参考答案；
- 系统生成 AI 辅助解答供学生对比学习；
- 学生可对 AI 答案进行**评分、修改与反思**；
- 评分结果将反馈给教师，用于优化教学与作业设计。

---

## 系统目标 (Objectives)

1. **教师端**
   - 上传课程与作业；
   - 查看 AI 生成的参考答案；
   - 管理学生作业与评分；
   - 分析学生学习数据与反馈。

2. **学生端**
   - 在线查看课程与作业；
   - 获取 AI 生成的答案参考；
   - 进行答案对比、修改与自评；
   - 查看其他同学的修改建议；
   - 通过评分系统了解答案质量。

3. **AI 辅助模块**
   - 自动生成参考答案；
   - 根据学生与教师评分进行优化；
   - 生成作业报告与改进建议。

---

## 技术架构 (Tech Stack)

| 模块 | 技术栈 |
|------|---------|
| 前端 (Frontend) | HTML / CSS / JavaScript / React (或 Vue) |
| 后端 (Backend) | Python (Flask / FastAPI) |
| 数据库 (Database) | SQLite / PostgreSQL |
| AI 模块 (AI Module) | OpenAI GPT 系列 API / LLM 微调模型 |
| 可视化 (Visualization) | ECharts / D3.js |
| 文件系统 | 支持作业与答案上传、下载 |

---

## 项目结构 (Project Structure)

| 目录/文件 | 功能说明 |
|------------|-----------|
| `frontend/` | 前端界面代码（教师端 + 学生端） |
| `backend/` | 后端接口与数据逻辑 |
| `models/` | AI 生成与优化模块 |
| `database/` | 数据表定义与存储脚本 |
| `static/` | 图片、CSS、JS 等静态资源 |
| `templates/` | 网页模板文件 |
| `data/` | 测试数据与作业样例 |
| `LLMs_all_v2.7.zip` | AI 模型及辅助脚本压缩包 |
| `README.md` | 项目说明文件 |

---

## 核心功能 (Core Features)

- ✅ **教师课程管理**：上传/编辑课程与作业内容；  
- ✅ **AI 答案生成**：调用 LLM 模型生成答案参考；  
- ✅ **学生互动学习**：对比 AI 答案与自解答案；  
- ✅ **答案评分与修订**：学生与教师共同参与评分、修改；  
- ✅ **学习数据分析**：统计 AI 参考使用率、学生参与度；  
- ✅ **文件上传与下载**：支持教师资料与学生作业的文件交互。

---

## 项目亮点 (Highlights)

- 🌟 **AI 辅助但非替代**：通过设计评分机制，防止学生“照抄”AI 答案。  
- 🌟 **双向反馈机制**：学生与教师共同参与 AI 答案优化。  
- 🌟 **教育伦理导向**：引导学生正确理解 AI 在学习中的角色。  
- 🌟 **可扩展架构**：可接入不同语言模型或课程模块。

---

## 使用方法 (How to Use)

1. 克隆仓库：
   ```bash
   git clone https://github.com/CLucyDX/course-selection-system.git
   cd course-learning-ai-system
---
## 展示
<img width="648" height="351" alt="Image" src="https://github.com/user-attachments/assets/98f4b9e4-c0c2-4b61-acca-b13bf8679165" />

<img width="863" height="390" alt="Image" src="https://github.com/user-attachments/assets/c09c9ae8-d5d8-427a-8c13-2cee4162b2bb" />

<img width="742" height="391" alt="Image" src="https://github.com/user-attachments/assets/10cfafe7-8e72-45e2-b4f6-4b7fc845474e" />

<img width="1034" height="582" alt="Image" src="https://github.com/user-attachments/assets/2dc160bb-1919-4431-962a-b350e30b1b84" />

<img width="1035" height="585" alt="Image" src="https://github.com/user-attachments/assets/7371fbd4-d29d-41c0-8d08-e55ce0aa9210" />

<img width="1036" height="582" alt="Image" src="https://github.com/user-attachments/assets/5a7d7392-9a71-4943-af6e-a987f2782fcc" />
仅用于展示，实际操作需要完整数据库进行
