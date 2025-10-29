# rcli - CLI for Swagger API

`rcli` 是一个基于 Swagger API 的命令行工具，支持通过命令行快速调用 API，支持多种输出格式和参数配置。

---

## 安装说明

### 1. 安装 Python
在 macOS 上，系统自带 Python，但建议安装最新版本的 Python。可以通过以下方式安装：

#### 使用 Homebrew 安装 Python
```bash
brew install python
```

安装完成后，检查 Python 和 `pip` 的版本：
```bash
python3 --version
pip3 --version
```

确保 Python 版本为 3.7 或更高。

---

### 2. 安装依赖
在项目目录下运行以下命令安装所需依赖：
```bash
pip3 install -r requirements.txt
```

如果没有 `requirements.txt` 文件，可以手动安装依赖：
```bash
pip3 install requests pandas pyyaml jsonschema
sudo chmod +x rcli
sudo ln -s $(pwd)/rcli /usr/local/bin/rcli
```

---

### 3. 配置 `rcli`
运行以下命令初始化配置：
```bash
rcli config --swagger <SWAGGER_JSON_URL> --url <API_BASE_URL> --bearer <BEARER_TOKEN>
```

示例：
```bash
rcli config --swagger http://127.0.0.1:9000/openapi.json --url http://127.0.0.1:9000/ --bearer my_token
```

---

## 使用说明

### 1. 查看帮助
运行以下命令查看 `rcli` 的帮助信息：
```bash
rcli --help
```

---

### 2. 配置命令
`rcli` 提供了 `config` 命令，用于配置 Swagger JSON URL、API 前缀 URL 和认证 Token。

#### 查看当前配置
```bash
rcli config
```

#### 更新配置
```bash
rcli config --swagger <SWAGGER_JSON_URL> --url <API_BASE_URL> --bearer <BEARER_TOKEN>
```

示例：
```bash
rcli config --swagger http://127.0.0.1:9000/openapi.json --url http://127.0.0.1:9000/ --bearer my_token
```

---

### 3. 自动生成的 API 命令
根据 Swagger JSON 自动生成的命令结构如下：
- 每个 API 路径会生成对应的命令。
- 支持 `GET`、`POST`、`PUT`、`DELETE` 等 HTTP 方法。
- 参数会根据 API 定义自动生成。

#### 示例
假设 Swagger 定义了以下 API：
```json
{
  "/user/{id}": {
    "get": {
      "summary": "Get user by ID",
      "parameters": [
        {
          "name": "id",
          "in": "path",
          "required": true,
          "schema": { "type": "integer" }
        }
      ]
    },
    "delete": {
      "summary": "Delete user by ID",
      "parameters": [
        {
          "name": "id",
          "in": "path",
          "required": true,
          "schema": { "type": "integer" }
        }
      ]
    }
  }
}
```

生成的命令如下：
```bash
rcli userg <id>
rcli userd <id>
```

---

### 4. 参数说明
#### 通用参数
- `-f, --format`: 指定输出格式，支持以下选项：
  - `json` 或 `j`: JSON 格式输出。
  - `table` 或 `t`: 表格格式输出。
  - `raw` 或 `r`: 原始 HTTP 请求和响应详情。
  - `line` 或 `l`: 默认格式，输出为 YAML。
- `-o, --out`: 指定输出文件路径，将结果保存到文件中。

#### 示例
```bash
rcli userg 1 -f json
rcli userd 1 -f raw
```

---

### 5. 请求体参数
对于需要请求体的 API，可以通过以下方式传递 JSON 数据：
- 使用 `--json` 参数直接传递 JSON 字符串。
- 使用 `--json` 参数传递 JSON 文件路径 或者 yaml 文件路径。

#### 示例
假设 API 定义如下：
```json
{
  "/user": {
    "post": {
      "summary": "Create a new user",
      "requestBody": {
        "content": {
          "application/json": {
            "schema": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "age": { "type": "integer" }
              },
              "required": ["name"]
            }
          }
        }
      }
    }
  }
}
```

生成的命令如下：
```bash
rcli userp --json '{"name": "Alice", "age": 30}'
```

或者：
```bash
echo '{"name": "Alice", "age": 30}' > user.json
rcli userp --json user.json

echo 'name=Alice \n age=30' > user.yaml
rcli userp --json user.yaml

```

---

### 6. 输出格式
#### JSON 格式
```bash
rcli userg 1 -f json
```
输出：
```json
{
  "id": 1,
  "name": "Alice",
  "age": 30
}
```

#### 表格格式
```bash
rcli userg 1 -f table
```
输出：
```
   id   name    age
0   1  Alice     30
```

#### 原始格式
```bash
rcli userg 1 -f raw
```
输出：
```
------------------------------------HTTP Request Details:------------------------------------
Method: GET
URL: http://127.0.0.1:9000/user/1
Headers: {
  "Authorization": "Bearer my_token"
}

------------------------------------HTTP Response Details:------------------------------------
Status Code: 200
Headers: {
  "Content-Type": "application/json"
}
Body: {
  "id": 1,
  "name": "Alice",
  "age": 30
}
```

#### YAML 格式
```bash
rcli userg 1 -f line
```
输出：
```yaml
id: 1
name: Alice
age: 30
```

---

## 开发者说明

### 代码结构
- `rcli`: 主程序文件，包含命令行解析和 API 请求逻辑。
- `config.json`: 配置文件，存储 Swagger URL、API 前缀和认证信息。

### 依赖
- `requests`: 用于发送 HTTP 请求。
- `pandas`: 用于表格格式化输出。
- `pyyaml`: 用于 YAML 格式化输出。
- `jsonschema`: 用于验证请求体是否符合 API 定义。

---

## 常见问题

### 1. 如何更新配置？
运行以下命令更新配置：
```bash
rcli config --swagger <NEW_SWAGGER_URL> --url <NEW_API_URL> --bearer <NEW_BEARER_TOKEN>
```

### 2. 如何查看支持的命令？
运行以下命令查看支持的命令：
```bash
rcli --help
```

---

## 贡献
欢迎提交 Issue 和 Pull Request 来改进 `rcli`。

---

## 许可证
MIT License
```
