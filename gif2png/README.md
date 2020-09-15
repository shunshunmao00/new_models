# GIF动态图转图片

该模型使用PIL工具实现将GIF动态读逐帧转为静态PNG图片

## API接口

本模型提供了2个API接口：

- API接口1：

    - API端点： /api/model
    
    - HTTP方法： POST
    
    - HTTP请求体：
    
            {
                "method": "gen_test_img_base64"
                "kwargs": {}
            }

    - HTTP响应体：
        
            {
                "status": "ok"|"err",
                "value": <压缩图像的base64编码字符串>|<错误描述>
            }
    
- API接口2：

    - API端点： /api/model
    
    - HTTP方法： POST
    
    - HTTP请求体：
    
            {
                "method": "split_gif_base64"
                "kwargs": {
						"img_base64": <压缩图像的base64编码字符串>
				}
            }

    - HTTP响应体：
			{
                "status": "ok"|"err",
                "value": <手写数字识别结果>|<错误描述>
            }
        
## 模型开发

1. 开发环境准备

    建议使用PyCharm作为Python的IDE集成开发环境。 
    
    建议在PyCharm中为每一个模型项目都新建一个Python虚拟环境（venv）。执行以下操作进入界面，然后选择添加相应的Python版本。 

            'File | Settings | Project <项目名> | Project Interpreter'

2. 依赖包安装

    在requirements.txt文件中添加模型运行所需要的依赖包信息。
    
    在terminal窗口当前目录下，执行如下命令来安装所有依赖包：
    
            sh pip-install-reqs
        
3. 开发模型推理程序

    - 模型程序位置
    
        指定在 core 目录下开发模型推理程序。
        
        主程序位于model_core.py文件中，其中必须定义一个名为 ModelCore 的类，作为模型运行和调用的主入口。
    
    - 模型初始化和数据加载
    
        在 ModelCore 中定义构造函数 __init__() ，执行模型初始化和模型数据加载等相关操作。
    
    - 模型方法
    
        在 ModelCore 中定义其他方法，作为模型方法对外提供API接口服务。
        
        可在 ModelCore 中定义一个类变量 public_methods ，用于声明可对外提供API接口服务的方法名。不在该列表中的方法不能通过API接口方式访问。如果public_methods变量不存在或值为None，则 ModelCore 中定义的所有方法都对外开放。
    
    - 模型方法输入参数
    
        在 ModelCore 中定义的模型方法， 可定义0至多个输入参数。
        
        如果某个模型方法只定义了一个输入参数且约定该输入参数类型为 bytes（二进制字节流），则在模型部署后，该模型方法需要通过端点为 /api/stream/<method-name> 或 /api/file/<method-name> 的HTTP API接口来进行访问。如果通过 /api/stream 接口访问，则在HTTP POST请求体中直接携带bytes类型的二进制字节流；如果通过 /api/file 接口访问，则在HTTP POST请求体中携带用于HTTP文件上传的XHR格式请求体。
        
        在所有其他情况下（模型方法中定义了0至多个输入参数，且约定每一个输入参数类型都不为bytes），模型部署后该模型方法通过端点为 /api/model 的HTTP API接口进行访问。访问时在HTTP POST请求体中携带JSON格式数据，格式如下：
        
                    {
                        "method": <与ModelCore中定义的模型方法同名的字符串>
                        "kwargs": {
                            <参数名1>: <参数值1>,
                            <参数名2>: <参数值2>,
                            ...
                        }
                    }
    
        其中 kwargs 为键值对形式的参数列表， 各参数名必须与 ModelCore 中相应模型方法的参数名保持一致。
    
    - 模型方法返回值
    
        ModelCore中所定义模型方法的返回值，可以是bytes类型的二进制字节流，也可以是其他任意Python类型的数据。如果是后者，则该返回值必须能够使用 json.dumps() 函数序列化为JSON字符串，也就是说其中不能嵌套无法被序列化的特殊类型数据。
        
        模型部署后通过HTTP API访问时，如果ModelCore中所定义模型方法的返回值为bytes类型，则HTTP响应体中直接包含该bytes类型的字节流；否则HTTP响应体中包含一个序列化后的JSON对象字符串，其格式如下：
        
                    {
                        "status": "ok"|"err",
                        "value": <模型方法返回结果>
                    }
        
        其中 "status" 指示模型调用状态，为 "ok" 表示正常， "err" 表示模型调用或运行过程中发生异常。
        
        当 "status" 的值 "ok" 时， "value" 的值为模型方法的返回结果；当 "status" 的值 "err" 时， "value" 的值为错误或异常描述字符串。

