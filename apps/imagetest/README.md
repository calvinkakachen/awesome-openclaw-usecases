# imagetest — Web App

上传产品图片，AI 自动识别产品类型，生成完整亚马逊图集。

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 GOOGLE_API_KEY

# 3. 启动服务
uvicorn app:app --reload --port 8000

# 4. 打开浏览器
# http://localhost:8000
```

## 项目结构

```
amazon-image-auto/
├── app.py                        # FastAPI 主程序
├── requirements.txt
├── .env.example
├── services/
│   ├── detector.py               # Gemini Vision 产品识别
│   ├── generator.py              # Imagen 3 图像生成 + 流式进度
│   └── pipelines/
│       ├── composite.py          # 贴图流水线（window film）
│       ├── hardware.py           # 五金建模流水线（窗帘扣）
│       ├── fabric.py             # 织物流水线（窗帘布）
│       └── solid.py              # 实体产品流水线（通用）
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## 支持的产品类型

| 产品示例 | 识别类型 | 核心生成策略 |
|---------|---------|------------|
| window film、防晒膜、磨砂膜 | COMPOSITE | 提取花纹 → 贴到玻璃场景 |
| 窗帘扣、窗帘环、挂钩、五金件 | HARDWARE | 多角度 3D 渲染 + 安装场景 |
| 窗帘布、遮光布、桌旗 | FABRIC | 悬垂模拟 + 房间场景 |
| 花瓶、蜡烛、收纳盒 | SOLID | 多角度渲染 + 生活场景 |

## 每次生成的图集（13 张）

| 序号 | 图片 | 尺寸 | 用途 |
|-----|-----|------|------|
| 1–4 | 白底渲染图 | 2000×2000 | 亚马逊主图/副图 |
| 5–8 | 生活场景图 | 2000×2000 | listing 副图 |
| 9   | A+ 主图 | 2000×2000 | Amazon A+ |
| 10  | A+ 功能信息图 | 970×600 | A+ 模块1 |
| 11  | A+ 横幅图 | 970×300 | A+ 模块2 |
| 12  | A+ 竖版图 | 300×400 | A+ 模块3 |
| 13  | A+ 品牌背景 | 970×600 | A+ 模块4 |

## API 端点

| 方法 | 路径 | 说明 |
|-----|-----|------|
| POST | `/api/analyze` | 上传图片，Gemini 识别产品类型 |
| GET  | `/api/generate/{session_id}` | SSE 流式生成图集 |
| GET  | `/api/results/{session_id}` | 获取生成结果清单 |
| GET  | `/api/download/{session_id}` | 下载全部图片 ZIP |

## 费用参考

每次完整生成约 $0.40–0.60（Google AI Studio 计费）：
- Gemini Vision 分析：~$0.01
- Imagen 3 生成 13 张：~$0.40–0.55
