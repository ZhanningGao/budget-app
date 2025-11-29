# 装修预算表管理系统

一个便捷的Web应用，用于管理装修预算表Excel文件，支持项目的增删改查和导出功能。

## 功能特性

- ✅ **查看数据** - 自动加载Excel文件中的所有装修项目，按分类组织展示
- ✅ **AI智能添加** - 🤖 通过自然语言对话输入，AI自动解析并创建项目（需配置API Key）
- ✅ **手动添加项目** - 通过表单便捷地添加新的装修项目
- ✅ **编辑项目** - 修改现有项目的详细信息
- ✅ **删除项目** - 支持单个或批量删除项目
- ✅ **导出Excel** - 导出为相同格式的Excel文件

## 安装步骤

1. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置AI API Key（可选但推荐）**
   
   为了使用AI智能解析功能，需要配置OpenAI API Key：
   
   **方式1：通过Web界面配置（推荐）**
   - 启动应用后，在页面顶部点击 "⚙️ 配置API Key" 按钮
   - 按照提示获取并输入OpenAI API Key
   
   **方式2：通过环境变量配置**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **如何获取OpenAI API Key：**
   1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
   2. 登录账号（如果没有需要先注册）
   3. 点击右上角头像 → "View API keys"
   4. 点击 "Create new secret key" 创建新密钥
   5. 复制生成的密钥（格式：sk-...）
   
   > **注意**：Cursor本身不提供API Key，需要使用OpenAI的API Key。如果不配置API Key，AI智能解析功能将不可用，但仍可使用手动添加功能。

3. **确保Excel文件存在**
   确保 `红玺台复式装修预算表.xlsx` 文件在当前目录下

## 使用方法

1. **启动服务**
   ```bash
   python app.py
   ```

2. **访问应用**
   打开浏览器访问：http://localhost:5000

3. **操作说明**
   - **AI智能添加**（推荐）：
     - 在顶部AI输入框中输入自然语言，例如："全屋基础装修，1套，预算24500元，实际花费24500元，备注：黄江工长介绍"
     - 点击"解析预览"查看AI解析结果，确认后添加
     - 或直接点击"直接添加"让AI自动解析并添加
     - 支持 Ctrl+Enter 快捷键快速添加
   - **手动添加项目**：点击"添加项目"按钮，填写表单后保存
   - **编辑项目**：点击表格中的"编辑"按钮修改项目
   - **删除项目**：勾选要删除的项目，点击"删除选中"按钮
   - **导出Excel**：点击"导出Excel"按钮下载最新数据

## 注意事项

- 所有修改会直接保存到原始的Excel文件中
- 导出功能会生成带时间戳的新文件，不会覆盖原文件
- 建议定期备份原始Excel文件

## 技术栈

- **后端**：Flask (Python Web框架)
- **数据处理**：Pandas (Excel文件处理)
- **前端**：原生HTML/CSS/JavaScript

## 文件结构

```
hxt/
├── app.py                          # Flask应用主文件
├── requirements.txt                # Python依赖
├── 红玺台复式装修预算表.xlsx        # 原始Excel文件
├── templates/
│   └── index.html                 # 前端界面
├── uploads/                       # 上传文件目录（自动创建）
└── exports/                       # 导出文件目录（自动创建）
```

