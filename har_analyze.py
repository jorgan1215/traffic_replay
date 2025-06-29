import json
import pandas as pd
from hashlib import md5
from urllib.parse import quote

def jmx_encoder(str:str):
  str_dict={"\'":r"&quot;","&":r"&amp;","\"":r"&quot;"}
  for i in str_dict:
    str=str_dict[i].join(str.split(i))
  return  str



def gen_jmx(file,url_process_list):
  if url_process_list is None:
    return
  jmx_file = open(file,'a',encoding="utf-8")
  jmx_file.truncate(0)
  TestPlan = '''<TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="auto_test">
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
    </TestPlan>\n'''
  ThreadGroup = '''<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组">
        <intProp name="ThreadGroup.num_threads">1</intProp>
        <intProp name="ThreadGroup.ramp_time">1</intProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器">
          <stringProp name="LoopController.loops">1</stringProp>
          <boolProp name="LoopController.continue_forever">false</boolProp>
        </elementProp>
      </ThreadGroup>\n'''
  jmx_file.write('''<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">\n''')
  jmx_file.write('<hashTree>\n')
  jmx_file.write(TestPlan)
  jmx_file.write('<hashTree>\n')
  jmx_file.write(ThreadGroup)

  jmx_file.write('<hashTree>\n')

  collectionProp=''
  for item in url_process_list:
    method=item[5]
    print(method)
    if method=='GET':

      # get方式
      prop_list=json.loads(item[9])
      if prop_list[0]:
        collectionProp+='<collectionProp name="Arguments.arguments">\n'
        for i in prop_list:

          prop=tuple(i.items())
          for j in prop:

            collectionProp+=f'''<elementProp name="{j[0]}" elementType="HTTPArgument">
                  <boolProp name="HTTPArgument.always_encode">false</boolProp>
                  <stringProp name="Argument.value">{j[1]}</stringProp>
                  <stringProp name="Argument.metadata">=</stringProp>
                  <boolProp name="HTTPArgument.use_equals">true</boolProp>
                  <stringProp name="Argument.name">{j[0]}</stringProp>
                </elementProp>\n'''
        collectionProp+='</collectionProp>\n'
      else:
        collectionProp='<collectionProp name="Arguments.arguments"/>\n'
    elif method=='POST':

      # post方式
      postData= jmx_encoder(json.dumps(item[7]))
      print(postData)

      if postData is not None:
        collectionProp += '<collectionProp name="Arguments.arguments">\n'
        collectionProp += f'''<elementProp name="" elementType="HTTPArgument">
                  <boolProp name="HTTPArgument.always_encode">false</boolProp>
                  <stringProp name="Argument.value">{postData}</stringProp>
                  <stringProp name="Argument.metadata">=</stringProp>
                </elementProp>\n'''
        collectionProp += '</collectionProp>\n'
      else:
        collectionProp = '<collectionProp name="Arguments.arguments"/>\n'
    else:
      pass

    jmx_file.write(f'''<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="HTTP请求">
          <stringProp name="HTTPSampler.domain">{item[1]}</stringProp>
          <stringProp name="HTTPSampler.port">{item[2]}</stringProp>
          <stringProp name="HTTPSampler.protocol">{item[3]}</stringProp>
          <stringProp name="HTTPSampler.path">{item[4]}</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <stringProp name="HTTPSampler.method">{item[5]}</stringProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.postBodyRaw">false</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量">
            {collectionProp}
          </elementProp>
        </HTTPSamplerProxy>\n''')
    jmx_file.write('<hashTree>\n')
    jmx_file.write('''<JSONPathAssertion guiclass="JSONPathAssertionGui" testclass="JSONPathAssertion" testname="JSON断言">
            <stringProp name="JSON_PATH">$.code</stringProp>
            <stringProp name="EXPECTED_VALUE">200</stringProp>
            <boolProp name="JSONVALIDATION">true</boolProp>
            <boolProp name="EXPECT_NULL">false</boolProp>
            <boolProp name="INVERT">false</boolProp>
            <boolProp name="ISREGEX">true</boolProp>
          </JSONPathAssertion>\n''')
    jmx_file.write('<hashTree/>\n')
    jmx_file.write('</hashTree>\n')
  jmx_file.write('''</hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>''')

  jmx_file.close()




def url_filter(url,start=-6):
  try:
    start = url.index('://')
    url = url[start + 3:]
  except:
    pass
  try:
    end = url.index('?')
    url = url[:end]
  except:
    pass
  # 移除路径参数
  if url[start:].isdigit():
    url = '/'.join(url.split('/')[:-1])
  return url

