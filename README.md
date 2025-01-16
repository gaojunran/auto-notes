# 基于大模型的自动笔记系统

## 技术栈
成品形态：适配Windows/Mac OS的客户端。在客户端中，通过上传一段录音或手动录音，调用大模型接口生成课程摘要、课堂重点、以及精美的课程笔记可供在线浏览或导出、生成思考题等功能。
客户端前端：Vue3、TypeScript、TailwindCSS、PrimeVue等。
客户端后端：Tauri、Rust；
服务端：FastAPI、Python。

## 功能清单（待定）
- 直接录音或上传录音文件（客户端）； 
- 语音转文字（服务端）； 
- 展示识别结果（客户端）； 
- 根据录音内容生成笔记（服务端）； 
- 展示笔记、可导出（客户端）； 
- 根据笔记内容生成思考题（服务端）； 
- 展示思考题、用户可以在线作答（客户端）； 
- 展示历史课程（客户端）。


## 服务端
[项目目录](./api)  [README.md](./api/README.md)