4. 开发前端web界面（可选）

    在 webapp 目录下开发交互式前端web界面。
    
    模板程序中使用 Angular 框架来编写前端，编程语言采用 TypeScript 和 html。所有 Angular 代码位于 webapp/bpp 目录之下。
    
    典型的开发过程如下：
    
    1. 第一次拷贝样例程序后，应先安装前端开发需要的Node依赖：

            cd webapp
            yarn install
            
    2. 运行 run_model_server.py 程序（或者在terminal命令行窗口中执行： cubeai_model_runner 命令），在本地启动 cubeai_model_runner 服务器。
    
    3. 在 webapp/bpp 目录下开发前端代码。普通开发者基于样例程序开发，只需要修改 webapp/bpp/app/home 目录下的 home.component.ts 和 home.component.html 两个程序文件即可。高级开发者也可在此基础上进行扩展。
    
       在开发过程中，当 Angular 代码修改之后，在terminal命令行窗口中 cd 至 webapp 目录之下，然后执行 yarn webpack:build 命令来编译代码：
    
            cd webapp
            yarn webpack:build
            
       或者在PyCharm中直接运行 build_web_dev.py 程序亦可。
            
    4. 在浏览器中打开并刷新网页 http://127.0.0.1:3330/web/ , 查看并调试web界面。
    
    5. 如需继续调试，转至第3步。
    
    6. 开发结束后，执行如下命令编译生产环境代码：
    
            cd webapp
            yarn webpack:prod
            
        或者在PyCharm中直接运行 build_web_prod.py 程序亦可。
            
    7. 开发完成之后，就可以运行 pack_model.py 程序来进行模型打包了。
    
    8. 模型部署之后，可以通过docker容器对外提供的API端点 /web/ 来进行访问web页面，例如： http://172.17.0.2:3330/web/ 。
    
    > 注意： 前端web代码编译后，存放在 webapp/www 目录之下。其实本系统并不限制前端web开发一定使用 Angular，使用其他任何前端框架都开发者可以，只要保证最终编译生成的生产代码存放在 webapp/www 目录之下就行。

## 模型测试

1. 本地开发测试

    运行程序：test_dev.py，直接以函数调用的方式对模型方法进行测试。
    
    适用于模型开发过程中验证模型推理程序的正确性。

2. 本地API测试

    - 首先运行程序：run_model_server.py，或者直接在terminal中执行命令：cubeai_model_runner，在本地启动模型服务器。
    
    - 修改test_api.py中url的值，改为： url = 'http://127.0.0.1:3330/api/model'。
    
    - 然后运行程序：test_api.py，等待模型服务器返回结果。
    
    - web可视化测试： http://127.0.0.1:3330/web/
    
    适用于模型开发完成、部署之前对模型的可用性进行测试。

3. 远程API测试

    - 模型部署之后，获取模型对外提供服务的URL地址。例如将模型以docker方式部署在本机，其IP地址可能是：172.17.0.2。
    
    - 修改test_api.py中url的值，改为： url = 'http://172.17.0.2:3330/api/model' （IP地址根据实际情况修改）。
    
    - 然后运行程序：test_api.py，等待模型服务器返回结果。
    
    - web可视化测试： http://172.17.0.2:3330/web/  （IP地址根据实际情况修改）
    
    适用于模型部署之后的测试。

## 模型打包

1. 首先编辑模型配置文件：application.yml

    - model_runner.version: 模型运行器版本号，必须为“v2”，必填。
    
    - python.version: Python版本号，应与当前开发环境保持一致，必填。
    
    - model.name: 模型名，必填。建议用中文短语，不要太长。
    
    - model.version: 模型版本号，例如v1.0.0，可选。
    
    - apis: 模型提供的API接口列表，目前仅用于展示，可选。

2. 然后运行 pack_model.py 程序，或者直接在terminal命令行窗口中执行 cubeai_model_pack 命令，打包完成后将在out文件夹下生成一个.zip压缩文件。

3. （可选：打包二进制模型，与步骤2二选一）运行 pack_model_bin.py 程序，或者直接在terminal命令行窗口中执行 cubeai_model_pack_bin 命令，打包完成后将在out文件夹下生成一个.zip压缩文件。

    该步骤先将模型Python程序编译成.so静态库二进制代码，然后再进行打包封装。
    
    > 注意：并不是所有Python程序都能够成功编译成二进制代码。
    
    - 如果程序中包含__init__目录，代码编译时会出现异常。请删除所有__init__目录或者改造程序后再尝试编译。
        
    - 如果出现其他编译错误或异常，可能需要对程序结构进行适当改造，或者放弃编译。


## 模型托管

1. 打开CubeAI智立方主页：

    https://cubeai.dimpt.com
        
2. 进入CubeAI平台“模型导入”界面：

    https://cubeai.dimpt.com/pmodelhub/#/onboarding
        
3. 将模型打包阶段生成的.zip文件导入CubeAI模型共享平台，自动生成微服务docker镜像。

4. 在CubeAI模型共享平台中浏览已托管模型。

    https://cubeai.dimpt.com/pmodelhub/#/market

## 模型部署

1. 进入CubeAI模型共享平台“我的模型”界面：

    https://cubeai.dimpt.com/pmodelhub/#/personal
        
2. 选择刚导入的模型，进入模型详情界面，点击“模型部署”按钮，将模型docker镜像部署至CubeAI能力开放平台。

## 模型调用

1. 进入CubeAI能力开放平台界面：

    https://cubeai.dimpt.com/popen/#/market
    
2. 打开某个模型部署实例详情界面，查看模型运行状态，执行模型调用测试操作。

## 模型应用示范

1. 进入CubeAI示范应用界面

    https://cubeai.dimpt.com/pdemo/#/
    
2. 在交互式图形界面中试用、体验模型功能。