def locate_page(url):
  url_md5=md5(url)

  page_template=[{'name':'课程详情页','url':'','md5':''},
                 {'name':'班级详情页','url':'','md5':''},
                 {'name':'课程学习页','url':'','md5':''},
                 {'name':'lms管理台','url':'','md5':''},
                 {'name':'做课页','url':'','md5':''},
                 {'name':'开发者工作台','url':'','md5':''}]

  for i in page_template:
    if url_md5==i['md5']:
      return i['name']
  return '其他页面'
def explain_url():
  # 判定接口功能，需要先清洗yaml
  pass

def if_sxz_url(url):
  # 分辨是否是课程接口
  pass
# 传入
def har_analyze(harfile):
    print(f"开始处理HAR文件：{harfile}")
    try:
        with open(harfile, 'r', encoding='utf-8') as harfile:
            conent = harfile.read()
        if conent.startswith(u'\ufeff'):
            conent = conent.encode('utf8')[3:].decode('utf8')

        har_dict = json.loads(conent)

        requestList = har_dict['log']['entries']

        if len(requestList) == 0:
            msg = "HAR文件中无请求内容！"
            return msg

        No = 1
        test_data_list = []
        for item in requestList:
            # 筛选xhr请求
            if item['_resourceType']!='xhr':
              continue

            method = item['request']['method']

            # 筛选请求方式
            # if method.lower() not in ['get', 'post']:
            #     continue

            # 处理url
            url = item['request']['url']
            start = url.index('://')
            protocol = url[:start]
            temp_str_start=url[:start+3]
            domain_start=temp_str_start.index('/')
            port=80
            if start+1==domain_start:
              if protocol=='https':
                port=443
              elif protocol=='http':
                port=80
              else:
                port=int(temp_str_start[start+1:domain_start])

            temp_str_end = url[start + 3:]
            url_start = temp_str_end.index('/')

            domain = temp_str_end[:url_start]
            host = protocol + domain
            path=temp_str_end[url_start+1:]

            # 处理请求体
            try:
              requst_type = item['request']['postData']['mimeType']
              request_data  = item['request']['postData']['text']
            except:
              requst_type = "null"
              request_data = "null"
            req_params,req_json,req_data = '', '', ''
            if request_data and requst_type:
                # get请求URL中已经携带参数，此处不再提取参数
                if method.lower() == 'post' and requst_type == 'application/json':
                    req_json = request_data
                else:
                    req_data = request_data

            # 处理负载
            try:
                queryList = []
                queryItem = {}
                queryString=item['request']['queryString']
                for i in queryString:
                  queryItem[i['name']]=i['value']
                queryList.append(queryItem)
            except:
                queryList = 'null'

            # 处理请求体

            postData=item.get('request').get('postData')
            # print(postData)
            if postData is not None:
              pass
            else:
              postData = 'null'





            # 处理请求头
            new_headers={'Authorization':'null','Cookie':'null','Referer':'null'}
            headers = item['request']['headers']
            for j in headers:
                try:
                    # 处理名称

                    name=j['name'].lower()
                    if name[0]==':':
                       name=name[1:]
                    name=name[0].upper()+name[1:]

                    # 设置默认字段

                    keys_list=list(new_headers.keys())

                    try:
                      index=keys_list.index(name)
                      new_headers[keys_list[index]] = j['value']
                    except:
                      pass

                except Exception as e:
                    pass
                new_headers[j['name']] = j['value']

            # 处理响应
            try:
              response = item['response']['content']['text']
            except:
              response = "null"
            # if not response:
            #     continue

            # 生成结果
            # new_list =[No, URL, method, json.dumps(new_headers), req_params,
            #             req_data, req_json, 'AssertJsonTree', response, '', '', '']
            new_list = [No,domain,port,protocol,url_filter(url),method,url,postData,url_filter(url),json.dumps(queryList),new_headers['Referer'],url_filter(new_headers['Referer'])]

            test_data_list.append(new_list)
            No +=1
            print(new_list)
        if len(test_data_list)>1:
            print(f"HAR文件解析成功，共有:{len(test_data_list)-1}个请求")
            return test_data_list
        else:
            print("HAR解析出来的数据为0个请求")
            return
    except Exception as e:
            print("HAR文件解析失败:")




def to_excel(output,data):
  # 导出到Excel
  # pip install pandas openpyxl
  # data = {
  #   'Column1': [1, 2, 3, 4],
  #   'Column2': ['A', 'B', 'C', 'D']
  # }
  # pd.DataFrame(data).to_excel(output,columns=['序号', '接口','方法','参数','来源','asdf'], index=False)
  pd.DataFrame(data).to_excel(output,index=False)
# list=har_analyze("./har.txt")
# to_excel('output.xlsx',list)
# gen_jmx('test.jmx',list)





